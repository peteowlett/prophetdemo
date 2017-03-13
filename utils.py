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


def get_order_data():
  conn_str = os.environ['REDSHIFT_AS_PETE']
  conn = connect(conn_str)
  query = "select (delivered_at::date)::varchar as ds, count(*)::float as y from orders where delivered_at > '2014-01-01' group by 1 order by 1;"
  data = pd.read_sql(query, conn)
  conn.close()
  data = data.dropna()
  data['y'] = np.log(data['y'])
  return data


def get_metric_data(ddog_query, ddog_period):

  options = {
      'api_key':os.environ['DDOG_API_KEY'],
      'app_key': os.environ['DDOG_APP_KEY']
  }
  initialize(**options)

  metric_data = api.Metric.query(
    start=int(time.time()) - ddog_period,
    end=int(time.time()),
    query=ddog_query
  )

  base_data = metric_data['series'][0]['pointlist']
  df = pd.DataFrame(base_data, columns=['ds', 'y'])
  df.loc[:, 'ds'] = pd.to_datetime(df.ds, unit='ms')
  df.loc[:, 'ds'] = df.ds.dt.strftime('%Y-%m-%d').astype(str)

  return df
