import json
import pandas as pd
from textblob import TextBlob


def read_json(json_file: str)->list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """
    
    tweets_data = []
    for tweets in open(json_file,'r'):
        tweets_data.append(json.loads(tweets))
    
    
    return len(tweets_data), tweets_data

class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    ------
    dataframe
    """
    def __init__(self, tweets_list):
        
        self.tweets_list = tweets_list
        self.df = pd.json_normalize(tweets_list)
        self.df.loc

    # an example function
    def find_statuses_count(self)->list:
        statuses_count = self.df['user.statuses_count'].to_list()
        return statuses_count

    def find_full_text(self)->list:
        text = self.df['full_text'].fillna(self.df['retweeted_status.full_text']).to_list()
        return text    

       
    
    def find_sentiments(self, text)->list:
        subjectivity = [TextBlob(text).sentiment.subjectivity for text in text]

        polarity = [TextBlob(text).sentiment.polarity for text in text]

        return polarity, subjectivity

    def find_created_time(self)->list:
        created_at = self.df['created_at'].to_list()
        return created_at

    def find_source(self)->list:
        source = self.df['source'].to_list()

        return source

    def find_screen_name(self)->list:
        screen_name = self.df['user.screen_name'].to_list()

    def find_followers_count(self)->list:
        followers_count = self.df['user.followers_count'].to_list()
        return followers_count

    def find_friends_count(self)->list:
        friends_count = self.df['user.friends_count']
        return friends_count

    def is_sensitive(self)->list:
        try:
            is_sensitive = [x['possibly_sensitive'] for x in self.tweets_list]
        except KeyError:
            is_sensitive = None

        return is_sensitive

    def find_favourite_count(self)->list:
        return self.df['retweeted_status.favorite_count'].to_list()
    
    def find_retweet_count(self)->list:
        retweet_count = self.df['retweeted_status.retweet_count'].to_list()
        return retweet_count

    def find_hashtags(self)->list:
        hashtags = self.df['entities.hashtags'].to_list()
        return hashtags

    def find_mentions(self)->list:
        mentions = self.df['entities.user_mentions'].to_list()
        return mentions


    def find_location(self)->list:
        try:
            location = self.tweets_list['user']['location']
        except TypeError:
            location = ''
        
        return location

    def find_lang(self)->list:
        lang=self.df['lang'].to_list()
        return lang
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("data/global_twitter_data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 
    print("I have Started")
    # use all defined functions to generate a dataframe with the specified columns above