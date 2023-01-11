# Geocity - build your (geo)-forms easily! ![Geocity CI](https://github.com/yverdon/geocity/workflows/Geocity%20CI/badge.svg?branch=main)

**[What is Geocity ?](https://geocity.ch/about)**

**[Features and user guide](https://github.com/yverdon/geocity/wiki)**

## Contribution guideline

To contribute to the project use **[gitflow](https://www.atlassian.com/fr/git/tutorials/comparing-workflows/gitflow-workflow)**

The default configuration is used in this project, check below

```bash
git flow init
Branch name for production releases: [main]
Branch name for "next release" development: [develop]
Feature branches? [feature/]
Release branches? [release/]
Hotfix branches? [hotfix/]
Support branches? [support/]
Version tag prefix? []
```

To start a new feature use : `git flow feature start feature_branch` instead of `git checkout -b feature_branch`

To finish a feature there's two options:

1. The feature requires a review (most of the cases)
   - `git flow feature publish feature_branch` then create a PR from `feature_branch` to `main`
2. The feature doesn't require a review (small commits)
    - `git flow feature finish feature_branch`

Here is a cheatsheet to use `gitflow` **[gitflow-cheatsheet](https://danielkummer.github.io/git-flow-cheatsheet/)**

## Setting up full Docker non persistent demo

This will bring up a demo instance with preset fixtures served by the
Django development server in reload mode.

```bash
git clone git@github.com:yverdon/geocity.git && cd geocity
# copy default config
cp -n .env.example .env
# start the stack
docker-compose up --build -d --remove-orphans
# run the migrations
docker-compose run web scripts/migrate.sh
# load demo data
docker-compose run web python manage.py fixturize_demo
```

## Setting up production instance

### Database

1. Create a PostgreSQL database
2. Install required extensions:

```sql
CREATE EXTENSION postgis;
CREATE EXTENSION pg_trgm;
CREATE EXTENSION unaccent;
```

3. Edit DB connection in .env file

### Environment variables

:warning: :warning: :warning:

Set the following variables as follow

```ini
COMPOSE_FILE=docker-compose.yml
```

And review all other variables in order to fine tune your instance

### Deploying changes

New changes are deployed with the following command. :warning: **WARNING**: on PROD, docker-compose up will automatically
run migrations, collect static files, compile messages and update integrator permissions in the entrypoint.

```bash
# update the stack
docker-compose up --build -d --remove-orphans
```

## Default Site

The default site is automatically created and every PermitAdministrativeEntity is associated to this site.

If you have `www.geocity.ch` as domain, you should put `geocity.ch`

```ini
DEFAULT_SITE=geocity.ch
```

## Development tools

### Setup your Environment file

Following variable setup in your .env file will setup the development environment for you

```ini
PRIVATE_DOCUMENTS_DIR=C:\some\directory\for\mounting\geocity\private_documents
ARCHIVE_DIR=C:\some\directory\for\mounting\geocity\archive
DEFAULT_SITE=localhost
```

### Run the tests from within the docker container

Run tests in a the running container

```bash
docker-compose exec web python manage.py test --settings=geocity.settings_test
```

Run a specific test in the running container (adding the `--keepdb` flag speeds up iterations)

```bash
docker-compose exec web python manage.py test --settings=geocity.settings_test --keepdb geocity.apps.permits.tests.test_a_permit_request.PermitRequestTestCase.test_administrative_entity_is_filtered_by_tag
```

Test for report generation will fail when run in the running web container, because they spawn a test server to allow other container to communicate with it. You can run them in their own container, but need first to stop the running web container.

```bash
docker-compose stop web
docker-compose run --service-ports --name=web --rm --entrypoint="" web python manage.py test --settings=geocity.settings_test --keepdb geocity.tests.reports
```

These tests compare generated PDFs to expected PDFs. To regenerate the expected images, you need to provide the following env var to the docker-compose run command `-e TEST_UPDATED_EXPECTED_IMAGES=TRUE`. By definition, when doing so, tests will succeed, so don't forget to manually review the changes to the files.

```bash
docker-compose run --service-ports --name=web --rm --entrypoint="" -e TEST_UPDATED_EXPECTED_IMAGES=TRUE web python manage.py test --settings=geocity.settings_test --keepdb geocity.tests.reports
```

### Run the fixturize_demo.py

```bash
docker-compose exec web python manage.py fixturize_demo
```

### Linting

We use [pre-commit](https://pre-commit.com/) as code formatter. Just use the following command to automatically format your code when you commit:

```
$ pip install pre-commit
$ pre-commit install
```

If you wish to run it on all files:

```
$ pre-commit run --all-files
```

### Show urls

We use [django-extensions](https://django-extensions.readthedocs.io/en/latest/command_extensions.html?highlight=show_urls#command-extensions) to show urls. Can be used to export models to a file (as text or picture), to display them in terminal and much more things

```
./manage.py show_urls
```

### Testing emails

A Mailhog container is working on the dev environment, you can access it by going to localhost:8025.
Just ensure to setup the following entries in your `.env` file:

```ini
EMAIL_HOST=mailhog
EMAIL_PORT=1025
EMAIL_HOST_USER=null
EMAIL_HOST_PASSWORD=null
# Set TLS to false for mailhog
EMAIL_USE_TLS=false
EMAIL_TO_CONSOLE=false
```

### Dependency management

Dependencies are managed with [`pip-tools`](https://github.com/jazzband/pip-tools).

### Installing packages

To install a new package, add it to `requirements.in`, without pinning it to a
specific version unless needed. Then run:

```
docker-compose exec web pip-compile requirements.in
docker-compose exec web pip-compile requirements_dev.in
docker-compose exec web pip install -r requirements.txt
docker-compose exec web pip install -r requirements_dev.txt
```

Make sure you commit both the `requirements.in` and the `requirements.txt` files.
And the `requirements_dev.in` and the `requirements_dev.txt` files.

### Upgrading packages

To upgrade all the packages to their latest available version, run:

```
docker-compose exec web pip-compile -U requirements.in
docker-compose exec web pip install -r requirements.txt
```

To upgrade only a specific package, use `pip-compile -P <packagename>`.
The following commands will upgrade Django to its latest version, making sure
it's compatible with other packages listed in the `requirements.in` file:

```
docker-compose exec web pip-compile -P django requirements.in
docker-compose exec web pip install -r requirements.txt
```

## Permissions and authentication

### Permissions

The user belonging to backoffice group can be granted specific permissions:
- `view_private_submission`, "Voir les demandes restreintes": allows the user to make requests that are not visible by standard user. Typically during the setup stage of a new form configuration
- `amend_submission`,"Traiter les demandes de permis": allow the user the process (amend) the requests (fill the backoffice fields), require validation for other departments and print the documents
- `validate_submission`,"Valider les demandes de permis": allow the user to fill the validation form
- `classify_submission`,"Classer les demandes de permis" allow the user to accept/reject the requests if validations services have all accepted it
- `edit_submission`, "Éditer les demandes de permis": allow the user to edit de requests filled by another person

### Two factor authentication

You can enable 2FA by setting the variable `ENABLE_2FA` to `true`. Defaults to `false`.

### Access to admin views under 2FA

Super users require to enable 2FA to have access to the admin app.

Follow the following steps:

1. Go to the `/account/login/` and sign in with your super user credentials
2. Follow the steps to activate 2FA
3. Open `/admin/`

Next time you sign in, you will be asked for a token.
Once you provided your token go to `/admin/` to access the admin app.

### Locked failed logins

Django-axes is used to limit login attempts from users.
Please read https://django-axes.readthedocs.io/en/latest/index.html to learn how to use it.

### Geocity as a OAuth2 provider
* [Access to a ressources with QGIS](docs/OAuth2_Qgis.md)
* [Access to a ressources with a bearer token](docs/OAuth2_access_api.md)

### Consuming OAuth2 providers
You can login with a GeoMapFish account if you have one.
* Create a SocialApp using the GeoMapFish provider
* Add the fields required for oauth2 process:

```
client_id
secret
key
certificate_key
```

* Save the SocialApp, the GEOMAPFISH login is ready to use
* Don't create 2 SocialApp with the same provider

* Redirect URI configuration in oAuth provider for dev

```
http://localhost:9095/geomapfish/login/callback/
```

**Optional:**

Create a setting `SOCIALACCOUNT_PROVIDERS["geomapfish"]["APP"]` containing a dict with the same keys,
(`client_id`, `secret`, `key`, `certificate_key`).
This will override the data of any SocialApp with provider GeoMapFish.

**Warning:**

GeoMapFish login process will raise an error if no App settings and no SocialApp
object are present.

## Migrations

To run a migration, for example when the model has changed, execute
`manage.py makemigrations` from inside the docker service of the web app.
Then execute `manage.py migrate`.

```
docker-compose exec web python3 manage.py makemigrations <app_label>
docker-compose exec web python3 manage.py migrate <app_label> <migration_name>
```

For more information about Django's migrations, help is available at:

```
docker-compose exec web python3 manage.py makemigrations --help
docker-compose exec web python3 manage.py migrate --help
```

### Practical example

Note: prepend `docker-compose exec web ` to the following python calls if your app is containerized.

`<app_label>`: this is set automatically depending on which model file is modified. In Geocity, it will always be "permits" => so there is nothing to specify.

`<migration_name>`: we try to name it with something meaningful, but there is no convention, for example, this command: `python manage.py makemigrations -n my_changes_to_the_user_model` will automatically create the following migration file for the "permits" app_label: `0056_my_changes_to_the_user_model.py`

Finally, you can apply it using:
`python manage.py migrate permits 0056_my_changes_to_the_user_model`

## Wiki

Sidebar of wiki to show the new pages is managed by : [github-wiki-sidebar](https://www.npmjs.com/package/github-wiki-sidebar).

Used `_` instead of `:` for `Define the category separator` because the character was not allowed, the other parameters just press enter and keep it has default.

```bash
? Define the category separator for multi-level menu: _
? Define the format of the page links: ./%s
? Define the _Sidebar.md content template: %s
? Select the items to be excluded from menu: (Press <space> to select, <a> to toggle all, <i> to invert selection)
? Change the priority/order of the items in menu <space separated list of ids - ex: 0 2 3>
```

## Cronjobs

To manage the planned tasks we use the django-cron extension (https://github.com/Tivix/django-cron). The script to be executed is defined on the **permits/cron.py** file.

In order to run it on a server instance, modify the following line accordingly and add it to the crontab:

```
*/10 * * * * <path_to_manage.py>/manage.py runcrons >/dev/null 2>&1
```
