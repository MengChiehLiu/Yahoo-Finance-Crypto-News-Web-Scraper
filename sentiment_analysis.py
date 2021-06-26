"""
yahoo finance news web scraper (main_page)

Created on Sun 2021-06-13 20:01:25

@author: Jack.M.Liu
"""

# NLTK VADER for sentiment analysis
#import nltk
#nltk.download('vader_lexicon')

from nltk.sentiment.vader import SentimentIntensityAnalyzer


# New words and values
new_words = {
    'crushes': 10,
    'beats': 5,
    'misses': -5,
    'trouble': -10,
    'falls': -100,
}
# Instantiate the sentiment intensity analyzer with the existing lexicon
vader = SentimentIntensityAnalyzer()
# Update the lexicon
vader.lexicon.update(new_words)


import pandas as pd
scored_news = pd.read_csv ('yahoo finance news.csv')
# Iterate through the headlines and get the polarity scores
scores = [vader.polarity_scores(headline) for headline in scored_news.headline.values]
# Convert the list of dicts into a DataFrame
scores_df = pd.DataFrame(scores)
# Join the DataFrames
scored_news = pd.concat([scored_news, scores_df], axis=1)
scored_news["datetime"]=scored_news["date"]+" "+scored_news["time"]
scored_news.set_index(pd.to_datetime(scored_news["datetime"], format='%Y-%m-%d %H:%M:%S'),inplace=True)
#print(scored_news.head())


import matplotlib.pyplot as plt

#compound折線圖
'''
fig,ax=plt.subplots(figsize=(10,5))
ax.plot(scored_news['compound'],color='blue',label='2303')
plt.grid()
plt.show()
'''

#compound bar chart
'''
import matplotlib.pyplot as plt
fig,ax = plt.subplots()
scored_news['compound'].hist(ax=ax ,bins=50, alpha=0.5,color="b")
#ax.set_xlabel("Log Return")
#ax.set_ylabel("Freq of Log Return")
#ax.set_title("Volatility of " + str(stocknumber) + " is " +str(round(Volatility,4)*100) +"%")
plt.show()
'''

#1 Set the index to ticker and date
single_day = scored_news.set_index(['date'])
#3 Select the 3rd of January of 2019
single_day = single_day.loc['2021-06-11']
#4 Convert the datetime string to just the time
single_day['time'] = pd.to_datetime(single_day['time'])
single_day['time'] = single_day.time.dt.time 
#5 Set the index to time and 
single_day = single_day.set_index('time')
#6 Sort it
single_day = single_day.sort_index(ascending=True)

TITLE = "Positive, negative and neutral sentiment in yahoo crypto news on 2021-06-11"
COLORS = ["red", "green", "yellow"]
# Drop the columns that aren't useful for the plot
plot_day = single_day.drop(['Unnamed: 0','author','datetime','headline', 'compound','content'], axis=1)
# Change the column names to 'negative', 'positive', and 'neutral'
plot_day.columns = ['negative', 'neutral','positive' ]
# Plot a stacked bar chart
plot_day.plot.bar(stacked = True, 
                  figsize=(10, 6),
                  color = COLORS).legend(bbox_to_anchor=(1.01, 0.5))
plt.title(TITLE,fontsize=20)
plt.xlabel("Time",fontsize=15)
plt.ylabel("Scores",fontsize=15)
#plt.savefig('2021-06-11.png')
plt.show()
