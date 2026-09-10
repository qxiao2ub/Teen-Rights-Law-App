# Legal Counsel — Teen Legal Learning App

**Legal Counsel** is an open-source, teen-friendly legal education prototype built in Python and Streamlit. The interface in this repository is a Streamlit-native migration of the supplied Legal Counsel UI design, preserving its soft teal/coral visual system, **Nova** assistant, Voicebox, Chatbox, Minigames, and Progress Gavel concepts while connecting them to the existing Python legal-learning and safety engine.

> **Educational use only.** This app provides general legal information and learning support, not legal advice. Laws vary by jurisdiction, age, setting, and facts. Serious or real-world cases should be handled with a qualified local attorney, legal-aid organization, trusted adult, or emergency service as appropriate.

## Credits

- **Author:** Arya Patel
- **Mentor:** Dr. Qingyang Xiao

The author's first name is used only in the required project credit. It is not the app name, assistant name, or product branding.

## Streamlit Community Cloud

The repository is ready for Streamlit Community Cloud with the entrypoint in the repository root:

```text
streamlit_app.py
```

Deployment steps:

1. Upload the contents of this repository to GitHub.
2. In Streamlit Community Cloud, create a new app from that GitHub repository.
3. Choose the desired branch (usually `main`).
4. Set **Main file path** to `streamlit_app.py`.
5. Deploy. No API key is required for the included local legal-learning prototype.

## Local launch

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Main features

- Home experience modeled on the supplied UI design
- **Nova Voicebox**: browser audio capture, transcript confirmation, and browser text-to-speech answer playback
- **Nova Chatbox**: plain-language questions routed through a local TF-IDF topic engine
- Safety screening for urgent or unsafe requests
- Legal topic learning cards
- Scenario-based minigames and quizzes
- Progress Gavel, session XP, and topic activity
- K-means learning-preference demonstration using non-sensitive features
- Bounded reinforcement-learning activity recommender
- Session-only moderated teen community prototype
- Optional state/country context with clear jurisdiction warnings
- Exportable session progress

## Repository structure

```text
.
├── streamlit_app.py              # Streamlit Cloud entrypoint + migrated UI
├── requirements.txt              # Runtime dependencies
├── requirements-dev.txt          # Development/test dependencies
├── src/
│   └── legal_engine.py           # NLP router, safety guard, moderation, ML/RL demos
├── data/
│   └── legal_topics.json         # Reviewed educational topic/quiz content
├── notebooks/
│   └── Teen_Law_App_Colab_Prototype.ipynb
├── tests/
│   └── test_legal_engine.py
├── docs/
├── .streamlit/config.toml
├── .github/workflows/tests.yml
├── LICENSE
├── SECURITY.md
└── CODE_OF_CONDUCT.md
```

## Voice design note

The app intentionally avoids requiring a paid speech API. Streamlit's browser audio capture can collect a voice question, while the user confirms/types the transcript before it is processed by the local engine. Nova's answer can then be read aloud through the browser's speech-synthesis capability. A production iOS/web release can add an on-device or privacy-reviewed speech-to-text model.

## Privacy and teen-safety design

- No login is required in the prototype.
- Learning history is kept in Streamlit session state and is not designed as a persistent teen profile.
- Community posts are screened for common PII and high-risk content before being added to the session.
- K-means clustering uses learning-preference scores, not sensitive demographic attributes.
- Reinforcement learning is limited to selecting learning activities; it cannot alter legal/safety content.

See `SECURITY.md`, `CODE_OF_CONDUCT.md`, and `docs/CONTENT_REVIEW_CHECKLIST.md` before extending the app.
