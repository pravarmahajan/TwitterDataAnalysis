'''This script has been generated as part of the assignment 1 of
the course on "Social Media and Text Analytics". It contains libraries
related to geo-location analysis of the tweets. Expected twitter data
is a list of tweets represented in the form of python dictionary.
The tweets should be text tweets only, other user actions related data
will throw error which has not been handled.
'''
import operator
import os

import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

import iso_country_code
import twitter_lang_config as tlc

def ensure_dir(f):
    if not os.path.exists(f):
        os.makedirs(f)

def get_country_code_for_tweet(tweet):
    if tweet['place'] is not None:
        return tweet['place']['country_code']
    else:
        return None

def get_country_for_tweet(tweet):
    if tweet['place'] is not None:
        return tweet['place']['country']
    else:
        return None

def is_tweet_geo_tagged(tweet):
    return not (tweet['geo'] is None)

def get_freq_by_country(twitter_data):
    freq_by_country = dict() #dict containing mapping country -> freq
    for tweet in twitter_data:
        country = get_country_code_for_tweet(tweet)
        freq_by_country[country] = freq_by_country.get(country, 0) + 1

def get_tweets_for_country_code(twitter_data, country_code):
    tweets_for_country = []
    for tweet in twitter_data:
        if get_country_code_for_tweet(tweet) == country_code:
            tweets_for_country.append(tweet)

    return tweets_for_country

'''This function uses tweet_lang api to calculate language distribution
for every country. Currently it handles only twitter's tag for language
identification.
'''
#TODO: Add flag to allow using langid for getting language label
def get_lang_dist_by_country(twitter_data):
    lang_dist_by_country = dict()
    total_tweets_by_country = dict()

    for tweet in twitter_data:
        country = get_country_code_for_tweet(tweet)
        if country is None:
            continue    #We skip the cases when country is not specified
        total_tweets_by_country[country] = \
                total_tweets_by_country.get(country, 0) + 1
        if country not in lang_dist_by_country:
            lang_dist_by_country[country] = dict()
        lang_tag = tweet['lang']
        lang_dist_by_country[country][lang_tag] = \
                lang_dist_by_country[country].get(lang_tag, 0) + 1

    for (country, lang_dist) in lang_dist_by_country.iteritems():
        for (lang, frequency) in lang_dist.items():
            lang_dist[lang] = \
                    frequency*100/float(total_tweets_by_country[country])

    return lang_dist_by_country

def get_lang_to_country_map(lang_dist_by_country):
    lang_country_map = dict()
    all_countries = lang_dist_by_country.keys()

    for (country, lang_dist) in lang_dist_by_country.items():
        for (lang, freq) in lang_dist.items():
            if lang not in lang_country_map.keys():
                lang_country_map[lang] = dict()
            lang_country_map[lang][country] = freq

    for (lang, lang_dist) in lang_country_map.items():
        for country in all_countries:
            if country not in lang_dist.keys():
                lang_dist[country] = 0

    return lang_country_map

'''Creates a stacked bar given the language distribution by country
The format of the input is the output of the function:
get_lang_dist_by_country
'''
def plot_lang_freq_dist_stacked_bar(lang_dist_by_country):
    #get all languages list
    lang_country_map = get_lang_to_country_map(lang_dist_by_country)

    cm = plt.get_cmap('gist_rainbow')
    num_colors = len(lang_country_map.keys())
    colors = [cm(1.*i/num_colors) for i in range(num_colors)]

    bar_height = 1.0
    bar_bottom = [i for i in range(len(lang_dist_by_country.keys()))]
    tick_pos = [i+(bar_height/2) for i in bar_bottom]
    country_list = lang_dist_by_country.keys()

    plt.yticks(tick_pos,
              [iso_country_code.country_code[x] for x in country_list])
    plt.xlabel("Percentage of users")
    left = np.zeros(len(lang_dist_by_country.keys()))

    count = 0
    for (lang, countries) in lang_country_map.items():
        width = [countries[x] for x in country_list]
        plt.barh(bar_bottom,
                 width,
                 left=left,
                 height=bar_height,
                 color=colors[count],
                 edgecolor="white",
                 label=lang
                )
        left = left + width
        count += 1

    plt.legend(loc='upper center', ncol=5, bbox_to_anchor=(0.5, -0.15))
    
    ensure_dir("plot")
    plt.savefig('plot/1_5.png', bbox_inches='tight', pad_inches=2)
    print "saved plot to plot/1_5.png"
    plt.close()

'''Analysis on twitter data for US'''
def analyse_us_twitter_data(twitter_data):
    US_tweets = get_tweets_for_country_code(twitter_data, "US")
    us_tweets_lang_dist = get_lang_dist_by_country(twitter_data)['US']

    sorted_lang_list = sorted(us_tweets_lang_dist.items(),
                              key=operator.itemgetter(1),
                              reverse=True)

    print
    print "Twitter language distribution in US:"
    print "===================================="
    print "{0:^15}|{1:^15}".format("Language", "Pct of Tweets")
    for (lang, num) in sorted_lang_list:
        print "{0:^15}|{1:^8}".format(tlc.iso_lang_mapping[lang], num)
    
    num_geo_tagged = \
    len([tweet for tweet in US_tweets if is_tweet_geo_tagged(tweet)])

    print
    print "Pct GeoTagged: %.2f" %(num_geo_tagged*100.0/len(US_tweets))

def plot_world_lang_dist_hist(twitter_data):
    lang_dist_by_country = get_lang_dist_by_country(twitter_data)
    plot_lang_freq_dist_stacked_bar(lang_dist_by_country)
