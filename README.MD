# IconMason

Import IconJar files into a Django database and use consume them from a rest
API or use the bundled Vue frontend.

## Running the back-end

The backend is a standard Django application, you will need to install
dependencies, install a proxy such as Nginx and configure a WSGI daemon to run
it. Manuals are available for that here:
[Deploying Django](https://docs.djangoproject.com/en/2.1/howto/deployment/)

To install dependencies:

``` bash
git clone git@github.com/SnijderC/IconMason.git
cd IconMason/
pip install -r requirements.txt
```

From here follow Django deployment instructions.

If you want to hack on this project you can run the development server which
is __not__ suitable for production:

``` bash
./manage.py runserver 8080
```

## Running the front-end

You can make a build of the static Vue application by running:

``` bash
cd frontend/
npm run build
```

You can put the files in `dist` on any server that serves static file.

If you want to hack on the frontend you can start it by running:

```
cd frontend/
npm run dev
```

__Note:__ There is nothing served from the index of the django instance, it
will give you a `404` error page. There is only an AIP, if you want so "see"
the API, there is a GUI at: `[yourhostname]:[port]/api` that is browsable and
that has a schema generator.


## Adding users

You will first need to add an admin account, following the usual procedure to
create Django super users.

```bash
./manage.py createsuperuser
```

This user can add more users, you can find the Django admin interface at: `[
yourhostname]:[port]/admin`.

## Importing IconJars

This application reads proprietary IconJar files, it is currently the only way
to get icons to appear in the interface. There is no file upload facility yet
either. Instead you should upload the IconJar to the server using something
like `scp` and then import it using the custom Django command:

```
./manage.py importiconjar [path]
```

This import command supports directories as well as compressed archives (ZIP,
GZIP, BZ, LZ, etc.) Anything that contains the structure of an IconJar: `icons/
` directory and `META` file containing JSON data should import. There is an
open source icon set (Google Material) in the `test/fixtures/` directory to
get you started.

```
./manage.py importiconjar ./backend/tests/fixtures/google-material–icons.iconjar.tgz
```

It may take a while for bigger sets to import. This might be improved in the
future.