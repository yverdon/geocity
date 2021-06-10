# OAuth2, use bearer token to access to the api

## Register an extern app

- Go to : <http://localhost:9095/oauth/applications/register/>
  - Name : `${YOUR_APP_NAME}`
  - Cliend id -> **Keep it**, you will need it later
  - Client secret -> **Keep it**, you will need it later
  - Client type : Confidential
  - Authorization grant type : Authorization code
  - Redirect uris : <http://localhost:9095/noexist/callback>
  - Algorithm : HMAC with SHA-2 256

---

## Connect to the new extern app

- Go to : <http://localhost:9095/oauth/authorize/?response_type=code&client_id=${CLIENT_ID}>
  - Click on "Authorize"
  - An HTTP 404 is expected here, cause redirect URL doesn't exist
  - **Keep the code** in 404 url, `code=......`

---

## Get access token

Here you can use an API Client, like [Insomnia](https://insomnia.rest/), [Postman](https://www.postman.com/), [hoppscotch](https://hoppscotch.io/). Use your favorite programming language or simply with a terminal.

If you want to use the following curl in a API Client, simply use `Form URL Encoded`, the `Body` tab will be replaced by `Form` tab and the header `Content-Type: application/x-www-form-urlencoded` will automatically appear. For each `-H` write the content in `Header` tab. For each `-d` write the content in `Form` tab and for the `Bearer token`, under the `Auth` tab you can select `Bearer` and simply give the `access_token`.

- Multiline advice for curl requests :
  - `^` is for windows
  - `\` is for linux

```bash
    curl -X POST ^
    -H "Cache-Control: no-cache" ^
    -H "Content-Type: application/x-www-form-urlencoded" ^
    "http://localhost:9095/oauth/token/" ^
    -d "client_id=${ID}" ^
    -d "client_secret=${SECRET}" ^
    -d "code=${CODE}" ^
    -d "redirect_uri=http://localhost:9095/noexist/callback" ^
    -d "grant_type=authorization_code"
```

- Copy the response. Here is an example :

```json
{
  "access_token": "JlR0B5PxLg4IZjS6EYDdvnoVEFpTG8",
  "expires_in": 36000,
  "token_type": "Bearer",
  "scope": "read write",
  "refresh_token": "ELSajrfZX8ddCqbjLKMzObm5Gnbjxj"
}
```

---

## Access to the ressource with the token

- User curl with access token to get access to the resource (remplace "^" with "\" on linux)

```bash
    curl ^
    -H "Authorization: Bearer ${ACCESS_TOKEN}" ^
    -X GET http://localhost:9095/rest/permits/
```
