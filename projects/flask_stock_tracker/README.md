# Stock Tracker

Hi. This is the repository for a project I completed with a great group of students at NYU. The project consisted of using Flask to create a Stock Tracking app.

---

**Project Title:** Stock Tracking App

**Project Description:** This project started out by creating a Python script (data.py) that would take in a specific stock ticker (e.g. 'AAPL'), collect the stock's history within a certain period of time using Python's yfinance library, and export a CSV file with the results. In addition to this, we used Oracle's database management system to create an empty table for the CSV data to be inserted after. After this, we created the main Flask app file (app.py) where we coded the Stock Tracker's interface. The app works as follows: the user has to run the data.py file while including the stock tickers it desires. As mentioned, this will export a CSV file for each stock ticker that is included. Once this step is finished, the user now runs app.py, clicks 'Choose file', and uploads the specific CSV file they want to analyze. The app then populates both the table in Oracle and the app's graph. The user can also insert, edit, and delete rows if they wish.

A major issue we had was that our initial intention was to simply include this function in the main file where the app resides (app.py). However, we used Python's cx_Oracle library to connect to Oracle, as well as Pandas in our data.py file. For some reason, due to our Macbooks' architecture, the app.py file would not work if we included Pandas in it. This is why we had to create a separate data.py file. This is obviously not ideal, but we found a workaround.