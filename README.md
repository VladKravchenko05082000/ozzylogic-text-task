Server:

## Setup

```bash
cd server
python -m venv venv
If Windows - venv\Scripts\activate, if Linux or MacOS - source venv/bin/activate
pip install -r requirements.txt
python -m main
```

# IMPORTANT

I intentionally did not add the .env file to .gitignore for the convenience of reviewing the assignment.

# Potential Improvements

Add a request limiter for a certain time period
Pagination for large volumes of data

Client:

## Setup

```bash
cd client
npm i
npm run dev
```

# Potential Improvements

Pagination for large volumes of data
Add theme switcher
