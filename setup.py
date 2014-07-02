from setuptools import setup, find_packages


setup(
    name="oauth2app",
    version="0.3.0",
    packages=find_packages(),
    install_requires=['Django>=1.2.3', 'simplejson>=2.1.5'],
    include_package_data=True,

    # metadata for upload to PyPI
    author="John Wehr",
    author_email="johnwehr@gmail.com",
    description="Django OAuth 2.0 Server App",
    license="MIT License",
    keywords="django oauth2 oauth app server",
    url="https://github.com/hiidef/oauth2app",
)
