# Basic OAuth2.0 API
Built using Google Auth, Flask & React Typescript


This API uses Google Secure OAuth2.0 Authentication to sign in users into your website.


**Features**
- Landing Page with "Sign In With Google" button
- API endpoints for interacting with Google and frontend
- Dashboard page showing the retrieved user's info

### Build Instructions

1. Setting up the environment

***a. Python Environment***
- Inside root folder, run `python3 -m venv env`. Ensure you have `python` installed already on your system.
- In your terminal, run `. activate`.
- In your terminal with a "(env)" before your device's name, run `. installpy`.
- Wait till all packages are fully installed.

***b. React Environment***
- Inside root folder, run `cd frontend`.
- Inside frontend directory, run `npm install`. Ensure you have `node` and `npm` installed already on your system.
- Wait till all packages are fully installed.

2. Configuring the environment

***a. Python Configuration***
- In root directory, rename `.env.example` to `.env`.
- Get your secure credentials from Google Cloud Console and replace them in the new `.env` file.
- Replace only (GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)
- Generate any secure key (string) and save it as your (FLASK_SECRET_KEY) for sessions


3. Run the development servers

***a. Run Python***
- Inside the (.env) terminal, run `. run`
- You should see something like this

```bash
✅ Database initialized successfully!
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
✅ Database initialized successfully!
 * Debugger is active!
 * Debugger PIN: 452-163-820
```

***b. Run React***
- Inside the frontend directory in another terminal, run `npm run dev`
- You should see something like this

```bash
> googleauth@0.0.0 dev
> vite


  VITE v8.0.12  ready in 2315 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help

```

### Test Instructions

**NOTE: Ensure you're connected to the internet**
1. Testing the API endpoints

***a. Python***
- API endpoints exposed are: 
    - /api/v1/health - GET request
    - /api/v1/auth/google - GET request
    - /api/v1/auth/callback - GET request
    - /api/v1/auth/me - GET request
    - /api/v1/auth/logout - GET request
    - /api/v1/auth/debug - GET request
- Test any endpoint with `curl` with the following

```curl
curl http://127.0.0.1:5000/api/v1/health
```

- You should see something like this

``` bash
{
  "code": 200,
  "message": "Service is up and running at 15:57:09",
  "status": "SUCCESS"
}
```

- Replace the `/api/v1/health` with other endpoints


***b. React***

To visualize the effect of the endpoints
- Go to any browser and enter `http://127.0.0.1:5173` as the url
- View the landing page
- Click on "Sign In with Google" to authenticate
- Authenticate with any of your google accounts
- It will redirect you to your Dashboard
- View your details as fetched from google
- Click on "Sign Out" to log out from the site


### Authors
***Name: Okesh***


***Version: 1.0.0***


***Portfolio: Backend Developer***


***Link: [Github](https://github.com/Okesh101)***
