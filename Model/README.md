# Follow these steps to run the Model code successfully:
 
Modularized Final Model: [Model/final-model.ipynb](https://github.com/im-ukr/SmartStay/blob/test/Model/final-model.ipynb)

To run this code you'd need these 6 things set:

1. Environment Variables File (.env):
This file should contain your Google API key. This is used to generate description for the plots in the Analytics Report. Generate your api key from https://aistudio.google.com/app/apikey
Content of .env file:
```sh
GOOGLE_API_KEY="your_google_api_key_here"
```
2. Database and Email credentials(db_config.py) with the following content:
```sh
# db_config.py
username = 'your-username'
password = 'your-password'
host = 'localhost'
port = '3306'
database = 'smartstay'

# mail credentials
email="email-id"
passw="password"
```

3. Email.csv file containing the email list you'd like to mail the final report to.

4. The database set up as mentioned in [sql/smartstay.sql](https://github.com/im-ukr/SmartStay/blob/test/sql/smartstay.sql)

5. Any other file present in this directory.

6. You should have all the requirements installed as mentioned in [notebooks/Dynamic Pricing Model/Final-model.ipynb](https://github.com/im-ukr/SmartStay/blob/test/notebooks/Dynamic%20Pricing%20Model/Final-model.ipynb). **This directory contains the modularized final model of the same file.**
