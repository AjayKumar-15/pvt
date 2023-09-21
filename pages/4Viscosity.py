import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
from PIL import Image
import os

#Dead Oil Viscosity
def uod_Beal():
    a=10**(0.43+8.33/api)
    uod=(0.32+1.8*10**7/api**4.53)*(360/(T+200))**a
    return uod

def uod_Beggs_Robinson():
    Z=3.0324-0.02023*api
    Y=10**Z
    X=Y*(T)**(-1.163)
    uod=10**X-1
    return uod

def uod_Glaso():
    a=10.313*(np.log10(T))-36.447
    uod=3.141*10**10*T**(-3.444)*(np.log10(api))**a
    return uod

#Saturated Oil Viscosity
def uob_Chew_Connally():
    c,d,e=8.62*10**(-5)*rs,1.1*10**(-3)*rs,3.74*10**(-3)*rs
    b=0.68/10**c+0.25/10**d+0.062/10**e
    a=rs*(2.2*10**(-7)*rs-7.4*10**(-4))
    uob=10**a*uod**b
    return uob

def uob_Beggs_Robinson():
    a=10.715*(rs+100)**(-0.515)
    b=5.44*(rs+150)**(-0.338)
    uob=a*uod**b
    return uob

#Undersaturated Oil Viscosity
def uo_Vasquez_Beggs(p):
    a=-3.9*10**(-5)*p-5
    m=2.6*p**1.187*10**a
    uo=uob*(p/pb)**m
    return uo

#graph parameters
def graph(x,y):
    """fig = make_subplots()

    fig.add_trace(go.Scatter(
            x=x,
            y=y,
            name="Bo vs P"
           ))"""
    fig = px.line( x=x, y=y)
    fig.update_layout(
    plot_bgcolor='white'
    )
    fig.update_xaxes(
    title="Pressure(psia)",
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='white',
    gridcolor='lightgrey'
    )
    fig.update_yaxes(
    title="uo (cp)",
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='white',
    gridcolor='lightgrey'
    )

    #fig.show()
    #fig.update_xaxes(minor=dict(ticks="inside", ticklen=6, showgrid=True))
    return st.write(fig)


@st.cache_data
def load_data_csv(url):
    data=pd.read_csv(url)
    return data

@st.cache_data
def load_data_excel(url):
    data=pd.read_excel(url)
    return data


st.title("Viscosity of oil")
st.markdown('---')
st.write('''viscosity of oil is calculated above or below bubble point by different correlations.

''')

path = os.path.dirname(__file__)
st.image(path+"/oil_viscosity.png",caption='Viscosity of oil')
st.markdown('---')
st.subheader('Input Data') 
col1,col2,col3=st.columns(3)   

with col1:
    pi=st.number_input('Reservoir Pressure(psia) ',value=5000)
    T=st.number_input('Temperature(°F) ',value=250)
    pb=st.number_input('Bubble point pressure(psia) ',value=2377)

with col2:
    rs=st.number_input('Gas solublity(scf/STB) ',value=751)
    #e_Bo=st.number_input('Experimental_Bo(bbl/STB)',value=1.528)
    #rho_o=st.number_input('Density of oil(lb/ft^3)',value=38.13)
    #co=st.number_input('compressibility at p>pb',value=38.13)
    #p_sep=st.number_input('Seperator Pressure(psig)',value=150)
    #t_sep=st.number_input('Separator Temperature(°F)',value=60)
    api=st.number_input('API',value=47.1)
    #yg=st.number_input('specific gas gravity of the solution gas',value=0.851)

st.header("Calculation of viscosity of Dead Oil")

st.markdown("Calculation of viscosity of Dead Oil by different correlations")   
select=st.multiselect('Calcultion of uod(Dead Oil Viscosity) by ', ["Beal","Beggs-Robinson",'Glaso'])
if 'Beal' in select or len(select)==0:
    st.subheader('Beal Correlation')
    uod=uod_Beal()
    st.write(uod)

if 'Beggs-Robinson' in select:
    st.subheader('Beggs-Robinson Correlation')
    uod=uod_Beggs_Robinson()
    st.write(uod)

if 'Glaso' in select:
    st.subheader("Glaso Correlation")
    uod=uod_Glaso()
    st.write(uod)


st.header("Estimation of oil Viscosity till bubble point")
st.markdown("Upload :green[Excel or csv] file only file consists of pressure(psia) and Gas Solubility(Rs) of one reservoir")
ext=st.radio("choose your file type",
                 ["csv","excel"])
uploaded_file=st.file_uploader("Choose a file")

if uploaded_file is not None:
        file=uploaded_file
        if ext=="csv":df=load_data_csv(file)
        else:df=load_data_excel(file)
        #Bo is calculated for pressure below bubble point(p<=pb)
        col=df.columns
        col1=col[0]
        col2=col[1]
        df=df[df[col1]<=pb]
        if st.checkbox("Show Raw Data",False):
            st.subheader("Raw Data")
            st.write(df)
        rs=df[col2]
else:
    file=None
    st.markdown("**Default test data is provided for understanding and you can change in input parameters in side bar")

st.header("Calculation of Saturated Oil Viscosity")
st.markdown("Calculation of Saturated Oil viscosity by different correlations")   
select2=st.multiselect('Calcultion of uob(viscosity at buubble point) by ', ["Chew-Connally","Beggs-Robinson"])

if "Chew-Connally" in select2 or len(select2)==0:
    st.subheader("Chew-Connally Correlation ")
    uo_lst=uob_Chew_Connally()
    st.write()
    if file:
        df["uo_chew_connally"]=uo_lst
        st.write(df)
        graph(df[col1],df["uo_chew_connally"])
        uob=df[df.columns[-1]].iat[-1]
    else:st.write(uo_lst);uob=uo_lst

if "Beggs-Robinson" in select2:
    st.subheader("Beggs-Robinson Correlation ")
    uo_lst=uob_Beggs_Robinson()
    st.write()
    if file:
        df["uo_Beggs-Robinson"]=uo_lst
        st.write(df)
        graph(df[col1],df["uo_Beggs-Robinson"])
        uob=df[df.columns[-1]].iat[-1]
    else:st.write(uo_lst);uob=uo_lst

st.header("Calculation of Viscosity of Undersatured oil by Vasquez-Beggs Correlation")
st.subheader("Vaquez-Beggs Correlation")
p=np.arange(pb,pi)
data=pd.DataFrame({"Pressure(psia)":p})

st.markdown(f""""
            * Viscosity of oil at bubble point": {uob}
            """)
uo_lst=uo_Vasquez_Beggs(p)
data["uo_p>pb"]=uo_lst
st.write(data)
graph(p,uo_lst)

st.markdown("Graph for Viscosity(cp) vs pressure(psia) for entire range of pressure")
#st.markdown("You must :red[upload excel files] for graph below bubble point")
st.markdown("You must select :red[only one correlation] for below and above bubble point pressure")

if file is not None:
    df_new=df.drop((df.columns)[1],axis=1)
    df_new.rename(columns={(df_new.columns)[1]:'uo'},inplace=True)
    data.rename(columns={(data.columns)[1]:'uo'},inplace=True)
    #st.write(df_new.columns)
    #st.write(data.columns)
    total_df=pd.concat([df_new,data],axis=0)
    st.write(total_df)
    graph(total_df["Pressure(psia)"],total_df["uo"])
else:st.markdown("You must :red[upload excel files] for graph below bubble point")





    

