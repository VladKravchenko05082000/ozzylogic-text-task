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

# Potential Improvements

Pagination for large volumes of data
Add theme switcher

# Tasks that were completed —

Server:

Use the MinFin API to fetch up-to-date currency exchange rates
Use the NBU API to fetch up-to-date currency exchange rates
Set up regular automatic updates of exchange rates
Set up regular automatic updates of bank branch data
Retrieve a list of banks along with information about them (name, logo, rating, phone number, email)
Retrieve all information about a specific bank, including current exchange rates and a list of branches
Retrieve the nearest bank branches based on the user's location
Retrieve a list of currencies
Retrieve the current list of exchange rates with the ability to filter data by specific banks and currencies
Retrieve the current NBU exchange rate and the average rate across all banks
User registration and authentication
Ability to edit account data

Client:

Viewing the list of banks and detailed information about a bank
Viewing current exchange rates
Filtering rates by banks and currencies
Viewing the NBU rate and the average rate across banks
Viewing statistics of rate changes over a selected period
Retrieving the nearest bank branches based on the user's geolocation
Optional: user registration, authorization, and profile management
Responsive interface (desktop + mobile)

UI/UX:

Ease of use
Clarity of interaction
Adherence to commonly accepted UI/UX patterns

# Tasks that were not completed —

Server:

Currency exchange rate change history

Implement a mechanism for collecting history of significant changes in exchange rates (for example, 5%)
Add the ability to retrieve the history of significant changes over a defined period

Notifications

Implement a notification mechanism to email the user about important changes in exchange rates, with the additional option to subscribe to specific currencies or banks
Allow the user to enable/disable notifications about significant changes in exchange rates

Statistics

Provide the user with statistics on exchange rate changes over a defined period, with the ability to filter data by specific banks and currencies

Client:

Preferably implement statistics visualization (chart)
Preferably use a map to display branches
Optional: ability to configure subscriptions to notifications about rate changes
