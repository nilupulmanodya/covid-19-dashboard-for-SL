import pandas as pd
import altair as alt
from .altairplt import pcrtestbarchart, global_covid_map
from .clean_country_data import clean_country_data
import urllib3
from urllib3 import request# to handle certificate verification
import certifi# to manage json data
import json# for pandas dataframes
from pandas.io.json import json_normalize
import matplotlib.pyplot as plt 
import matplotlib.colors as mcolors
plt.style.use('fivethirtyeight')
import mpld3
from statsmodels.tsa.arima_model import ARIMA
import datetime
from datetime import timedelta
from sklearn.model_selection import train_test_split





confirmed_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')

sl_confirmed_df = pd.DataFrame(confirmed_df.loc[[236]])

deaths_df = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

cols = sl_confirmed_df.keys()

sl_deaths_df = pd.DataFrame(deaths_df.loc[[236]])

sl_confirmed = sl_confirmed_df.loc[:, cols[4]:cols[-1]]
sl_deaths = sl_deaths_df.loc[:, cols[4]:cols[-1]]

dates = sl_confirmed.keys()


def daily_increase(data):
    d = [] 
    for i in range(len(data)):
        if i == 0:
            d.append([data[i][0],data[0][1]])
        else:
            d.append([data[i][0],data[i][1]-data[i-1][1]])
    return d 


    
def get_country_info(country_name):
    country_cases = []
    country_deaths = []
#     country_recoveries = []  
    
    for i in dates:
        country_cases.append([(datetime.datetime.strptime(i, '%m/%d/%y')).date(),confirmed_df[confirmed_df['Country/Region']==country_name][i].sum()])
        country_deaths.append([(datetime.datetime.strptime(i, '%m/%d/%y')).date(),deaths_df[deaths_df['Country/Region']==country_name][i].sum()])
#         country_recoveries.append(recoveries_df[recoveries_df['Country/Region']==country_name][i].sum())
    return (country_cases, country_deaths)

    
def country_visualizations(country_name):
    country_info = get_country_info(country_name)
    country_cases = country_info[0]
    country_deaths = country_info[1]
    
    country_daily_increase = daily_increase(country_cases)
    country_daily_death = daily_increase(country_deaths)
#     country_daily_recovery = daily_increase(country_recoveries)
    
    return ( country_cases, country_daily_increase, country_daily_death, country_name)

country_cases, country_daily_increase, country_daily_death, country_name = country_visualizations('Sri Lanka')

country_cases_df = pd.DataFrame(country_cases, columns=['Date','cases'])
country_daily_increase_df = pd.DataFrame(country_daily_increase, columns=['Date','cases'])
country_daily_death_df = pd.DataFrame(country_daily_death, columns=['Date','cases'])



arima = ARIMA(country_cases_df['cases'], order=(5, 1, 0))
arima = arima.fit(trend='c', full_output=True, disp=True)
forecast = arima.forecast(steps= 30)
pred = list(forecast[0])

start_date = country_cases_df['Date'].iloc[-1]
prediction_dates = []
for i in range(30):
    date = start_date + timedelta(days=1)
    prediction_dates.append(date)
    start_date = date

fig=plt.figure()
#plt.xlabel("Dates",fontsize = 20)
plt.ylabel('Total cases',fontsize = 20)
#plt.title("Predicted Total cases for the next 15 Days" , fontsize = 20)

obj, = plt.plot_date(y= pred,x= prediction_dates,linestyle ='dashed',color = '#ff9999',label = 'Predicted');
obj, = plt.plot_date(y=country_cases_df['cases'],x=country_cases_df['Date'],linestyle = '-',color = 'blue',label = 'Actual');
plt.legend();


html_str = mpld3.fig_to_html(fig)
mpld3.save_html(fig,"templates/figure1.html")

#Html_file= open("index.html","w")
#Html_file.write(html_str)
#Html_file.close()

#obj, = plt.plot([3,1,4,1,5])



arima = ARIMA(country_daily_death_df['cases'], order=(5, 1, 0))
arima = arima.fit(trend='c', full_output=True, disp=True)
forecast = arima.forecast(steps= 30)
pred = list(forecast[0])

start_date = country_daily_death_df['Date'].iloc[-1]
prediction_dates = []
for i in range(30):
    date = start_date + timedelta(days=1)
    prediction_dates.append(date)
    start_date = date
fig=plt.figure()
#plt.xlabel("Dates",fontsize = 20)
plt.ylabel('Total cases',fontsize = 20)
#plt.title("Predicted Daily Deaths for the next 15 Days" , fontsize = 20)

plt.plot_date(y= pred,x= prediction_dates,linestyle ='dashed',color = '#ff9999',label = 'Predicted');
plt.plot_date(y=country_daily_death_df['cases'],x=country_daily_death_df['Date'],linestyle = '-',color = 'blue',label = 'Actual');
plt.legend();

html_str = mpld3.fig_to_html(fig)
mpld3.save_html(fig,"templates/figure2.html")
#plt.savefig('test.png')








def local_all_status():
    df_local = pd.read_json("https://hpb.health.gov.lk/api/get-current-statistical").data

    hospital_data = df_local.hospital_data
    hospital_data_list = []

    for i in range (0,len(hospital_data)): 
        hospital_data_list.append(hospital_data[i])
    local_hospital_details=hospital_data_list
    #print(local_hospital_details[0])
 
    local_active_cases=df_local.local_active_cases
    local_deaths = df_local.local_deaths
    local_recovered =df_local.local_recovered
    local_new_cases =df_local.local_new_cases
    local_total_cases=df_local.local_total_cases
    update_date_time =df_local.update_date_time

    #data create for pcr visualize
    daily_pcr_testing_data=df_local.daily_pcr_testing_data
    date_pcr =[]
    count_pcr =[]
    for i in range(0,len(daily_pcr_testing_data)):
        date_pcr.append(daily_pcr_testing_data[i]['date'])
        count_pcr.append(int(daily_pcr_testing_data[i]['count']))
    data_pcr = {'date_pcr':date_pcr,'count_pcr':count_pcr}
    local_pcr_test_df = pd.DataFrame(data_pcr)
    local_pcr_test_chart_json = pcrtestbarchart(local_pcr_test_df)

    local_death_rate = round(int(local_deaths)/int(local_total_cases)*100,2)
    local_recovery_rate = round(int(local_recovered)/int(local_total_cases)*100,2)

    return (local_hospital_details, local_active_cases, local_deaths, local_recovered
    ,local_new_cases, local_total_cases, local_pcr_test_chart_json,update_date_time,
    local_death_rate, local_recovery_rate)
    

def global_all_status():
    http = urllib3.PoolManager(
       cert_reqs='CERT_REQUIRED',
       ca_certs=certifi.where())

    url = 'https://api.covid19api.com/summary' 
    r = http.request('GET', url)
    print("r global url status:", r.status)
    #try:
    data = json.loads(r.data.decode('utf-8'))
    #except ValueError:  # includes simplejson.decoder.JSONDecodeError
    #    print ('Decoding JSON has failed')
    
    global_total_confirmed = data['Global']['TotalConfirmed']
    global_today_new = data['Global']['NewConfirmed']
    global_total_deaths = data['Global']['TotalDeaths']
    global_total_recovered = data['Global']['TotalRecovered']
    global_update_date = data['Global']['Date']
    counties_df = pd.json_normalize(data,'Countries')
    global_active_cases = global_total_confirmed-global_total_recovered
    #import country geo data for map

    c_url = "https://gist.githubusercontent.com/komasaru/9303029/raw/9ea6e5900715afec6ce4ff79a0c4102b09180ddd/iso_3166_1.csv"
    country_code = pd.read_csv(c_url)
    cleaned_country_code = clean_country_data(country_code)
    #merge data frames
    cc_m=pd.merge(cleaned_country_code,counties_df,how='inner',on='Country')

    global_map_json = global_covid_map(cc_m)
    #print(global_map_json)

    global_death_rate = round(int(global_total_deaths)/int(global_total_confirmed)*100,2)
    global_recovery_rate = round(int(global_total_recovered)/int(global_total_confirmed)*100,2)

    return (global_active_cases, global_total_confirmed, global_today_new, global_total_deaths, global_total_recovered,
     global_update_date, global_map_json, global_death_rate, global_recovery_rate)


def vaccination_data():
    '''df = pd.read_json("http")'''
    df = pd.read_csv("covid_data_set.csv")
    df_lka=df.LKA
    df_lka_data_days_str = df_lka[14].replace("'", '"')
    df_lka_data_days_str.replace(" ",'')

    df_lka_data_days_str='{"data":'+df_lka_data_days_str+"}"
    
    df_lka_data_days_data_dict = json.loads(df_lka_data_days_str)
    df_lka_data_days_data_dict['data']
    new_df=pd.DataFrame.from_dict(df_lka_data_days_data_dict['data'])
    vaccinated_data = new_df[['date','people_vaccinated','people_fully_vaccinated']]
    vaccinated_data.fillna(0, inplace=True)
    vaccinated_data=vaccinated_data[300:]

    vaccinated_chart_json=vaccinated_chart(vaccinated_data)

    return vaccinated_chart_json



def vaccinated_chart(data):     
   
    base = alt.Chart(data).mark_line().encode(
    x='date:T',
    y='people_vaccinated:Q',
   # color='symbol:O'
    )

    chart = alt.Chart(data).mark_bar().encode(
    x='date:T',
    y='people_fully_vaccinated:Q',).properties(
    width=400,
    height=250
)
    #y='people_fully_vaccinated:Q',
    #color='symbol:O')
    
    
    
    chart=chart+base
    chart_json = chart.to_json()
    #return chart_json
    return chart_json

