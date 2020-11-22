# Picture gallery

A small picture gallery built with Django

## How to deploy?

Deployement is made relatively easy in this project with the help of Docker containers.

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (obviously...)
- [Docker compose](https://docs.docker.com/compose/install/) as well
- A working web server, such as Apache or Nginx. You don't need anything in particular, or anything that can handle WSGI request, it will only act as a reverse proxy to route the incoming request to the Nginx container.

### 1 - Get the code

```
git clone https://github.com/bastantoine/django-picture-gallery.git
```

### 2 - Configure the `.env` files

Inside `docker/prod/env` you will find 3 files `db.prod.env.sample`, `django.prod.env.sample` and `gunicorn.prod.env.sample`.

First copy them and remove the `.sample`.
Then update the values if needed:

#### 2.2 - Configuration `db.prod.env`

| Variable           | Explanation                                             |
|--------------------|---------------------------------------------------------|
| `POSTGRES_USER`    | The username to use in the Postgres DB                  |
| `POSTGRES_PASSWORD`| The password to use in the Postgres DB                  |
| `POSTGRES_DB`      | The database to use in Postgres                         |

**Note:** there are others environment variables you can set there, check out the [PG Docker Hub page](https://hub.docker.com/_/postgres) for more info

#### 2.2 - Configuration `django.prod.env`

| Variable       | Explanation                                                 |
|----------------|-------------------------------------------------------------|
| `SQL_ENGINE`   | Leave it to `django.db.backends.postgresql` if you are using the Postgres container |
| `SQL_DATABASE` | Same value as `POSTGRES_DB`                                 |
| `SQL_USER`     | Same value as `POSTGRES_USER`                               |
| `SQL_PASSWORD` | Same value as `POSTGRES_PASSWORD`                           |
| `SQL_HOST`     | Leave it to `db` if you are using the Postgres container    |
| `SQL_PORT`     | Leave it to `5432` if you haven't changed the mapping of the ports in the `docker-compose.prod.yml` file |
| `DATABASE`     | Leave it to `postgres` if you are using the Postgres container, this way gunicorn will wait for the PG db to be up to start |
| `DEBUG`        | Leave it to `0`                                             |
| `SECRET_KEY`   | The secret key of Django                                    |
| `PAGETITLE`    | The base title page to use as tab names                     |

#### 2.3 - Configuration `gunicorn.prod.env`

| Variable       | Explanation                                                 |
|----------------|-------------------------------------------------------------|
| `ACCESS_LOG`   | The `.log` file to use for the access logs of gunicorn      |
| `ERROR_LOG`    | The `.log` file to use for the error logs of gunicorn       |

### 3. Build and up the prod images

```
docker-compose -f docker/prod/docker-compose.prod.yml up -d --build
```

**Note:** make sure all the images are up and running with: `docker ps`, you should see all 3 images (gunicorn, postgres and nginx).

You have trouble there, remove the logging system of gunicorn in `docker/prod/docker-entrypoint.sh` and try with `docker-compose -f docker/prod/docker-compose.prod.yml up --build`

### 4. Django migrations and collectstatic

```
docker-compose -f docker/prod/docker-compose.prod.yml exec web python manage.py makemigrations core
docker-compose -f docker/prod/docker-compose.prod.yml exec web python manage.py migrate --noinput
docker-compose -f docker/prod/docker-compose.prod.yml exec web python manage.py collectstatic --noinput
```

### 5. Configure your web server

The nginx image has its port `1337` mapped to host port `80`, so you need to configure your web server to route all incoming calls to your app to the port `1337`.

If you are using Nginx, you can follow the steps below, otherwise you'll have to look at your server's doc.

1. Configure a new site in `/etc/nginx/sites-available`, and paste the following:

```
upstream picture_gallery {
	server localhost:1337;
}

server {
        listen 80;
        listen [::]:80;

        server_name ...; # Set here the name of your domain or subdomain

	location / {
		proxy_pass http://picture_gallery;
        	proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
	        proxy_set_header Host $host;
        	proxy_redirect off;
	        client_max_body_size 20M;
	}

}
```

2. Enable it:

```
cd /etc/nginx/sites-enabled
ln -s /etc/nginx/sites-available/<yournewsite> <yournewsite>
```

3. Test the conf by running `nginx -t`. If everything is ok, reload nginx to apply the new conf.

And voilà!

### Note:

If you start with an empty database, you won't have any user account created, so no way to access to the admin panel. To create one, there's two possibilities:

1. You run the custom `initadmin` command (`docker-compose -f docker/prod/docker-compose.prod.yml exec web python manage.py initadmin`). This command wil create a superuser with `admin` as username and password, so be sure to either update it, or create an account with a more secure username and password.

2. Directly run the `createsuperuser` command in the `web` container

```
sudo docker exec -it web /bin/sh # Alpine images doesn't have bash, only sh

python manage.py createsuperuser
```
