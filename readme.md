# How To Run

To run this repository you will need to: 

    install docker 
        - Mac: https://docs.docker.com/desktop/install/mac-install/ 
        - Windows: https://docs.docker.com/desktop/install/windows-install/ 
        - Linux: https://docs.docker.com/desktop/install/linux-install/

    install docker-compose - https://docs.docker.com/compose/install/

## Docker using docker-compose

    open the base directory of the repository in your console

    run `docker-compose up -d`

    run `docker-compose exec web bash`

    when in the SH'd into the container, you can run django manage.py commands via the shortcut dj

    To start the django webserver run `djrun` (alias of `python manage.py runserver 0.0.0.0:8000`) 

    To run the gunicorn webserver run `djgun` (alias of `gunicorn core.wsgi:application --reload`) 

## Docker with Fabric

    install fabric - https://www.fabfile.org/installing.html

    open the base directory of the repository in your console

    run `fab build` to run the build steps for the docker container

    run `fab start` to start the docker container

    run `fab sh` to SH into the container

    when in the SH'd into the container, you can run django manage.py commands via the shortcut dj

    To start the django webserver run `djrun` (alias of `python manage.py runserver 0.0.0.0:8000`) 

    To run the gunicorn webserver run `djgun` (alias of `gunicorn core.wsgi:application --reload`) 

## view on heroku
    https://sddo-proj-sept2022.herokuapp.com/
