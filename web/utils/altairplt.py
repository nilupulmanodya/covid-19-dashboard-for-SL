import altair as alt
from vega_datasets import data

#local pcr test chart
def pcrtestbarchart(data):     
   
    chart = alt.Chart(data).mark_bar().encode(
        x='date_pcr',
        y='count_pcr',
    )
    chart_json = chart.to_json()
    return chart_json



#global covid map
def global_covid_map(cc_m):
    world_source = cc_m

    source = alt.topo_feature(data.world_110m.url, "countries")
    background = alt.Chart(source).mark_geoshape(fill="white")

    foreground = (
        alt.Chart(source)
        .mark_geoshape(stroke="black", strokeWidth=0.15)
        .encode(
            color=alt.Color(
                "TotalConfirmed:N", scale=alt.Scale(scheme="redpurple"), legend=None,
            ),
            tooltip=[
                alt.Tooltip("Country:N", title="Country"),
                alt.Tooltip("TotalConfirmed:Q", title="confirmed cases"),
            ],
        
        ).transform_lookup(
            lookup="id",
            from_=alt.LookupData(world_source, "id", ["TotalConfirmed", "Country"]),
        )
    )

    final_map = (
        (background + foreground)
        .configure_view(strokeWidth=0)
        .properties(width=700, height=400)
        .project("naturalEarth1")
    )
    final_map_json = final_map.to_json()
    return final_map_json
