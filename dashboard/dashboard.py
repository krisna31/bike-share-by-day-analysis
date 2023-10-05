import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
import numpy as np
sns.set(style='dark')

# Disable warning
st.set_option('deprecation.showPyplotGlobalUse', False)

# Function to create bar plot of bikes rented by season
def create_bikes_by_seasons(day_df):
  plt.figure(figsize=(15, 5)) # set the size of the plot

  rent_by_holiday = day_df[day_df['dteday'] >= '2012-01-01'].groupby('season')['cnt'].sum() # Mengelompokkan data berdasarkan season dan menjumlahkan data pada kolom cnt

  axis = rent_by_holiday.plot(kind='bar', color='skyblue', edgecolor='black') # Membuat bar plot dari data season_counts

  axis.set_title('Number of Bikes Rented by Season', fontsize=14) # Memberi judul pada bar plot
  axis.set_xlabel('Season') # Memberi label pada sumbu x
  axis.set_ylabel('Number of Bikes Rented') # Memberi label pada sumbu y

  season_in_name = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}  # Membuat dictionary season_labels
  season_colors = {1: 'green', 2: 'orange', 3: 'brown', 4: 'blue'}
  axis.set_xticklabels([season_in_name[x] for x in rent_by_holiday.index], rotation=45, ) # Memberi label pada sumbu x berdasarkan dictionary season_labels

  for index, value in enumerate(rent_by_holiday):
      plt.text(index, value, str(value), ha='center', va='bottom', fontsize=10) # Menampilkan nilai dari setiap bar plot
      plt.bar(index, value, color=season_colors[index+1]) # Menampilkan bar plot

  legend_labels = [plt.Rectangle((0, 0), 1, 1, color=season_colors[i+1]) for i in range(len(season_colors))]
  plt.legend(legend_labels, season_in_name.values(), loc='upper left')

  st.pyplot()

# Function to create bar plot of bikes rented by holiday or working day
def create_bikes_by_day(day_df):
  from matplotlib.ticker import FuncFormatter
  plt.figure(figsize=(8, 5)) # set the size of the plot

  rent_by_holiday = day_df[day_df['dteday'] >= '2012-01-01'].groupby('workingday')['cnt'].sum() # Mengelompokkan data berdasarkan season dan menjumlahkan data pada kolom cnt

  axis = rent_by_holiday.plot(kind='bar') # Membuat bar plot dari data season_counts

  axis.set_title('Number of Bikes Rented by Holiday or Working day') # Memberi judul pada bar plot
  axis.set_ylabel('Number of Bikes Rented') # Memberi label pada sumbu y

  season_in_name = {0: 'Working day', 1: 'Holiday'}  # Membuat dictionary season_labels
  axis.set_xticklabels([season_in_name[x] for x in rent_by_holiday.index], rotation=0) # Memberi label pada sumbu x berdasarkan dictionary season_labels

  for index, value in enumerate(rent_by_holiday):
      plt.text(index, value, str(value), ha='center', va='bottom') # Menampilkan nilai dari setiap bar plot
      plt.bar(index, value) # Menampilkan bar plot

  axis.yaxis.set_major_formatter(FuncFormatter(lambda value, pos: "{:,}".format(int(value)))) # Menampilkan nilai pada sumbu y dalam format ribuan

  st.pyplot()

# Function to create line plot of bikes rented by last 12 months
def plot_last_12_months(day_df):
  plt.figure(figsize=(15, 5)) # set the size of the plot

  # kelompokkan jumlah penjualan dalam 12 bulan terakhir dan buat dalam bentuk line plot
  rent_by_holiday = day_df[day_df['dteday'] >= '2012-01-01'].groupby('month')['cnt'].sum() # Mengelompokkan data berdasarkan season dan menjumlahkan data pada kolom cnt

  axis = rent_by_holiday.plot(kind='line') # Membuat bar plot dari data season_counts

  axis.set_title('Number of Bikes Rented by Last 12 Month') # Memberi judul pada bar plot
  axis.set_xlabel('Month') # Memberi label pada sumbu x
  axis.set_ylabel('Number of Bikes Rented') # Memberi label pada sumbu y

  # show all the x ticks
  plt.xticks(np.arange(1, 13, 1))

  season_in_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'Desember'}  # Membuat dictionary season_labels
  axis.set_xticklabels([season_in_name[x] for x in rent_by_holiday.index], rotation=45) # Memberi label pada sumbu x berdasarkan dictionary season_labels

  plt.plot(rent_by_holiday, marker='o', color='blue', linestyle='solid') # Menampilkan nilai dari setiap bar plot

  st.pyplot()

# Read the cleaned data
day_df = pd.read_csv('dashboard/cleaned_data.csv')

# Create the dashboard title and description
st.title('Bike Rental Dashboard')
st.markdown("""
This dashboard shows the number of bikes rented by season, holiday or working day, and the last 12 months.
""")

# Create a sidebar for user input
st.sidebar.title('Options')
plot_option = st.sidebar.selectbox('Select Plot', ['Seasonal Rentals', 'Holiday vs. Working Day', 'Last 12 Months'])

# Create the plots
if plot_option == 'Seasonal Rentals':
  # Create a plot of the number of bikes rented by season
  st.sidebar.info('View the number of bikes rented by season.')
  st.sidebar.info('Season = 1: Spring, 2: Summer, 3: Fall, 4: Winter')
  create_bikes_by_seasons(day_df)
elif plot_option == 'Holiday vs. Working Day':
  # Create a plot of the number of bikes rented by holiday or working day
  st.sidebar.info('View the number of bikes rented by holiday or working day.')
  create_bikes_by_day(day_df)
elif plot_option == 'Last 12 Months':
  # Create a plot of the number of bikes rented by last 12 months
  st.sidebar.info('View the number of bikes rented for the last 12 months.')
  plot_last_12_months(day_df)

# show description for all the plots
st.write('This is a dashboard to visualize the data from the cleaned_data.csv file.')

# create footer
st.write('@2023 ~ Created by: [krisna31](https://github.com/krisna31)')