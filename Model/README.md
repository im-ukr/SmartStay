This file is divided in two parts:<br>
A. Instructions to set up the Model.<br>
B. Documentation

# A. Steps to set up the Model to run it successfully:
 
Modularized Final Model: [Model/final-model.ipynb](https://github.com/im-ukr/SmartStay/blob/test/Model/final-model.ipynb)

To run this code you'd need these 6 things set:

1. Environment Variables File (.env):
This file should contain your Google API key. This is used to generate description for the plots in the Analytics Report. Generate your api key from https://aistudio.google.com/app/apikey
The content of .env file that should be created by you within this directory is provided below:
```sh
GOOGLE_API_KEY="your_google_api_key_here"
```
2. Create a Database and Email credentials(db_config.py) file in this directory with the following content:
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

# B. (Documentation) Section 1 - Pricing Adjustments Overview

Room price is computed for new bookings in [Option 1](https://github.com/im-ukr/SmartStay/blob/test/Model/room_price_computation.py) based the following parameters:

## 1. Room Type Adjustment
**Description:** The base pricing structure varies by room type, which is classified as either 'Deluxe' or 'Normal'.  
**Adjustment:** 
- For `room_type == 'D'`, the price is increased by 20%. 
- For `room_type == 'N'`, the price is increased by 10%.

## 2. Weekend Surge Charge
**Description:** Prices are subject to an increase if the reservation check-in falls on a weekend (Saturday or Sunday).  
**Adjustment:** The price is increased by 5% if the check-in date is on a weekend.

## 3. Summer Season Adjustment
**Description:** Increased demand during the summer season (March and April) results in higher prices.  
**Adjustment:** The price is increased by 15% if the check-in date falls within March or April.

## 4. Festive Period Amendments
**Description:** Prices are adjusted during high-demand periods such as festivals and holidays.  
**Adjustment:** A linear interpolation method is employed to adjust prices within a specified range (e.g., 20% to 30% increase) based on the proximity of the booking to the start or end of the festive period.

## 5. Early Bird Discount(Smart Booking Optimization)
**Description:** Discounts are available for bookings made well in advance.  
**Adjustment:** A 10% to 15% discount is applied if the reservation is made at least 90 days prior to the check-in date.

## 6. Late Minute Price Surge(Smart Booking Optimization)
**Description:** Prices are increased for last-minute bookings.  
**Adjustment:** A 10% to 20% price increase is applied if the reservation is made less than 3 days before the check-in date.

## 7. CLV-oriented Discount
**Description:** Guests enrolled in a loyalty program receive discounts.  
**Adjustment:** A 20% discount is applied if the guest is a loyalty program member.

## 8. Special Offer Period
**Description:** Discounts are available during specific promotional periods.  
**Adjustment:** A 7% discount is applied if the reservation falls within a designated special offer period.

## 9. Holiday Discounts
**Description:** Additional discounts are offered during specific holiday periods.  
**Adjustment:** The price is reduced by 15% to 25%, depending on the proximity of the booking to the start or end of the holiday period.

## 10. Peak-Load Pricing
**Description:** Prices are adjusted based on the hotel's overall occupancy rate.  
**Adjustment:** 
- If occupancy is below 25%, prices decrease by 10%.
- If occupancy is above 85%, prices increase by 15%.

![parameters.png](https://github.com/im-ukr/SmartStay/blob/test/Model/assets/parameters.png)

# Section 2 - Final Receipt Generation 

Final Receipt is generated in [Option 2](https://github.com/im-ukr/SmartStay/blob/test/Model/fetch_reservation_and_calculate.py) depending on the duration of stay once the guest checks-out.

![Final Receipt.jpg](https://github.com/im-ukr/SmartStay/blob/test/Model/assets/Booking_Receipt_2_page-0001.jpg)

# Section 3 - View Analytics

You can view SmartStay Analytics in [Option 3](https://github.com/im-ukr/SmartStay/blob/test/Model/view_analytics.py) for the following currently:

- Room Vacancy Status
- Current Bookings by Room Type
- Booking Trends by Day of Week
- Reservation Trends
- Average Stay Duration by Room Type
- Room Price Distribution
- Average Revenue by Room Type
- Guest Origin by City
- Violin Plot for Price Distribution by Room Type
- Room Utilization Treemap
- Revenue by Quarter

# Section 4 - Export Full Report to PDF and receive via mail

Export Full Analytics Report to PDF in [Option 4](https://github.com/im-ukr/SmartStay/blob/test/Model/report_export.py) and get the same mailed to the registered admin email id(s) in [email.csv](https://github.com/im-ukr/SmartStay/blob/test/Model/email.csv)

![Analytics-Report-1.jpg](https://github.com/im-ukr/SmartStay/blob/test/Model/assets/SmartStay-Analytics-Report_page1.jpg)
## Example content:
![Analytics-Report.jpg](https://github.com/im-ukr/SmartStay/blob/test/Model/assets/SmartStay-Analytics-Report%20(1).jpg)


