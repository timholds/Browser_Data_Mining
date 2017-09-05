import pandas as pd
import json
import time
import datetime
import numpy as np
from urllib.parse import urlparse
import matplotlib.pyplot as plt

file = #path to file "Chrome_Data/Chrome/BrowserHistory.json"
data = pd.read_json(file)

class Browser_Mining():
    # Method to drop unwanted columns and create a new dataframe, taking in a pandas json data and returning the dataframe
    def data_cleaning(data):
        # drop unneeded columns
        dataframe = data.drop(['client_id', 'favicon_url'], 1)
        # put rows in chronological order
        df = dataframe.sort_values(['time_usec'], ascending=True)
        return df

    # Method to convert time to readable format
    def date_time(df):
        df['time_usec'] = df['time_usec'] / 1000000
        return datetime.datetime.fromtimestamp(
            int(df['time_usec'])
        ).strftime('%Y-%m-%d %H:%M:%S')

    # Method to set the index to the dates and times
    def index_set(df):
        df = df.set_index(['dates_and_times'])
        df.index.name = None
        # df = df.drop(['time_usec', 'url'], 1)
        return df

    # Method to remove chrome extention prefixes from url's
    def url_shortener(df):
        if (df.url[0:3] == 'chr'):
            return df.url[71:]
        else:
            return df.url

    # Function to create a column with the main root url
    def main_url_extractor(df):
        u = urlparse(df['url_short'])
        return u.netloc

    # Function to make a copy of the dataframe and drop some more columns
    def second_cleaning(df):
        # df = df.set_index(['dates_and_times'])
        # df.index.name=None
        # make a copy of the dataframe and drop unneccesary columns
        df1 = pd.DataFrame.copy(df)
        df1 = df1.drop(['time_usec', 'url', 'page_transition'], 1)
        return df1


    def main(data):
        df = data_cleaning(data)
        df['dates_and_times'] = df.apply(date_time, axis=1)
        df = index_set(df)
        df['url_short'] = df.apply(url_shortener, axis=1)
        df['page'] = df.apply(main_url_extractor, axis=1)
        df1 = second_cleaning(df)
        # Reorder columns
        df1 = df1[['page', 'url_short', 'title']]
        return df1

    main(data)

    if __name__ == "main":
        main(data)


class Browser_Plots():
    # Make a dictionary, site_count, of sites and how many times I visited
    def website_counter(df1):
        site_count = {}
        for site in sites:
            # Special case if we're seeing this word for the first time.
            if not site in site_count:
                site_count[site] = 1
            else:
                site_count[site] = site_count[site] + 1
        return site_count

    # Function to plot hourly frequently visited websites with the dataframe of sites and times
    def plot_sites(df1):
        # List of every site with no repeats
        sites = df1['page']
        site_count = website_counter(df1)
        site_series = sort_by_least_popular(site_count)
        return site_series

    # Funciton that sorts websites from least to most visited as measured by page visits
    def sort_by_least_popular(site_count):
        site_count = pd.Series(site_count)
        site_count = pd.Series.sort_values(site_count)
        return site_count

    # Function to plot the top 20 sites
    def plot_top_sites():
        fig, ax = plt.subplots()
        pos = np.arange(20) + .5  # the bar centers on the y axis
        ax.barh(pos, site_series[-20:].values, align='center', fc='#80d0f1', ec='w')
        ax.set_xlabel("Site Visits Between January and November 2016")
        ax.set_yticks(pos)
        k = site_series[-20:].index
        ax.set_yticklabels(k)
        ax.set_title("Top Sites")
        return plt.tight_layout()

    # Function that creates a Series of hour and clicks
    def clicks_by_hour(df):
        hours = np.arange(24)
        clicks = np.zeros((24,), dtype=np.int)
        clicks_per_hour = pd.Series(clicks, hours)
        return clicks_per_hour

    # Function that creates a dictionary of hour and clicks
    def clicks_by_hour_dict(df):
        hours = np.arange(24)
        clicks = np.zeros((24,), dtype=np.int)
        dictionary = dict(zip(hours, clicks))
        return dictionary

    # Function that creates a new column with the hour of day
    def hour(df1):
        return df1.index.str[11:13]

    # Function that counts instances of each page per hour
    def hour_int_list(df, clicks_per_hour):
        hour = list(map(int, df['hour']))
        return (hour)

    # Funciton to create a dictionary with the number of aggregate clicks through the day
    def cph(clicks_per_hour, hour_click):
        for item in hour_click:
            clicks_per_hour[item] = clicks_per_hour[item] + 1
        return clicks_per_hour


    def main(df1):
        site_count = website_counter(df1)
        site_series = sort_by_least_popular(site_count)
        print("Plotting Top 20 Sites")
        plot_top_sites()
        clicks_per_hour = clicks_by_hour(df)
        clicks_per_hour_dict = clicks_by_hour_dict(df)
        a = hour(df)
        df['hour'] = a
        hour_click = hour_int_list(df, clicks_per_hour)
        hr_clicks = cph(clicks_per_hour, hour_click)
        print("Plotting average activity over 24 hours")
        hr_clicks.plot(kind='bar', rot=90)

    if __name__ == "main":
        main(df1)

df1 = Browser_Mining().main(data)
Browser_Plots().main(df1)