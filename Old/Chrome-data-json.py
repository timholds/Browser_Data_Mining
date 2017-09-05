import pandas as pd
from pandas.io.json import json_normalize
import json
import time
data = pd.read_json("Chrome_Data/Chrome/BrowserHistory2.json")
#create a new dataframe and drop unwanted columns 
dataframe = data.drop(['client_id', 'favicon_url'], 1)

#put rows in chronological order
#dataframe = dataframe.set_index(['time date'])
df = dataframe.sort_index()
#df['time date'] = df['time_usec'].apply(lambda x: time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(x)))
#print(df['time date'].head())

#for i in range(len(df)):
df['time int'] = pd.to_numeric(df['time_usec'], errors='coerce')
#print(df['time int'].head())

#print(len(df))
for i in range(len(df)):
    df['Date Time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(df.iloc[i]['time int']))
a = df['Date Time']
print(a.head())


"""
# In[ ]:




# In[ ]:

for i in range(len(df)):
    df['Date Time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(df.iloc[i]['time_usec']))
df['Date Time']



# In[ ]:


json_string =   {
            "page_transition": "LINK",
            "title": "Suspended Tab",
            "url": "chrome-extension:https://www.cs.cmu.edu/~mblum/search/AGTML35.pdf",
            "client_id": "paiNiq/dF5aqAqf2kuEBdA\u003d\u003d",
            "time_usec": 1478976729525846}


parsed_json2 =  {
        "739c5b1cd5681e668f689aa66bcc254c": {
        "plain":"test",
        "hexplain":"74657374",
        "algorithm":"MD5X5PLAIN"
    }
}

print(parsed_json2['739c5b1cd5681e668f689aa66bcc254c'])

data[['url']]
data[['time_usec']]

#df = df[[ ['title'], ['url'], ['page_transition']]]
df = df[['page_transition', 'title', 'url']]
cols = list(df.columns.values)
cols

"""
