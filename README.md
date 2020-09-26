# EMS
An API web application designed to manage and review employee tasks.

## Setup of development environment

Clone this project:

    $ git clone git@github.com:atleyvarghese/ems.git

It is best to use the python `virtualenv` tool to build locally:

```sh
$ virtualenv -p python3 venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ source env/local.env
$ python manage.py migrate
```

Redis is used as the celery broker, you can get how to install redis [here](https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04)
The Sample data has a cron scheduled for 1 am(UTC) on every Monday
To run the celery worker use the following command:

    $ celery -A ems worker -l info

To run the celery beat use the following command:

    $ celery -A ems beat -l info


## Populating sample data
Use the following commands to populating sample data.
Sample username / password are
* superadmin / password
* employee / password
* employee1 / password


    $ python manage.py loaddata fixtures/*


## Starting app

    $ python manage.py runserver

The app will be served by django **runserver**

Access it through **http://localhost:8000**
