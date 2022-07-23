from ast import While, operator
from json import load
from numpy import NaN, sin
import streamlit as st 
import pandas as pd

from gspread_pandas import Spread,Client
from google.oauth2 import service_account


import matplotlib.pyplot as plt
import numpy as np


from datetime import datetime

# Disable certificate verification (Not necessary always)
import ssl

from visualization import line_chart, pie
ssl._create_default_https_context = ssl._create_unverified_context

# Create a Google Authentication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)
client = Client(scope=scope,creds=credentials)

total_event_achieved = []
event_date = []
    

# Functions 
@st.cache()

# Get the sheet as dataframe
def load_the_spreadsheet(yr,mo,st_date,ed_date):
    try:
        spreadsheetname = "{} {} Details".format(yr,mo)
        print(yr,mo,st_date,ed_date)
        sh = client.open(spreadsheetname)
        spreadsheetname = 'Client Details'
        worksheet = sh.worksheet(spreadsheetname)
        worksheet_val  = worksheet.get_all_records()
        
        main = []
        for i in worksheet_val:
            empty = dict()
            for key,value in i.items():
                if key == "Client Name" or key == "Event Name " or key == "Event Date " or key == "Package Amount":
                    if key == "Event Date " and type(value)==str:
                        empty[key] = NaN
                    else:
                        empty[key] = value
            main.append(empty)
        
                
        df = pd.DataFrame.from_dict(main)
        df2 = df.dropna()
        df2['Event Date '] = df2['Event Date '].astype(int)

        
        df['Package Amount'] = df['Package Amount'].astype(str).str.replace(r'\D', '')
        df2 =df2.loc[df['Event Date ']>st_date]
        df2 =df2.loc[df['Event Date ']<ed_date]
        df3 = df2.loc[df['Event Name ']=="Wedding"]
        months_dict = {1:"Baishakh",2:"Jestha",3:"Asar",4:"Shrawan",5:"Bhadra",6:"Ashwin",7:"Kartik",8:"Mangshir",9:"Poush",10:"Magh",11:"Falgun",12:"Chaitra"}
        print(mo)
        for keyss,valuess in months_dict.items():
            print(mo)
            if valuess == mo:
                df3['Months'] = keyss
            
        df3['Year_Event'] = yr
        
        


        print("Here")
        print(yr)
        print("Done")
        return df2,df3
        #st.dataframe(df)
    except:
        df2 = pd.DataFrame()
        df3 = pd.DataFrame()
        return df2,df3
        
def selected_date(start_yr,start_mo,start_date,end_yr,end_mo,end_date):
    event_count_df = pd.DataFrame()
    client_details = pd.DataFrame()
    if start_yr != end_yr or start_mo!= end_mo:
        months_dict = {1:"Baishakh",2:"Jestha",3:"Asar",4:"Shrawan",5:"Bhadra",6:"Ashwin",7:"Kartik",8:"Mangshir",9:"Poush",10:"Magh",11:"Falgun",12:"Chaitra"}
        year = []
        mo = []
        if start_yr == end_yr:
            for i in range((end_mo+1-start_mo)):
                mon = start_mo + i

                for j,k in months_dict.items():
                    if j == mon:
                        year.append(start_yr)
                        mo.append(k)
            
            print(mo)           
            for j,k in months_dict.items():
                if j == start_mo:
                    start_mon_num = k
                if j == end_mo:
                    end_mon_num = k
            for z in mo:              
                if z == start_mon_num:
                    now_df,df3 = load_the_spreadsheet(start_yr,z,start_date,40)
                    client_details = pd.concat([client_details,now_df])
                    event_count_df = pd.concat([event_count_df,df3])
                    
                elif z == end_mon_num:
                    now_df,df3 = load_the_spreadsheet(start_yr,z,0,end_date)
                    client_details = pd.concat([client_details,now_df])
                    event_count_df = pd.concat([event_count_df,df3])
                else:
                    now_df,df3 = load_the_spreadsheet(start_yr,z,0,40)
                    client_details = pd.concat([client_details,now_df])
                    event_count_df = pd.concat([event_count_df,df3])
            print(event_count_df)
            return event_count_df,client_details
                    
                    
            
        else:
            for i in range((end_yr+1-start_yr)):
                yr = start_yr+i
                print(yr)
                
                if yr == start_yr:
                    for i in range((13-start_mo)):
                        mon = start_mo + i
                        for j,k in months_dict.items():
                            if j == mon:
                                year.append(yr)
                                mo.append(k)
                elif yr == end_yr:
                    for i in range((end_mo-0)):
                        mon = 1 + i
                        print(mon)
                        for j,k in months_dict.items():
                            if j == mon:
                                year.append(yr)
                                mo.append(k)
                else:
                    for i in range(12):
                        mon = i+1
                        for j,k in months_dict.items():
                            if j == mon:
                                year.append(yr)
                                mo.append(k)
            
            for j,k in months_dict.items():
                if j == start_mo:
                    start_mon_num = k
                if j == end_mo:
                    end_mon_num = k
            
            for z,x in zip(mo,year):              
                if z == start_mon_num and x == year[0] :
                    now_df,df3 = load_the_spreadsheet(x,z,start_date,40)
                    client_details = pd.concat([client_details,now_df])
                    event_count_df = pd.concat([event_count_df,df3])
                    
                elif z == end_mon_num and x == year[len(year)]:
                    now_df,df3 = load_the_spreadsheet(x,z,0,end_date)
                    client_details = pd.concat([client_details,now_df])
                    event_count_df = pd.concat([event_count_df,df3])
                else:
                    now_df,df3 = load_the_spreadsheet(x,z,0,40)
                    client_details = pd.concat([client_details,now_df])
                    event_count_df = pd.concat([event_count_df,df3])
            
            return event_count_df,client_details
             
    else:
        
        client_details,df3 = load_the_spreadsheet(start_yr,start_mo,start_date,end_date)
        event_count_df = pd.concat([event_count_df,df3])
        return event_count_df,client_details    

#client_details = selected_date(2079,1,1,2079,2,20)

combo = ['&']
def event_number(client_details):
    print(client_details)
    print(type(client_details))
    event_name = []
    event_count = []


    event_list = []
    for k in client_details['Event Name ']:
        event_list.append(k)
    for i in event_list:
        if i not in event_name:
            event_name.append(i)
    print(event_list)
    print(event_name)
    for i in range(len(event_name)):
        events = event_name[i]
        count = 0
        for i in event_list:
            if i == events:
                count += 1
        event_count.append(count)

    st.title("")
    st.title("")
    st.subheader("Detailed Bar Chart of Event Name with Numbers")
    
    st.title("")
    st.title("")
    
    fig = line_chart(event_name,event_count)
    st.pyplot(fig)

def caste_bar(client_details):
    castes = []
    client_detail = []
    for i in client_details['Client Name']:
        if i != "":
            client_detail.append(i)
    for i in client_detail:
        count = 0
        for j in i:
            count += 1
            if j in combo:
                Names = [i[:count-1],i[count+1:]]
                break
        else:
            Names = [i]
        for j in Names:
            caste = j.split(" ")
            if len(caste)>2:
                caste.remove('')
            
            caste.pop(0)
            for x in caste:
                castes.append(x)
    print(castes)

    caste_df = pd.ExcelFile('castes.xlsx')
    view = pd.read_excel(caste_df,'Sheet2')


    caste_list = []

    for k in castes:
        for i,j in zip(view['Surname'],view['Caste']):
            if k == i:
                caste_list.append(j)
    castes = []
    for i in caste_list:
        if i not in castes:
            castes.append(i)
    values = []
    for j in range(len(castes)):
        cast = castes[j]
        count = 0
        for k in caste_list:
            if k == cast:
                count += 1
        values.append(count)

    
    st.title("")
    st.title("")
    st.subheader("Detailed Bar Chart of Caste with Person")
    
    st.title("")
    st.title("")
    fig = line_chart(castes,values)
    st.pyplot(fig)

def bar_event(event_count_df,yr1,mo1,dy1,yr2,mo2,dy2):
    print("EVENTS CHECK")
    print(event_count_df)
    print("CHECKED COMPLETED")
    evnt_date = []
    evnt_achieve = []
    lagans_df  = pd.ExcelFile('lagan.xlsx')
    df2 = pd.read_excel(lagans_df,'Marriage')
    marriage_date = df2.loc[(df2['Year']>=yr1) & (df2['Months']>=mo1)]
    for index, row in marriage_date.iterrows():
        if row['Months'] <= mo1 and row['Day'] < dy1:
            marriage_date.drop(index, inplace=True)
            
    print(marriage_date)
    marriage_date = marriage_date.loc[(marriage_date['Year']<=yr2) & (marriage_date['Months']<=mo2)]
    for index, row in marriage_date.iterrows():
        if row['Months'] >= mo2 and row['Day'] > dy2:
            marriage_date.drop(index, inplace=True)
            
    
    
    print(marriage_date)
    bartabanda_date = pd.read_excel(lagans_df,'Bartabandha')
    for i,j,k in zip(marriage_date['Day'],marriage_date['Months'],marriage_date['Year']):
        counterrr = 0
        for m,n,b in zip(event_count_df['Event Date '],event_count_df['Months'],event_count_df['Year_Event']):
            if i == m and j == n and k == b:
                counterrr += 1
        combined_month_Date = str(i)+"/"+str(j)
        evnt_date.append(combined_month_Date)
        evnt_achieve.append(counterrr)
        
                

    print(evnt_date)
    print(evnt_achieve)
    st.title("")
    st.title("")
    st.subheader("Detailed Chart of Wedding Event Achieved with Lagan Date")
    
    st.title("")
    st.title("")
    fig = plt.figure(figsize=(12,6))
    y_pos = np.arange(len(evnt_date))
    plt.bar(y_pos, evnt_achieve, align='center', alpha=0.5)
    plt.xticks(y_pos, evnt_date)
    st.pyplot(fig)