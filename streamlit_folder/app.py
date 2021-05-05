import streamlit as st
import pandas as pd 
import matplotlib.pyplot as plt 
import plotly.graph_objects as go 
import plotly.express as px 
import seaborn as sns
import numpy as np


st.title('Life Expectancy vs GNI per capita')


@st.cache 
def upload():
     
    df_life = pd.read_csv("data/life_expectancy_years.csv")
    df_percapita = pd.read_csv("data/ny_gnp_pcap_pp_cd.csv")
    df_pop = pd.read_csv("data/population_total.csv")
    

    df_life.backfill(inplace=True)
    df_life.ffill(inplace=True)
    df_life_tidy = pd.melt(df_life, ["country"], var_name="year", value_name="life expectancy")


    df_percapita.backfill(inplace=True)
    df_percapita.ffill(inplace=True)
    df_percapita_tidy = pd.melt(df_percapita, ["country"], var_name="year", value_name="GNI per capita")


    df_pop.backfill(inplace=True)
    df_pop.ffill(inplace=True)
    df_pop_tidy = pd.melt(df_pop, ["country"], var_name="year", value_name="population")

    merged_df = pd.merge(pd.merge(df_life_tidy, df_percapita_tidy, how= 'left', on=['country', 'year']), df_pop_tidy, how= 'left', on=['country', 'year'])

    return merged_df

merged_df = upload()
countries = st.sidebar.multiselect('Select Countries', merged_df.country.unique())

sdf = merged_df.loc[lambda d: d['country'].isin(countries)]


year = st.sidebar.slider('year', min_value = 1990, max_value= 2019)
year = str(year)

sdf = sdf.loc[sdf['year'] == year]



fig = px.scatter(sdf, x= 'GNI per capita', y='life expectancy', color = 'country', size= 'population', log_x= True, size_max= 60)
st.plotly_chart(fig)