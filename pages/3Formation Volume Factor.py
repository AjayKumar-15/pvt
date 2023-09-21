import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
from PIL import Image
import os


def Bo_Standing():
    yo=141.5/(api+131.5)
    bo=0.9759+0.000120*(rs*(yg/yo)**0.5+1.25*T)**1.2
    return bo
def Ygs():
    return yg*(1+5.912*10**(-5)*api*(t_sep)*np.log10((p_sep+14.7)/114.7))

def Bo_Vasquez_Beggs():
    ygs=Ygs()
    if api<=30:c1,c2,c3=4.677*10**(-4),1.751*10**(-5),-1.811*10**(-8)
    else:c1,c2,c3=4.670*10**(-4),1.100*10**(-5),1.337*10**(-9)
    bo=1.0+c1*rs+(T-60)*(api/ygs)*(c2+c3*rs)
    return bo

def Bo_Glaso():
    yo=141.5/(api+131.5)
    b_ob_star=rs*(yg/yo)**0.526+0.968*T
    a=-6.58511+2.91329*np.log10(b_ob_star)-0.27683*(np.log10(b_ob_star))**2
    bo=1+10**a
    return bo

def Bo_Marhoun():
    yo=141.5/(api+131.5)
    a,b,c=0.742390,0.323294,-1.202040
    F=rs**a*yg**b*yo**c
    bo=0.497069+0.862963*10**(-3)*(T+460)+0.182594*10**(-2)*F+0.318099*10**(-5)*F**2
    return bo

def Bo_Petrosky_Farshad():
    yo=141.5/(api+131.5)
    bo=1.0113+7.2046*10**(-5)*(rs**0.3738*(yg**0.2914/yo**0.6265)+0.24626*T**0.5371)**3.0936
    return bo

def Bo_MBE():
    yo=141.5/(api+131.5)
    bo=(62.4*yo+0.0136*rs*yg)/rho_o
    return bo

#Functions for calculations of compressibility at pressure above bubble point pressure
def Co_Vasquez_Beggs():
    ygs=Ygs()
    co=(-1433+5*rsb+17.2*T-1180*ygs+12.61*api)*10**(-5)*p
    return co

def Co_Petrosky_Farshad():
    co=1.705*10**(-7)*rsb**0.69357*yg**0.1885*api**0.3272*T**0.6729*p**(-0.5906)
    return co


#Functions for calculation after bubble point

def above_pb_Vasquez_Beggs():
    ygs=Ygs()
    A=10**(-5)*(-1433+5*rsb+17.2*T-1180*ygs+12.61*api)
    bo=bob*np.exp(-A*np.log(p/pb))
    return bo

def above_pb_Petrosky_Farshad():
    A=4.1646*10**(-7)*rsb**0.69357*yg**0.1885*api**0.3272*T**0.6729
    bo=bob*np.exp(-A*(p**0.4094-pb**0.4094))
    return bo
   
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
    title="Bo(rb/STB)",
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


st.set_page_config(page_title="Formation Volume Factor", layout="centered")


st.title("Formation Volume Factor")
st.markdown('---')
st.write('''The oil formation volume factor, Bo, is defined as the ratio of the volume of oil (plus the gas in solution) at the prevailing reservoir temperature and pressure to the volume of oil at standard conditions. Bo is always
greater than or equal to unity.

''')
path = os.path.dirname(__file__)
st.image(path+'/Bg plot.png',caption='Bg plot (Credit: Tarek Ahmed)')
st.markdown('---')
st.subheader('Input Data') 
col1,col2,col3= st.columns(3)

with col1:
    pi=st.number_input('Reservoir Pressure(psia) ',value=5000)
    T=st.number_input('Temperature(°F) ',value=250)
    pb=st.number_input('Bubble point pressure(psia) ',value=2377)
    rs=st.number_input('Gas solublity(scf/STB) ',value=751)
with col2:
    e_Bo=st.number_input('Experimental_Bo(bbl/STB)',value=1.528)
    rho_o=st.number_input('Density of oil(lb/ft^3)',value=38.13)
    co=st.number_input('compressibility at p>pb',value=38.13)
    p_sep=st.number_input('Seperator Pressure(psig)',value=150)
with col3:
    t_sep=st.number_input('Separator Temperature(°F)',value=60)
    api=st.number_input('API',value=47.1)
    yg=st.number_input('specific gas gravity of the solution gas',value=0.851)


st.markdown('---')
st.header("Estimation of Formation Volume Factor below Bubble Point")   
st.subheader('Selection of Correlation')

select=st.selectbox('Choose the Correlation: ', ['Standing','Vasquez-Beggs','Glaso','Marhoun','Petrosky-Farshad',"Material Balance Equation"])

st.subheader('File Upload')
st.markdown("Upload :green[Excel or csv] file consisting of pressure(psia) and Gas Solubility(Rs) columns of a reservoir")
ext=st.radio("Choose the file type",
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
    st.markdown(" :red[NOTE: Default test data has been used for understanding purposes but you can change the Input Parameters in the Input section]")



if 'Standing' in select or len(select)==0:
    st.subheader('Documentation')
    with st.expander('Read Standing\'s Correlation Documentation'):

        st.subheader('Standing\'s Correlation')
        st.write('''Standing (1947) presented a graphical correlation for estimating the oil
formation volume factor with the gas solubility, gas gravity, oil gravity,
and reservoir temperature as the correlating parameters. This graphical
correlation originated from examining a total of 105 experimental data
points on 22 different California hydrocarbon systems. An average error
of 1.2% was reported for the correlation.

''')

    bo_lst=Bo_Standing()
    st.write()
    if file:
        df["Bo_standing"]=bo_lst
        st.write(df)
        graph(df[col1],df["Bo_standing"])
        bob=df[df.columns[-1]].iat[-1]
    else:st.write(bo_lst);bob=bo_lst

if "Vasquez-Beggs" in select:
    st.subheader('Vasquez-Beggs')
    bo_lst=Bo_Vasquez_Beggs()
    if file:
        df["Bo_Vasquez_Beggs"]=bo_lst
        st.write(df)
        graph(df[col1],df["Bo_Vasquez_Beggs"])
        bob=df[df.columns[-1]].iat[-1]
    else:st.write(bo_lst);bob=bo_lst

if "Glaso" in select:
    st.subheader('Glaso')
    bo_lst=Bo_Glaso()
    if file:
        df["Bo_Glaso"]=bo_lst
        st.write(df)
        graph(df[col1],df["Bo_Glaso"])
        bob=df[df.columns[-1]].iat[-1]
    else:st.write(bo_lst);bob=bo_lst

if "Marhoun" in select:
    st.subheader('Marhoun')
    bo_lst=Bo_Marhoun()
    if file:
        df["Bo_Marhoun"]=bo_lst
        st.write(df)
        graph(df[col1],df["Bo_Marhoun"])
        bob=df[df.columns[-1]].iat[-1]
    else:st.write(bo_lst);bob=bo_lst

if "Petrosky-Farshad" in select:
    st.subheader('Petrosky-Farshad')
    bo_lst=Bo_Petrosky_Farshad()
    if file:
        df["Bo_Petrosky-Farshad"]=bo_lst
        st.write(df)
        graph(df[col1],df["Bo_Petrosky-Farshad"])
        bob=df[df.columns[-1]].iat[-1]
    else:st.write(bo_lst);bob=bo_lst

if "Material Balance Equation" in select:
    st.subheader('Material Balance Equation')
    bo_lst=Bo_MBE()
    if file:
        df["Bo_MBE"]=bo_lst
        st.write(df)
        graph(df[col1],df["Bo_MBE"])
        bob=df[df.columns[-1]].iat[-1]
    else:st.write(bo_lst);bob=bo_lst

st.header("Calculations of Formation Volume Factor after bubble point")
rsb=st.number_input("Enter the gas solubility at bubble point pressure")
p=np.arange(pb,pi)
data=pd.DataFrame({"Pressure(psia)":p})

st.markdown(f""""
            * Formation Volume Factor at bubble point": {bob}
            """)
options = st.multiselect(
    'choose one or many correlations',
    ['Vasquez-Beggs','Petrosky-Farshad']
    )
if 'Vasquez-Beggs'in options or len(options)==0:
    st.subheader('Vasquez-Beggs')
    bo_lst=above_pb_Vasquez_Beggs()
    data["Bo_p>pb"]=bo_lst
    st.write(data)
    graph(p,bo_lst)
if 'Petrosky-Farshad' in options:
    st.subheader('Petrosky-Farshad')
    bo_lst=above_pb_Petrosky_Farshad()
    data["Bo_p>pb"]=bo_lst
    st.write(data)
    graph(p,bo_lst)

st.markdown("Graph for Bo(rb/STB) vs pressure(psia) for entire range of pressure")
#st.markdown("You must :red[upload excel files] for graph below bubble point")
st.markdown("You must select :red[only one correlation] for below and above bubble point pressure")

if file is not None:
    df_new=df.drop((df.columns)[1],axis=1)
    df_new.rename(columns={(df_new.columns)[1]:'Bo'},inplace=True)
    data.rename(columns={(data.columns)[1]:'Bo'},inplace=True)
    #st.write(df_new.columns)
    #st.write(data.columns)
    total_df=pd.concat([df_new,data],axis=0)
    st.write(total_df)
    graph(total_df["Pressure(psia)"],total_df["Bo"])
else:st.markdown("You must :red[upload excel files] for graph below bubble point")









