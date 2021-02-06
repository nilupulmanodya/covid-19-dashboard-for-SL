import altair as alt

def pcrtestbarchart(data):     
   
    chart = alt.Chart(data).mark_bar().encode(
        x='date_pcr',
        y='count_pcr',
    )
    chart_json = chart.to_json()
    return chart_json

