Access Token Generation
=======================

TokenGenerator
--------------

The TokenGenerator is used by the oauth2app.token.handler method to generate access tokens. It responds to several
grant types, specified through the grant_type request parameter.

* **authorization_code:** Grants an access token based on an authorization code issued via :doc:`authorize`.
* **refresh_token:** Refreshes an access token.
* **password:** Grants an access token based on a POST containing a username and password.
* **client_credentials:** Grants an access token based specific to the client to access internal resources.

Connect the handler method to the access endpoint. ::

    from django.conf.urls.defaults import patterns, url

    urlpatterns = patterns('',
        (r'^oauth2/token/?$',  'oauth2app.token.handler'),
    )

Module Reference 
----------------

.. automodule:: oauth2app.token
   :members:
   :undoc-members: