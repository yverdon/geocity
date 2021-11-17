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

## Connect to the new external application with QGIS

- Add a WFS layer
- Create a new connection to a server
  - Set a name
  - Set the ressource URL (example <http://localhost:9095/wfs3/>)
  - Create an OAuth2 authentication
    - Set a description
    - Set the request URL (example <http://localhost:9095/oauth/authorize/>)
    - Set the token URL (example <http://localhost:9095/oauth/token/>) **Note the trailing `/`**
    - Set the refresh token URL (example <http://localhost:9095/oauth/token/>)
    - Set the client ID
    - Set the client secret
- Connect to this server
  - A new web page will open and will ask
    - To login to Geocity
    - To authorize QGIS to access Geocity features
- Add the permits layers
  - Set the layer CRS to `EPSG:2056` before adding it to the map (also the project if not already the case)

## Other sources

Camptocamp have their own documentation for OAuth2 with QGIS, [here](https://camptocamp.github.io/c2cgeoportal/master/integrator/authentication_oauth2.html?highlight=oauth2).
