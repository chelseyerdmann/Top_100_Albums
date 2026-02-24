# Fix "Invalid redirect URI" – Spotify Dashboard

The redirect URI in your **code** must **exactly match** one of the URIs in your **Spotify app settings**.

## What to put in the Spotify Dashboard

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and open your app.
2. Click **Settings** (or **Edit**).
3. Under **Redirect URIs**, add **exactly** this (copy-paste, no spaces):
   ```
   http://127.0.0.1:8080/callback
   ```
4. Click **Save**.

## Rules (from [Spotify’s docs](https://developer.spotify.com/documentation/web-api/concepts/redirect_uri))

- **Do not use** `localhost` – use `127.0.0.1` instead.
- Use **http** (not https) for local development.
- Use the **exact** format: `http://127.0.0.1:PORT/callback` (this project uses port **8080**).

## If you use a different port

If you already have a different URI in the Dashboard (e.g. `http://127.0.0.1:3000/callback`), tell me the **exact** URI and I’ll update the notebook and `.env` to match it.
