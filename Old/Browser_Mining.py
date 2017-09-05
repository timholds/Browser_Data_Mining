import pandas as pd
import json
import time
import datetime
import numpy as np
from urllib.parse import urlparse
import matplotlib.pyplot as plt

class Data_to_Dataframe(file):
    def Import_Data(filepath):
        #Replace the argument in this with "Filepath"
        data = pd.read_json("Chrome_Data/Chrome/BrowserHistory2.json")
        # Create a new dataframe and drop unwanted columns
        dataframe = data.drop(['client_id', 'favicon_url'], 1)
        # Put rows in chronological order
        df = dataframe.sort_values(['time_usec'], ascending=True)

    def url_shortener(df):
        if (df.url[0:3] == 'chr'):
            return df.url[71:]
        else:
            return df.url

    def date_time(df):
        df['time_usec'] = df['time_usec'] / 1000000
        return datetime.datetime.fromtimestamp(
            int(df['time_usec'])
        ).strftime('%Y-%m-%d %H:%M:%S')

    def cleaning(df):
        # Set the index to be the 'dates_and_times' column
        df = df.set_index(['dates_and_times'])
        df.index.name = None
        # Make a copy of the dataframe and drop unneccesary columns
        df1 = pd.DataFrame.copy(df)
        df1 = df1.drop(['time_usec', 'url'], 1)
        return df1

    def main_url_extractor(df):
        u = urlparse(df['url_short'])
        return u.netloc

    # Function that gets a list of every site I've visited with no repeats
    sites = df1['page']
    def unique_urls(df1):
        sites_unique = set(sites)
        return sites_unique

    df['url_short'] = df.apply(url_shortener, axis=1)
    df['dates_and_times'] = df.apply(date_time, axis=1)
    df1['page'] = df1.apply(main_url_extractor, axis=1)
    site_list = unique_urls(df1)
