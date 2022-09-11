# How to use the Google Sheets API
Here's a quick guide for getting the Google Sheets API set up!
What you'll need:
- Credentials in the same folder as the code you're running, it should be named credentials.json (if you're using Anna's, they're posted in Discord)
- A Google account that's a test user on a Google Cloud project with the Google Sheets API enabled (if you're using Anna's, make sure they've added your email)
- Python 2.6+ and pip
Install the Google client library
- In your terminal/command line, run the following command:
```
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
Using the API
- sheetsAPIfuncs.py has some functions for interfacing with the API built in to make your life easier, just put import sheetsAPIfuncs at the top of your code
- The first time you use the API, you'll get a pop up window to login to your Google account and authenticate the API - you should only need to do this once! This will create a file called token.json, if it is deleted you will need to log in again. DO NOT commit token.json to the github - it's in the gitignore but just be careful!

You should be ready to use the API! You can get some sample code and a guide to get started [here](https://developers.google.com/sheets/api/quickstart/python). Contact Anna if you have any questions!

