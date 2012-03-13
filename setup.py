from setuptools import setup, find_packages
import codecs
import os
import sys

def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(

    name = "oauth2app-draft-16",

    version = "0.3.0",
    
    long_description=read('README.rst'),
    
    packages = find_packages(),

    install_requires = ['Django>=1.2.3', 'simplejson>=2.1.5', "django-uni-form>=0.8.0"],
    include_package_data = True,

    # metadata for upload to PyPI
    author = "John Wehr",
    author_email = "johnwehr@gmail.com",
    description = "Django OAuth 2.0 Server App",
    license = "MIT License",
    keywords = "django oauth2 oauth app server",
    url = "https://github.com/hiidef/oauth2app"

)
