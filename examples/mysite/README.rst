The example site uses django.db.backends.sqlite3, virtualenv and requires minimal configuration. ::
    
    # create and activate virtualenv
    virtualenv oauth2_mysite
    source oauth2_mysite/bin/activate
    # install required python modules
    pip install https://github.com/hiidef/oauth2app/tarball/master django django-uni-form django-nose
    # create folder for temporary code
    mkdir code && cd code
    # clone oauth2app repository
    git clone https://github.com/hiidef/oauth2app.git oauth2app
    cd oauth2app/examples/mysite
    # syncdb and run development server
    python manage.py syncdb --noinput
    python manage.py runserver

Visit http://127.0.0.1:8000/ on your local machine and follow the instructions.