# IconMason

Import IconJar files into a Django database and use consume them from a rest
API or use the bundled Vue frontend.

## Running the backend

The backend is a standard Django application, you will need to install
dependencies, install a proxy such as Nginx and configure a WSGI daemon to run it. Manuals are available for that here: [Deploying Django](https://docs.djangoproject.com/en/2.1/howto/deployment/)

To install dependencies:

``` bash
git clone git@github.com/SnijderC/IconMason.git
cd IconMason/
pip install -r requirements.txt
```

From here follow Django deployment instructions.

If you want to hack on this project you can run the development server which is __not__ suitable for production:

``` bash
./manage.py runserver 8080
```

## Running the frontend

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
