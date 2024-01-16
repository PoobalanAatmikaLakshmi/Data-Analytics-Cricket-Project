#!/usr/bin/env python
# coding: utf-8

# In[20]:


import pandas as pd
import json 


# In[21]:


with open('t20_wc_match_results.json') as f:
    data = json.load(f)

df_match = pd.DataFrame(data[0]['matchSummary'])
df_match.head()


# In[30]:


df_match.rename({'scorecard': 'match_id'}, axis = 1, inplace = True)
df_match.head()
df_match.to_csv('dim_match_summary.csv', index = False)


# Batting summary 

# In[23]:


with open('t20_wc_batting_summary.json') as f:
    data = json.load(f)
    
    all_records = []
    
    for rec in data:  
        all_records.extend(rec['battingSummary'])

df_batting = pd.DataFrame(all_records)
df_batting.head()


# In[24]:


df_batting['out/not_out'] = df_batting['dismissal'].apply(lambda x: "out" if len(x)>0 else "not_out")
df_batting.head()


# In[25]:


df_batting.drop(columns = ['dismissal'],inplace = True )


# In[26]:


df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x:x.replace('€å',''))
df_batting['batsmanName'] = df_batting['batsmanName'].apply(lambda x:x.replace('\xa0',''))


# In[27]:


#key to link both tables is the match and team name 
#both combination of team1 vs team 2 and team2 vs team1 needed
match_ids_dict = {}

for index,row in df_match.iterrows():
    key1 = row['team1'] + ' Vs ' + row['team2']
    key2 = row['team2'] + ' Vs ' + row['team1']
    
    match_ids_dict[key1] = row['match_id']
    match_ids_dict[key2] = row['match_id']
    
match_ids_dict 
    
    


# In[28]:


df_batting['match_id'] = df_batting['match'].map(match_ids_dict)
df_batting.head()


# In[40]:


df_batting.to_csv('fact_bating_summary.csv', index = False)


# In[33]:


with open('t20_wc_bowling_summary.json') as f:
    data = json.load(f)
print(data) 


# In[36]:


all_records = []
for rec in data:
        all_records.extend(rec['bowlingSummary'])


# In[37]:


all_records


# In[38]:


df_bowling = pd.DataFrame(all_records)
print(df_bowling.shape)
df_bowling.head()


# In[39]:


df_bowling['match_id'] = df_bowling['match'].map(match_ids_dict)
df_bowling.head()


# In[41]:


df_bowling.to_csv('fact_bowling_summary.csv', index = False)


# In[42]:


with open('t20_wc_player_info.json') as f:
    data = json.load(f)


# In[43]:


df_players = pd.DataFrame(data)
df_players['name'] = df_players['name'].apply(lambda x: x.replace('â€', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('\xa0', ''))
df_players['name'] = df_players['name'].apply(lambda x: x.replace('†', ''))
df_players.head(2)


# In[44]:


df_players.to_csv('dim_players_no_images.csv', index = False)


# In[ ]:




