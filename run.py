import os
import time
from datadog import initialize
from datadog import api
from psycopg2 import connect
import pandas as pd
import numpy as np
from fbprophet import Prophet
import matplotlib.pyplot as plt
import datetime

from utils import get_order_data, get_metric_data

# First lets plot some business volumetric data
df = get_order_data()
m = Prophet(yearly_seasonality=True)
m.fit(df);
future = m.make_future_dataframe(periods=90)
forecast = m.predict(future)

my_fig = m.plot(forecast);
my_fig.axes[0].set_xlim([datetime.date(2016, 6, 1), datetime.date(2017, 6, 10)])
my_fig.axes[0].set_ylim([10, 12.5])
my_fig.set_size_inches(18.5, 10.5)
plt.show()


# Now we do a system metric from data dog
my_period = 14515200
my_query = 'avg:heroku.dyno.load.avg.15m{*}'
df = get_metric_data(my_query, my_period)
df.plot()
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
plt.show()

m = Prophet(yearly_seasonality=False)
m.fit(df);

future = m.make_future_dataframe(periods=90)

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()

m.plot(forecast);
fig = plt.gcf()
fig.set_size_inches(18.5, 10.5)
plt.show()
