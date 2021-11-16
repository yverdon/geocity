# OAuth2, use bearer token to access to the WFS3 Open Feature api

## Register an external application

- Go to : <http://localhost:9095/oauth/applications/register/>
  - Name : `${YOUR_APP_NAME}`
  - Cliend id -> **Keep it**, you will need it later
  - Client secret -> **Keep it**, you will need it later
  - Client type : Confidential
  - Authorization grant type : Authorization code
  - Redirect uris : <http://127.0.0.1:7070/>
  - Algorithm : HMAC with SHA-2 256

---

## Connect to the new external application with QGIS

**⚠ Configuration is probably not totally correct, this documentation is still in progress, find how to configure correctly and fix it**

- Add a WFS layer
- Create a new connection to a server
  - Set a name
  - Put the url to the ressource. Example <http://localhost:9095/wfs3>
  - Create an OAuth2 authentication
    - Set a name
    - Set the request URL. Example <http://localhost:9095/oauth/authorize>
    - Set the token URL. Example <http://localhost:9095/oauth/token/>
    - Set the refresh token URL. Example <http://localhost:9095/oauth/token/>
    - Set the client ID
    - Set the client secret

**Please note the trailing slash "/" after the token URL**

Now you can try to connect.


---

## Other sources

Camp to camp have their own documentation for OAuth2 with QGIS, [here](https://camptocamp.github.io/c2cgeoportal/master/integrator/authentication_oauth2.html?highlight=oauth2).
