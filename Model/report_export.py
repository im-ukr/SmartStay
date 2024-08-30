#code for Option 4 - Export Analytics Report to PDF
def report_export():

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

    Session = sessionmaker(bind=engine)
    session = Session()

    # Create the 'test_plots' directory if it doesn't exist
    output_dir = 'test_plots'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Convert HTML to PNG
    def html_to_png(html_file, output_file):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(f"file://{os.path.abspath(html_file)}")

        # Capture screenshot
        driver.save_screenshot(os.path.join(output_dir, output_file))
        driver.quit()


    # Function to get the total number of rooms
    def get_total_rooms():
        total_rooms = session.query(func.count(Room.id)).scalar()
        return total_rooms

    # Function to get the number of booked rooms
    def booked():
        booked_rooms = session.query(func.count(Reservation.id)).filter(Reservation.check_out == None).scalar()
        return booked_rooms

    # Function to get the number of vacant rooms
    def vacant():
        return get_total_rooms() - booked()

    # Function to get booking counts by room type
    def bookings():
        deluxe_count = session.query(func.count(Reservation.id)).\
        join(Room, Reservation.r_id == Room.id).\
        filter(Room.room_type == 'D', Reservation.check_out == None).scalar()

        normal_count = session.query(func.count(Reservation.id)).\
        join(Room, Reservation.r_id == Room.id).\
        filter(Room.room_type == 'N', Reservation.check_out == None).scalar()

        return [deluxe_count, normal_count]
    
    # All plots :

    # Plot vacancy status using plotly
    def plot_vacancy_status():
        total = get_total_rooms()
        booked_count = booked()
        vacant_count = total - booked_count

        labels = ['Booked', 'Vacant']
        sizes = [booked_count, vacant_count]

        fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=0.4)])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', marker=dict(colors=['red', 'green']))
        fig.update_layout(title_text='Room Vacancy Status')
        fig.update_layout(width=650, height=370)
    
        fig.write_html("vacancy_status.html")
        html_to_png("vacancy_status.html", "vacancy_status.png")
        sample_file_1 = PIL.Image.open('test_plots/vacancy_status.png')

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        prompt = '''describe this plot in 5 points
        dont mention anything about axis'''
        response = model.generate_content([prompt, sample_file_1])

        description = response.text 
        description_with_line_breaks = '<br>-'.join(description.split('-'))


        # Create the HTML content with the description
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Room Vacancy Status</title>
        </head>
        <body>
        <h1>Room Vacancy Status</h1>
        <p>{description_with_line_breaks}</p>
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
        </body>
        </html>
        """

        with open("vacancy_status.html", "w") as f:
            f.write(html_content)

    # Plot number of bookings by room type
    def plot_bookings_by_room_type():
        booking_counts = bookings()
        room_types = ['Deluxe', 'Normal']

        fig = go.Figure([go.Bar(x=room_types, y=booking_counts, marker_color=['blue', 'green'])])
        fig.update_layout(title='Current Bookings by Room Type', xaxis_title='Room Type', yaxis_title='Number of Bookings')
        fig.update_layout(width=650, height=370)
    
        fig.write_html("bookings_by_room_type.html")
        html_to_png("bookings_by_room_type.html", "bookings_by_room_type.png")
        sample_file_2 = PIL.Image.open('test_plots/bookings_by_room_type.png')

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        prompt = '''dont mention anything about axis. describe this plot in three or four points without numbering them but
        answer in points only'''
        response = model.generate_content([prompt, sample_file_2])

        description = response.text 
        description_with_line_breaks = '<br>-'.join(description.split('-'))


        # Create the HTML content with the description
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Bookings By Room Type</title>
        </head>
        <body>
        <h1>Bookings By Room Type</h1>
        <p>{description_with_line_breaks}</p>
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
        </body>
        </html>
        """

        with open("bookings_by_room_type.html", "w") as f:
            f.write(html_content)
    
    # Plot number of bookings on each day of the week
    def plot_booking_trends_by_day_of_week():
        check_in_dates = session.query(Reservation.check_in).all()
        df_check_in = pd.DataFrame(check_in_dates, columns=['check_in'])

        df_check_in['check_in'] = pd.to_datetime(df_check_in['check_in'])
        df_check_in['day_of_week'] = df_check_in['check_in'].dt.day_name()

        day_of_week_counts = df_check_in['day_of_week'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

        fig = px.bar(day_of_week_counts, x=day_of_week_counts.index, y=day_of_week_counts.values, 
                 labels={'x': 'Day of the Week', 'y': 'Number of Bookings'}, color=day_of_week_counts.values, color_continuous_scale='Viridis')
        fig.update_layout(title_text='Booking Trends by Day of Week', xaxis_title='Day of the Week', yaxis_title='Number of Bookings')
        fig.update_layout(width=650, height=370)

        fig.write_html("booking_trends_by_day_of_week.html")
        html_to_png("booking_trends_by_day_of_week.html", "booking_trends_by_day_of_week.png")
        sample_file_3 = PIL.Image.open('test_plots/booking_trends_by_day_of_week.png')

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        prompt = '''describe this plot in 5 points without numbering them, yellow
        color indicates highest number of bookings
        dont mention anything about axis'''
        response = model.generate_content([prompt, sample_file_3])

        description = response.text 
        description_with_line_breaks = '<br>-'.join(description.split('-'))


        # Create the HTML content with the description
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Booking Trends By Days Of Week</title>
        </head>
        <body>
        <h1>Booking Trends By Days Of Week</h1>
        <p>{description_with_line_breaks}</p>
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
        </body>
        </html>
        """

        with open("booking_trends_by_day_of_week.html", "w") as f:
            f.write(html_content)

    # Plot Reservation Trends Over the Year 
    def plot_reservation_trends():
        # Query to get reservation trends  -- getting number of reservations in each month
        reservation_trends = (
        session.query(func.year(Reservation.check_in), func.month(Reservation.check_in), func.count(Reservation.id))
        .group_by(func.year(Reservation.check_in), func.month(Reservation.check_in))
        .order_by(func.year(Reservation.check_in), func.month(Reservation.check_in))
        .all()
        )

        # Convert the query result to a DataFrame
        df_trends = pd.DataFrame(reservation_trends, columns=['Year', 'Month', 'Count'])

        # Convert Year and Month to datetime using pd.to_datetime
        df_trends['Date'] = pd.to_datetime(df_trends[['Year', 'Month']].assign(DAY=1))

        # Create a complete date range for the last 12 months
        date_range = pd.date_range(end=df_trends['Date'].max(), periods=12, freq='MS')

        # Merge with the original dataframe to include missing months
        df_complete = pd.DataFrame(date_range, columns=['Date']).merge(df_trends, on='Date', how='left')

        # Fill missing reservation counts with 0
        df_complete['Count'].fillna(0, inplace=True)

        # Use np.array to handle the datetime values
        x_values = np.array(df_complete['Date'])
        y_values = np.array(df_complete['Count'])

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', name='Reservations'))

        # Update layout with tick mode and interval to display all months
        fig.update_layout(
        title='Reservation Trends This Year',
        xaxis_title='Month',
        yaxis_title='Number of Reservations',
        xaxis_tickformat='%b %Y',
        xaxis=dict(
            tickmode='linear',  
            tick0=x_values[0],  # Start tick at the first date
            dtick='M1'          # Set tick interval to 1 month
        ),
        showlegend=False
        )
        fig.update_layout(width=620, height=350)

        # Save the figure as an HTML file
        fig.write_html("reservation_trends.html")
        html_to_png("reservation_trends.html", "reservation_trends.png")
        sample_file_4 = PIL.Image.open('test_plots/reservation_trends.png')

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        prompt = '''describe the reservation trends observed in four or five points without
        numbering them. it has nothing to do with color. mention month names too'''
        response = model.generate_content([prompt, sample_file_4])

        description = response.text 
        description_with_line_breaks = '<br>-'.join(description.split('-'))


        # Create the HTML content with the description
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Reservation Trends</title>
        </head>
        <body>
        <h1>Reservation Trends This Year</h1>
        <p>{description_with_line_breaks}</p>
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
        </body>
        </html>
        """

        with open("reservation_trends.html", "w") as f:
            f.write(html_content)


    # Plot Average stay duration of each room type
    def plot_avg_stay_duration_by_room_type():
        stay_duration = (
        session.query(Room.room_type, func.round(func.avg(func.datediff(Reservation.check_out, Reservation.check_in)), 2))
        .join(Room, Reservation.r_id == Room.id)
        .filter(Reservation.check_out != None)  
        .group_by(Room.room_type)
        .all()
        )

        df_stay = pd.DataFrame(stay_duration, columns=['Room Type', 'Avg Duration'])
        fig = px.bar(df_stay, x='Room Type', y='Avg Duration', labels={'Avg Duration': 'Average Duration (days)'}, 
                 title='Average Stay Duration by Room Type', color='Avg Duration')
        fig.update_layout(xaxis_title='Room Type', yaxis_title='Average Stay Duration (days)')
        fig.update_layout(width=650, height=360)
    
        fig.write_html("avg_stay_duration_by_room_type.html")
        html_to_png("avg_stay_duration_by_room_type.html", "avg_stay_duration_by_room_type.png")
        sample_file_5 = PIL.Image.open('test_plots/avg_stay_duration_by_room_type.png')

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        prompt = '''dont mention revenue in words. describe this plot in 5 points without numbering 
        them. dont mention anything about axis. mention avg stay duration of each type too'''
        response = model.generate_content([prompt, sample_file_5])

        description = response.text 
        description_with_line_breaks = '<br>-'.join(description.split('-'))


        # Create the HTML content with the description
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Average Stay Duration By Room Type</title>
        </head>
        <body>
        <h1>Average Stay Duration By Room Type</h1>
        <p>{description_with_line_breaks}</p>
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
        </body>
        </html>
        """

        with open("avg_stay_duration_by_room_type.html", "w") as f:
            f.write(html_content)
    
    # Plot number of rooms in each price segment
    def plot_room_price_distribution():
        # Query to get the price of each room
        room_prices = session.query(Room.price).all()
    
        df_prices = pd.DataFrame(room_prices, columns=['Price'])
    
        # Define price bins (adjust these ranges based on our data)
        bins = [4000, 5000, 6000, 7000, 8000, 9000, 10000]
        labels = ['4000-5000', '5000-6000', '6000-7000', '7000-8000', '8000-9000', '10000+']
    
        # Categorize the prices into the defined bins
        df_prices['Price Range'] = pd.cut(df_prices['Price'], bins=bins, labels=labels, include_lowest=True)
    
        # Count the number of rooms in each price range
        price_distribution = df_prices['Price Range'].value_counts().sort_index()
    
        fig = px.bar(price_distribution, x=price_distribution.index, y=price_distribution.values, 
                 labels={'x': 'Price Range', 'y': 'Number of Rooms'}, 
                 title='Distribution of Rooms Across Different Price Ranges',
                 color=price_distribution.values)
    
        fig.update_layout(xaxis_title='Price Range', yaxis_title='Number of Rooms')
        fig.update_layout(width=600, height=330)
    
        fig.write_html("room_price_distribution.html")
        html_to_png("room_price_distribution.html", "room_price_distribution.png")
        sample_file_6 = PIL.Image.open('test_plots/room_price_distribution.png')

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        prompt = '''just mention the number of rooms in each price category and write
        your conclusion'''
        response = model.generate_content([prompt, sample_file_6])

        description = response.text 


        # Create the HTML content with the description
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Room Price Distribution</title>
        </head>
        <body>
        <h1>Room Price Distribution</h1>
        <p>{description}</p>
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
        </body>
        </html>
        """

        with open("room_price_distribution.html", "w") as f:
            f.write(html_content)
    


    # Plotting room utilization tree map
    def plot_room_utilization_treemap():
        # Calculate the duration in days for each reservation and total revenue for each room
        room_utilization = (
        session.query(
            Room.id,
            Room.room_no,
            func.count(Reservation.id).label('total_times_booked'),
            func.round(func.avg(
                (func.datediff(Reservation.check_out, Reservation.check_in)) * Room.price
            ), 2).label('avg_revenue')
          )
        .join(Reservation, Reservation.r_id == Room.id)
        .filter(Reservation.check_out != None)  # Ensure the room is checked-out
        .group_by(Room.id)
        .all()
        )

        df_utilization = pd.DataFrame(room_utilization, columns=['Room ID', 'Room Number', 'Total Times Booked', 'Avg Revenue'])

        hover_text = df_utilization.apply(
        lambda row: f"Room Number: {row['Room Number']}<br>Total Times Booked: {row['Total Times Booked']}<br>Average Revenue: {row['Avg Revenue']}",
        axis=1
        )

        # Creating a Treemap
        fig = go.Figure(go.Treemap(
        labels=df_utilization['Room Number'],
        parents=[''] * len(df_utilization),  
        values=df_utilization['Total Times Booked'],
        marker=dict(
            colors=df_utilization['Avg Revenue'],
            colorscale='Greens',
            colorbar_title='Avg Revenue'
        ),
        textinfo='label',  
        hovertext=hover_text, 
        hoverinfo='text', 
        textfont=dict(size=20)
        ))

        fig.update_layout(
        title='Room Utilization Treemap',
        margin=dict(t=50, l=25, r=25, b=25),
        coloraxis_colorbar_title='Avg Revenue'
        )
        fig.update_layout(width=600, height=330)

        fig.write_html("room_treemap.html")
        html_to_png("room_treemap.html", "room_treemap.png")
        sample_file_7 = PIL.Image.open('test_plots/room_treemap.png')

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        prompt = '''mention the following : room numbers with high utilization(dark green shades) then room numbers with average utlizations(medium green shade)
        and then room numbers with low utlization(light green or white shade). mention that dark green means high utlization. the full answer should be in points'''
        response = model.generate_content([prompt, sample_file_7])

        description = response.text 
        description_with_line_breaks = '<br>-'.join(description.split('-'))


        # Create the HTML content with the description
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Room Treemap</title>
        </head>
        <body>
        <h1>Room Utlization Treemap</h1>
        <p>{description_with_line_breaks}</p>
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
        </body>
        </html>
        """

        # Save the HTML content to a file
        with open("room_treemap.html", "w") as f:
            f.write(html_content)

    # Function to format higher revenue values
    def format_revenue(value):
        if value >= 1_000_000_000:
            return f'{value / 1_000_000_000:.1f}B'
        elif value >= 1_000_000:
            return f'{value / 1_000_000:.1f}M'
        elif value >= 1_000:
            return f'{value / 1_000:.1f}K'
        return f'{value:.2f}'
   
    # Plot total revnue generated in each quarter 
    def plot_revenue_by_quarter():
        monthly_revenue = (
        session.query(
        extract('year', Reservation.check_out).label('year'),
        extract('month', Reservation.check_out).label('month'),
            func.sum(Room.price * func.datediff(Reservation.check_out, Reservation.check_in)).label('total_revenue')
         )
        .join(Room, Reservation.r_id == Room.id)
        .filter(Reservation.check_out != None)
         #.filter(extract('year', Reservation.check_out) == 2024)  # Filter for the year as per requirements
        .group_by(extract('year', Reservation.check_out), extract('month', Reservation.check_out))
        .order_by(extract('year', Reservation.check_out), extract('month', Reservation.check_out))
        .all()
          )

        df_revenue = pd.DataFrame(monthly_revenue, columns=['Year', 'Month', 'Total Revenue'])

        df_revenue['Total Revenue'] = df_revenue['Total Revenue'].astype(float).round(2)

        df_revenue['Quarter'] = pd.to_datetime(df_revenue[['Year', 'Month']].assign(Day=1)).dt.to_period('Q').astype(str)

        quarterly_revenue = df_revenue.groupby('Quarter')['Total Revenue'].sum().reset_index()

        quarterly_revenue['Formatted Revenue'] = quarterly_revenue['Total Revenue'].apply(format_revenue)


        custom_blue_scale = [
        [0, 'rgb(173, 216, 230)'],  
        [0.5, 'rgb(100, 149, 237)'],  
        [1.0, 'rgb(0, 0, 139)']  
        ]

        fig = px.bar(
        quarterly_revenue,
        x='Quarter',
        y='Total Revenue',
        labels={'Quarter': 'Quarter', 'Total Revenue': 'Total Revenue'},
        title='Total Revenue by Quarter',
        text='Formatted Revenue',
        color='Total Revenue',
        color_continuous_scale=custom_blue_scale  
        )

        fig.update_traces(
        texttemplate='%{text}',
        textposition='auto',  
        hovertemplate='Quarter: %{x}<br>Total Revenue: %{text}<extra></extra>'
        )

        fig.update_layout(
        xaxis_title='Quarter',
        yaxis_title='Total Revenue',
        plot_bgcolor='#E5ECF6',
        paper_bgcolor='#E5ECF6',
        title_font=dict(size=24, color='darkblue'),
        font=dict(size=16),
        xaxis=dict(showgrid=True, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridcolor='lightgray'),
        margin=dict(t=90, l=40, r=20, b=40),
        coloraxis_showscale=True
        )
        fig.update_layout(width=600, height=350)

        # Save the figure as an HTML file
        fig.write_html("revenue_by_quarter.html")
        html_to_png("revenue_by_quarter.html", "revenue_by_quarter.png")
        sample_file_8 = PIL.Image.open('test_plots/revenue_by_quarter.png')

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        prompt = '''mention revenue of every quarter in digits/numbers only along with quarter name and
        frame proper sentences for it, write conclusion in one ot two points without mentioning the word conclusion'''
        response = model.generate_content([prompt, sample_file_8])

        description = response.text 
        description_with_line_breaks = '<br>-'.join(description.split('-'))

        # Create the HTML content with the description
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Revenue By Quarter</title>
        </head>
        <body>
        <h1>Revenue By Quarter</h1>
        <p>{description_with_line_breaks}</p>
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
        </body>
        </html>
        """

        with open("revenue_by_quarter.html", "w") as f:
            f.write(html_content)
    
    # Violin plot for room price distribution
    def plot_violin_price_distribution_by_room_type():
        # Query to get room prices along with room types
        room_data = session.query(Room.room_type, Room.price).all()

        df_rooms = pd.DataFrame(room_data, columns=['Room Type', 'Price'])

        fig = px.violin(df_rooms, x='Room Type', y='Price', 
                    box=True,  
                    points='all',  
                    hover_data=['Price'], 
                    title='Violin Plot for Price Distribution by Room Type',
                    color='Room Type', 
                    labels={'Price': 'Room Price', 'Room Type': 'Room Type'})

        fig.update_layout(xaxis_title='Room Type', yaxis_title='Room Price', title_x=0.5)
        fig.update_layout(width=630, height=350)

        fig.write_html("violin_plot.html")
        html_to_png("violin_plot.html", "violin_plot.png")
        sample_file_9 = PIL.Image.open('test_plots/violin_plot.png')

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        prompt = '''describe this plot in 5 points without numbering them'''
        response = model.generate_content([prompt, sample_file_9])

        description = response.text 
        description_with_line_breaks = '<br>-'.join(description.split('-'))


        # Create the HTML content with the description
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Violin Plot</title>
        </head>
        <body>
        <h1>Violin Plot for Price Distribution By Room Type</h1>
        <p>{description_with_line_breaks}</p>
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
        </body>
        </html>
        """

        with open("violin_plot.html", "w") as f:
            f.write(html_content)

    # Plot average revenue generated by each room type
    def plot_avg_revenue_by_room_type():
        # Query to calculate average revenue by room type, considering only rooms in the reservations table
        avg_revenue_by_room_type = (
        session.query(Room.room_type, func.round(func.avg(Room.price), 2))
        .join(Reservation, Reservation.r_id == Room.id)
        .group_by(Room.room_type)
        .all()
        )
    
        df_avg_revenue = pd.DataFrame(avg_revenue_by_room_type, columns=['Room Type', 'Average Revenue'])

        fig = px.bar(df_avg_revenue, x='Room Type', y='Average Revenue', 
                 labels={'Average Revenue': 'Average Revenue', 'Room Type': 'Room Type'},
                 title='Average Revenue per Day by Room Type',
                 color='Average Revenue')


        fig.update_layout(xaxis_title='Room Type', yaxis_title='Average Revenue', title_x=0.5)
        fig.update_layout(width=600, height=350)
    
        fig.write_html("avg_revenue.html")
        html_to_png("avg_revenue.html", "avg_revenue.png")
        sample_file_10 = PIL.Image.open('test_plots/avg_revenue.png')

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        prompt = '''describe this plot in 5 points without numbering them
        also mention avg revenue generated by each room type'''
        response = model.generate_content([prompt, sample_file_10])

        description = response.text 
        description_with_line_breaks = '<br>-'.join(description.split('-'))


        # Create the HTML content with the description
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Average Revenue per Day By Room Type</title>
        </head>
        <body>
        <h1>Average Revenue per Day By Room Type</h1>
        <p>{description_with_line_breaks}</p>
        {fig.to_html(full_html=False, include_plotlyjs='cdn')}
        </body>
        </html>
        """

        with open("avg_revenue.html", "w") as f:
            f.write(html_content)

    # Call the functions to plot the data and save as HTML files
    print("Analyzing data...")
    plot_vacancy_status()
    plot_bookings_by_room_type()
    plot_revenue_by_quarter()
    plot_avg_revenue_by_room_type()
    plot_room_utilization_treemap()
    plot_booking_trends_by_day_of_week()
    plot_reservation_trends()
    plot_violin_price_distribution_by_room_type()
    plot_avg_stay_duration_by_room_type()
    plot_room_price_distribution()


    # Create the 'test_plots' directory if it doesn't exist
    output_dir = 'test_plots'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Convert HTML to PNG
    def html_to_png(html_file, output_file):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")


        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        driver.get(f"file://{os.path.abspath(html_file)}")

        # Capture screenshot
        driver.save_screenshot(os.path.join(output_dir, output_file))
        driver.quit()

    # Convert each HTML file to PNG
    print("Done! Exporting to PDF. This might take a couple of minutes. Please wait..")
    html_to_png("vacancy_status.html", "vacancy_status.png")
    html_to_png("bookings_by_room_type.html", "bookings_by_room_type.png")
    html_to_png("booking_trends_by_day_of_week.html", "booking_trends_by_day_of_week.png")
    html_to_png("reservation_trends.html", "reservation_trends.png")
    html_to_png("avg_stay_duration_by_room_type.html", "avg_stay_duration_by_room_type.png")
    html_to_png("room_price_distribution.html", "room_price_distribution.png")
    html_to_png("avg_revenue.html", "avg_revenue.png")
    html_to_png("violin_plot.html", "violin_plot.png")
    html_to_png("room_treemap.html", "room_treemap.png")
    html_to_png("revenue_by_quarter.html", "revenue_by_quarter.png")

    # PDF Part starts here..

    class PDF(FPDF):
        def header(self):
            pass

        def footer(self):
            self.set_y(-26)
            self.set_text_color(0, 0, 0)
            self.set_font('Arial', 'I', 11)
            self.cell(0, 10, '', 0, 1, 'C')  # This will create a line break
            # Page number
            self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')
        
            # Get current timestamp
            current_time = time.strftime('%Y-%m-%d %H:%M:%S')
        
            self.set_xy(self.l_margin, -15)  
            self.cell(0, 10, f'Generated on: {current_time}', 0, 0, 'L')


        def table_of_contents(self, titles, start_page):
            self.set_font("Arial", '', 12)
            content_column_width = 120  # Wider column for content names
            page_number_column_width = 40  # Narrower column for page numbers

            # Calculate total table width
            table_width = content_column_width + page_number_column_width
        
            page_width = self.w - 2 * self.l_margin  # Page width minus margins
            x_start = (page_width - table_width) / 2

            self.set_x(x_start)

            self.cell(content_column_width, 10, 'Content', 1, 0, 'C')
            self.cell(page_number_column_width, 10, 'Page Number', 1, 1, 'C')
        
            # Add rows for Table of Contents
            for i, title in enumerate(titles):
                self.set_x(x_start)  # Ensure x is reset for each new row
                self.cell(content_column_width, 10, title, 1)
                self.cell(page_number_column_width, 10, str(start_page + i), 1, 1, 'C')


    pdf = PDF()
    #pdf.add_page()

    # **First Page - Title, Description, and Table of Contents**
    pdf.add_page()
    pdf.ln(10)
    # Title
    pdf.set_font("Arial", 'B', 24)
    pdf.cell(0, 10, "SmartStay Analytics Report", 0, 1, 'C')

    pdf.ln(14)  # Add some space

    # Description
    pdf.set_font("Arial", '', 12)
    description = (
    "This report provides a comprehensive overview of key analytics related to "
    "SmartStay operations. It includes visualizations of various trends and statistics "
    "that are critical for understanding performance metrics."
    )
    pdf.multi_cell(0, 10, description)

    # adding 1st page data image
    pdf.set_xy(80, 70)  
    pdf.image("Data-logo.png", w=50)  

    pdf.ln(10) 

    # Table of Contents Title
    pdf.set_font("Arial", 'B', 18)
    pdf.cell(0, 10, "Table of Contents", 0, 1, 'C')

    pdf.ln(5)  

    # Table of Contents
    image_titles = [
    "Vacancy Status",
    "Bookings by Room Type",
    "Booking Trends by Day of Week",
    "Reservation Trends",
    "Average Stay Duration by Room Type",
    "Room Price Violin Plot",
    "Room Utilization Treemap",
    "Revenue by Quarter",
    "Average Revenue By Room Type",
    "Room Price Range Distribution"
    ]

    toc_start_page = 2
    pdf.table_of_contents(image_titles, toc_start_page)

    pdf.ln(2)  

    # Position to add signature image
    #pdf.set_xy(160, 250)  
    #pdf.image("sign-ukr.png", w=30) 

    # Text below the signature
    #pdf.set_xy(160, 265)  
    #pdf.set_font("Arial", '', 12)
    #pdf.cell(0, 10, "Utkarsh Roy - SmartStay", 0, 1, 'C')

    image_files = [
    "vacancy_status.png",
    "bookings_by_room_type.png",
    "booking_trends_by_day_of_week.png",
    "reservation_trends.png",
    "avg_stay_duration_by_room_type.png",
    "violin_plot.png",
    "room_treemap.png",
    "revenue_by_quarter.png",
    "avg_revenue.png",
    "room_price_distribution.png"
    ]

    # Adding all pages to the PDF
    for image_file in image_files:
        pdf.add_page()
        pdf.image(os.path.join(output_dir, image_file), x=10, y=10, w=190)  

    
    # Saving the PDF
    pdf_output_path = "SmartStay-Analytics-Report.pdf"
    pdf.output(pdf_output_path)
    print(f"File saved as {pdf_output_path}!")

    # EmaiL Part:
    # Reading email addresses from CSV file -- create a file email.csv
    email_list = []
    with open('email.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email_list.append(row['email'])

    # Mail details:
    subject = "Analytics Report - SmartStay"
    body = "Please find attached the requested Analytics Report of SmartStay.\n\nBest Regards,\nAdmin"
    pdf_file_name = "SmartStay-Analytics-Report.pdf"

    # Send the PDF via email
    try:
        yag = yagmail.SMTP(db_config.email, db_config.passw)
        for email in email_list:
            yag.send(to=email, subject=subject, contents=body, attachments=pdf_file_name)
            print(f"\033[1mThe copy of the same is successfully mailed to {email}!\033[0m")
    except Exception as e:
        print(f"Failed to send email: {e}")

    # Clean up HTML and image files after adding to PDF
    html_files = [
    "vacancy_status.html",
    "bookings_by_room_type.html",
    "booking_trends_by_day_of_week.html",
    "reservation_trends.html",
    "avg_stay_duration_by_room_type.html",
    "room_price_distribution.html",
    "avg_revenue.html",
    "violin_plot.html",
    "room_treemap.html",
    "revenue_by_quarter.html"
    ]

    for file in html_files:
        try:
            os.remove(file)
        except FileNotFoundError:
            print(f"File not found: {file}")

    session.close()