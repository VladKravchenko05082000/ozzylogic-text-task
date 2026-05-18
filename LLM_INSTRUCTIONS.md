Disclaimer: All tasks were solved using Claude Code, Claude.ai, and Grok.ai

A small note — not all tasks were described here. Some I simply forgot to add.

1.  Server
    Promts:
    Prepare me a list of necessary libraries for developing an application in pure Python according to the following requirements: (requirements from the technical specification)

    Generate code for launching the server, with the ability to shut it down via hotkeys, in pure Python without using frameworks

    Implement a helper for logging errors via logger. Write logs to the logs folder. The helper accepts the file name as input, and if no such file exists, it creates one and writes the necessary errors to it, or simply appends a new error to it

    Implement an SQL query for forming the database schema with a check for whether the table already exists in the database.
    Approximate requirements for the tables:
    Banks table — should contain the following fields (name, description, logo, website, phone number, email, legal address, rating)
    Table for coordinates of bank branch locations — address, coordinates, phone number, branch name
    Table for NBU currency rates — currency and its rate
    Table for currency rates of a specific bank — currency and bank name

    Create sync rates handlers that would fetch lists of currency rates from the minfin API() from the list of currencies located in currency (the min_fin_fetch_bank_rates function in http-clients\minfin) without writing to the database, only output to the console

    For sync_min_fin_bank_rates pass today's date as date; if rates is returned empty, make 1 more request, but with the date one day earlier, and so on up to 7 times maximum

    Write logic in native Python that would launch a thread which, after a certain time interval, would execute a passed callback.
    Accept the time interval in minutes. Accept the callback and time interval via arguments

    Generate retrieval of sync functions following the example from rates/controller but for banks — namely, using finance_ua_fetch_banks_list obtain data on all banks that are defined in general_constants as the SUPPORTED_BANKS config, and also for these banks using finance_ua_fetch_branches obtain data about the branches of these banks. Also, at this stage writing to the database is not required; take the implementation example from rates/controller, parsing the data according to the schema described in db_config SCHEMA, the banks and bank_branches tables

    Implement a database query that would return the following data from the banks table — name, logo, rating, phone number, email. This data needs to be returned for all banks

    Create a function get_bank_info that will accept a slug and return data about the bank corresponding to the passed slug; the required data is as follows — Retrieval of all information about a specific bank with current currency rates and the list of branches. You take the specific bank from the banks table, rates from the bank_rates table, branches from the bank_branches table.

    Generate a function based on the geopy library that would select a list of the nearest branches within a 10 km radius

    Implement a database query that would fetch the coordinates of all bank branches from the bank_branches table; also, immediately create a corresponding controller in bank controllers that will accept latitude and longitude coordinates from the params, and also add a check that they are required

    Implement a database query that would retrieve an up-to-date list of currency rates with the ability to filter the data by specific banks and currencies. You can take the currency data from the bank_rates table. Do it following the example as implemented in bank_models.py, the def get_bank_info function. This function is an example of what the implementation should look like

    Implement a database query for retrieving the current NBU currency rates

    Implement a database query for retrieving the average rate across all banks. You can take the data from the bank_rates table

    Add to the existing database schema another users table which will contain: email, password hash, subscription status for notifications about rate changes

    Add to the existing database schema another table for storing the refresh token

    Create in the user model functions for user registration, a function for finding a user by email to check whether a user is not already registered with such an email, a function for finding a user by their id, and a function that will update the following fields:
    email, password_hash, newsletter_enabled. For context of the user entity, here is the users table
    {id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    newsletter_enabled INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP}

    Generate helpers for me for decoding the authorization token and for obtaining pairs of refresh and authorization tokens

    Generate middleware for me for protecting non-public API endpoints using a bearer token

    Generate endpoints for token refresh and logout

    Generate endpoints for updating user data and for changing the password

    Implement a database query that would retrieve data on currency rates from the bank_rates table over a specified time period

    Tasks solved thanks to AI:
    Fixing bugs based on messages from tracing
    Server launch
    Logging
    Database schema initialization
    Retrieving data on currency rates
    Implementation of the event scheduler
    Creating a model for writing data about banks and branches
    Creating an endpoint for retrieving the nearest bank branches
    Creating functions for retrieving from the database the list of current currencies with filtering by specific banks and currencies
    Retrieving the average currency rate across all supported banks
    Creating user and refresh token tables
    Creating an endpoint for user registration
    Creating an endpoint for user login
    Creating middleware for protecting non-public endpoints using a bearer token
    Creating endpoints for token refresh and logout
    Creating endpoints for updating user data and for changing the password
    Creating an endpoint for retrieving currency rate history

    Parts of the code were refined manually:
    validate_type (Plays the role of logging in case of a programmer error or unexpected input data)
    get_file_logger (Centralized error logging into the corresponding files, an analog of any logging module on any hosting service)
    Any configs
    parse_rate_entry
    sync_nbu_rates
    Adding logic for converting the execution time for the scheduler according to the passed time type — for example, the time I pass can be hours, minutes, or seconds
    insert_min_fin_rate
    insert_nbu_rate
    get_full_bank_info
    get_nearest_branches_with_coords
    get_latest_currency_list (the part with validation of valid currency and banks in the query)
    session_tokens_models — overall, after generation I refined the appearance itself and the checks within the functions
    user_models — overall, after generation I refined the appearance itself and the checks within the functions
    jwt_helpers — logging and fixing function and property names
    Endpoint for retrieving currency rate history

    Solutions were modified after generation:
    If you request currency rate data from minfin at the beginning of the day, an empty date will be returned; it was decided to add handling for iterating through the intervals of the week for currency rates (the fetch_min_fin_rates_with_fallback function)
    Implementation of the event scheduler
    insert_min_fin_rate (changes related to compatibility with the schema)
    insert_nbu_rate (changes related to compatibility with the schema)
    parse_bank_entry — rating, as it turns out, can also be null, but this is, in my opinion, a bit strange, so the fallback lets us understand that we always want to see rating as a float.
    nearest_branches
    get_latest_rates
    get_nbu_latest (logic with concatenation for placeholder)

2.  Client
    Prompts:
    viewing the list of banks and detailed information about a bank
    viewing current currency rates
    filtering rates by banks and currencies
    viewing the NBU rate and the average rate across banks
    viewing statistics on rate changes over a selected period
    obtaining the nearest bank branches based on the user's geolocation
    Based on these requirements, generate a minimal boilerplate for the pages in views, and add them via lazy-loading in routes

    For branches, validation of the input fields will also need to be written for the inputs, similar to LoginForm. Use nearestBranchesSchema as the schema. Also add 1 more select with the maximum distance, with the following options — 1, 5, 10, 20, 50, 100

    I have some really very similar components with tables (example code of the tables)
    Make them into a reusable component that will accept a config for columns and rows.

    In onSubmit, in case of an error, call setError from useForm and pass this error in case it is present in (the element with the error)

    Implement refresh (via the refresh function in authApi) of the authorization token in axios on a 401 error

    Replace (some part of parent component layout ) to (name of child component) and updates import in child component and remove old imports in parent component

    Tasks solved thanks to AI:
    Creating the routing
    Debugging and typing of the component library
    Generation of markup according to the given styles (there were a lot of prompts along the lines of — here are the CSS styles and HTML code, generate me this markup in Tailwind, so I decided to consolidate that into 1 such section)
    Implementation of the configurable table component
    Token refresh in the axios interceptor
    Determining the user's geolocation
    Component decomposition

    Parts of the code were refined manually:
    Login logic
    Registration logic
    Logic for retrieving currency rate history, and its parsing on the frontend
    All stores were manually refined
    Component decomposition

    Solutions were modified after generation:
    Validation of the inputs on branches
    Logic for retrieving currency rate history, and its parsing on the frontend
    Overall all the pages, because initially I made them purely static
