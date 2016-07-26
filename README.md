# Flask Boilerplate
This is a boiler plate flask application for larger applications.  I have created this project because I have found that working examples of larger flask based 
applications to be somewhat lacking. 

## Requirements
To use this for your flask application some requirements must be meet. I highly recommend the use of the use of virtualenv!

    1. You have Python 2.7.x installed
    2. You have Python PIP installed
    3. You have Node Package Manager installed (npm)    

## What is included
I have baked in flask extensions that I find to be useful for nearly all my flask projects. Node asset management with bootstrap-sass and font-awesome. I have also
extended some of the extensions to make them slightly easier to use (in my humble opinion), and some customizations I make to every flask application. I have also
setup a directory structure that I find to be easy to work with that helps to organize my projects better.
#### Backed In:
    1. SQLAlchemy, Flask-SQLAlchemy, and SQLAlchemy-Utils
    2. Alembic (for database migrations)
    3. Celery, Flask-Celery, Flask-Celery-Helper, a Custom Task Router
    4. Flask-Script; with some custom commands to wrap running gulp tasks and some database commands
    5. Flask-DebugToolbar
    6. Flask-Classy; with a custom base view class for class based views
    7. Flask-Admin
    8. WTForms
    9. PyYAML, used here for database seeds
    10. Gunicorn, for application server with gevent
    11. Bootstrap-sass
    12. Font-Awesome
    
#### Work in Progress
This project is a work in progress, documentation and base are not yet fully developed. Support for the community is welcome!