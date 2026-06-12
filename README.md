# 🧘‍♀️ Summer Yoga & Fitness Tracker

A mobile-optimized, full-stack Python web application built to track a 70-day, 100+ class summer yoga challenge. This app integrates automated email parsing, native iOS calendar alarms, and a custom data-entry interface to log qualitative and quantitative fitness metrics.

## 🏗️ System Architecture

This project utilizes a decoupled architecture, using automation for data ingestion and a Python-based web app for data enhancement and tracking.

* **Frontend / UI:** [Streamlit](https://streamlit.io/) (Configured as an iOS Progressive Web App)
* **Database:** Google Sheets (via `st-gsheets-connection`)
* **Authentication:** Google Cloud Service Account (Google Drive & Sheets APIs)
* **Automation Middleware:** Zapier & Custom Python Regex
* **Hosting:** Streamlit Community Cloud

## ✨ Features

### 1. Automated Data Ingestion Pipeline
When a yoga class is booked via Mindbody, a Zapier automation catches the confirmation email and runs a custom Python Regular Expression script. This script extracts the `Class Name`, `Teacher`, `Date`, and `Time`. 
* **Smart Alarms:** Zapier automatically creates an Apple/Google Calendar event with a hard-coded 30-minute alert to trigger native iOS push notifications.
* **Database Seeding:** Zapier pushes the extracted class data into the Google Sheet, ready for the user to review post-class.

### 2. Post-Class Evaluation
* Dynamically pulls class data and allows the user to log 1-5 star ratings for: Overall Sentiment, Verbal Cues, Choreography, Music, and Friendliness.
* Captures qualitative data: Injuries, Target Postures, and Best/Worst parts of class (Data utilized later for Yoga Teacher Certification analysis via Seaborn).

### 3. Daily Metrics Tracker
* Logs daily weight (lbs), water intake (cups), and body measurements (Chest, Waist, Hips, Biceps, Thighs) directly to the database.

### 4. Weight Training & Plank Timer
* Features a custom asynchronous Python timer (`time.time()`) to track weightlifting session durations without blocking the Streamlit UI thread.
* Includes a high-visibility, looping visual countdown clock for plank holds.

## 🚀 Local Development Setup

To run this application locally, you must have an active Google Cloud Service Account with the Google Drive and Google Sheets APIs enabled.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/carolinefrance/Summer-Yoga-App.git](https://github.com/carolinefrance/Summer-Yoga-App.git)
   cd Summer-Yoga-App

2. **Create a virtual environment and install dependencies:**

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

3. **Configure Secrets:**

Create a .streamlit/secrets.toml file at the root of the project and add your Google Cloud JSON credentials. Ensure this file is added to your .gitignore.

4. **Run the application:**

streamlit run app.py
