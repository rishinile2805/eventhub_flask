# EventHub — College Event Management Portal

> **Note:** This is a very simple web application created for academic coursework to demonstrate full-stack development using Python, Flask, SQLite, and HTML/CSS.

## Overview

**EventHub** is a lightweight web portal designed to streamline college event organization. It allows students to browse upcoming events and register online, while providing administrators with a password-protected dashboard to host events, view registered participants, and export attendance lists as CSV files.

## Features

* **Public Event Feed:** Displays all upcoming college events sorted by date, including venue details and live registration counts.
* **Student Registration:** Simple inline registration form for students to sign up using their name and college email.
* **Admin Authentication:** Session-based login system protecting administrative actions.
* **Event Management:** Admins can create new events and delete existing ones along with their associated registrations.
* **Participant Tracking & CSV Export:** Admins can view the list of registered students for any event and download the data as a `.csv` file generated on the fly in memory.

## Tech Stack

* **Backend:** Python 3, Flask
* **Database:** SQLite3 (serverless, file-based storage)
* **Frontend:** HTML5, CSS3, Jinja2 Templating

## Project Structure

```text
eventhub_flask/
├── app.py                  # Main Flask application, routes, and SQLite logic
├── requirements.txt        # Python dependencies
├── eventhub.db             # Auto-generated SQLite database file
└── templates/
    ├── base.html           # Base layout and styling (Jinja parent template)
    ├── index.html          # Home page displaying events and registration forms
    ├── create.html         # Admin form to publish new events
    ├── login.html          # Admin login page
    └── participants.html   # Admin view of registered students with CSV export
```

## Setup & Installation

1. **Navigate to the project folder:**
   ```bash
   cd eventhub_flask
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the portal:**
   Open your browser and go to `http://127.0.0.1:5000`

## Default Admin Credentials

* **Admin Password:** `admin123` *(can be changed via the `ADMIN_PASSWORD` variable in `app.py`)*
