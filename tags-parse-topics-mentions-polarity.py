# Script for parsing tweets, mentions and polarity out of a csv file created with TAGS
# Modified from script originally developed by Aku Hiltunen, Tampere University of Technology

import re
from textblob import TextBlob

import pandas as pd
from ttp import ttp as prep

# Function for cleaning a tweet for sentiment analysis
def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())

# Function for performing the sentiment analysis
def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(clean_tweet(tweet))
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

# sets up filepath for an incoming csv file, change path to fit your case
# filename = "../data/data.csv"
filename = "OECDForum_en.csv"

# reads a csv file into the program
df = pd.read_csv(filename, sep=',', encoding="utf-8")

# prints are used for testing purposes throughout the script
print(df.head())
parser = prep.Parser()

print(df.columns)

# sets up new dicts to store mentions and hashtags
mentions = {'user': [], 'times mentioned': [], 'positivity': [], 'negativity': [], 'neutrality': []}
hashtags = {'hashtag': [], 'times used': [], 'positivity': [], 'negativity': [], 'neutrality': []}

# sets up a list for the polarity column
polarities = []

# goes through the table one row at a time
for row in df.itertuples():
  tweet = parser.parse(row.text.encode('utf-8').decode('utf-8'))
  user_from = row.from_user.lower()
  sentiment = get_tweet_sentiment(row.text)

  # this for loop collects information about mentions and stores it into the mentions dict created earlier
  for mention in tweet.users:
      ignore = 0
      user_to = mention.lower()

      for index, user in enumerate(mentions['user']):
          if user_to == user:
              mentions['times mentioned'][index] += 1
              if sentiment == 'positive':
                  mentions['positivity'][index] += 1
              elif sentiment == 'negative':
                  mentions['negativity'][index] += 1
              else:
                  mentions['neutrality'][index] += 1
              ignore += 1
              break

      if ignore == 0:
        mentions['user'].append(user_to)
        mentions['times mentioned'].append(1)
        if sentiment == 'positive':
            mentions['positivity'].append(1)
            mentions['negativity'].append(0)
            mentions['neutrality'].append(0)
        elif sentiment == 'negative':
            mentions['positivity'].append(0)
            mentions['negativity'].append(1)
            mentions['neutrality'].append(0)
        else:
            mentions['positivity'].append(0)
            mentions['negativity'].append(0)
            mentions['neutrality'].append(1)

  # this for loop collects information about hashtags and stores it into the hashtags dict created earlier
  for tag in tweet.tags:
      ignore = 0
      hashtag = tag.lower()
      for index, thing in enumerate(hashtags['hashtag']):
          if hashtag == thing:
              hashtags['times used'][index] += 1
              if sentiment == 'positive':
                  hashtags['positivity'][index] += 1
              elif sentiment == 'negative':
                  hashtags['negativity'][index] += 1
              else:
                  hashtags['neutrality'][index] += 1
              ignore += 1
              break

      if ignore == 0:
          hashtags['hashtag'].append(hashtag)
          hashtags['times used'].append(1)
          if sentiment == 'positive':
              hashtags['positivity'].append(1)
              hashtags['negativity'].append(0)
              hashtags['neutrality'].append(0)
          elif sentiment == 'negative':
              hashtags['positivity'].append(0)
              hashtags['negativity'].append(1)
              hashtags['neutrality'].append(0)
          else:
              hashtags['positivity'].append(0)
              hashtags['negativity'].append(0)
              hashtags['neutrality'].append(1)

  # stores the polarity for each row
  polarities.append(sentiment)

  # part of old implementation that lumps all tags and mentions in a single column
  '''mention_list = []
  for mention in tweet.users:
      user_to = mention.lower()
      mention_list.append(user_to)

  mentions.append(mention_list)

  tag_list = []
  for tag in tweet.tags:
      tag_list.append(tag)
  #print(tweet.users)
  #print(tweet.tags)
  hashtags.append(tag_list)'''

#old implementation
#df['mentions'] = mentions
#df['hashtags'] = hashtags
#print(hashtags)

# creates a new column for polarity
df['polarity'] = polarities

print(df.head())
print(mentions['user'])
print(mentions['times mentioned'])

df2 = pd.DataFrame(data=mentions)
df3 = pd.DataFrame(data=hashtags)

# sets up filepaths for the csv files to be written
# output = "../data/output.csv"
# output2 = "../data/mentions.csv"
# output3 = "../data/hashtags.csv"
output = "tags_output.csv"
output2 = "tags_mentions.csv"
output3 = "tags_hashtags.csv"

# writes three new csv files
# first one is the original + a new column for polarity

# second one includes columns for each unique mention, number of times a mention was mentioned +
# number of times a mention appeared in the context of each polarity

# third one includes columns for each unique hashtag, number of times a hashtag was used +
# number of times a hashtag appeared in the context of each polarity

df.to_csv(output, sep=',', encoding='utf-8')
df2.to_csv(output2, sep=',', encoding='utf-8')
df3.to_csv(output3, sep=',', encoding='utf-8')

# Instruction for running in Pythonanywhere
# In Bash console write: python3.4 tags-parse-topics-mentions-polarity.py