import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

st.set_page_config(
    page_title="Gas Solubility",
    layout="centered",
    initial_sidebar_state="expanded",
)


## creating the header of the calculator that shows the basic info ----------------------------------------------------------------------------------
st.title('Gas Solubility Calculator using Correlations')
st.markdown("---")
st.write("""
         The gas solubility Rs is defined as the number of standard cubic feet of
gas which will dissolve in one stock-tank barrel of crude oil at certain pressure and temperature. The solubility of a natural gas in a crude oil is a
strong function of the pressure, temperature, API gravity, and gas gravity.
         """)
path = os.path.dirname(__file__)
st.image(path+"/Rs plot.png",caption='Gas Solubility plot(Credit: Tarek Ahmed)')
st.markdown('---')


## This section takes user input on the selection of the correlation -------------------------------------------------------------------------------
st.subheader('Input data')


column1,column2,column3=st.columns(3)

with column1:
    Pr=st.number_input('Reservoir Pressure(psia)',min_value=500,max_value=12000,value=8000)
    Pb=st.number_input('Bubble Point Pressure(psig)',min_value=100,max_value=10000,value=2377)
    API=st.number_input('API Gravity of the oil',min_value=10.0,max_value=60.0,value=47.1)
with column2:
    Yg=st.number_input('Gas specific gravity',min_value=0.0,max_value=1.0,value=0.851)
    Psep=st.number_input('Separator Pressure(psig)',min_value=14,max_value=1000,value=150)
with column3:
    Tsep=st.number_input('Separator Temperature(F)',min_value=10,max_value=400,value=60)
    T=st.number_input('Reservoir Temperature(F)',min_value=50,max_value=400,value=250)
st.markdown('---')
st.subheader('Select the Correlation')

## takes choice of the user
correlation_choice=st.selectbox('Choose the correlation for Rs calculation',('Standings Correlation','Vasequez-Beggs Correlation','Marhouns Correlation','Petrosky-Farshad Correlation'),)

T=T+460
Tsep=Tsep+460
Pb=Pb+14.7
Rs_standing_lst=[]
Rs_beggs_lst=[]
Rs_Marhouns_lst=[]
Rs_petrosky_lst=[]
p=np.arange(500,Pr,1)

###--------------------------------------------------------------------------------------------------------------------------------------------------------------------
## defining the standing function
def Rs_standing():

        ## creating the 'x' using the input parameters
        x=0.0125*API-0.00091*(T-460)

    
        ## creating the 'Rs' function using the conditions of the Standing for below and above bubble point

        for pressure in p:

            if pressure<Pb:
                Rs=Yg*(((pressure/18.2+1.4)*10**x)**1.2048)
                Rs_standing_lst.append(Rs)

            else:
                Rs=Yg*(((Pb/18.2+1.4)*10**x)**1.2048)
                Rs_standing_lst.append(Rs)
            
    
## ---------------------------------------------------------------------------------------------------------------------------------------------------------------

def Rs_beggs():


        ## Calculation of the adjusted gas gravity at 100 psig

        Ygs=Yg*(1+5.912*pow(10,-5)*API*(Tsep-460)*(np.log10((Psep+14.7)/114.7)))
        

        C1,C2,C3= 0,0,0

        if API<30:
            C1=0.0362
            C2=1.0937
            C3=25.7240
        else:
            C1=0.0178
            C2=1.1870
            C3=23.931

        ## creating the Rs function    

        for pressure in p:

            if pressure<Pb:
                Rs=C1*Ygs*(pressure**C2)*np.exp(C3*(API/T))
                Rs_beggs_lst.append(Rs)

            else:
                Rs=C1*Ygs*(Pb**C2)*np.exp(C3*(API/T))
                Rs_beggs_lst.append(Rs)

###-----------------------------------------------------------------------------------------------------------------------------------------------------------------
def Rs_Marhouns():
            
        Yo =(141.5)/(131.5+API)
        
        a=185.843208; b=1.877840; c=-3.1437; d=-1.3265; e=1.398441
        
        for pressure in p:
            if pressure<Pb:
                Rs=(a*pow(Yg,b)*pow(Yo,c)*pow(T,d)*pressure)**e
                Rs_Marhouns_lst.append(Rs)
            else:
                Rs=(a*pow(Yg,b)*pow(Yo,c)*pow(T,d)*Pb)**e
                Rs_Marhouns_lst.append(Rs)

##-----------------------------------------------------------------------------------------------------------------------------------------------------------------

## creating the Petrosky farshad correlation
def Rs_Petrosky_farshad():
        
        x=7.916*pow(10,-4)*pow(API,1.5410)-4.561*pow(10,-5)*pow((T-460),1.3911)
        
        for pressure in p:
                
            if pressure<Pb:
                Rs=((pressure/112.727+12.340)*pow(Yg,0.8439)*pow(10,x))**1.73184
                Rs_petrosky_lst.append(Rs)

            else:
                Rs=((Pb/112.727+12.340)*pow(Yg,0.8439)*pow(10,x))**1.73184
                Rs_petrosky_lst.append(Rs)

###--------------------------------------------------------------------------------------------------------------------------------------------------------- 
def graph(x,y):
    
    fig = px.line( x=x, y=y)
    fig.update_layout( plot_bgcolor='white',title_text=correlation_choice)
    fig.update_xaxes(
    title="Pressure(psia)",
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='white',
    gridcolor='lightgrey'
    )
    fig.update_yaxes(
    title="Rs(scf/STB))",
    mirror=True,
    ticks='outside',
    showline=True,
    linecolor='white',
    gridcolor='lightgrey'
    )
    
    return st.write(fig)

### ------------------------------------------------------------------------------------------------------

def tab(Rs_lst):

    tab1,tab2=st.tabs(['🗃 Show Complete Data','Rs at Bubble Point'])

    with tab1:

        col1,col2=st.columns(2)
        with col1:
            st.write('This tab shows the complete data generated for Rs')
            df=pd.DataFrame({'Pressure(psia)':p,'Rs(scf/STB)':Rs_lst},)
            
            st.dataframe(data=df)

        with col2:
            @st.cache_data
            def convert_df(df):
                return df.to_csv().encode('utf-8')
            csv=convert_df(df)

            st.download_button(
                label='Download P vs Rs data as CSV',
                data=csv,
                file_name=correlation_choice+'_data.csv',
                mime='text/csv'
            )

    with tab2:
        st.write('This tab shows the Rs at Bubble Point Pressure')

        df_comparison.loc[0,'Correlation']=correlation_choice
        df_comparison.loc[0,'Bubble point pressure(psig)']=Pb-14.7
        df_comparison.loc[0,'Rs(scf/STB)']=Rs_lst[-1]
        
        st.dataframe(df_comparison,hide_index=True)

###--------------------------------------------------------------------------------------------------------------------------
    
## creating a table that will show the Rs value at Bubble point pressure calculated when a particular correlation is selected
df_comparison=pd.DataFrame({'Correlation':[],
                            'Bubble point pressure(psig)':[],'Rs(scf/STB)':[]})

## creating the logic for the standing correlation --------------------------------------------------------------------------------------------------
## --------------------------------------------------------------------------------------------------------------------------------------------------

if correlation_choice=='Standings Correlation':

    ## an expander to show the documentation of the correlation
    st.subheader('Documentation')
    with st.expander('Read Standing\'s Correlation Documentation'):
                     
        st.subheader("Standing's Correlation")
        st.write("""Standing (1947) proposed a graphical correlation for determining the
    gas solubility as a function of pressure, gas specific gravity, API gravity,
    and system temperature. The correlation was developed from a total of
    105 experimentally determined data points on 22 hydrocarbon mixtures
    from California crude oils and natural gases. The proposed correlation has
    an average error of 4.8%.
    """)
        
        st.latex(r'''\begin{equation}
    \mathrm{R}_{\mathrm{s}}=\gamma_{\mathrm{g}}\left[\left(\frac{\mathrm{p}}{18.2}+1.4\right) 10^{\mathrm{x}}\right]^{1.2048}
    \end{equation}
    ''')
        
        st.latex(r'''\begin{equation}
    x=0.0125API-0.00091(T-460)
    \end{equation}''')
        
        st.write("T= temperature,R")
        st.write("p=pressure,psia")
        st.write('Yg=solution gas specific gravity')

    Rs_standing()

    tab(Rs_standing_lst)

    st.subheader('Gas Solubility Plot')

    graph(p,Rs_standing_lst)
    
    ## creating tabs to select the data and Rs table to show up when clicked
    
##--------------------------------------------------------------------------------------------------------------------------------------------------------------
##  -------------------------------------------------------------------------------------------------------------------------------------------------------------    

elif correlation_choice=='Vasequez-Beggs Correlation':

    st.subheader('Documentation')
    with st.expander('Read Vasequez-Beggs Correlation Documentation'):

        st.subheader('Vasequez-Beggs Correlation')

        st.write("""Vasquez and Beggs (1980) presented an improved empirical correlation for estimating Rs. The correlation was obtained by regression analysis
                using 5,008 measured gas solubility data points. Based on oil gravity,
    the measured data were divided into two groups. This division was made
    at a value of oil gravity of 30°API
    """)
        st.latex(r'''\begin{equation}
    \mathrm{R}_{\mathrm{s}}=\mathrm{C}_1 \gamma_{\mathrm{gs}} \mathrm{p}^{\mathrm{C}_2} \exp \left[\mathrm{C}_3\left(\frac{\mathrm{API}}{\mathrm{T}}\right)\right]
    \end{equation}
    ''')
        
        df_coff=pd.DataFrame({'Coefficient':['C1','C2','C3'],
                            "API''30":[0.0362,1.0937,25.7240],
                            'API>300':[0.0178,1.1870,23.931]})
        st.dataframe(df_coff,hide_index=True,)

        st.latex(r'''\begin{equation}
    \gamma_{\mathrm{gs}}=\gamma_{\mathrm{g}}\left[1+5.912\left(10^{-5}\right)(\mathrm{API})\left(\mathrm{T}_{\text {sep }}-460\right) \log \left(\frac{\mathrm{p}_{\text {sep }}}{114.7}\right)\right]
    \end{equation}''')
        
        st.latex(r'''\begin{equation}
    \text { where } \begin{aligned}
    \gamma_{\mathrm{gs}} & =\text { gas gravity at the reference separator pressure } \\
    \gamma_{\mathrm{g}} & =\text { gas gravity at the actual separator conditions of } \mathrm{p}_{\mathrm{sep}} \text { and } \mathrm{T}_{\mathrm{sep}} \\
    \mathrm{p}_{\mathrm{sep}} & =\text { actual separator pressure, psia } \\
    \mathrm{T}_{\text {sep }} & =\text { actual separator temperature },{ }^{\circ} \mathrm{R}
    \end{aligned}
    \end{equation}

    ''')
        
    Rs_beggs()
    
    tab(Rs_beggs_lst)
    
    st.subheader('Gas Solubility Plot')
    
    graph(p,Rs_beggs_lst)


elif correlation_choice=='Marhouns Correlation':

    with st.expander('Read Marhoun\'s Correlation Documentation'):

        st.subheader('Marhoun\'s Correlation')
        st.write("""Marhoun (1988) developed an expression for estimating the saturation
                pressure of the Middle Eastern crude oil systems. The correlation originates from 160 
                experimental saturation pressure data.

    """)

        st.latex(r'''\begin{equation}
    \mathrm{R}_{\mathrm{s}}=\left[\mathrm{a} \gamma_{\mathrm{g}}^{\mathrm{b}} \gamma_{\mathrm{o}}^{\mathrm{c}} \mathrm{T}^{\mathrm{d}} \mathrm{p}\right]^{\mathrm{e}}
    \end{equation}

    ''')
        
        st.latex(r'''\begin{equation}
    \text { where } \begin{aligned}
    \gamma_{\mathrm{g}} & =\text { gas specific gravity } \\
    \gamma_{\mathrm{o}} & =\text { stock-tank oil gravity } \\
    \mathrm{T} & =\text { temperature, }{ }^{\circ} \mathrm{R} \\
    \mathrm{a}-\mathrm{e} & =\text { coefficients of the above equation having these values: } \\
    \mathrm{a} & =185.843208 \\
    \mathrm{~b} & =1.877840 \\
    \mathrm{c} & =-3.1437 \\
    \mathrm{~d} & =-1.32657 \\
    \mathrm{e} & =1.398441
    \end{aligned}
    \end{equation}

    ''')
    

    Rs_Marhouns()

    tab(Rs_Marhouns_lst)
    
    st.subheader('Gas Solubility Plot')

    graph(p,Rs_Marhouns_lst)

#--------------------------------------------------------------------------------------------------------------------------------------------------------------
#  ------------------------------------------------------------------------------------------------------------------------------------------------------------- 

elif correlation_choice=='Petrosky-Farshad Correlation':

    with st.expander('Read Petrosky-Farshad Correlation Documentation'):
    
        st.subheader('Petrosky-Farshad Correlation')
        st.write("""Petrosky and Farshad (1993) used a nonlinear multiple regression software to develop a gas solubility correlation. The authors constructed a
    PVT database from 81 laboratory analyses from the Gulf of Mexico crude
    oil system.

    """)
    
#     st.latex(r'''


# ''')
    
    Rs_Petrosky_farshad()  
    
    tab(Rs_petrosky_lst)

    st.subheader('Gas Solubility plot')

    graph(p,Rs_petrosky_lst)

###--------------------------------------------------------------------------------------------------------------------------------------------------------------


          
        

              




