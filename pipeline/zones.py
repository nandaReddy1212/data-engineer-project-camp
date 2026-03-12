#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


get_ipython().system('uv add sqlalchemy')


# In[5]:


from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg://root:root@localhost:5432/ny_taxi')


# In[7]:


df_zones = pd.read_csv('taxi_zone_lookup.csv')


# In[12]:


df_zones.head(n=0).to_sql(name='zones', con=engine, if_exists='replace')


# In[22]:


df_zones.count()


# In[18]:


from tqdm.auto import tqdm


# In[24]:


df_zones_iter = pd.read_csv(
    'taxi_zone_lookup.csv',
    iterator=True,
    chunksize=100
)


# In[25]:


for record in tqdm(df_zones_iter):
    record.to_sql(name='zones' ,con=engine, if_exists='append')


# In[ ]:




