# GitHub and Streamlit Community Cloud Deployment Guide

## 1. Unzip the repository

Extract `Legal-Counsel-Streamlit-GitHub.zip`. The extracted files should include `streamlit_app.py`, `requirements.txt`, `src/`, `data/`, `.streamlit/`, and the other project files.

## 2. Upload the extracted repository to GitHub

A suggested repository name is `Legal-Counsel-Teen-Law-App`.

### GitHub website method

1. Create a new GitHub repository.
2. Do not add a second README or license if you plan to upload all files from this package.
3. Extract this ZIP on your computer.
4. Upload the extracted files and folders so that `streamlit_app.py` is at the **root** of the GitHub repository.
5. Commit the upload to the `main` branch.

### Git Bash / terminal method

```bash
git init
git add .
git commit -m "Add Legal Counsel Streamlit app"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## 3. Confirm the repository root

```text
streamlit_app.py
requirements.txt
README.md
src/
data/
.streamlit/
docs/
tests/
```

Do **not** upload only the ZIP file. Streamlit must be able to see the extracted `streamlit_app.py` and `requirements.txt`.

## 4. Deploy to Streamlit Community Cloud

1. Sign in to Streamlit Community Cloud with GitHub.
2. Create a new app from your GitHub repository.
3. Select the `main` branch.
4. Set the main file path to `streamlit_app.py`.
5. Choose a supported Python version compatible with the packages in `requirements.txt` (Python 3.12 is a safe choice for this repository).
6. No API key is required for the included local legal-learning engine.
7. Deploy the app.

## 5. Validate the migrated UI

Open each navigation tab:

- Home
- Voicebox
- Chatbox
- Minigames
- Learn
- Community
- Progress
- Features

Also check:

- Legal Counsel branding and Nova assistant branding.
- Author credit shows **Arya Patel** and mentor credit shows **Dr. Qingyang Xiao**.
- The author's first name is not used as product/assistant branding.
- Voicebox can capture browser audio, accept a confirmed transcript, and read a generated answer aloud.
- Chatbox answers a general legal-learning question.
- Mini-game answers update Progress Gavel metrics.
- Community moderation rejects obvious personal contact information.
- Progress export downloads JSON.

## 6. Common deployment issues

### `ModuleNotFoundError`

Confirm every third-party package is listed in `requirements.txt`. Keep `src/__init__.py` in the repository.

### App cannot find `legal_topics.json`

Keep `data/legal_topics.json` in its current location and preserve the lowercase `data` directory name.

### Streamlit cannot find the entrypoint

Set the main file path exactly to `streamlit_app.py` and confirm that file is not nested inside another folder in GitHub.

### App contains only a ZIP file

Extract the package before uploading it to GitHub. Streamlit Community Cloud cannot use the source if the application files remain only inside the ZIP.
