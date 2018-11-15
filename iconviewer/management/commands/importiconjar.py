"""Feed this command an IconJar file to import it into the iconviewer."""
import shutil
import gzip
import tempfile
import json
from pathlib import Path
from iconviewer.models import Icon, Tag, Group, Set
from django.core.management.base import BaseCommand, CommandError


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

    def handle(self, *args, **options):
        """Run the importer module with the given arguments."""
        try:
            path = options['path']
            stdout = self.stdout if options['verbosity'] > 1 else None
            importer = IconJarImporter(path, stdout)
            if importer.jars:
                self.stdout.write(
                    "Importing these iconjars: \n- {}".format(
                        "\n- ".join([str(p[0].parent) for p in importer.jars])
                    )
                )
                importer.import_all()
                self.stdout.write(self.style.SUCCESS(
                    "Successfully imported your IconJars!"
                ))
            else:
                self.stdout.write(self.style.ERROR(
                    "No IconJars found with {}".format(path)
                ))
        except Exception as exc:
            raise exc
            raise CommandError(exc)


class IconJarImporter:
    """Load data from an IconJar file into the django database."""

    def __init__(self, path, stdout=None):
        """
        Import iconjars.

        @param str path to an iconjar(s)
        """
        self.stdout = stdout
        self.tags = {}
        self.groups = {}
        self.sets = {}
        self.path = path
        self.jars = self.get_jar_data(path)

    def import_all(self):
        """
        Import icon groups (sets) defined in the iconjar metadata file.

        @param dict metadata Decoded JSON from the metadata file.
        @param Path icons_path Icon path corresponding with the metadata file.
        """
        for icons_path, metadata in self.jars:
            self.import_sets(metadata['sets'])
            self.import_groups(metadata['groups'])
            for icon in metadata['items'].values():
                self.import_icon(icon, icons_path)

    def import_icon(self, icon, icons_path):
        """
        Import icons defined in the iconjar metadata file.

        @param dict metadata from the JSON data of the metadata file.
        """
        tags = self.import_icon_tags(icon.get('tags', "").split(","))

        icon, created = Icon.objects.get_or_create(
            uuid=icon['identifier'],
            name=icon['name'],
            file=icon['file'],
            parent=self.sets.get(icon['parent'], None),
            svg=(icons_path / icon['file']).read_text(encoding='utf-8')
        )
        self.log("Created icon: {}".format(icon.name))
        icon.tags.add(*tags)
        icon.save()

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
        self._import_organisational_unit(self.sets, Set, sets)

    @staticmethod
    def _import_organisational_unit(unit_store, unit_model, data):
        """
        Be DRY: Import similar organisation objects such as sets and groups.

        @param dict unit_store Where to keep a reference to the model instance.
        @param Group|Set Unit model
        @param dict data from the JSON data of the metadata file.
        """
        # First add all sets without hierarchy.
        for unit in data.values():
            unit_obj = unit_model(
                name=unit['name'],
                uuid=unit['identifier'],
            )
            unit_obj.save()
            unit_store[unit['identifier']] = unit_obj

        # Now that all sets exist we can easily add their parents
        for unit in data.values():
            parent = unit.get('parent', None)
            if not parent:
                continue
            parent = unit_store.get(parent, None)
            if parent:
                child = unit_store[unit['identifier']]
                child.parent = parent
                child.save()

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
                    self.log("Created tag {}".format(tag))
                self.tags[tag] = tag_obj
            icon_tags.append(self.tags[tag])
        return icon_tags

    @classmethod
    def get_jar_data(cls, path):
        """
        Find jars in given path and extract data from an IconJar file.

        @param str path of the IconJar file(s).
        @return list of tuples (icons_path, metadata)
        """
        path = Path(path)
        compressed_extentions = shutil.get_unpack_formats()[1]
        extension = ".".join(path.suffixes)
        try:
            if path.is_file() and extension in compressed_extentions:
                path = cls.uncompress(path)
            jars = []
            for meta_file in path.rglob("META"):
                # There should be a dir with icons in the same directory as the
                # META file.
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

        finally:
            # Clean up the temp file if the input was a compressed file.
            try:
                path.cleanup()
            except AttributeError:
                pass

        return jars

    @staticmethod
    def uncompress(path):
        """
        Return raw data from GZIP files.

        @param str|Path path of the compressed file.
        @return Path object of a temporary directory context.
        """
        self.log("Uncompressing iconjar META file: {}".format(path))
        tmpdir = tempfile.TemporaryDirectory()
        shutil.unpack_archive(path, tmpdir)
        return Path(tmpdir)

    def log(self, logstr):
        """
        Send a log message through Django.

        @param str logstr String to log through Django.
        """
        if self.stdout:
            self.stdout.write(logstr)