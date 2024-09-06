#Our code for Option 2 : Receipt Generation

#Receipt Generation for Checked-out guests

from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, func, extract, text 
from sqlalchemy.orm import declarative_base, sessionmaker, relationship 
import datetime
import time
import pandas as pd
import plotly.graph_objs as go 
import plotly.express as px
from fpdf import FPDF 
import plotly.io as pio 
import matplotlib.pyplot as plt 
import os
import random
import numpy as np 
import PIL 
from PIL import Image 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.chrome.options import Options 
from webdriver_manager.chrome import ChromeDriverManager 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import yagmail  
import requests 
import csv
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from geopy.geocoders import Nominatim  # To convert city names to coordinates
from prettytable import PrettyTable 
from io import StringIO
from IPython.display import display, clear_output 
from dotenv import load_dotenv 
import google.generativeai as genai
import db_config
from preprocess_clv_data import process_clv_data


# Configure generative AI API key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Load environment variables
load_dotenv()

# Database connection parameters from db_config
username = db_config.username
password = db_config.password
host = db_config.host
port = db_config.port
database = db_config.database

# Create an engine instance with provided credentials
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

# Define the ORM base class
Base = declarative_base()

# Define the ORM mapping for the rooms table
class Room(Base):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    room_no = Column(Integer, unique=True)
    price = Column(Integer)
    room_type = Column(String(2))
    currently_booked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    reservations = relationship("Reservation", back_populates="room")

# Define the ORM mapping for the reservations table
class Reservation(Base):
    __tablename__ = 'reservations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    g_id = Column(Integer, ForeignKey('guests.id'))
    r_date = Column(DateTime)
    check_in = Column(DateTime)
    check_out = Column(DateTime)
    meal = Column(Boolean)
    r_id = Column(Integer, ForeignKey('rooms.id'))
    r_type = Column(String(2))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    guest = relationship("Guest", back_populates="reservations")
    room = relationship("Room", back_populates="reservations")

# Define the ORM mapping for the guests table
class Guest(Base):
    __tablename__ = 'guests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    address = Column(String(50))
    email_id = Column(String(50))
    phone = Column(Integer)
    city = Column(String(20))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    reservations = relationship("Reservation", back_populates="guest")

# Define the ORM mapping for the loyalty table
class Loyalty(Base):
    __tablename__ = 'loyalty'
    id = Column(Integer, primary_key=True, autoincrement=True)
    guest_id = Column(Integer, ForeignKey('guests.id'))
    email_id = Column(String(50), default=None)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


# Define the ORM mapping for the CLV table
class CLV(Base):
    __tablename__ = 'CLV'
    id = Column(Integer, primary_key=True, autoincrement=True)
    guest_id = Column(Integer)
    guest_name = Column(String(30))          
    email_id = Column(String(50))            
    check_in_date = Column(DateTime)
    check_out_date = Column(DateTime)
    room_number = Column(Integer)
    room_type = Column(String(2))            
    room_price_per_day = Column(Integer)     
    duration_of_stay = Column(Integer)
    meal_charges = Column(Integer, default=0)  
    discount = Column(Integer, default=0)      
    gst = Column(Integer)                    
    grand_total_amount = Column(Integer)     
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))


Session = sessionmaker(bind=engine)
session = Session()

# Function to calculate the duration of stay in days
def calculate_duration_of_stay(check_in, check_out):
    return (check_out - check_in).days

# Function to calculate the final price based on room price and duration of stay
def calculate_final_price(room_price, duration):
    return room_price * duration

def fetch_reservation_and_calculate(room_no, session):
    reservation = session.query(Reservation).join(Room).filter(Room.room_no == room_no, Reservation.check_out != None).order_by(Reservation.check_out.desc()).first()
    if not reservation:
        print("Kindly ensure check-out is done for Receipt Generation.")
        return

    duration = calculate_duration_of_stay(reservation.check_in, reservation.check_out)
    base_amount = calculate_final_price(reservation.room.price, duration)

    # Meal charges calculation
    meal_charge = 0
    if reservation.meal:
        meal_charge = base_amount * 0.11

    # Discount for long stays
    discount = 0
    if duration > 7:
        discount = base_amount * 0.09

    # Final amount calculation
    final_amount = base_amount + meal_charge - discount

    # Apply GST
    gst = final_amount * 0.05
    total_amount_with_gst = final_amount + gst

    # Rounding the amounts
    final_amount = round(final_amount, 2)
    meal_charge = round(meal_charge, 2)
    discount = round(discount, 2)
    gst = round(gst, 2)
    total_amount_with_gst = round(total_amount_with_gst, 2)

    # Displaying details in a tabular format using PrettyTable
    table = PrettyTable()
    table.field_names = ["Field", "Data"]
    table.add_row(["Guest ID", reservation.g_id])
    table.add_row(["Guest Name", reservation.guest.name])
    table.add_row(["Email ID", reservation.guest.email_id])
    table.add_row(["Check-in Date", reservation.check_in.strftime('%Y-%m-%d %H:%M:%S')])
    table.add_row(["Check-out Date", reservation.check_out.strftime('%Y-%m-%d %H:%M:%S')])
    table.add_row(["Room Number", reservation.room.room_no])
    table.add_row(["Room Type", "Deluxe" if reservation.room.room_type=='D' else "Normal"])
    table.add_row(["Room Price per Day", f'₹{reservation.room.price}'])
    table.add_row(["Duration of Stay (Days)", duration])
    table.add_row(["Meal Included", "Yes" if reservation.meal else "No"])
    table.add_row(["Meal Charges", "Not Applicable" if meal_charge == 0 else f'{meal_charge}'])
    table.add_row(["Discount", "Not Applicable" if discount == 0 else f'₹{discount}'])
    table.add_row(["GST (5%)", f'₹{gst}'])
    table.add_row(["Grand Total Amount", f'₹{total_amount_with_gst}'])
    table.add_row(["Time Generated At", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

    print("\nReservation Details:")
    print(table)

    # Directory for saving CSV files
    csv_folder = 'csv_files'

    # Create the directory if it doesn't exist
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder)

    # Define the path for the CSV file
    csv_filename = os.path.join(csv_folder, 'final-rectfied-clv-data.csv')
    # Adding above data to CLV Table
    clv = CLV(
    guest_id=reservation.g_id,
    guest_name=reservation.guest.name,
    email_id=reservation.guest.email_id,
    check_in_date=reservation.check_in,
    check_out_date=reservation.check_out,
    room_number=reservation.room.room_no,
    room_type=reservation.room.room_type,
    room_price_per_day=reservation.room.price,
    duration_of_stay=duration,
    meal_charges=meal_charge,
    discount=discount,
    gst=gst,
    grand_total_amount=total_amount_with_gst
    )
    
    session.add(clv)
    session.commit()

    # Define the starting ID
    starting_id = 109

   # Check if the file exists and get the next ID
    file_exists = os.path.isfile(csv_filename)

    if file_exists:
        # Read the existing CSV file
        with open(csv_filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            existing_ids = [int(row['id']) for row in reader if row['id'].isdigit()]
            # Find the highest ID from the existing file
            last_id = max(existing_ids, default=starting_id - 1)
    else:
        # If the file doesn't exist, start from the initial ID
        last_id = starting_id - 1

    # Determine the new ID
    new_id = last_id + 1

    # Convert the latest CLV record to a dictionary with the new ID
    latest_clv_data = {
    'id': new_id,
    'guest_id': clv.guest_id,
    'guest_name': clv.guest_name,
    'email_id': clv.email_id,
    'check_in_date': clv.check_in_date,
    'check_out_date': clv.check_out_date,
    'room_number': clv.room_number,
    'room_type': clv.room_type,
    'room_price_per_day': clv.room_price_per_day,
    'duration_of_stay': clv.duration_of_stay,
    'meal_charges': clv.meal_charges,
    'discount': clv.discount,
    'gst': clv.gst,
    'grand_total_amount': clv.grand_total_amount,
    'created_at': clv.created_at
}

    # Append the latest record to the CSV file
    with open(csv_filename, 'a', newline='') as csvfile:
        fieldnames = latest_clv_data.keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # If the file doesn't exist, write the header first
        if not file_exists:
            writer.writeheader()

        # Write the latest record
        writer.writerow(latest_clv_data)

    print(f"New CLV record appended to {csv_filename} with ID {new_id}")

    process_clv_data()    # Call the function bro

    # Directory for saving receipts
    receipts_folder = 'receipts'

    # Create the directory if it doesn't exist
    if not os.path.exists(receipts_folder):
        os.makedirs(receipts_folder)

    # Generate PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Generate a random receipt ID and transaction number
    receipt_id = f"R{random.randint(1000, 9999)}"
    transaction_number = f"T{random.randint(100000, 999999)}"
    payment_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="SmartStay", ln=True, align='C')
    pdf.cell(200, 10, txt="Booking Receipt", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Receipt ID: {receipt_id}", ln=True, align='C')
    pdf.ln(2)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Dear {reservation.guest.name},", ln=True)
    pdf.ln(2)

    pdf.multi_cell(0, 10, txt="Thank you for choosing SmartStay for your accommodation needs.")
    
    # Add booking information table
    pdf.set_font("Arial", size=10)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 10, txt="Below is your Booking Receipt:", ln=True, align='L', fill=True)
    pdf.ln(1)

    # Add details as cells
    pdf.set_font("Arial", size=12)
    pdf.cell(50, 10, txt="Guest ID", border=1)
    pdf.cell(0, 10, txt=str(reservation.g_id), border=1, ln=True)
    pdf.cell(50, 10, txt="Guest Name", border=1)
    pdf.cell(0, 10, txt=reservation.guest.name, border=1, ln=True)
    pdf.cell(50, 10, txt="Email ID", border=1)
    pdf.cell(0, 10, txt=reservation.guest.email_id, border=1, ln=True)
    pdf.cell(50, 10, txt="Check-in Date", border=1)
    pdf.cell(0, 10, txt=reservation.check_in.strftime('%Y-%m-%d %H:%M:%S'), border=1, ln=True)
    pdf.cell(50, 10, txt="Check-out Date", border=1)
    pdf.cell(0, 10, txt=reservation.check_out.strftime('%Y-%m-%d %H:%M:%S'), border=1, ln=True)
    pdf.cell(50, 10, txt="Room Number", border=1)
    pdf.cell(0, 10, txt=str(reservation.room.room_no), border=1, ln=True)
    pdf.cell(50, 10, txt="Room Type", border=1)
    pdf.cell(0, 10, txt="Deluxe" if reservation.room.room_type=='D' else "Normal", border=1, ln=True)
    pdf.cell(50, 10, txt="Room Price per Day", border=1)
    pdf.cell(0, 10, txt="Rs." + str(reservation.room.price), border=1, ln=True)
    pdf.cell(50, 10, txt="Duration of Stay (Days)", border=1)
    pdf.cell(0, 10, txt=str(duration), border=1, ln=True)
    pdf.cell(50, 10, txt="Meal Charges", border=1)
    pdf.cell(0, 10, txt="Not Applicable" if meal_charge == 0 else f"Rs.{meal_charge}", border=1, ln=True)
    pdf.cell(50, 10, txt="Discount", border=1)
    pdf.cell(0, 10, txt="Not Applicable" if discount == 0 else f"Rs.{discount}", border=1, ln=True)
    pdf.cell(50, 10, txt="GST (5%)", border=1)
    pdf.cell(0, 10, txt=f"Rs.{gst}", border=1, ln=True)
    pdf.cell(50, 10, txt="Grand Total Amount", border=1)
    pdf.cell(0, 10, txt=f"Rs.{total_amount_with_gst}", border=1, ln=True)

    pdf.ln(1)

    pdf.set_font("Arial", size=10)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 10, txt="Payment Details:", ln=True, align='L', fill=True)

    pdf.ln(1)
    
    pdf.cell(50, 10, txt="Transaction Number", border=1)
    pdf.cell(0, 10, txt=transaction_number, border=1, ln=True)
    pdf.cell(50, 10, txt="Payment Date", border=1)
    pdf.cell(0, 10, txt=payment_date, border=1, ln=True)
    pdf.cell(50, 10, txt="Payment Mode", border=1)
    pdf.cell(0, 10, txt="Cash/Card/UPI", border=1, ln=True)
    
    pdf.ln(2)
    
    pdf.set_font("Arial",'B', 10)
    pdf.cell(0, 10, txt="We hope you had a pleasant stay! Looking forward to welcoming you back. Safe Travels!", ln=True)
    #pdf.set_font("Arial", 'B', 10)
    #pdf.cell(0, 10, txt="Safe travels!")
    #pdf.set_font("Arial", 'I', 10)
    pdf.set_font("Arial",'I', 10)
    pdf.cell(200, 10, txt=f"Time Generated At: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)

    # Define the path with the folder and filename
    filename = os.path.join(receipts_folder, f"Booking_Receipt_{reservation.guest.id}.pdf")
    pdf.output(filename)
    
    print(f"PDF receipt saved as {filename}")
    
    # Send the PDF via email
    try:
        yag = yagmail.SMTP(db_config.email, db_config.passw) 
        subject = "Your Booking Receipt - SmartStay"
        body = "Dear Guest,\n\nPlease find attached your booking receipt.\n\nBest Regards,\nSmartStay Team"
        yag.send(to=reservation.guest.email_id, subject=subject, contents=body, attachments=filename)
        print(f"\033[1mBooking Receipt successfully mailed to {reservation.guest.email_id}!\033[0m")
    except Exception as e:
        print(f"Failed to send email: {e}")