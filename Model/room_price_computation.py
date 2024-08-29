# function for room price computation (Option 1)
def room_price_computation():

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

    # Configure generative AI API key
    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

    # Load environment variables
    load_dotenv()

    # Database connection parameters
    username = 'root'
    password = 'iamukr77'
    host = 'localhost'
    port = '3306'  # Default MySQL port
    database = 'smartstay'  # Your schema name

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

    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Function to apply Early Bird Discount and Late Minute Price Surge
    def early_and_late(current_price, reservation):
        previous_price = current_price
    
        # Calculate days between reservation creation and check-in date
        days_in_advance = abs((reservation.check_in - reservation.created_at).days)
    
        # Apply Early Bird Discount
        if days_in_advance >= 90:
            discount = 0.10 + (days_in_advance - 90) / 10 * 0.05  # 10% - 15% discount
            current_price = int(current_price * (1 - min(discount, 0.15)))
    
        # Apply Late Minute Price Surge
        if days_in_advance < 3:
            surge = 0.10 + (3 - days_in_advance) / 3 * 0.10  # 10% - 20% increase
            current_price = int(current_price * (1 + min(surge, 0.20)))
    
        percentage_change = ((current_price - previous_price) / previous_price) * 100
        sign = "+" if percentage_change > 0 else ""
        print(f"Price after Smart Booking Optimization => {current_price} ({sign}{percentage_change:.2f}%)")
        return current_price, f"{sign}{percentage_change:.2f}%" if percentage_change != 0 else "No Change"

    # Function to calculate dynamic price based on room type, weekends, and summer season
    def calculate_dynamic_price(room, reservation):
        prices = []
        labels = []
        changes = []
    
        base_price = 5000  # Example base price
        prices.append(base_price)
        labels.append('Initial Price')
        changes.append('')
        print(f"Initial Price => {base_price}")

        # Adjust price based on room type
        previous_price = base_price
        if room.room_type == 'D':  # Deluxe room
            base_price += 1000
        elif room.room_type == 'N':  # Normal room
            base_price += 500
    
        percentage_change = ((base_price - previous_price) / previous_price) * 100
        prices.append(base_price)
        labels.append('Room Type Adjustment')
        changes.append(f"+{percentage_change:.2f}%" if percentage_change != 0 else "No Change")
        print(f"Price After Room Type Adjustment => {base_price} ({changes[-1]})")
    
        # Check if the check_in date was a weekend
        previous_price = base_price
        created_at_date = reservation.check_in
        is_weekend_flag = created_at_date.weekday() >= 5  # 5 represents Saturday, 6 represents Sunday

        if is_weekend_flag:
            base_price *= 1.05  # Increase price by 5% for rooms created on weekends

        percentage_change = ((base_price - previous_price) / previous_price) * 100
        prices.append(int(base_price))
        labels.append('Weekend Surge Charge')
        changes.append(f"+{percentage_change:.2f}%" if percentage_change != 0 else "No Change")
        print(f"Price After Weekend Surge Charge => {int(base_price)} ({changes[-1]})")
    
        # Check if the created_at date falls within the summer season (March and April)
        previous_price = base_price
        if created_at_date.month in [3, 4]:
            base_price *= 1.15  # Increase price by 15% for rooms booked during the summer season
    
        percentage_change = ((base_price - previous_price) / previous_price) * 100
        prices.append(int(base_price))
        labels.append('Summer Season Adjustment')
        changes.append(f"+{percentage_change:.2f}%" if percentage_change != 0 else "No Change")
        print(f"Price After Summer Season Adjustment => {int(base_price)} ({changes[-1]})")

        # Special high price periods with linear interpolation
        high_price_periods = [
        (datetime.datetime(2024, 1, 13), datetime.datetime(2024, 1, 15), 1.20, 1.30),  # Makar Sankranti (Long weekend)
        (datetime.datetime(2024, 3, 8), datetime.datetime(2024, 3, 8), 1.20, 1.30),  # Holi
        (datetime.datetime(2024, 4, 7), datetime.datetime(2024, 4, 10), 1.20, 1.30),  # Good Friday & Easter Weekend
        (datetime.datetime(2024, 10, 11), datetime.datetime(2024, 10, 15), 1.20, 1.30),  # Navratri and Dussehra
        (datetime.datetime(2024, 12, 23), datetime.datetime(2024, 12, 31), 1.20, 1.30),   # Christmas to New Year’s Eve
        ]

        # Apply high price adjustments based on special periods
        for start_date, end_date, min_multiplier, max_multiplier in high_price_periods:
            if start_date <= created_at_date <= end_date:
                # Calculate the fraction of the period that has passed
                total_period = (end_date - start_date).days
                days_passed = (created_at_date - start_date).days
                fraction_passed = days_passed / total_period
            
                # Linearly interpolate price based on the fraction of the period passed
                current_multiplier = min_multiplier + (max_multiplier - min_multiplier) * fraction_passed
                previous_price = base_price
                base_price *= current_multiplier
                percentage_change = ((base_price - previous_price) / previous_price) * 100
                prices.append(int(base_price))
                labels.append('Festive Period Amendments')
                changes.append(f"+{percentage_change:.2f}%" if percentage_change != 0 else "No Change")
                print(f"Price After Festive Period Amendments => {int(base_price)} ({changes[-1]})")
                break  # Exit loop after Festive Periiod adjustment
    
        return int(base_price), prices, labels, changes

    # Function to check if the room is booked
    def is_room_booked(room_no, session):
        reservation = session.query(Reservation).join(Room).filter(Room.room_no == room_no, Reservation.check_out == None).first()
        return reservation is not None

    # Function to apply dynamic price based on room availability
    def update_room_price(room_no, session, current_price):
        previous_price = current_price
        if is_room_booked(room_no, session):
            current_price *= 1.18  # Increase price by 18%
    
        percentage_change = ((current_price - previous_price) / previous_price) * 100
        print(f"Price After Room Availability Charge => {int(current_price)} ({f'+{percentage_change:.2f}%' if percentage_change != 0 else 'No Change'})")
        return int(current_price), f"+{percentage_change:.2f}%" if percentage_change != 0 else "No Change"

    # Function to apply loyalty discount
    def apply_loyalty_discount(current_price, guest, session):
        previous_price = current_price

        # Check if the guest's email_id is in the loyalty table
        loyalty_member = session.query(Loyalty).filter_by(email_id=guest.email_id).first()

        if loyalty_member:
            current_price = int(current_price * 0.8)  # Apply 20% discount

        percentage_change = ((current_price - previous_price) / previous_price) * 100
        print(f"Price After Loyalty Discount => {current_price} ({f'{percentage_change:.2f}%' if percentage_change != 0 else 'No Change'})")
        return current_price, f"{percentage_change:.2f}%" if percentage_change != 0 else "No Change"
 

    # Function to apply special offer period specific date
    def apply_special_offer(current_price, reservation):
        previous_price = current_price
        offer_start_date = datetime.datetime(2024, 4, 20)
        offer_end_date = datetime.datetime(2024, 4, 30)
    
        if offer_start_date <= reservation.check_in <= offer_end_date:
            current_price = int(current_price * 0.93)  # Apply 7% discount

    # Function to apply special offer period specific date
    def apply_special_offer(current_price, reservation):
        previous_price = current_price
        offer_start_date = datetime.datetime(2024, 4, 20)
        offer_end_date = datetime.datetime(2024, 4, 30)
        if offer_start_date <= reservation.check_in <= offer_end_date:
            current_price = int(current_price * 0.93)  # Apply 7% discount

        # Discount periods for holidays
        holiday_discounts = [
        (datetime.datetime(2024, 2, 1), datetime.datetime(2024, 2, 28), 0.85, 0.75),  # February discount range
        (datetime.datetime(2024, 7, 15), datetime.datetime(2024, 9, 7), 0.85, 0.75),  # Mid-July to Early September discount range
        (datetime.datetime(2024, 11, 1), datetime.datetime(2024, 11, 30), 0.85, 0.75),  # After Diwali discount range

        ]

        # Apply discounts based on holiday periods
        for start_date, end_date, min_discount, max_discount in holiday_discounts:
            if start_date <= reservation.check_in <= end_date:
                # Calculate the fraction of the period that has passed
                total_period = (end_date - start_date).days
                days_passed = (reservation.check_in - start_date).days
                fraction_passed = days_passed / total_period
            
                # Linearly interpolate discount based on the fraction of the period passed
                current_discount = min_discount + (max_discount - min_discount) * fraction_passed
                current_price = int(current_price * current_discount)
                break  # Exit loop after applying discount
    
        percentage_change = ((current_price - previous_price) / previous_price) * 100
        print(f"Price After Special Offer Period => {current_price} ({f'{percentage_change:.2f}%' if percentage_change != 0 else 'No Change'})")
        return current_price, f"{percentage_change:.2f}%" if percentage_change != 0 else "No Change"

    def apply_peak_load_pricing(current_price, total_rooms, vacant_rooms):
        previous_price = current_price

        # Calculate occupancy rate
        occupancy_rate = ((total_rooms - vacant_rooms) / total_rooms) * 100

        # Set thresholds and percentage adjustments
        low_occupancy_threshold = 25
        high_occupancy_threshold = 85  # or 90.0 based on your preference
        low_occupancy_decrease = 0.90    # Decrease by 10% if occupancy is below the low threshold
        high_occupancy_increase = 1.15   # Increase by 15% if occupancy is above the high threshold

        # Adjust prices based on occupancy rate
        if occupancy_rate <= low_occupancy_threshold:
            current_price = int(current_price * low_occupancy_decrease)
        elif occupancy_rate >= high_occupancy_threshold:
            current_price = int(current_price * high_occupancy_increase)

        percentage_change = ((current_price - previous_price) / previous_price) * 100
        sign = "+" if percentage_change > 0 else ""
        print(f"Price After Peak-Load Pricing => {current_price} ({f'{sign}{percentage_change:.2f}%' if percentage_change != 0 else 'No Change'})")
        return current_price, f"{sign}{percentage_change:.2f}%" if percentage_change != 0 else "No Change"

    # Function to fetch and display guest information along with reservation and room details
    def get_guest_info(guest_id, session, final_price, prices, labels, changes):
        guest = session.query(Guest).filter_by(id=guest_id).first()
        reservation = session.query(Reservation).filter_by(g_id=guest_id, check_out=None).first()
        room = session.query(Room).filter_by(id=reservation.r_id).first() if reservation else None
    
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
        if guest and reservation and room:
            # Create a PrettyTable instance
            table = PrettyTable()
            table.field_names = ["Field", "Data"]
            table.max_width["Field"] = 20
            table.max_width["Data"] = 50
            table.add_row(["Name", guest.name])
            table.add_row(["Address", guest.address])
            table.add_row(["Email", guest.email_id])
            table.add_row(["Phone", guest.phone])
            table.add_row(["Check-in Date", reservation.check_in.strftime('%Y-%m-%d %H:%M:%S')])
            table.add_row(["Room Number", room.room_no])
            table.add_row(["Room Type", room.room_type])
            table.add_row(["Room Price", final_price])
            table.add_row(["Booking Time", current_time])
        
            # Save PrettyTable data to PDF
            save_table_to_pdf(guest.id, session, final_price, prices, labels, changes)
        
            print("\nBooking Information:")
            print(table)
        else:
            print(f"No guest or reservation found with ID {guest_id}")

    # Function to display animated calculation steps
    def display_price_calculation_animation():
        messages = [
            "\033[1mVerifying base price...🔎\033[0m",
            "\033[1mAdjusting price based on room type...🏡\033[0m",
            "\033[1mChecking for weekend surge charge...🚀\033[0m",
            "\033[1mReviewing Seasonal & Festive adjustment...⛱️\033[0m",
            "\033[1mSmart Booking Optimization...🚨\033[0m",
            "\033[1mApplying loyalty discount...🎁\033[0m",
            "\033[1mCalculating special offer discount...🌟\033[0m",
            "\033[1mMonitoring Demand & Room Occupancy...📊\033[0m",
            "\033[1mDone!✅\033[0m",
            "\033[1mDisplaying Final Price with the Breakdown..💻\033[0m"
            ]
        for message in messages:
            clear_output(wait=True)
            print(message)
            time.sleep(1)  
        clear_output(wait=True)

    # Function to save PrettyTable data to PDF
    class PDF(FPDF):
        def header(self):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, '        Booking Information', 0, 1, 'C')

        def chapter_title(self, title):
            self.set_font('Arial', 'B', 12)
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(5)

        def chapter_body(self, body):
            self.set_font('Arial', '', 12)
            self.multi_cell(0, 10, body)
            self.ln()

        def add_table(self, table):
            self.set_font('Arial', 'B', 12)
            col_widths = [self.get_string_width(col) for col in table.field_names]
            col_widths = [max(w, 80) for w in col_widths]  # Minimum column width
            # Header
            for i, field in enumerate(table.field_names):
                self.cell(col_widths[i], 10, field, 1, 0, 'C')
            self.ln()

            # Data
            self.set_font('Arial', '', 12)
            for row in table.rows:
                for i, field in enumerate(row):
                    self.cell(col_widths[i], 10, str(field), 1, 0, 'C')
                self.ln()

        def add_narrow_table(self, table):
            self.set_font('Arial', 'B', 12)
            col_widths = [self.get_string_width(col) for col in table.field_names]
            col_widths = [max(w, 58) for w in col_widths]  # Minimum column width

            # Header
            for i, field in enumerate(table.field_names):
                self.cell(col_widths[i], 10, field, 1, 0, 'C')
            self.ln()

            # Data
            self.set_font('Arial', '', 12)
            for row in table.rows:
                for i, field in enumerate(row):
                    self.cell(col_widths[i], 10, str(field), 1, 0, 'C')
                self.ln()

        def add_page_title(self, title):
            self.add_page()
            self.set_font('Arial', 'B', 14)
            self.cell(0, 10, title, 0, 1, 'C')
            self.ln(10)

    def save_table_to_pdf(guest_id, session, final_price, prices, labels, changes):
        guest = session.query(Guest).filter_by(id=guest_id).first()
        reservation = session.query(Reservation).filter_by(g_id=guest_id, check_out=None).first()
        room = session.query(Room).filter_by(id=reservation.r_id).first() if reservation else None

        if guest and reservation and room:
            # Create a PrettyTable instance for the data
            table = PrettyTable()
            table.field_names = ["Field", "Data"]

            # Data to be added
            data = [
                ["Name", guest.name],
                ["Address", guest.address],
                ["Email", guest.email_id],
                ["Phone", guest.phone],
                ["Check-in Date", reservation.check_in.strftime('%Y-%m-%d %H:%M:%S')],
                ["Room Number", room.room_no],
                ["Room Type", "Delux" if room.room_type=='D' else 'Normal'],
                ["Room Price", final_price],
                ["Time Booked At", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
            ]

            # Add rows to the table
            for row in data:
                table.add_row(row)

            # Calculate max width based on content length
            table.max_width["Field"] = max(len(row[0]) for row in data) + 5  # +5 for padding
            table.max_width["Data"] = max(len(str(row[1])) for row in data) + 5  # +5 for padding

            # Create the PDF
            pdf = PDF()
            pdf.add_page()

            # Add header and introductory text
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="SmartStay", ln=True, align='C')
            pdf.set_font("Arial", 'I', 12)
            pdf.cell(200, 10, txt="Your Booking Confirmation!", ln=True, align='C')
            pdf.ln(10)

            # Add introduction
            pdf.set_font("Arial", '', 12)
            pdf.multi_cell(0, 10, 
                "Dear {name},\n\n"
                "Thank you for choosing our hotel for your stay. We are pleased to confirm your booking and "
                "hope you have a pleasant experience with us. Below are the details of your reservation.\n\n".format(name=guest.name)
            )
        
            # Add table with booking information
            pdf.add_table(table)

            # Adding Terms & Conditions, edit it if you find some interesting ones  
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(0, 10, 'Terms & Conditions:', 0, 1)
            pdf.set_font("Arial", '', 10)
            pdf.multi_cell(0, 10,
                "1. Prices are subject to change based on SmartStay's Policies.\n"
                "2. All guests are required to provide a valid ID proof at the time of check-in.\n"
                "3. Cancellations made within 24 hours of check-in will incur a 50% charge.\n"
                "4. Pets are not allowed in the hotel premises.\n"
                "5. The hotel is not responsible for the loss of any personal belongings.\n"
            )

            # Add the second page for the dynamic pricing breakdown
            pdf.add_page()
            pdf.chapter_title("Dynamic Pricing Breakdown")
            breakdown_table = PrettyTable()
            breakdown_table.field_names = ["Step", "Price After Step", "% Change"]

            for label, price, change in zip(labels, prices, changes):
                breakdown_table.add_row([label, price, change])
        
            pdf.add_narrow_table(breakdown_table)

            # Add footer
            pdf.ln(10)
            pdf.set_font("Arial", 'I', 10)
            pdf.multi_cell(0, 10,
                "For any inquiries or additional assistance, please contact us at smartstaytcet@gmail.com or call us at (123) 456-7890.\n"
                "We look forward to welcoming you to our hotel.\n\n"
                "Sincerely,\nSmartStay Team"
            )

            # Save the PDF
            pdf_file_name = f"Booking_Info_{guest_id}.pdf"
            pdf.output(pdf_file_name)

            print(f"PDF saved as {pdf_file_name}")
        
            # Send the PDF via email
            try:
                yag = yagmail.SMTP("smartstaytcet@gmail.com", "vmla cyse ruho svsc")
                subject = "Your Booking Information"
                body = "Dear Guest,\n\nPlease find attached your booking information.\n\nBest Regards,\nSmartStay Team"
                yag.send(to=guest.email_id, subject=subject, contents=body, attachments=pdf_file_name)
                print(f"\033[1mBooking info sucessfully mailed to {guest.email_id}!\033[0m")
            except Exception as e:
                print(f"Failed to send email: {e}")
        else:
            print("No guest or reservation found.")

    # Main function
    def update_room_price_main():
        try:
            # Create a session
            session = Session()
        
            # Take room number input from the user
            room_number_to_update = int(input("Enter the room number to update: "))
        
            # Fetch the room with the specific room_no
            room = session.query(Room).filter_by(room_no=room_number_to_update).first()
    
            if room:
                # Fetch the reservation associated with the room
                reservation = session.query(Reservation).filter_by(r_id=room.id, check_out=None).first()
    
                if reservation:
                    # Fetch the guest associated with the reservation
                    guest = session.query(Guest).filter_by(id=reservation.g_id).first()
                
                    # Display the price calculation animation
                    display_price_calculation_animation()

                    # Calculate the new dynamic price
                    new_price, prices, labels, changes = calculate_dynamic_price(room, reservation)

                    # Apply Early Bird Discount and Late Minute Price Surge
                    new_price, change = early_and_late(new_price, reservation)
                    prices.append(new_price)
                    labels.append('Smart Booking Optimization')
                    changes.append(change)

                    # Apply dynamic price based on room availability
                    new_price, change = update_room_price(room.room_no, session, new_price)
                    prices.append(new_price)
                    labels.append('Room Availability Charge')
                    changes.append(change)
    
                    # Apply loyalty discount if applicable
                    new_price, change = apply_loyalty_discount(new_price, guest, session)
                    prices.append(new_price)
                    labels.append('Loyalty Discount')
                    changes.append(change)
                
                    # Apply special offer period specific date
                    new_price, change = apply_special_offer(new_price, reservation)
                    prices.append(new_price)
                    labels.append('Special Offer Period')
                    changes.append(change)

                    # query to get total number of rooms
                    result = session.execute(text("SELECT COUNT(*) FROM rooms"))
                    total_rooms = result.scalar()

                    # query to get number of vacant rooms
                    query = """
                         SELECT COUNT(*) FROM rooms
                         WHERE id NOT IN (
                         SELECT DISTINCT r_id FROM reservations
                         WHERE check_out IS NULL
                          )
                        """
                    result = session.execute(text(query))
                    vacant_rooms = result.scalar()


                    # Apply peak-load pricing
                    new_price, change = apply_peak_load_pricing(new_price, total_rooms, vacant_rooms)
                    prices.append(new_price)
                    labels.append('Peak-Load Pricing')
                    changes.append(change)

                    # Update the price in the database
                    room.price = new_price
                    session.commit()  # Commit the changes
                
                    # Save guest information to PDF
                    get_guest_info(guest.id, session, new_price, prices, labels, changes)
                
                    # Print the final price update message in bold
                    print(f"\033[1mFinal price updated successfully for room {room_number_to_update} to {new_price}✔️\033[0m")
                
                    # To verify the update, fetch the data again and display the updated DataFrame
                    query = f"SELECT * FROM rooms WHERE room_no = {room_number_to_update}"
                    data = pd.read_sql(query, engine)
                    display(data)
            
    
                    # Plot the price changes
                    plt.figure(figsize=(10, 6))
                    plt.plot(labels, prices, marker='o', linestyle='-', color='b')
                    for i, (label, price, change) in enumerate(zip(labels, prices, changes)):
                        plt.text(i, price, f'{change}', ha='right')
                    plt.xlabel('Adjustment Steps')
                    plt.ylabel('Price')
                    plt.title('Price Adjustments After Each Step')
                    plt.xticks(rotation=45)
                    plt.grid(True)
                    plt.show()

                else:
                    print(f"No active reservation found for room number {room_number_to_update}.")
    
            else:
                print(f"No room found with number {room_number_to_update}.")
    
        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            # Close the session
            session.close()

    # Execute the main function
    update_room_price_main()