Settings
=========

The following settings can be specified in Django settings.py:

Client Key Length
-----------------
::

   OAUTH2_CLIENT_KEY_LENGTH

Length of the client key.

*Default 30*

Client Secret Length
--------------------
::

   OAUTH2_CLIENT_SECRET_LENGTH

Length of the client secret.

*Default 30*

Code Key Length
---------------
::

   OAUTH2_CODE_KEY_LENGTH

Length of the code key.

*Default 30*

Access Token Length
-------------------
::

   OAUTH2_ACCESS_TOKEN_LENGTH

Length of the access token.

*Default 10*

Refresh Token Length
--------------------
::

   OAUTH2_REFRESH_TOKEN_LENGTH

Length of the refresh token.

*Default 10*

Refreshable Tokens
------------------
::

   OAUTH2_REFRESHABLE

Issue refreshable tokens.

*Default True*

Authorization Code Expiration
-----------------------------
::

   OAUTH2_CODE_EXPIRATION

Number of seconds in which an authorization code should expire.

*Default 120*

Access Token Expiration
-----------------------
::

   OAUTH2_ACCESS_TOKEN_EXPIRATION

Number of seconds in which an access token should expire.

*Default 3600*

MAC Authentication
------------------
::

   OAUTH2_MAC_KEY

Send MAC style authentication parameters. See http://tools.ietf.org/html/draft-ietf-oauth-v2-http-mac-00

*Default True*

