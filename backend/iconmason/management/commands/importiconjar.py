"""Feed this command an IconJar file to import it into IconMason."""
import shutil
import gzip
import tempfile
import json
from pathlib import Path
from contextlib import contextmanager
from iconmason.settings import MEDIA_ROOT
from iconmason.models.tag import Tag
from iconmason.models.group import Group
from iconmason.models.iconset import IconSet
from iconmason.models.icon import Icon
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File


class LogLevels():
    """Define some loglevels to help self document log calls."""

    ERROR = 0
    SUCCESS = 1
    INFO = 2


class Command(BaseCommand):
    """Run the CLI application, basically instance an import_jar.Importer."""

    help = 'Import an IconJar file into the database.'

    def add_arguments(self, parser):
        """Add our own arguments to the manage.py command."""
        parser.add_argument(
            'path',
            type=str,
            help="Path to an iconjar or a tree of iconjars."
        )

    def log(self, logstr, *args, level=LogLevels.INFO, **kwargs):
        """
        Log an info level message to stdout.

        @param str logstr String to send to stdout/stderr.
        @param LOGLEVEL level
        """
        if self.verbosity > level:

            logstr = str(logstr).format(*args, **kwargs)

            if level < 1:
                self.stderr.write(self.style.ERROR(logstr))
            elif level < 2:
                self.stdout.write(self.style.SUCCESS(logstr))
            else:
                self.stdout.write(logstr)

    def error(self, logstr, *args, **kwargs):
        """
        Log an error level message to stderr.

        @param str logstr String to send to stderr.
        """
        self.log(logstr, level=LogLevels.ERROR, *args, **kwargs)

    def success(self, logstr, *args, **kwargs):
        """
        Log a success level message to stdout.

        @param str logstr String to send to stdout.
        """
        self.log(logstr, level=LogLevels.SUCCESS, *args, **kwargs)

    def handle(self, *args, **options):
        """Run the importer module with the given arguments."""
        self.verbosity = options.get("verbosity", LogLevels.ERROR)

        importer = IconJarImporter(self.error, self.log)
        importer.import_all(options['path'])
        if not importer.errors:
            self.success("Successfully imported your IconJars!")
        else:
            self.error("Import completed with errors ({})!", importer.errors)


class IconJarImporter:
    """Load data from an IconJar file into the django database."""

    def __init__(self, error_func=None, log_func=None):
        """
        Import iconjars.

        @param str path to an iconjar(s)
        """
        self.errors = 0
        self.error_func = error_func
        self.log_func = log_func
        self.tags = {}
        self.groups = {}
        self.sets = {}

    def import_all(self, str_path):
        """
        Import icon groups (sets) defined in the iconjar metadata file.

        @param str str_path Path to search for IconJars to import.
        """
        with self.with_path(str_path) as path:
            jars = self.get_jar_data(path)
            if jars:
                self.log(
                    "Importing these iconjars: \n- {}",
                    "\n- ".join([str(str_path) for p in jars])
                )
            else:
                self.error("No IconJars found with {}", str(path))

            for icons_path, metadata in jars:
                self.import_groups(metadata['groups'])
                self.import_sets(metadata['sets'])
                for icon in metadata['items'].values():
                    self.import_icon(icon, icons_path)

    def import_icon(self, icon, icons_path):
        """
        Import icons defined in the iconjar metadata file.

        @param dict metadata from the JSON data of the metadata file.
        """
        tags = self.import_icon_tags(icon.get('tags', "").split(","))

        try:
            icon_obj, created = Icon.objects.get_or_create(
                uuid=icon['identifier'],
                name=icon['name'],
                icon_set=self.sets.get(icon['parent'], None)
            )
            if created:
                self.log("Created icon: {}", icon_obj.name)
                # Relatively costly operations are done after we know it needs
                # to be done, i.e. this is a new record.
                icon_obj.file.save(
                    icon['file'],
                    open(icons_path / icon['file'], 'r', encoding='utf-8')
                )
            else:
                self.log("Icon: {} exists.", icon_obj.name)
            if set(icon_obj.tags.all()) != set(tags):
                self.log("Setting Tags on {}.", icon_obj.name, tags)
                icon_obj.tags.add(*tags)
            else:
                self.log(
                    "Tags {} already set on {}.",
                    icon_obj.name,
                    ", ".join([t.name for t in tags])
                )
            icon_obj.save()
        except (FileNotFoundError, OSError) as exc:
            self.error(exc)

    def import_groups(self, groups):
        """
        Import icon groups defined in the iconjar metadata file.

        @param dict groups from the JSON data of the metadata file.
        """
        self._import_organisational_unit(self.groups, Group, groups)

    def import_sets(self, sets):
        """
        Import icon sets defined in the iconjar metadata file.

        @param dict sets from the JSON data of the metadata file.
        """
        self._import_organisational_unit(self.sets, IconSet, sets)

    def _import_organisational_unit(self, unit_store, unit_model, data):
        """
        Be DRY: Import similar organisation objects such as sets and groups.

        @param dict unit_store Where to keep a reference to the model instance.
        @param Group|IconSet Unit model
        @param dict data from the JSON data of the metadata file.
        """
        # First add all sets without hierarchy.
        for unit in data.values():
            unit_obj, created = unit_model.objects.get_or_create(
                name=unit['name'],
                uuid=unit['identifier'],
            )
            unit_store[unit['identifier']] = unit_obj
            if created:
                self.log(
                    "Created {}: {} ({})", unit_model._meta.model_name,
                    unit_obj.name,
                    unit_obj.uuid
                )

        # Now that all sets exist we can easily add their parents
        for unit in data.values():
            parent = unit.get('parent', None)
            if not parent:
                continue
            try:
                parent = self.sets.get(parent, self.groups[parent])
                child = unit_store[unit['identifier']]
                child.group = parent
                child.save()
            except KeyError as exc:
                self.error(
                    "{}: {} ({}) defines parent: {} which does not exist.",
                    unit_model._meta.model_name,
                    unit['name'],
                    unit['identifier'],
                    parent
                )
                raise exc

    def import_icon_tags(self, tags):
        """
        Insert tags of an icon if they don't exist yet.

        @param Iterable list or tuple or tags to add.
        @return list of Tag model instances that apply to the icon.
        """
        icon_tags = []
        for tag in tags:
            if tag not in self.tags.keys():
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                if created:
                    self.log("Created tag {}", tag)
                self.tags[tag] = tag_obj
            icon_tags.append(self.tags[tag])
        return icon_tags

    def get_jar_data(self, path):
        """
        Find jars in given path and extract data from an IconJar file.

        @param Path path of the IconJar file(s).
        @return list of tuples (icons_path, metadata)
        """
        jars = []
        if path.suffix == ".iconjar":
            paths = [path]
        else:
            paths = path.rglob('*.iconjar')
        for jar in paths:
            # There should be a dir with icons in the same directory as the
            # META file.
            meta_file = jar / "META"
            icons_path = meta_file.parent / "icons"
            if not icons_path.is_dir():
                raise IOError(
                    "Can't find an icons directory under {}".format(path)
                )
            if not meta_file.is_file():
                raise IOError(
                    "Can't find a META file under {}".format(path)
                )
            with gzip.open(meta_file, mode='rb') as meta_file_handle:
                metadata = json.load(meta_file_handle)
            jars.append((icons_path, metadata))
        return jars

    def uncompress(self, path):
        """
        Return raw data from GZIP files.

        Note: TempDirectory objects need to be cleaned after they are no longer
        needed. You should call tmpdir.cleanup()

        @param str|Path path of the compressed file.
        @return TempDirectory object of a temporary directory.
        """
        self.log("Uncompressing path: {}", str(path))
        tmpdir = tempfile.TemporaryDirectory(dir=MEDIA_ROOT)
        shutil.unpack_archive(str(path), tmpdir.name)
        return tmpdir

    @contextmanager
    def with_path(self, path):
        """
        Context for transparently using compressed files and dirs as dirs.

        @param Path path to the file or directory.
        @yield Path as a context, use with `with`.
        """
        path = Path(path)
        formats = shutil.get_unpack_formats()
        compressed_extensions = [ext for f in formats for ext in f[1]]
        ext = "".join(path.suffixes)
        is_compressed = any([ext.endswith(x) for x in compressed_extensions])
        if path.is_file() and is_compressed:
            # This is a compressed archive, uncompress it in a tmpdir and yield
            # the tmpdir as a Path.
            tmpdir = self.uncompress(path)
            yield Path(tmpdir.name)
            tmpdir.cleanup()
        else:
            # This is an existsing path, yield as is.
            yield path

    def log(self, logstr, *args, **kwargs):
        """
        Send a log message through Django.

        @param str logstr String to log through Django.
        """
        self.log_func(logstr, *args, **kwargs)

    def error(self, logstr, *args, **kwargs):
        """
        Log an error message through Django.

        @param str logstr String to log through Django.
        """
        self.errors += 1
        self.error_func(logstr, *args, **kwargs)
