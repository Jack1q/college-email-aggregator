# college-email-aggregator
Stores every college email you've ever received in a csv spreadsheet

### How to Use
1) Clone this repository
2) Setup Gmail API: https://developers.google.com/gmail/api/quickstart/python?authuser=1
- Follow steps 1 and 2 in the quickstart.
- Make sure you remember to place credentials.json into the directory you cloned.
2) Open up your command line and cd into this directory. 
3) Run this command to get all emails:
```
python collegeemails.py
```
Run this command to only get emails containing fee-waivers:
```
python collegeemails.py waiver-only
```

The emails will be stored in data.csv. It might take a little bit for everything to get collected if you have a lot of them.
