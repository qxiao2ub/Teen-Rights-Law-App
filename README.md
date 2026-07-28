# Teen Rights and Law Lab

An open-source Streamlit prototype that helps teenagers learn general legal concepts, rights, privacy, evidence preservation, and safe next steps in everyday language.

**Author:** Arya Patel  
**Mentor:** Dr. Qingyang Xiao

> Educational information only. This project is not legal advice, is not a verified legal database, and should not be used during an emergency.

## Features

- Transparent TF-IDF natural-language topic routing.
- Teen-friendly topic cards stored in a reviewable JSON knowledge base.
- Safety screening before every educational response.
- Mini-games and session-only progress tracking.
- K-means clustering of non-sensitive learning preferences.
- A bounded epsilon-greedy activity recommender.
- Community-post moderation for obvious privacy and safety risks.
- Browser text-to-speech.
- Colab-ready core-AI notebook.
- Streamlit Community Cloud deployment files.

## Repository structure

```text
Teen-Rights-Law-App/
|-- streamlit_app.py
|-- requirements.txt
|-- data/
|   `-- legal_topics.json
|-- src/
|   |-- __init__.py
|   `-- legal_engine.py
|-- notebooks/
|   `-- Teen_Law_App_Colab_Prototype.ipynb
|-- docs/
|   |-- DEPLOYMENT_GUIDE.md
|   |-- IOS_APP_ROADMAP.md
|   |-- CONTENT_REVIEW_CHECKLIST.md
|   `-- VALIDATION_REPORT.md
|-- tests/
|   `-- test_legal_engine.py
|-- .streamlit/config.toml
|-- CONTRIBUTING.md
|-- CODE_OF_CONDUCT.md
|-- SECURITY.md
`-- LICENSE
```

## Run locally

Use Python 3.11 or 3.12 for a deployment environment that is easy to reproduce.

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run streamlit_app.py
```

macOS or Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository and upload the contents of this folder.
2. Confirm `streamlit_app.py` and `requirements.txt` are in the repository root.
3. Open Streamlit Community Cloud and create a new app.
4. Choose the repository and branch.
5. Set the entrypoint to `streamlit_app.py`.
6. In Advanced settings, choose a compatible Python version such as 3.12.
7. Deploy.

See `docs/DEPLOYMENT_GUIDE.md` for detailed instructions and troubleshooting.

## Colab notebook

Open `notebooks/Teen_Law_App_Colab_Prototype.ipynb` in Google Colab. It demonstrates the core topic router, safety guard, quiz engine, clustering, bounded reinforcement-learning recommender, moderation, and test cases without requiring a paid API.

## Safety and privacy boundaries

- No user login or persistent database is included.
- The app should not collect names, contact information, precise location, school identifiers, private messages, health information, or other sensitive information in this prototype.
- Emergency and exploitation patterns trigger a real-world-help message.
- Reinforcement learning can only change activity recommendations.
- Legal and safety content must be versioned and reviewed by qualified people before production use.

## Open-source license

The code is released under the MIT License. Educational content still needs jurisdiction-specific legal review before public reliance or commercialization.
