# Code for Option 3 -- view analytics
def view_Analytics():

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

    def get_total_rooms():
        total_rooms = session.query(func.count(Room.id)).scalar()
        return total_rooms

    def booked():
        booked_rooms = session.query(func.count(Reservation.id)).filter(Reservation.check_out == None).scalar()
        return booked_rooms

    def vacant():
        return get_total_rooms() - booked()

    def bookings():
        deluxe_count = session.query(func.count(Reservation.id)).\
        join(Room, Reservation.r_id == Room.id).\
        filter(Room.room_type == 'D', Reservation.check_out == None).scalar()

        normal_count = session.query(func.count(Reservation.id)).\
        join(Room, Reservation.r_id == Room.id).\
        filter(Room.room_type == 'N', Reservation.check_out == None).scalar()

        return [deluxe_count, normal_count]

    def plot_vacancy_status():
        total = get_total_rooms()
        booked_count = booked()
        vacant_count = total - booked_count

        labels = ['Booked', 'Vacant']
        sizes = [booked_count, vacant_count]

        fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=0.4)])
        fig.update_traces(hoverinfo='label+percent', textinfo='value', marker=dict(colors=['red', 'green']))
        fig.update_layout(title_text='Room Vacancy Status')
        fig.show()
                               
    def plot_bookings_by_room_type():
        booking_counts = bookings()
        room_types = ['Deluxe', 'Normal']

        fig = go.Figure([go.Bar(x=room_types, y=booking_counts, marker_color=['blue', 'green'])])
        fig.update_layout(title='Current Bookings by Room Type', xaxis_title='Room Type', yaxis_title='Number of Bookings')
        fig.show()

    def plot_booking_trends_by_day_of_week():
        check_in_dates = session.query(Reservation.check_in).all()
        df_check_in = pd.DataFrame(check_in_dates, columns=['check_in'])

        df_check_in['check_in'] = pd.to_datetime(df_check_in['check_in'])
        df_check_in['day_of_week'] = df_check_in['check_in'].dt.day_name()

        day_of_week_counts = df_check_in['day_of_week'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

        fig = px.bar(
        day_of_week_counts, 
        x=day_of_week_counts.index, 
        y=day_of_week_counts.values, 
        labels={'x': 'Day of the Week', 'y': 'Number of Bookings'}, 
        color=day_of_week_counts.values, 
        color_continuous_scale='Viridis'
        )

        fig.update_traces(
        hovertemplate='Day of the Week: %{x}<br>Number of Bookings: %{y}<extra></extra>'
        )

        fig.update_layout(
        title_text='Booking Trends by Day of Week', 
        xaxis_title='Day of the Week', 
        yaxis_title='Number of Bookings'
        )

        fig.show()

    def plot_reservation_trends():
        reservation_trends = (
        session.query(func.year(Reservation.check_in), func.month(Reservation.check_in), func.count(Reservation.id))
        .group_by(func.year(Reservation.check_in), func.month(Reservation.check_in))
        .order_by(func.year(Reservation.check_in), func.month(Reservation.check_in))
        .all()
        )
        df_trends = pd.DataFrame(reservation_trends, columns=['Year', 'Month', 'Count'])
        df_trends['Date'] = pd.to_datetime(df_trends[['Year', 'Month']].assign(DAY=1))
        date_range = pd.date_range(end=df_trends['Date'].max(), periods=12, freq='MS')
        df_complete = pd.DataFrame(date_range, columns=['Date']).merge(df_trends, on='Date', how='left')
        df_complete['Count'].fillna(0, inplace=True)
        x_values = np.array(df_complete['Date'])
        y_values = np.array(df_complete['Count'])
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_values, y=y_values, mode='lines+markers', name='Reservations'))
        fig.update_layout(
        title='Reservation Trends This Year',
        xaxis_title='Month',
        yaxis_title='Number of Reservations',
        xaxis_tickformat='%b %Y',
        xaxis=dict(
            tickmode='linear',  
            tick0=x_values[0],  
            dtick='M1'          
        ),
        showlegend=False
        )

        fig.show()

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
        fig.show()

    def plot_room_price_distribution():
        room_prices = session.query(Room.price).all()

        df_prices = pd.DataFrame(room_prices, columns=['Price'])

        bins = [4000, 5000, 6000, 7000, 8000, 9000, 10000]
        labels = ['4000-5000', '5000-6000', '6000-7000', '7000-8000', '8000-9000', '10000+']

        df_prices['Price Range'] = pd.cut(df_prices['Price'], bins=bins, labels=labels, include_lowest=True)

        price_distribution = df_prices['Price Range'].value_counts().sort_index()

        fig = px.bar(
        price_distribution, 
        x=price_distribution.index, 
        y=price_distribution.values, 
        labels={'x': 'Price Range', 'y': 'Number of Rooms'}, 
        title='Distribution of Rooms Across Different Price Ranges',
        color=price_distribution.values
        )

        fig.update_traces(
        hovertemplate='Price Range: %{x}<br>Number of Rooms: %{y}<extra></extra>'
        )

        fig.update_layout(
        xaxis_title='Price Range', 
        yaxis_title='Number of Rooms'
        )

        fig.show()

    def plot_avg_revenue_by_room_type():
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
    
        fig.show()

    def get_city_coordinates(city_name):
        geolocator = Nominatim(user_agent="smartstay_app", timeout=10)
        location = geolocator.geocode(city_name)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
        
    def plot_guest_origin_by_city():
        guest_origins = session.query(Guest.city, func.count(Guest.id)).group_by(Guest.city).all()

        df_guest_origins = pd.DataFrame(guest_origins, columns=['City', 'Guest Count'])

        df_guest_origins['Latitude'] = df_guest_origins['City'].apply(lambda city: get_city_coordinates(city)[0])
        df_guest_origins['Longitude'] = df_guest_origins['City'].apply(lambda city: get_city_coordinates(city)[1])

        df_guest_origins.dropna(subset=['Latitude', 'Longitude'], inplace=True)

        fig = px.scatter_geo(
        df_guest_origins,
        lat="Latitude",
        lon="Longitude",
        size="Guest Count",
        hover_name="City",
        color="Guest Count",
        color_continuous_scale=px.colors.sequential.Plasma,
        title="Distribution of Guests by City",
        projection="natural earth"
        )

        fig.update_layout(title_x=0.5, geo=dict(showframe=False, showcoastlines=True))

        fig.show()

    def plot_violin_price_distribution_by_room_type():
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

        fig.show()

    def plot_room_utilization_treemap():
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
        .filter(Reservation.check_out != None)  
        .group_by(Room.id)
        .all()
         )

        df_utilization = pd.DataFrame(room_utilization, columns=['Room ID', 'Room Number', 'Total Times Booked', 'Avg Revenue'])

        hover_text = df_utilization.apply(
        lambda row: f"Room Number: {row['Room Number']}<br>Total Times Booked: {row['Total Times Booked']}<br>Average Revenue: {row['Avg Revenue']}",
        axis=1
        )

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

        fig.show()

    def format_revenue(value):
        if value >= 1_000_000_000:
            return f'{value / 1_000_000_000:.1f}B'
        elif value >= 1_000_000:
            return f'{value / 1_000_000:.1f}M'
        elif value >= 1_000:
            return f'{value / 1_000:.1f}K'
        return f'{value:.2f}'

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

        fig.show()


    plot_vacancy_status()
    plot_bookings_by_room_type()
    plot_revenue_by_quarter()
    plot_violin_price_distribution_by_room_type()
    plot_avg_revenue_by_room_type()
    plot_booking_trends_by_day_of_week()
    plot_reservation_trends()
    plot_room_utilization_treemap()
    plot_avg_stay_duration_by_room_type()
    plot_room_price_distribution()
    plot_guest_origin_by_city()


    session.close()
