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
    from geopy.geocoders import Nominatim 
    from prettytable import PrettyTable 
    from io import StringIO
    from IPython.display import display, clear_output 
    from dotenv import load_dotenv 
    import google.generativeai as genai
    import db_config

    genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

    load_dotenv()

    username = db_config.username
    password = db_config.password
    host = db_config.host
    port = db_config.port
    database = db_config.database

    engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

    Base = declarative_base()

    class Room(Base):
        __tablename__ = 'rooms'
        id = Column(Integer, primary_key=True, autoincrement=True)
        room_no = Column(Integer, unique=True)
        price = Column(Integer)
        room_type = Column(String(2))
        currently_booked = Column(Boolean, default=False)
        created_at = Column(DateTime, default=datetime.datetime.utcnow)

        reservations = relationship("Reservation", back_populates="room")

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

    class Loyalty(Base):
        __tablename__ = 'loyalty'
        id = Column(Integer, primary_key=True, autoincrement=True)
        guest_id = Column(Integer, ForeignKey('guests.id'))
        email_id = Column(String(50), default=None)
        created_at = Column(DateTime, default=datetime.datetime.utcnow)

    Session = sessionmaker(bind=engine)
    session = Session()
    
    def early_and_late(current_price, reservation):
        previous_price = current_price
        # Early bird discount
        days_in_advance = abs((reservation.check_in - reservation.created_at).days)
        if days_in_advance >= 90:
            discount = 0.10 + (days_in_advance - 90) / 10 * 0.05  
            current_price = int(current_price * (1 - min(discount, 0.15)))
    
        # Apply Late Minute Price Surge
        if days_in_advance < 3:
            surge = 0.10 + (3 - days_in_advance) / 3 * 0.10  
            current_price = int(current_price * (1 + min(surge, 0.20)))
    
        percentage_change = ((current_price - previous_price) / previous_price) * 100
        sign = "+" if percentage_change > 0 else ""
        print(f"Price after Smart Booking Optimization => {current_price} ({sign}{percentage_change:.2f}%)")
        return current_price, f"{sign}{percentage_change:.2f}%" if percentage_change != 0 else "No Change"

    def calculate_dynamic_price(room, reservation):
        prices = []
        labels = []
        changes = []
    
        base_price = 5000 
        prices.append(base_price)
        labels.append('Initial Price')
        changes.append('')
        print(f"Initial Price => {base_price}")

        previous_price = base_price
        if room.room_type == 'D': 
            base_price += 1000
        elif room.room_type == 'N':  
            base_price += 500
    
        percentage_change = ((base_price - previous_price) / previous_price) * 100
        prices.append(base_price)
        labels.append('Room Type Adjustment')
        changes.append(f"+{percentage_change:.2f}%" if percentage_change != 0 else "No Change")
        print(f"Price After Room Type Adjustment => {base_price} ({changes[-1]})")
    
        previous_price = base_price
        created_at_date = reservation.check_in
        is_weekend_flag = created_at_date.weekday() >= 5 

        if is_weekend_flag:
            base_price *= 1.05  

        percentage_change = ((base_price - previous_price) / previous_price) * 100
        prices.append(int(base_price))
        labels.append('Weekend Surge Charge')
        changes.append(f"+{percentage_change:.2f}%" if percentage_change != 0 else "No Change")
        print(f"Price After Weekend Surge Charge => {int(base_price)} ({changes[-1]})")
    
        previous_price = base_price
        if created_at_date.month in [3, 4]:
            base_price *= 1.15  
    
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
                total_period = (end_date - start_date).days
                days_passed = (created_at_date - start_date).days
                fraction_passed = days_passed / total_period
            
                current_multiplier = min_multiplier + (max_multiplier - min_multiplier) * fraction_passed
                previous_price = base_price
                base_price *= current_multiplier
                percentage_change = ((base_price - previous_price) / previous_price) * 100
                prices.append(int(base_price))
                labels.append('Festive Period Amendments')
                changes.append(f"+{percentage_change:.2f}%" if percentage_change != 0 else "No Change")
                print(f"Price After Festive Period Amendments => {int(base_price)} ({changes[-1]})")
                break  
    
        return int(base_price), prices, labels, changes
    
    def is_room_booked(room_no, session):
        reservation = session.query(Reservation).join(Room).filter(Room.room_no == room_no, Reservation.check_out == None).first()
        return reservation is not None

    def update_room_price(room_no, session, current_price):
        previous_price = current_price
        if is_room_booked(room_no, session):
            current_price *= 1.18  
    
        percentage_change = ((current_price - previous_price) / previous_price) * 100
        print(f"Price After Room Availability Charge => {int(current_price)} ({f'+{percentage_change:.2f}%' if percentage_change != 0 else 'No Change'})")
        return int(current_price), f"+{percentage_change:.2f}%" if percentage_change != 0 else "No Change"

    def apply_loyalty_discount(current_price, guest, session):
        previous_price = current_price

        loyalty_member = session.query(Loyalty).filter_by(email_id=guest.email_id).first()

        if loyalty_member:
            current_price = int(current_price * 0.8)  

        percentage_change = ((current_price - previous_price) / previous_price) * 100
        print(f"Price After Loyalty Discount => {current_price} ({f'{percentage_change:.2f}%' if percentage_change != 0 else 'No Change'})")
        return current_price, f"{percentage_change:.2f}%" if percentage_change != 0 else "No Change"
 
    def apply_special_offer(current_price, reservation):
        previous_price = current_price
        offer_start_date = datetime.datetime(2024, 4, 20)
        offer_end_date = datetime.datetime(2024, 4, 30)
    
        if offer_start_date <= reservation.check_in <= offer_end_date:
            current_price = int(current_price * 0.93)  

    def apply_special_offer(current_price, reservation):
        previous_price = current_price
        offer_start_date = datetime.datetime(2024, 4, 20)
        offer_end_date = datetime.datetime(2024, 4, 30)
        if offer_start_date <= reservation.check_in <= offer_end_date:
            current_price = int(current_price * 0.93)  

        # Discount periods for holidays
        holiday_discounts = [
        (datetime.datetime(2024, 2, 1), datetime.datetime(2024, 2, 28), 0.85, 0.75),  # February discount range
        (datetime.datetime(2024, 7, 15), datetime.datetime(2024, 9, 7), 0.85, 0.75),  # Mid-July to Early September discount range
        (datetime.datetime(2024, 11, 1), datetime.datetime(2024, 11, 30), 0.85, 0.75),  # After Diwali discount range

        ]

        # Apply discounts based on holiday periods
        for start_date, end_date, min_discount, max_discount in holiday_discounts:
            if start_date <= reservation.check_in <= end_date:
                total_period = (end_date - start_date).days
                days_passed = (reservation.check_in - start_date).days
                fraction_passed = days_passed / total_period
    
                current_discount = min_discount + (max_discount - min_discount) * fraction_passed
                current_price = int(current_price * current_discount)
                break  
    
        percentage_change = ((current_price - previous_price) / previous_price) * 100
        print(f"Price After Special Offer Period => {current_price} ({f'{percentage_change:.2f}%' if percentage_change != 0 else 'No Change'})")
        return current_price, f"{percentage_change:.2f}%" if percentage_change != 0 else "No Change"

    def apply_peak_load_pricing(current_price, total_rooms, vacant_rooms):
        previous_price = current_price

        occupancy_rate = ((total_rooms - vacant_rooms) / total_rooms) * 100

        # Set thresholds and percentage adjustments
        low_occupancy_threshold = 25
        high_occupancy_threshold = 85  # or 90.0 based on your preference
        low_occupancy_decrease = 0.90    # Decrease by 10% if occupancy is below the low threshold
        high_occupancy_increase = 1.15   # Increase by 15% if occupancy is above the high threshold

        if occupancy_rate <= low_occupancy_threshold:
            current_price = int(current_price * low_occupancy_decrease)
        elif occupancy_rate >= high_occupancy_threshold:
            current_price = int(current_price * high_occupancy_increase)

        percentage_change = ((current_price - previous_price) / previous_price) * 100
        sign = "+" if percentage_change > 0 else ""
        print(f"Price After Peak-Load Pricing => {current_price} ({f'{sign}{percentage_change:.2f}%' if percentage_change != 0 else 'No Change'})")
        return current_price, f"{sign}{percentage_change:.2f}%" if percentage_change != 0 else "No Change"

    def get_guest_info(guest_id, session, final_price, prices, labels, changes):
        guest = session.query(Guest).filter_by(id=guest_id).first()
        reservation = session.query(Reservation).filter_by(g_id=guest_id, check_out=None).first()
        room = session.query(Room).filter_by(id=reservation.r_id).first() if reservation else None
    
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
        if guest and reservation and room:
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
        
            save_table_to_pdf(guest.id, session, final_price, prices, labels, changes)
        
            print("\nBooking Information:")
            print(table)
        else:
            print(f"No guest or reservation found with ID {guest_id}")

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
            col_widths = [max(w, 80) for w in col_widths]  
            for i, field in enumerate(table.field_names):
                self.cell(col_widths[i], 10, field, 1, 0, 'C')
            self.ln()

            self.set_font('Arial', '', 12)
            for row in table.rows:
                for i, field in enumerate(row):
                    self.cell(col_widths[i], 10, str(field), 1, 0, 'C')
                self.ln()

        def add_narrow_table(self, table):
            self.set_font('Arial', 'B', 12)
            col_widths = [self.get_string_width(col) for col in table.field_names]
            col_widths = [max(w, 58) for w in col_widths] 

            for i, field in enumerate(table.field_names):
                self.cell(col_widths[i], 10, field, 1, 0, 'C')
            self.ln()

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
            table = PrettyTable()
            table.field_names = ["Field", "Data"]

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

            for row in data:
                table.add_row(row)

            table.max_width["Field"] = max(len(row[0]) for row in data) + 5 
            table.max_width["Data"] = max(len(str(row[1])) for row in data) + 5  

            receipts_folder = 'receipts'

            if not os.path.exists(receipts_folder):
                os.makedirs(receipts_folder)

            pdf = PDF()
            pdf.add_page()

            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="SmartStay", ln=True, align='C')
            pdf.set_font("Arial", 'I', 12)
            pdf.cell(200, 10, txt="Your Booking Confirmation!", ln=True, align='C')
            pdf.ln(10)

            pdf.set_font("Arial", '', 12)
            pdf.multi_cell(0, 10, 
                "Dear {name},\n\n"
                "Thank you for choosing our hotel for your stay. We are pleased to confirm your booking and "
                "hope you have a pleasant experience with us. Below are the details of your reservation.\n\n".format(name=guest.name)
            )
        
            pdf.add_table(table)
  
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

            pdf.ln(10)
            pdf.set_font("Arial", 'I', 10)
            pdf.multi_cell(0, 10,
                "For any inquiries or additional assistance, please contact us at smartstaytcet@gmail.com or call us at (123) 456-7890.\n"
                "We look forward to welcoming you to our hotel.\n\n"
                "Sincerely,\nSmartStay Team"
            )

            filename = os.path.join(receipts_folder, f"Booking_info_{guest.id}.pdf")
            pdf.output(filename)
    
            print(f"PDF receipt saved as {filename}")
        
            try:
                yag = yagmail.SMTP(db_config.email, db_config.passw)
                subject = "Your Booking Information"
                body = "Dear Guest,\n\nPlease find attached your booking information.\n\nBest Regards,\nSmartStay Team"
                yag.send(to=guest.email_id, subject=subject, contents=body, attachments=filename)
                print(f"\033[1mBooking info sucessfully mailed to {guest.email_id}!\033[0m")
            except Exception as e:
                print(f"Failed to send email: {e}")
        else:
            print("No guest or reservation found.")

    # Main function
    def update_room_price_main():
        try:
            session = Session()
            room_number_to_update = int(input("Enter the room number to update: "))
            room = session.query(Room).filter_by(room_no=room_number_to_update).first()

            if room:
                reservation = session.query(Reservation).filter_by(r_id=room.id, check_out=None).first()
    
                if reservation:
                    guest = session.query(Guest).filter_by(id=reservation.g_id).first()
                    display_price_calculation_animation()

                    new_price, prices, labels, changes = calculate_dynamic_price(room, reservation)

                    new_price, change = early_and_late(new_price, reservation)
                    prices.append(new_price)
                    labels.append('Smart Booking Optimization')
                    changes.append(change)

                    new_price, change = update_room_price(room.room_no, session, new_price)
                    prices.append(new_price)
                    labels.append('Room Availability Charge')
                    changes.append(change)
    
                    new_price, change = apply_loyalty_discount(new_price, guest, session)
                    prices.append(new_price)
                    labels.append('CLV-oriented Discount')
                    changes.append(change)
            
                    new_price, change = apply_special_offer(new_price, reservation)
                    prices.append(new_price)
                    labels.append('Special Offer Period')
                    changes.append(change)

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


                    new_price, change = apply_peak_load_pricing(new_price, total_rooms, vacant_rooms)
                    prices.append(new_price)
                    labels.append('Peak-Load Pricing')
                    changes.append(change)

                    room.price = new_price
                    session.commit() 
                
                    get_guest_info(guest.id, session, new_price, prices, labels, changes)
                
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
            session.close()
            
    update_room_price_main()