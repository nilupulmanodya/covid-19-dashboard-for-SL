import pandas as pd
from .altairplt import pcrtestbarchart, global_covid_map
from .clean_country_data import clean_country_data
import urllib3
from urllib3 import request# to handle certificate verification
import certifi# to manage json data
import json# for pandas dataframes
from pandas.io.json import json_normalize




def local_all_status():
    df_local = pd.read_json("https://hpb.health.gov.lk/api/get-current-statistical").data
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

    return (local_active_cases, local_deaths, local_recovered
    ,local_new_cases, local_total_cases, local_pcr_test_chart_json,update_date_time,
    local_death_rate, local_recovery_rate)
    

def global_all_status():
    http = urllib3.PoolManager(
       cert_reqs='CERT_REQUIRED',
       ca_certs=certifi.where())

    url = 'https://api.covid19api.com/summary' 
    r = http.request('GET', url)
    print("r global url status:", r.status)

    data = json.loads(r.data.decode('utf-8'))

    global_total_confirmed = global_total_confirmed = data['Global']['TotalConfirmed']
    global_today_new = data['Global']['NewConfirmed']
    global_total_deaths = data['Global']['TotalDeaths']
    global_total_recovered = data['Global']['TotalRecovered']
    global_update_date = data['Global']['Date']
    counties_df = pd.json_normalize(data,'Countries')

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

    return (global_total_confirmed, global_today_new, global_total_deaths, global_total_recovered,
     global_update_date, global_map_json, global_death_rate, global_recovery_rate)

