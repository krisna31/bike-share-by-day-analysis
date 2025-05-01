import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns  # type: ignore
import streamlit as st # type: ignore
from matplotlib.ticker import FuncFormatter # type: ignore
import numpy as np # type: ignore
sns.set_theme(style='darkgrid')
st.set_option('deprecation.showPyplotGlobalUse', False)

def create_bikes_by_seasons(day_df):
  plt.figure(figsize=(15, 5))
  rent_by_holiday = day_df[day_df['dteday'] >= '2012-01-01'].groupby('season')['cnt'].sum()
  axis = rent_by_holiday.plot(kind='bar', color='skyblue', edgecolor='black')
  axis.set_title('Number of Bikes Rented by Season', fontsize=14)
  axis.set_xlabel('Season')
  axis.set_ylabel('Number of Bikes Rented')
  season_in_name = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'} 
  season_colors = {1: 'green', 2: 'orange', 3: 'brown', 4: 'blue'}
  axis.set_xticklabels([season_in_name[x] for x in rent_by_holiday.index], rotation=45, )
  for index, value in enumerate(rent_by_holiday):
      plt.text(index, value, str(value), ha='center', va='bottom', fontsize=10)
      plt.bar(index, value, color=season_colors[index+1])
  legend_labels = [plt.Rectangle((0, 0), 1, 1, color=season_colors[i+1]) for i in range(len(season_colors))]
  plt.legend(legend_labels, season_in_name.values(), loc='upper left')
  st.pyplot()

def create_bikes_by_day(day_df):
  plt.figure(figsize=(8, 5))
  start_date, end_date = showDateFIlter()
  if start_date is None or end_date is None:
    st.warning("Please select a valid date range.")
    return
  rent_by_holiday = day_df[(day_df['dteday'] >= start_date) & (day_df['dteday'] <= end_date)].groupby('workingday')['cnt'].sum()
  axis = rent_by_holiday.plot(kind='bar')
  axis.set_title(f'Number of Bikes Rented From {start_date} to {end_date} by Holiday vs. Working Day')
  axis.set_ylabel('Number of Bikes Rented')
  season_in_name = {0: 'Working day', 1: 'Holiday'} 
  axis.set_xticklabels([season_in_name[x] for x in rent_by_holiday.index], rotation=0)
  for index, value in enumerate(rent_by_holiday):
      plt.text(index, value, str(value), ha='center', va='bottom')
      plt.bar(index, value)
  axis.yaxis.set_major_formatter(FuncFormatter(lambda value, pos: "{:,}".format(int(value))))
  st.pyplot()

def plot_last_12_months(day_df):
  plt.figure(figsize=(15, 5))
  rent_by_holiday = day_df[day_df['dteday'] >= '2012-01-01'].groupby('month')['cnt'].sum()
  axis = rent_by_holiday.plot(kind='line')
  axis.set_title('Number of Bikes Rented by Last 12 Month')
  axis.set_xlabel('Month')
  axis.set_ylabel('Number of Bikes Rented')
  plt.xticks(np.arange(1, 13, 1))
  season_in_name = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'Desember'} 
  axis.set_xticklabels([season_in_name[x] for x in rent_by_holiday.index], rotation=45)
  plt.plot(rent_by_holiday, marker='o', color='blue', linestyle='solid')
  st.pyplot()

def showDateFIlter():
  try:
    start_date, end_data = st.date_input(
        "Select date range",
        value=(pd.to_datetime(min_date), pd.to_datetime(max_date)),
        min_value=pd.to_datetime(min_date),
        max_value=pd.to_datetime(max_date),
    )
  except ValueError:
    return None, None
  return str(start_date), str(end_data)

day_df = pd.read_csv('dashboard/cleaned_data.csv')

min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

st.title('Bike Rental Dashboard')
st.markdown("""
This dashboard shows the number of bikes rented by season, holiday or working day, and the last 12 months.
And you can filter it by date
""")
with st.sidebar:
  st.title('Settings')
  plot_option = st.selectbox('Select Plot', ['Seasonal Rentals', 'Holiday vs. Working Day', 'Last 12 Months'])

if plot_option == 'Seasonal Rentals':
  st.sidebar.info("""Season = 1: Spring, 2: Summer, 3: Fall, 4: Winter""")
  create_bikes_by_seasons(day_df)
elif plot_option == 'Holiday vs. Working Day':
  st.sidebar.info('View the number of bikes rented by holiday or working day.')
  create_bikes_by_day(day_df)
elif plot_option == 'Last 12 Months':
  st.sidebar.info('View the number of bikes rented for the last 12 months.')
  plot_last_12_months(day_df)

st.write('@2025 ~ Created by: [krisna31](https://github.com/krisna31)')