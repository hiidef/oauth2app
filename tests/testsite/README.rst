oauth2app Test Django Project
--------------------------------

* See http://hiidef.github.com/oauth2app for documentation. 
* See https://github.com/hiidef/oauth2app for source code.

Installation
------------

The project uses django.db.backends.sqlite3 and requires minimal configuration. ::
    
    git clone git@github.com:hiidef/oauth2app.git oauth2app
    cd oauth2app/tests/testsite
    git checkout master
    pip install https://github.com/hiidef/oauth2app/tarball/master
    python manage.py test api

