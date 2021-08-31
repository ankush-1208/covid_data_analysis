import numpy as np
import pandas as pd
import streamlit as st 
import matplotlib.pyplot as plt
import seaborn as sns 
import PIL as Image
import altair as alt

st.title('COVID-19 Data Analysis')
st.set_option('deprecation.showPyplotGlobalUse', False)

st.markdown(
    '''
    This is a Data Analysis on COVID-19 in different countries in the World. Here you can compare the
    data of various countries in the form of plots and through visualizations and numbers get a better
    inference on what the data is showing. The [dataset](https://www.kaggle.com/imdevskp/corona-virus-report)
    used is from Kaggle.
    '''
)

# Loading the CSV data and converting it into pandas dataframe
def load_data(DATA):
    data = pd.read_csv(DATA)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis = 'columns', inplace = True)
    return data

covid_df = load_data('country_wise_latest.csv')
vaccine_df = load_data('country_vaccinations.csv')
daily_df = load_data('day_wise.csv')
# Removing uneccessary columns from the vaccine, day-wise dataset and converting to pd Date/Time
vaccine_df.drop('source_website', axis = 1, inplace = True)
vaccine_df.drop('source_name', axis = 1, inplace = True)
vaccine_df.drop('people_vaccinated_per_hundred', axis = 1, inplace = True)
daily_df.drop('deaths / 100 cases', axis = 1, inplace = True)
daily_df.drop('deaths / 100 recovered', axis = 1, inplace = True)
daily_df.drop('recovered / 100 cases', axis = 1, inplace = True)
pd.to_datetime(vaccine_df['date'])
pd.to_datetime(daily_df['date'])

# Toggle to show Raw data
if st.checkbox('Show raw data'):
    st.subheader('Raw Data for COVID')
    st.dataframe(covid_df)
    st.subheader('Vaccination Raw data')
    st.dataframe(vaccine_df)
    st.subheader('Day-wise data')
    st.dataframe(daily_df)

st.header('Worldwide spread of COVID-19')

# Plot showing a line chart of Confirmed cases, Total deaths and total recovered cases
plt.figure(figsize=(10, 5))
# plt.title('New Cases througout the world')
plt.xlabel('Days')
plt.ylabel('New Cases')
ax = plt.gca()
ax.axes.xaxis.set_ticks([])
plt.plot(daily_df['date'], daily_df['confirmed'], '-r')
plt.plot(daily_df['date'], daily_df['deaths'], '-b')
plt.plot(daily_df['date'], daily_df['recovered'], '-y')
plt.legend(['Confirmed Cases', 'Total Deaths', 'Total Recovered'])
st.pyplot()



st.subheader('See the Data Analysis for a specific country')

country_df = covid_df[['country/region', 'confirmed', 'deaths', 'recovered', 'active', 'new cases', 'new deaths', 'new recovered', 'who region']]
country_df.set_index('country/region')

# Using a selectbox to list out the different countries and using the selection display the required analysis
country = st.selectbox('Select Country', options= covid_df['country/region'], index=79)
st.write(f'The COVID-19 data for {country} shows that: \n')
st.table(country_df[country_df['country/region'] == country])

st.write(f'Relation between the confirmed cases, deaths and total recovered in {country}: \n')

# A Bar chart for relation between cases, deaths and recoveries
st.bar_chart(country_df[country_df['country/region'] == country][['confirmed', 'deaths', 'recovered']])

# Death rate for that particular country
death_rate = (country_df[country_df['country/region'] == country]['deaths'].sum() * 100)/country_df[country_df['country/region'] == country]['confirmed'].sum()

st.markdown(
    f'''
    ### Death rate
    The Death rate in {country} was reported to be **{death_rate:.2f}%**
    ## Vaccination Data 
    The daily vaccination graph for {country} shows 
    '''
)
vaccination_daily_df = vaccine_df[['country', 'daily_vaccinations', 'date']]
vaccination_daily_df['days'] = pd.DatetimeIndex(vaccine_df.date).day
st.line_chart(vaccination_daily_df[vaccination_daily_df['country'] == country][['daily_vaccinations']])
val = vaccination_daily_df[vaccination_daily_df['country'] == country]

