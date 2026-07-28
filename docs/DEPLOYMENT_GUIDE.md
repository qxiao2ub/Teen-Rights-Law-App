# GitHub and Streamlit Community Cloud Deployment Guide

## 1. Unzip the repository

Extract `Teen-Rights-Law-App-GitHub.zip`. The extracted folder should contain `streamlit_app.py`, `requirements.txt`, `src`, `data`, and the other repository files.

## 2. Upload to GitHub

### GitHub website method

1. Sign in to GitHub.
2. Select **New repository**.
3. Give the repository a name, such as `Teen-Rights-Law-App`.
4. Choose public or private visibility.
5. Create the repository without adding a second README or license.
6. Select **uploading an existing file**.
7. Drag the extracted files and folders into the upload page.
8. Commit the files to the `main` branch.

The ZIP file itself should not be the only file in the repository. Streamlit needs the extracted source files.

### Git command method

```bash
git init
git add .
git commit -m "Initial teen law education app"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## 3. Confirm repository layout

The repository root should look like this:

```text
streamlit_app.py
requirements.txt
README.md
src/
data/
.streamlit/
```

## 4. Deploy on Streamlit Community Cloud

1. Open `https://share.streamlit.io` and sign in with GitHub.
2. Select **Create app**.
3. Choose the GitHub repository and `main` branch.
4. Set the main file path to `streamlit_app.py`.
5. Open **Advanced settings** and select Python 3.12 when available.
6. Do not add secrets because this prototype does not use API keys.
7. Select **Deploy**.

## 5. Test after deployment

Check every navigation page:

- Home
- Ask the Rights Guide
- Learn
- Mini-Games
- Community Lab
- Progress and AI
- About and Safety

Also test:

- A normal question such as `What should I save after online harassment?`
- A privacy check by trying to post a phone number in the community lab.
- A prohibited evasion question to confirm the app gives a safe alternative.
- A quiz answer and progress export.

## 6. Common deployment problems

### `ModuleNotFoundError`

Confirm the missing package is listed in `requirements.txt`. Do not list Python built-in libraries such as `json`, `re`, or `datetime`.

### App cannot find `legal_topics.json`

Confirm `data/legal_topics.json` exists in the repository and that the folder name remains lowercase `data`.

### Streamlit cannot find the entrypoint

Set the main file path exactly to `streamlit_app.py`.

### App builds with an incompatible Python version

Delete and redeploy the Streamlit app, then select Python 3.12 in Advanced settings.

### Repository contains only the ZIP

Extract the ZIP locally and upload the individual repository files and folders.
