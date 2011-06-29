oauth2app Example Django Project
--------------------------------

* See http://hiidef.github.com/oauth2app for documentation. 
* See https://github.com/hiidef/oauth2app for source code.

Installation
------------

The project uses django.db.backends.sqlite3 and requires minimal configuration. ::

    pip install https://github.com/hiidef/oauth2app/tarball/master
    python manage.py syncdb
    python manage.py runserver

Visit http://127.0.0.1:8000/ on your local machine and follow the instructions.