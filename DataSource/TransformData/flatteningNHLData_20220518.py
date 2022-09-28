#%%1 /,.


import os
import requests
import pickle# Set up the API call variables
os.getcwd()


# In[2]:



game_data = []
year = '2019'
season_type = '02' 
max_game_ID = 1271


# In[3]:


# Loop over the counter and format the API call
#for i in range(0,max_game_ID):
#    r = requests.get(url='http://statsapi.web.nhl.com/api/v1/game/'
#        + year + season_type +str(i).zfill(4)+'/feed/live')    
#    data = r.json()
#    game_data.append(data)


# In[3]:


type(game_data)


# In[4]:


#with open('./input/NHLData/'+year+'FullDataset.pkl', 'wb') as f:
#    pickle.dump(game_data, f, pickle.HIGHEST_PROTOCOL)


# In[5]:


import numpy as np 
import pandas as pd 
import pickle    
import matplotlib
import matplotlib.pyplot as plt
color_map = plt.cm.winter
from matplotlib.patches import RegularPolygon
import math
from PIL import Image# Needed for custom colour mapping!
from matplotlib.colors import ListedColormap,LinearSegmentedColormap
import matplotlib.colors as mcolors

with open('C:/Users/User/Desktop/Python/Hockey/input/NHLData/2019FullDataset.pkl', 'rb') as f:
    game_data = pickle.load(f)

# In[6]:


#ListedColorMap = colors.ListedColorMap
c = mcolors.ColorConverter().to_rgb
positive_cm = ListedColormap([c('#e1e5e5'),c('#d63b36')])
negative_cm = ListedColormap([c('#e1e5e5'),c('#28aee4')]) 


# In[7]:




    


#Flatten every game matchup

matchup={}
matchup['away']=[]
matchup['home']=[]

columns=['GamePk','home','away','Year']

games=pd.DataFrame(columns=columns)

for data in game_data:   # It is possible that the game data is not assigned to the data
   #set, so to handle this we look for the key ‘liveData’ which 
   #contains all of the data we are looking for, otherwise we
   #continue
    if 'gameData' not in data:
        continue   # Drilling down into the dataset to extract the play by play
    #information for the game
    teams = data['gameData']['teams']
    for homeAway in teams: # For each play
        #if teams[homeAway]['name'] in team:                # If the event contains coordinates
        matchup[homeAway]=teams[homeAway]['name']
    df1=pd.DataFrame([[data['gameData']['game']['pk'],matchup['home'],matchup['away'],year]],columns=columns)
    df1.reset_index(drop=True,inplace=True)
    games.reset_index(drop=True,inplace=True)
    games=pd.concat([games,df1])#,ignore_index=True)

games.reset_index(drop=True,inplace=True)





#%% 8


#Each Player playing in each game with the team they played with

columns=['GamePk','Team','PlayerID','PlayerName','Year']

playerList=pd.DataFrame(columns=columns)

for data in game_data:   # It is possible that the game data is not assigned to the data
   #set, so to handle this we look for the key ‘liveData’ which 
   #contains all of the data we are looking for, otherwise we
   #continue
    if 'gameData' not in data:
        continue   # Drilling down into the dataset to extract the play by play
    #information for the game
    players = data['gameData']['players']
    for player in players: # For each play
        #if teams[homeAway]['name'] in team:                # If the event contains coordinates
        if 'currentTeam' in players[player]:
            df1=pd.DataFrame([[data['gameData']['game']['pk'],players[player]['currentTeam']['name'],player,players[player]['fullName'],year]],columns=columns)
            df1.reset_index(drop=True,inplace=True)
            playerList.reset_index(drop=True,inplace=True)
            playerList=pd.concat([playerList,df1])#,ignore_index=True)

playerList.reset_index(drop=True,inplace=True)






#%% 9


#Each Play

columns=['GamePK','Event','eventCode','eventTypeID','periodTime','periodTimeRemaining','periodType','period','CoorX','CoorY']

playList=pd.DataFrame(columns=columns)
count=0

playList.to_csv('C:/Users/User/Desktop/Python/Hockey/input/NHLData/FlattenData/playList_' + str(year)+'.csv',index=False)

game_data_len=len(game_data)

for data in game_data:   # It is possible that the game data is not assigned to the data
   #set, so to handle this we look for the key ‘liveData’ which 
   #contains all of the data we are looking for, otherwise we
   #continue
    count=count+1
    print(count, " of ", game_data_len)
    if 'liveData' not in data:
        continue   # Drilling down into the dataset to extract the play by play
    #information for the game
    plays = data['liveData']['plays']['allPlays'] 
    for play in plays: # For each play
        if 'x' in play['coordinates']:
            df1=pd.DataFrame([[data['gameData']['game']['pk'],play['result']['event'],play['result']['eventCode'],play['result']['eventTypeId'],play['about']['periodTime'],\
              play['about']['periodTimeRemaining'],\
                play['about']['periodType'],play['about']['period'],play['coordinates']['x'],play['coordinates']['y']]],columns=columns) 
        else:
            df1=pd.DataFrame([[data['gameData']['game']['pk'],play['result']['event'],play['result']['eventCode'],play['result']['eventTypeId'],play['about']['periodTime'],\
              play['about']['periodTimeRemaining'],
                play['about']['periodType'],play['about']['period'],'','']],columns=columns  )
        #df1=pd.DataFrame([[data['gameData']['game']['pk'],players[player]['currentTeam']['name'],player,players[player]['fullName'],year]],columns=columns)
        #df1.reset_index(drop=True,inplace=True)
        #playList.reset_index(drop=True,inplace=True)
        #playList=pd.concat([playList,df1])#,ignore_index=True)
        df1.to_csv('C:/Users/User/Desktop/Python/Hockey/input/NHLData/FlattenData/playList_'+ str(year)+'.csv', mode='a', index=False, header=False)


#playList.reset_index(drop=True,inplace=True)



#%% 10


























