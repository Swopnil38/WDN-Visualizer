import datetime
from turtle import title
import pandas as pd
import streamlit as st
import nepali_datetime
import streamlit.components.v1 as component
from nepali_date import NepaliDate

from read_sheet import bar_event, caste_bar, event_number, selected_date


st.set_page_config(page_title = "Wedding Dreams Nepal",layout="wide")

#st.date_input("TRY",nepali_datetime.date(2078, 1, 1))
#st.markdown("<iframe src="https://www.hamropatro.com/widgets/calender-small.php" frameborder="0" scrolling="no" marginwidth="0" marginheight="0" allowtransparency="true" title="Calender"></iframe>",unsafe_allow_html=True)
col1,col2,col3 = st.columns([5,2,2])
count = 0
with col3:
    component.iframe("https://www.hamropatro.com/widgets/calender-medium.php",320,360,False)
with col2:
    starter = st.date_input("Starting Date",datetime.date(2022,5,5),key = count)
    count = count+1
    nepali_starter = NepaliDate.to_nepali_date(starter)
    nepali_starter = str(nepali_starter)
    yr1 = int(nepali_starter[3:7])
    mo1 = int(nepali_starter[8:10])
    dy1 = int(nepali_starter[11:13])
    st.write()
    st.write(nepali_datetime.date(yr1,mo1,dy1).strftime('%K-%n-%D (%G)'))
    st.write()
    st.write()

    ender = st.date_input("Ending Date",datetime.date(2022,6,5),key = count)
    count = count +1
    nepali_ender = NepaliDate.to_nepali_date(ender)
    nepali_ender = str(nepali_ender)
    yr2 = int(nepali_ender[3:7])
    mo2 = int(nepali_ender[8:10])
    dy2 = int(nepali_ender[11:13])
    st.write()
    st.write(nepali_datetime.date(yr2,mo2,dy2).strftime('%K-%n-%D (%G)'))
    st.write()
    st.write()
with col1:
    st.write("Upcoming Frames")
    
st_yr = starter.year
st_mo = starter.month
st_date = starter.day
ed_yr = ender.year
ed_mo = ender.month
ed_date = ender.day
event_counter_df,client_details = selected_date(yr1,mo1,dy1,yr2,mo2,dy2)
print(client_details)
event_number(client_details)
caste_bar(client_details)
    
bar_event(event_counter_df,yr1,mo1,dy1,yr2,mo2,dy2)