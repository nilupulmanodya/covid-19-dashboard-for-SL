from flask import Flask, render_template
import utils
from utils.utils import local_all_status, global_all_status

app = Flask(__name__)

@app.route('/')
def dashbord():
    #taking local data status

    local_hospital_details,local_active_cases, local_deaths, local_recovered,local_new_cases, local_total_cases, local_pcr_test_chart_json,update_date_time, local_death_rate, local_recovery_rate = local_all_status()
    global_total_confirmed, global_today_new, global_total_deaths, global_total_recovered, global_update_date, global_map_json, global_death_rate, global_recovery_rate = global_all_status()


    context = {'local_active_cases':local_active_cases, 'local_deaths':local_deaths, 'local_recovered':local_recovered,'local_new_cases':local_new_cases,
     'local_total_cases':local_total_cases, 'local_pcr_test_chart_json':local_pcr_test_chart_json, 'update_date_time':update_date_time,'local_death_rate':local_death_rate,
     'local_recovery_rate':local_recovery_rate,'global_total_confirmed':global_total_confirmed, 'global_today_new':global_today_new,
     'global_total_deaths':global_total_deaths, 'global_total_recovered':global_total_recovered, 'global_update_date':global_update_date,'global_map_json':global_map_json, 'global_death_rate':global_death_rate,
     'global_recovery_rate':global_recovery_rate}




    return render_template("main.html",context=context)


if __name__ == "__main__":
    app.run(debug=True)