# Prophet Demo

A demo for the Deliveroo internal tech conference, 2017.

## Setting Up


This guide assumes you're on MacOS and you've already got homebrew installed, but have not used python before on your current machine. It also assumes you use iterm so we can do fancy plots.

Installing python

```bash
brew install python
pip install virtualenv
virtualenv --no-site-packages .venv
source .venv/bin/activate
```

Installing dependencies

```bash
pip install numpy
pip install pandas
pip install pystan
pip install ipython
pip install datadog
pip install psycopg2
```

Configure iterm plotting because its awesome

```bash
pip install matplotlib
pip install itermplot
export MPLBACKEND="module://itermplot"
```

Install prophet itself

```bash
pip install fbprophet
```

Create a clean profile and launch an ipython terminal session:

```bash
ipython profile create demo
ipython --profile=demo
```

Ok we're ready to rock!


## Building some forecasts

Now we can build some forecasts in the ipython terminal. Start with our imports, including two utility functions to get data.

```python
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
```

Lets plot some business volumetric data over time

```python
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
```


Now we do a system metric from data dog, showing how we can do sub yearly.

```python
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
```
