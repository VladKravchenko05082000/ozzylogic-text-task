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
npm install -D @tailwindcss/vite tailwindcss tw-animate-css
npm run dev
```

# IMPORTANT

There is some intentional type duplication between `api` and `store`. For some reason, Vite throws an error saying it can't see the file when the types are shared, so the duplication is a conscious workaround.

# Potential Improvements

Pagination for large volumes of data
Add theme switcher
