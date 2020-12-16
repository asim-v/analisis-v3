import matplotlib.pyplot  as plt
from matplotlib.animation import FuncAnimation
import pandas as pd 

# ‘FuncAnimation’ is the method that we’ll be using to update the graph continuously giving it that live effect.
# We will be using MatPlotLib in this tutorial to generate our graphs and the panda's library to read CSV files.

plt.style.use('seaborn')
fig = plt.figure()
ax = fig.add_subplot(1,1,1)



def animation(i):
	#called every iteration
	AAPL_STOCK = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2014_apple_stock.csv')
	print(AAPL_STOCK)
	x = AAPL_STOCK[0:i]['AAPL_x']
	y = AAPL_STOCK[0:i]['AAPL_y']

	ax.clear()
	ax.plot(x, y)	


animation = FuncAnimation(fig, func=animation, interval=1000)
plt.show()		




