# RPG Battle Arena

A simple Streamlit-powered RPG battle simulator built in Python 3.

## Overview

This app runs a small turn-based battle between a party of heroes and a boss. It uses Streamlit for the UI and maintains game state in `st.session_state`.

## Requirements

- Python 3.10+ (Python 3 is fine)
- Streamlit

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

## Run locally

```bash
streamlit run app.py
```

Then open the URL shown in your terminal.

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Select your repository.
4. Set the app file path to `app.py`.
5. Deploy.

## Project files

- `app.py` — Streamlit app entrypoint
- `entities.py` — hero and boss classes
- `items.py` — item definitions
- `base.py` — shared game entity base classes
- `requirements.txt` — dependencies for Streamlit Cloud
- `.gitignore` — ignored local environment and build files

## Notes

- The app currently depends only on Streamlit.
- Local environment files like `.venv` and `bin/` are ignored by `.gitignore`.
