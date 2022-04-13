# Epoque.art Website

## Stack of used technology

> Backend:
1. Python 3.9
2. Django 4.1
3. Gunicorn
4. Django related addons (watch requirements.txt)
5. PostgreSQL
6. Docker (including docker-compose)
7. Node.JS (used for compressing and obfuscating static files)
8. nginx (reverse proxy for gunicorn)
9. nginx-acme-companion (used to issue ssl certs)

> Frontend:
1. HTML
2. CSS
3. SASS

## Deploy or dev

### Development mode

#### Preparation

> Create some files in root directory of the project:
>> .env.dev
```
DEBUG=1
SECRET_KEY=SECURE_KEY
DJANGO_ALLOWED_HOSTS=*
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=epoqueart_dev
SQL_USER=epoqueart
SQL_PASSWORD=cVXeqT9JBGsUi26pPgfUX7sZieouUjOWbnk6TCAONLNkUY6M2QJnorj1hJqI88X
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

>> .env.dev.db
```
POSTGRES_USER=epoqueart
POSTGRES_PASSWORD=cVXeqT9JBGsUi26pPgfUX7sZieouUjOWbnk6TCAONLNkUY6M2QJnorj1hJqI88X
POSTGRES_DB=epoqueart_dev
```

------

#### Run project
>`sudo docker-compose -f docker-compose.yml -d --build`
>This command will build and start two containers - for db and website itself.

**Development server will be available on localhost:8000**

**A feature of the development server is that you can edit some files without restarting the containers, all your changes will be displayed dynamically.**

-------

#### Get name of web container
> Run  in root of the project - `sudo docker-compose -f docker-compose.yml ps`

>###### Example of output
>![Example of output](https://i.imgur.com/PGjaYPY.png "Example of output")

>In our case name of our web container is `epoqueart_web_1`

-------

#### Log into our web container

>`sudo docker container exec -it epoqueart_web_1 "/bin/sh"`
> ###### Example of output
>![Example of output](https://i.imgur.com/iGJ8KlJ.png "Example of output")

> Here we see interactive shell, where we can run tests, create superuser and interact with django manage.py

##### Example of creating superuser
> Run command in our interactive container shell - `python manage.py createsuperuser` and then follow the instructions.

##### Example of running tests
> Run command in our interactive container shell - `python manage.py test` and you should see OK output without errors.

###### Output
![Example of output](https://i.imgur.com/mxSMKVb.png "Example of output")

-------

#### Example of checking internal debug log
> Run command in our interactive container shell - `cd logs && cat debug.log`, if you want to display it constantly, run `cd logs && tail debug.log -f`

-------

#### Checking logs of containers
> Run  in root of the project - `sudo docker-compose -f docker-compose.yml logs`, if you want to display it constantly, run `sudo docker-compose -f docker-compose.yml logs -f`



### Production

#### Preparation

> Create some files in root directory of the project:
>> .env.prod
>> Replace SECRET KEY with randomly generated string with symbols and numbers (recommended length - 50)
```
DEBUG=0
SECRET_KEY=<SECRET KEY>
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=epoqueart_prod
SQL_USER=epoqueart
SQL_PASSWORD=cVXeqT9JBGsUi26pPgfUX7sZieouUjOWbnk6TCAONLNkUY6M2QJnorj1hJqI88X
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
VIRTUAL_HOST=epoque.art
VIRTUAL_PORT=8000
LETSENCRYPT_HOST=epoque.art
```

>> .env.dev.db
```
POSTGRES_USER=epoqueart
POSTGRES_PASSWORD=cVXeqT9JBGsUi26pPgfUX7sZieouUjOWbnk6TCAONLNkUY6M2QJnorj1hJqI88X
POSTGRES_DB=epoqueart_dev
```

>> .env.prod.proxy-companion
```
DEFAULT_EMAIL=admin@epoque.art
NGINX_PROXY_CONTAINER=nginx-proxy
```

---


#### Deploy

> Run in the root of the project - `sudo docker-compose -f docker-compose.prod.yml up -d --build`
> Wait till process end, then website will be deployed successfully.

**Website in production mode should be rebuild after change in source code of the project.**

---

#### Bind domain

> Open ports 80, 443 on your production server, then get public ipv4, and add DNS record (type A) to domain with public address of your server. DNS propagation takes up to 24 hours, but in real life it takes approximately from 10 minutes to 1 hour.


&copy; 2022 appxpy - [appxpy.com](https://appxpy.com "appxpy.com")