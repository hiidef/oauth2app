from setuptools import setup, find_packages
# Also requires python-dev and python-openssl
setup(

    name = "oAuth2",

    version = "0.0.1",

    packages = find_packages(),

    install_requires = ['Django>=1.2.3', 'simplejson>=2.1.5'],
    include_package_data = True,

    # metadata for upload to PyPI
    author = "John Wehr",
    author_email = "johnwehr@gmail.com",
    description = "Django oAuth2 App",
    license = "MIT License",
    keywords = "django oauth2 oauth app",
    url = "https://github.com/hiidef/oauth2"

)