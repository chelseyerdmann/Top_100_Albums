# Get Spotify Data From Your Account

Follow these steps to pull **your** saved albums, liked songs, and playlists using this repo.

---

## 1. Get Spotify API credentials

1. Go to the **Spotify Developer Dashboard**: https://developer.spotify.com/dashboard  
2. Log in with your Spotify account.  
3. Click **Create app**.  
4. Fill in:
   - **App name**: e.g. `My Data Retrieval`
   - **App description**: optional
   - **Redirect URI**: use `http://localhost:8888/callback` (or any URL you control; localhost is fine for local scripts)
   - Check the agreement and click **Save**.  
5. Open your app → **Settings** (or **Edit**).  
6. Copy your **Client ID** and **Client Secret** (click **Show** next to Client Secret).

---

## 2. Install dependencies

From the repo folder:

```bash
pip install requests
```

Or, if you use conda:

```bash
conda install requests
```

---

## 3. Run the user data notebook

1. Open **`src/spotify_user_data_retrieval.ipynb`** in Jupyter Notebook, JupyterLab, or VS Code.  
2. In the **first cell**, replace:
   - `your_client_id` → your **Client ID**
   - `your_client_secret` → your **Client Secret**
   - `your_redirect_uri` → the **exact** Redirect URI you set in the Dashboard (e.g. `http://localhost:8888/callback`)  
3. **Run the first cell.**  
   - Your browser will open the Spotify authorization page.  
   - Log in if needed and click **Agree**.  
   - You’ll be sent to your redirect URI (e.g. `http://localhost:8888/callback?code=...`).  
4. In the **address bar**, copy the part after `?code=` and before any `&`.  
   - Example: if the URL is `http://localhost:8888/callback?code=AQBx...&state=...`, copy `AQBx...` (the full code).  
5. In the **second cell**, replace `your_authorization_code` with that code.  
6. **Run the second cell.**  
   - It will exchange the code for an access token and then call the API to fetch:
     - **Saved albums**
     - **Liked songs**
     - **Playlists**  
   - Results are printed in the notebook.

---

## 4. Redirect URI must match

The Redirect URI in the notebook must be **identical** to the one in the Spotify app settings (including `http` vs `https`, port, and path). If they don’t match, Spotify will show an error when you authorize.

---

## Notes

- The **access token** from step 3 expires after about an hour. To fetch data again later, run the first cell again to re-authorize and get a new code, then run the second cell with that new code.  
- The repo’s [README](https://github.com/nurulashraf/spotify-data-retrieval) and this guide are based on the same flow; the dashboard link above is the official place to create your app.
