oauth2app Test Django Project
--------------------------------

Installation
------------

The project uses django.db.backends.sqlite3 and requires minimal configuration. ::
    
    git clone git@github.com:hiidef/oauth2app.git oauth2app
    cd oauth2app/tests/testsite
    git checkout master
    pip install https://github.com/hiidef/oauth2app/tarball/master django-test-coverage
    python manage.py test api

