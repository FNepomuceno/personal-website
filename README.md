# ABOUT
- The website uses the Django framework in Python as its backend
- PostgreSQL is used as the database
- Gunicorn and Nginx are used for deploying the project online

## USING THE VIRTUAL ENVIRONMENT
- in the root directory, enter:
> source webenv/bin/activate
- to exit out of the virtual environment, enter:
> deactivate

## SETUP
- The project uses PostgreSQL. Follow the instructions to set up the PostgreSQL database at the following website:
> https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04#create-the-postgresql-database-and-user
- The database information and Django secret key are kept in a file called secret.py. Rename the secret.py.template file to secret.py and fill in the relevante information.
