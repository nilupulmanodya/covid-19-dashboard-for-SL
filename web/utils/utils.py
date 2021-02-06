import pandas as pd
from .altairplt import pcrtestbarchart



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
    
