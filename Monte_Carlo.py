import statistics
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

register_matplotlib_converters()


prices = pd.read_csv(r"C:\Users\home\Downloads\LOW.csv")
                


# Parameter Definitions

# So    :   initial stock price
# dt    :   time increment -> a day in our case
# T     :   length of the prediction time horizon(how many time points to predict, same unit with dt(days))
# N     :   number of time points in the prediction time horizon -> T/dt
# t     :   array for time points in the prediction time horizon [1, 2, 3, .. , N]
# mu    :   mean of historical daily returns
# sigma :   standard deviation of historical daily returns
# b     :   array for brownian increments
# W     :   array for brownian path



So = prices.loc[prices.shape[0] - 1, "Close"]
dt = 1
d=30  #Number of days to run for#
T = d+1   
N = T / dt
t = np.arange(1, int(N) + 1)
returns = (prices.loc[1:, 'Close'] - \
          prices.shift(1).loc[1:, 'Close']) / \
          prices.shift(1).loc[1:, 'Close']
mu = np.mean(returns)
sigma = np.std(returns)
scen_size = 1000  #Number of Scenarios to run#
b = {str(scen): np.random.normal(0, 1, int(N)) for scen in range(1, scen_size + 1)}
W = {str(scen): b[str(scen)].cumsum() for scen in range(1, scen_size + 1)}

drift = (mu - 0.5 * sigma**2) * t
diffusion = {str(scen): sigma * W[str(scen)] for scen in range(1, scen_size + 1)}

S = np.array([So * np.exp(drift + diffusion[str(scen)]) for scen in range(1, scen_size + 1)]) 
S = np.hstack((np.array([[So] for scen in range(scen_size)]), S))

n=(range(0,scen_size))
for x in n:
    def plot(y):
        return plt.plot(S[x,0:y])
    plot(T)
    
results=[]
for x in n:
     results.append(S[x,T])
 
mean=statistics.mean(results)
sd=statistics.stdev(results)

high=mean+sd
low=mean-sd 

plt.axhline(y=high, color='r', linestyle='-')
plt.axhline(y=low, color='r', linestyle='-')

print(mean)
print(sd)
print(high)
print(low)
    
    

    


     
    






