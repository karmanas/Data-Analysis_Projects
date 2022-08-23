#!/usr/bin/env python
# coding: utf-8

# In[540]:


import numpy as np
import pandas as pd


# In[541]:


data = pd.read_csv(r"C:\Users\Manas Ranjan Kar\Downloads\Olympic_Data.csv\athlete_events.csv")
region_data = pd.read_csv(r"C:\Users\Manas Ranjan Kar\Downloads\Olympic_Data.csv\noc_regions.csv")


# In[542]:


data.shape


# In[543]:


data.head(2)


# In[544]:


data = data[data['Season'] == 'Summer']


# In[545]:


data.shape


# In[546]:


data = data.merge(region_data,on='NOC',how='left')


# In[547]:


data.head(2)


# In[548]:


data['region'].unique().shape


# In[549]:


data.isnull().sum()


# In[550]:


data.duplicated().sum()


# In[551]:


data.drop_duplicates(inplace=True)


# In[552]:


data.duplicated().sum()


# In[553]:


data = pd.concat([data,pd.get_dummies(data['Medal'])],axis=1)    ### one hot encoding 


# In[554]:


data.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index().head()


# In[555]:


medal_tally = data.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'])


# In[556]:


medal_tally.groupby('NOC').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index().head()


# In[557]:


medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()


# In[558]:


medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']


# In[559]:


medal_tally.head()


# In[560]:


Years = data['Year'].unique().tolist()


# In[561]:


Years.sort()
Years.insert(0,'Overall')
Years


# In[562]:


country = np.unique(data['region'].dropna().values).tolist()


# In[563]:


country.sort()
country.insert(0,'Overall')
country


# In[564]:


medal_data = data.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'])


# In[565]:


def fetch_medal_tally(data,year,country):
    medal_data = data.drop_duplicates(subset = ['Team','NOC','Games','Year','City','Sport','Event','Medal'])
    flag = 0
    if year == 'overall' and country == 'overall':
        temp_data = medal_data
    if year == 'overall' and country != 'overall':
        flag = 1
        temp_data = medal_data[medal_data['region']==country]
    if year != 'overall' and country == 'overall':
        temp_data = medal_data[medal_data['Year'] == int(year)]
    if year != 'overall' and country !='overall':
        temp_data = medal_data[(medal_data['Year']==int(year)) & (medal_data['region']==country)]
     
    if flag ==1:
        x = temp_data.groupby('Year').sum()[['Gold','Silver','Bronze']].sort_values('Year').reset_index()
    else:
        x = temp_data.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending = False).reset_index()
        
    x['Total'] = x['Gold'] + x['Silver'] + x['Bronze']
    
    print(x)


# In[566]:


fetch_medal_tally(medal_data,year = 'overall',country = 'India')


# ## Overall Analysis
#  #### NO. of editions
#  #### No. of cities
#  #### No. of events/sports
#  #### No. of athletes
#  #### Participating nations

# In[567]:


data.head(3)


# In[568]:


data['Year'].unique().shape[0]-1


# In[569]:


data['City'].unique().shape


# In[570]:


data['Sport'].unique().shape


# In[571]:


print(data['Event'].unique().shape)
print(data['Name'].unique().shape)
print(data['region'].unique().shape)


# In[572]:


nations_over_time = data.drop_duplicates(['Year','region'])['Year'].value_counts().reset_index().sort_values('index')
nations_over_time.rename(columns={'index': 'Year', 'Year': 'No of countries'},inplace = True)
nations_over_time


# In[573]:


import plotly.express as px


# In[574]:


fig  = px.line(nations_over_time , x= 'Year' , y = 'No of countries')
plt.figure(figsize=(6,6))
fig.show()


# In[575]:


data.drop_duplicates(['Year','Event'])['Year'].value_counts().reset_index().sort_values('index')
nations_over_time.rename(columns={'Event': 'Year', 'No of countries': 'Event'},inplace = True)
nations_over_time.head(10)


# In[576]:


fig  = px.line(nations_over_time , x= 'Year' , y = 'Event')
plt.figure(figsize=(6,6))
fig.show()


# In[577]:


x=data.drop_duplicates(['Year','Sport','Event'])


# In[578]:


import seaborn as sns
import matplotlib.pyplot as plt


# In[579]:


plt.figure(figsize=(14,14))
sns.heatmap(x.pivot_table(index = 'Sport',columns='Year',values = 'Event',aggfunc = 'count').fillna(0).astype('int'),annot=True)


# In[580]:


def most_sucessful(data,sport):
    temp_data = data.dropna(subset=['Medal'])
    
    if sport != 'Overall':
        temp_data = temp_data[temp_data['Sport'] == sport]
        
    x = temp_data['Name'].value_counts().reset_index().head(15).merge(data,left_on = 'index',right_on = 'Name',how = 'left')[['index','Name_x','Sport','region']].drop_duplicates('index')
    x.rename(columns = {'index':'Name','Name_x': 'Medals'}, inplace =True)
    return x


# In[581]:


most_sucessful(data,"Overall")


# ## Country-Wise Analysis

# #### 1. Country-Wise medal_Tally per year(line plot)
# #### 2. What Countries are good at heatmap
# #### 3. Most successful Athletes(Top 15)

# In[582]:


temp_data = data.dropna(subset=['Medal'])
temp_data.drop_duplicates(subset = ['NOC', 'Team', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace = True)


# In[583]:


new_data = temp_data[temp_data['region'] == 'USA']
final_data = new_data.groupby('Year').count()['Medal'].reset_index()
final_data.head(10)


# In[584]:


fig  = px.line(final_data , x= 'Year' , y = 'Medal')
plt.figure(figsize=(6,6))
fig.show()


# In[585]:


new_data = temp_data[temp_data['region'] == 'UK']


# In[586]:


plt.figure(figsize=(12,12))
sns.heatmap(new_data.pivot_table(index = 'Sport',columns='Year',values = 'Medal',aggfunc = 'count').fillna(0).astype('int'),annot=True)


# In[587]:


def most_sucessful(data,country):
    temp_data = data.dropna(subset=['Medal'])
    
 
    temp_data = temp_data[temp_data['region'] == country]
        
    x = temp_data['Name'].value_counts().reset_index().head(15).merge(data,left_on = 'index',right_on = 'Name',how = 'left')[['index','Name_x','Sport']].drop_duplicates('index')
    x.rename(columns = {'index':'Name','Name_x': 'Medals'}, inplace =True)
    return x


# In[588]:


most_sucessful(data,'India')


# ## Athlete-Wise Analysis

# In[589]:


import plotly
import plotly.figure_factory as ff


# In[590]:


athlete_data = data.drop_duplicates(subset=['Name', 'region'])


# In[591]:


athlete_data['Age'].dropna()


# In[592]:


x1 = athlete_data['Age'].dropna()
x2 = athlete_data[athlete_data['Medal'] == 'Gold']['Age'].dropna()
x3 = athlete_data[athlete_data['Medal'] == 'Silver']['Age'].dropna()
x4 = athlete_data[athlete_data['Medal'] == 'Bronze']['Age'].dropna()


# In[593]:


Fig = ff.create_distplot([x1,x2,x3,x4], ['Overall Age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist = False,show_rug = False)
Fig.show()


# In[594]:


famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']


# In[595]:


x = []
name = []
for sport in famous_sports:
        temp_data = athlete_data[athlete_data['Sport'] == sport]
        x.append(temp_data[temp_data['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)


# In[596]:


fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
fig.show()


# In[597]:


athlete_data['Medal'].fillna('No Medal',inplace = True)


# In[598]:


plt.figure(figsize = (6,6))
temp_data = athlete_data[athlete_data['Sport']=='Athletics']
sns.scatterplot(temp_data['Weight'],temp_data['Height'],hue = temp_data['Medal'],style = temp_data['Sex'],s = 100)


# In[599]:


men = athlete_data[athlete_data['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
women = athlete_data[athlete_data['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()


# In[600]:


final = men.merge(women, on='Year', how='left')
final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)


# In[601]:


final.head(10)


# In[602]:


final.fillna(0,inplace=True)
Fig = px.line(final, x= 'Year', y= ['Male','Female'])
plt.figure(figsize=(6,6))
Fig.show()


# In[ ]:




