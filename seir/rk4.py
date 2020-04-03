
import numpy as np
import plotly.graph_objects as go

def dfdt(f,D_incubation, D_infectious, D_recovery_mild, D_hospital_lag, D_recovery_severe, D_death, P_SEVERE, CFR, rate):
    S,E,I,R,Mild,Severe,Severe_H,Fatal,R_Mild,R_Severe,R_Fatal=f[0],f[1],f[2],f[3],f[4],f[5],f[6],f[7],f[8],f[9],f[10]
    beta      = rate/(D_infectious)
    a         = 1/D_incubation
    gamma     = 1/D_infectious

    p_severe  = P_SEVERE
    p_fatal   = CFR
    p_mild    = 1 - P_SEVERE - CFR

    dS        = -beta*I*S
    dE        =  beta*I*S - a*E
    dI        =  a*E - gamma*I
    dR        =  gamma*I

    dMild     =  p_mild*gamma*I   - (1/D_recovery_mild)*Mild
    dSevere   =  p_severe*gamma*I - (1/D_hospital_lag)*Severe
    dSevere_H =  (1/D_hospital_lag)*Severe - (1/D_recovery_severe)*Severe_H
    dFatal    =  p_fatal*gamma*I  - (1/D_death)*Fatal
    dR_Mild   =  (1/D_recovery_mild)*Mild
    dR_Severe =  (1/D_recovery_severe)*Severe_H
    dR_Fatal  =  (1/D_death)*Fatal

    return np.array([dS,dE,dI,dR,dMild,dSevere,dSevere_H,dFatal,dR_Mild,dR_Severe,dR_Fatal])


  # Finds value of f(x) for a given x using step size h 
def rungeKutta(dfdt,f0,D_incubation, D_infectious, D_recovery_mild, D_hospital_lag, D_recovery_severe, D_death, P_SEVERE, CFR, pop, rate, t0, t, n=20, dt=1): 
    # n = Count number of iterations using step size  or 
    # step height h 
    h = dt/n          # Default val : dt=1 ( Per day we are storing the data)  n= 20 ( Per day, we are taking 20 steps for integrating)
    n=int((t-t0)/h)
    # print('No of interpolation steps',n, ' and h =',h)
    f0=np.array(f0)
    f=f0/pop
    T,S,E,I,R,Mild,Severe,Severe_H,Fatal,R_Mild,R_Severe,R_Fatal=[],[],[],[],[],[],[],[],[],[],[],[]

    # Iterate for number of iterations
    for iteration in range(1, n + 1):

        "Apply Runge Kutta Formulas to find next value of f(x)"
        k1 = h * dfdt(f,D_incubation, D_infectious, D_recovery_mild, D_hospital_lag, D_recovery_severe, D_death, P_SEVERE, CFR,rate) 
        k2 = h * dfdt(f+0.5*k1,D_incubation, D_infectious, D_recovery_mild, D_hospital_lag, D_recovery_severe, D_death, P_SEVERE, CFR,rate)
        k3 = h * dfdt(f+0.5*k2,D_incubation, D_infectious, D_recovery_mild, D_hospital_lag, D_recovery_severe, D_death, P_SEVERE, CFR,rate)   
        k4 = h * dfdt(f+k3,D_incubation, D_infectious, D_recovery_mild, D_hospital_lag, D_recovery_severe, D_death, P_SEVERE, CFR,rate)
  
        # Update next value of f(x) 
        f = f + (1.0 / 6.0)*(k1 + 2 * k2 + 2 * k3 + k4)
        # Update next value of x 
        t0 = t0 + h 

        if iteration%20==0:
          T.append(round(t0))
          S.append(round(f[0]*pop))
          E.append(round(f[1]*pop))
          I.append(round(f[2]*pop))
          R.append(round(f[3]*pop))
          Mild.append(round(f[4]*pop))
          Severe.append(round(f[5]*pop))
          Severe_H.append(round(f[6]*pop))
          Fatal.append(round(f[7]*pop))
          R_Mild.append(round(f[8]*pop))
          R_Severe.append(round(f[9]*pop))
          R_Fatal.append(round(f[10]*pop))
    return T,S,E,I,R,Mild,Severe,Severe_H,Fatal,R_Mild,R_Severe,R_Fatal


def getSolution(dfdt,pop,E0,I0,R0,Mild0,Severe0,Severe_H0,Fatal0,R_Mild0,R_Severe0,R_Fatal0, D_incubation, D_infectious, D_recovery_mild, D_hospital_lag, D_recovery_severe, D_death, P_SEVERE, CFR, days, rates):
  T,S,E,I,R,Mild,Severe,Severe_H,Fatal,R_Mild,R_Severe,R_Fatal,intervention=[],[],[],[],[],[],[],[],[],[],[],[],[]
  
  S0=pop-E0-I0-R0
  for index in range(0,len(rates)):
    if index!=len(rates)-1:
      T0,S0,E0,I0,R0,Mild0,Severe0,Severe_H0,Fatal0,R_Mild0,R_Severe0,R_Fatal0=rungeKutta(dfdt,[S0,E0,I0,R0,Mild0,Severe0,Severe_H0,Fatal0,R_Mild0,R_Severe0,R_Fatal0],D_incubation, D_infectious, D_recovery_mild, D_hospital_lag, D_recovery_severe, D_death, P_SEVERE, CFR, pop, rates[index][1], rates[index][0], rates[index+1][0])
      T,S,E,I,R,Mild,Severe,Severe_H,Fatal,R_Mild,R_Severe,R_Fatal,intervention=T+T0,S+S0,E+E0,I+I0,R+R0,Mild+Mild0,Severe+Severe0,Severe_H+Severe_H0,Fatal+Fatal0,R_Mild+R_Mild0,R_Severe+R_Severe0,R_Fatal+R_Fatal0,intervention+[rates[index+1][0]]
    elif rates[index][0]< days:  
      T0,S0,E0,I0,R0,Mild0,Severe0,Severe_H0,Fatal0,R_Mild0,R_Severe0,R_Fatal0=rungeKutta(dfdt,[S0,E0,I0,R0,Mild0,Severe0,Severe_H0,Fatal0,R_Mild0,R_Severe0,R_Fatal0],D_incubation, D_infectious, D_recovery_mild, D_hospital_lag, D_recovery_severe, D_death, P_SEVERE, CFR, pop, rates[index][1], rates[index][0], days)
      T,S,E,I,R,Mild,Severe,Severe_H,Fatal,R_Mild,R_Severe,R_Fatal=T+T0,S+S0,E+E0,I+I0,R+R0,Mild+Mild0,Severe+Severe0,Severe_H+Severe_H0,Fatal+Fatal0,R_Mild+R_Mild0,R_Severe+R_Severe0,R_Fatal+R_Fatal0
    T0,S0,E0,I0,R0,Mild0,Severe0,Severe_H0,Fatal0,R_Mild0,R_Severe0,R_Fatal0=T[-1],S[-1],E[-1],I[-1],R[-1],Mild[-1],Severe[-1],Severe_H[-1],Fatal[-1],R_Mild[-1],R_Severe[-1],R_Fatal[-1]
  
  return T,S,E,I,R,Mild,Severe,Severe_H,Fatal,R_Mild,R_Severe,R_Fatal,intervention


def epidemic_calculator(dfdt,config,plotter=True,save=True):
    T,S,E,I,R,Mild,Severe,Severe_H,Fatal,R_Mild,R_Severe,R_Fatal,intervention=[],[],[],[],[],[],[],[],[],[],[],[],[]
    for group in Config.age_split:
        pop       = Config.pop*group['Pop_frac']
        days      = Config.days

        I0        = group['I0']     
        R0        = group['R0']      
        E0        = group['E0']
        Mild0     = group['Mild0'] 
        Severe0   = group['Severe0'] 
        Severe_H0 = group['Severe_H0']
        Fatal0    = group['Fatal0']
        R_Mild0   = group['R_Mild0'] 
        R_Severe0 = group['R_Severe0'] 
        R_Fatal0  = group['R_Fatal0'] 

        D_incubation        = group['D_incubation'] 
        D_infectious        = group['D_infectious']
        D_recovery_mild     = group['D_recovery_mild']
        D_hospital_lag      = group['D_hospital_lag']
        D_recovery_severe   = group['D_recovery_severe']
        D_death             = group['D_death']
        P_SEVERE            = group['P_SEVERE']
        CFR                 = group['CFR']
        rates               = group['Rates']

    T0,S0,E0,I0,R0,Mild0,Severe0,Severe_H0,Fatal0,R_Mild0,R_Severe0,R_Fatal0,intervention  =   getSolution(dfdt,pop,E0,I0,R0,Mild0,Severe0,Severe_H0,Fatal0,R_Mild0,R_Severe0,R_Fatal0, D_incubation, D_infectious, D_recovery_mild, D_hospital_lag, D_recovery_severe, D_death, P_SEVERE, CFR, days, rates)
    T,S,E,I,R,Mild,Severe,Severe_H,Fatal,R_Mild,R_Severe,R_Fatal=T+T0,S+S0,E+E0,I+I0,R+R0,Mild+Mild0,Severe+Severe0,Severe_H+Severe_H0,Fatal+Fatal0,R_Mild+R_Mild0,R_Severe+R_Severe0,R_Fatal+R_Fatal0

  
    if plotter == True:
        # import matplotlib.pyplot as plt
        # plt.figure(figsize=(20,10))
        # plt.title('Exposed (Blue), Infectious (Green) and Hospitalized (Red) plot vs Days')
        # for interval in intervention:
        #     if interval < days and interval>1:
        #         plt.vlines(interval,0,max(E), color="k", linestyles='dashed')
        # plt.plot(T[:days], E[:days], 'k',label='Exposed People vs Duration (days)')
        # plt.plot(T[:days], I[:days], 'm', label='Infectious People vs Duration (days)') 
        # plt.plot(T[:days], Severe_H[:days], 'b', label='Hospitalized People vs Duration (days)') 
        # plt.plot(T[:days], R_Fatal[:days], 'r', label='Fatalities vs Duration (days)') 
        # plt.legend()
        trace1 = go.Scatter(x=T[:days],y=E[:days],fillcolor='khaki',name='Exposed People vs Duration (days)')
        trace2 = go.Scatter(x=T[:days],y= I[:days])
        trace3 = go.Scatter(x=T[:days],y= Severe_H[:days])
        trace4 = go.Scatter(x=T[:days],y= R_Fatal[:days])
        layout = dict(
        title=dict(
            text='Exposed (Blue), Infectious (Green) and Hospitalized (Red) plot vs Days',
            font=dict(family="Open Sans, sans-serif", size=15, color="#515151"),
        ),
        font=dict(family="Open Sans, sans-serif", size=13),
        hovermode="closest",
        xaxis=dict(rangeslider=dict(visible=True), yaxis=dict(title="Records")),)
    
        return {"data": [trace1,trace2,trace3,trace4], "layout": layout}

    # plt.figure(figsize=(20,10))
    # plt.title('Susceptible (Red) and Removed (Green) plot vs Days')
    # for interval in intervention:
    #     if interval < days:
    #         plt.vlines(interval,0,max(S), color="k", linestyles='dashed')
    # plt.plot(T[:days], S[:days], 'r',label='Susceptible People vs Duration (days)')
    # plt.plot(T[:days], R[:days], 'c', label='Removed People vs Duration (days)') 
    # plt.plot(np.array(T)[:days], (np.array(R_Mild)+np.array(R_Severe))[:days], 'g', label='Totally Recovered People vs Duration (days)') 
    # plt.legend()
    # yield plt


    # if save==True:
    #     import uuid
    #     import pandas as pd
    #     runid=str(uuid.uuid4())[:12]
    #     df = pd.DataFrame(list(zip(*[list(T),list(S),list(E),list(I),list(R),list(Mild),list(Severe),list(Severe_H),list(Fatal),list(R_Mild),list(R_Severe),list(R_Fatal)])))
    #     df.columns =['Day', 'Susceptible', 'Exposed','Infectious','Removed','Recovering (Mild)','Recovering (Severe at home)','Recovering (Severe in hospital)','Recovering (Fatal)','Recovered','Recovered','Dead'] 

    #     df.to_csv(runid+'.csv', index=False)
    #     # with open(runid+'.txt','w') as file:
    #     #   file.write('tinc:'+str(tinc)+'\ntinf:'+str(tinf)+ '\nhos_rate:'+str(hos_rate)+'\nhos_time:'+str(hos_time)+ '\nhos_stay:'+str(hos_stay)+ '\ncfr:'+str(cfr)+ '\npop:'+str(pop)+ '\ne0:'+str(e0)+ '\ni0'+str(i0)+ '\nr0:'+str(r0)+ '\ndays:'+str(days)+ '\nrate1:'+str(rate1)+ '\nrate2:'+str(rate2)+ '\nrate3:'+str(rate3)+ '\nrate4:'+str(rate4)+ '\nrate5:'+str(rate5)+ '\nrate6:'+str(rate6)+ '\nnum_of_rates:'+str(num_of_rates))
    #     print('CSV and TXT files have been completed successfully in this current directory. Filenames are: \t',runid+'.csv','\t',runid+'.txt')
    #     yield df


class Config:
    pop	  =	7000000
    days  = 300
    t0    = 0    
    age_split = [	{	"age_group"		: "0-20",
    "Pop_frac"		: 0.25,
    "I0"		    		: 1,
    "R0"       		: 0,
    "E0"       		: 0,   
    "Mild0"    		: 0,       
    "Severe0"  		: 0,    
    "Severe_H0"		: 0,  
    "Fatal0"   		: 0,    
    "R_Mild0"   		: 0,    
    "R_Severe0"		: 0,    
    "R_Fatal0"  		: 0,
    "D_death"			: 32,
    "P_SEVERE"		: 0.2,             
    "D_hospital_lag"	: 5,
    "D_recovery_severe"	: 28.6,
    "D_hospital_lag"	: 5,
    "D_recovery_severe"	: 28.6,
    "D_recovery_mild"	: 11.1,
    "D_incubation": 5.2,
    "D_infectious": 2.9, 
    "CFR"			: 0.02,
    "Rates"			: [[0,2.2], [100,0.73], [180,1.9], [210,0.9], [250,1.3], [275,0.8]] },

    {	"age_group"		: "20-40",
    "Pop_frac"		: 0.35,
    "I0"		    		: 1,
    "R0"       		: 0,
    "E0"       		: 0,   
    "Mild0"    		: 0,       
    "Severe0"  		: 0,    
    "Severe_H0"		: 0,  
    "Fatal0"   		: 0,    
    "R_Mild0"   		: 0,    
    "R_Severe0"		: 0,    
    "R_Fatal0"  		: 0,
    "D_death"			: 32,
    "P_SEVERE"		: 0.2,             
    "D_incubation": 5.2,
    "D_infectious": 2.9,   
    "D_recovery_severe"	: 28.6,
    "D_recovery_mild"	: 11.1,
    "D_hospital_lag"	: 5,
    "CFR"			: 0.02,
    "Rates"			: [[0,2.2], [100,0.73], [180,1.9], [210,0.9], [250,1.3], [275,0.8]]},

    {	"age_group"		: "40-60",
    "Pop_frac"		: 0.25,
    "I0"		    		: 1,
    "R0"       		: 0,
    "E0"       		: 0,   
    "Mild0"    		: 0,       
    "Severe0"  		: 0,    
    "Severe_H0"		: 0,  
    "Fatal0"   		: 0,    
    "R_Mild0"   		: 0,    
    "R_Severe0"		: 0,    
    "R_Fatal0"  		: 0,
    "D_death"			: 32,
    "P_SEVERE"		: 0.2,             
    "D_hospital_lag"	: 5,
    "D_recovery_severe"	: 28.6,
    "D_recovery_mild"	: 11.1,
    "D_incubation": 5.2,
    "D_infectious": 2.9, 
    "CFR"			: 0.02,
    "Rates"			: [[0,2.2], [100,0.73], [180,1.9], [210,0.9], [250,1.3], [275,0.8]]},

    {	"age_group"		: "60+",
    "Pop_frac"		: 0.15,
    "I0"		    		: 1,
    "R0"       		: 0,
    "E0"       		: 0,   
    "Mild0"    		: 0,       
    "Severe0"  		: 0,    
    "Severe_H0"		: 0,  
    "Fatal0"   		: 0,    
    "R_Mild0"   		: 0,    
    "R_Severe0"		: 0,    
    "R_Fatal0"  		: 0,
    "D_death"			: 32,
    "P_SEVERE"		: 0.2,             
    "D_hospital_lag"	: 5,
    "D_incubation": 5.2,
    "D_infectious": 2.9, 
    "D_recovery_severe"	: 28.6,
    "D_recovery_mild"	: 11.1,
    "CFR"			: 0.02,
    "Rates"			: [[0,2.2], [100,0.73], [180,1.9], [210,0.9], [250,1.3], [275,0.8]]}
]
  
  # Please provide all the required variable:
  
  # days = Total no of duration or days
  # D_death : Time from end of incubation to death
  # P_SEVERE : Hospitalization Rate (Fraction of infected population admitted to the hospital)
  # D_hospital_lag : time_to_hospitalization
  # D_recovery_severe : Length of hospital stay 
  # D_recovery_mild : Recovery time for mild cases
  # CFR : Case Fatality Rate
  # D_incubation = Length of incubation period
  # D_infectious = Duration patient is infectious
  # pop = Total number of population
  
  #Initializations:
  
  
  # I0 = Initial number of Infectious persons (Number of infections actively circulating)
  # R0 = Initial number of Removed persons (Population no longer infectious due to isolation or immunity)
  # E0 = Initial number of Exposed persons Population currently in incubation.
  # Mild0     : Recovering (Mild)     
  # Severe0   : Recovering (Severe at home)
  # Severe_H0 : Recovering (Severe in hospital)
  # Fatal0    : Recovering (Fatal)
  # R_Mild0   : Recovered
  # R_Severe0 : Recovered
  # R_Fatal0  : Dead
  # Rate= reproduction rate [Measure of contagiousness: the number of secondary infections each infected individual produces]		->	Array of Array of day and rate -> [[Date1, Rate1],...,[Date_n,Rate_n]] . Examples : [[0,2.2],[100,0.7],etc]
  
epidemic_calculator(dfdt,Config,plotter=True,save=True)