import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px


st.set_page_config(
    page_title="Bubble Point",
    layout="centered",
    initial_sidebar_state="expanded",
)

### Bubble point estimator using correlations

st.title('Bubble point calculation using Correlations')
st.markdown('---')

st.write('''The bubble-point pressure pb of a hydrocarbon system is defined as the
highest pressure at which a bubble of gas is first liberated from the oil.
This important property can be measured experimentally for a crude oil
system by conducting a constant-composition expansion test.
In the absence of the experimentally measured bubble-point pressure, it
is necessary for the engineer to make an estimate of this crude oil property
from the readily available measured producing parameters. Several graphical and mathematical correlations for determining pb have been proposed
during the last four decades. These correlations are essentially based on
the assumption that the bubble-point pressure is a strong function of gas
solubility Rs, gas gravity gg, oil gravity API, and temperature T.

''')
st.markdown('---')
st.subheader('Input data')
column1,column2,column3=st.columns(3)

with column1:
    API=st.number_input('API Gravity of the oil',min_value=10.0,max_value=60.0,value=47.1)
with column2:
    Yg=st.number_input('Gas specific gravity',min_value=0.0,max_value=1.0,value=0.851)
    Psep=st.number_input('Separator Pressure(psig)',min_value=14,max_value=1000,value=150)
    Psep=Psep+14.7
with column3:
    Tsep=st.number_input('Separator Temperature(F)',min_value=10,max_value=400,value=60)
    T=st.number_input('Reservoir Temperature(F)',min_value=50,max_value=400,value=250)
    T=T+460
    Tsep=Tsep+460
st.markdown('---')
st.subheader('Selection of Correlation')
choice_Pb=st.selectbox('Choose the correlation to be used for Bubble point calculation',('Standings Correlation','Vasequez-Beggs Correlation','Marhouns Correlation','Petrosky-Farshad Correlation'))

Pb_standing_lst=[]
Pb_beggs_lst=[]
Pb_marhouns_lst=[]
Pb_petrosky_lst=[]
###--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def Pb_standing():

    a=0.00091*(T-460)-0.0125*API
        
    Pb=18.2*(pow(((df['Rs(scf/STB)'])/Yg),0.83)*pow(10,a)-1.4)
    Pb_standing_lst.append(Pb)

def Pb_beggs():

    C1,C2,C3=0,0,0
    if API<30:
        C1=27.624
        C2=0.914328
        C3=11.172
    else:
        C1=56.18
        C2=0.84246
        C3=10.393
    
    a=-C3*API/T

    Ygs=Yg*(1+5.912*pow(10,-5)*API*(Tsep-460)*(np.log10((Psep+14.7)/114.7)))

    Pb=((C1*df['Rs(scf/STB)']/Ygs)*pow(10,a))**C2
    Pb_beggs_lst.append(Pb)

def Pb_marhouns():

    a=5.38088*pow(10,-3)
    b=0.715082
    c=-1.87784
    d=3.1437
    e=1.32657

    Yo =(141.5)/(131.5+API) 

    Pb=a*pow(df['Rs(scf/STB)'],b)*pow(Yg,c)*pow(Yo,d)*pow(T,e)
    Pb_marhouns_lst.append(Pb)

def Pb_petrosky():

    x=7.916*pow(10,-4)*pow(API,1.5410)-4.561*pow(10,-5)*pow((T-460),1.3911)

    Pb= (112.727*pow(df['Rs(scf/STB)'],0.577421)/(pow(Yg,0.8439)*pow(10,x)))-1391.051
    Pb_petrosky_lst.append(Pb)

def graph(x,y):
    
    fig = px.line( x=x, y=y)
    fig.update_layout(
    plot_bgcolor='white'
    )
    fig.update_xaxes(
    title="Pb(psia)",
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='white',
    gridcolor='lightgrey'
    )
    fig.update_yaxes(
    title="Rs(scf/STB)",
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='white',
    gridcolor='lightgrey'
    )
    return st.write(fig)

def file_option():
    st.subheader('Upload Rs data')
    ext=st.radio('Choose the file type: CSV or Excel',['csv','Excel'])

##----------------------------------------------------------------------------------------------------

if choice_Pb=='Standings Correlation':

    st.subheader('Documentation')
    with st.expander('Read Standing correlation Documentation'):
        st.header('Standing\'s Correlation')
        st.write('''Based on 105 experimentally measured bubble-point pressures on 22
hydrocarbon systems from California oil fields, Standing (1947) proposed a graphical correlation for determining the bubble-point pressure
of crude oil systems. The correlating parameters in the proposed correlation are the gas solubility Rs, gas gravity gg, oil API gravity, and the system temperature. The reported average error is 4.8%.

''')
        
    
    file_option()
    
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        
        # Can be used wherever a "file-like" object is accepted:
        
        df = pd.read_csv(uploaded_file)
        st.write(df)
        Pb_standing()
        

        st.subheader('Pb Vs Rs Plot - Standing Correlation')
        graph(df['Rs(scf/STB)'],Pb_standing_lst)
       
elif choice_Pb=='Vasequez-Beggs Correlation':

    st.subheader('Documentation')
    with st.expander('Read Vasequez-Beggs Correlation Documentation'):
        st.header('Vasequez-Beggs Correlation')
        st.write('Vasquez and Beggs gas solubility correlation is presented by Equation below:')
    
 
    
    file_option()
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        
        # Can be used wherever a "file-like" object is accepted:
        
        df = pd.read_csv(uploaded_file)
        st.write(df)

        Pb_beggs()
        st.subheader('Pb Vs Rs Plot - Marhouns Correlation')
        graph(df['Rs(scf/STB)'],Pb_beggs_lst)


elif choice_Pb=='Marhouns Correlation':

    st.subheader('Documentation')
    with st.expander('Read Marhouns Correlation Documentation'):
        st.header('Marhouns Correlation')
        st.write('''Marhoun (1988) used 160 experimentally determined bubble-point
pressures from the PVT analysis of 69 Middle Eastern hydrocarbon mixtures to develop a correlation for estimating pb. The author correlated the
bubble-point pressure with the gas solubility Rs, temperature T, and specific gravity of the oil and the gas.

''')
    
 
    file_option()
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        
        # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file)
        st.write(df)
    
        Pb_marhouns()

        st.subheader('Pb Vs Rs Plot - Marhouns Correlation')
        graph(df['Rs(scf/STB)'],Pb_marhouns_lst)

elif choice_Pb=='Petrosky-Farshad Correlation':

    st.subheader('Documentation')
    with st.expander('Read Petrosky-Farshad Correlation Documentation'):
        st.header('Petrosky-Farshad Correlation')
        st.write('Petrosky-Farshad gas solubility correlation is presented by Equation below:')
    
 
    file_option()
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        
        # Can be used wherever a "file-like" object is accepted:
        df = pd.read_csv(uploaded_file)
        st.write(df)

        Pb_petrosky()

        st.subheader('Pb Vs Rs Plot - Petrosky Farshad Correlation')
        
        graph(df['Rs(scf/STB)'],Pb_petrosky_lst)

