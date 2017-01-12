'''This script has been generated as part of the assignment 1 of
the course on "Social Media and Text Analytics". It contains libraries
related to language analysis of the tweets. Expected twitter data
is a list of tweets represented in the form of python dictionary.
The tweets should be text tweets only, other user actions related data
will throw error which has not been handled.
'''
import operator
import os

import langid 
import matplotlib.pyplot as plt

import twitter_lang_config as tlc

def ensure_dir(f):
    if not os.path.exists(f):
        os.makedirs(f)

'''This function uses twitter's lang tag to determine language of
the tweet text. Given a list of tweets, it calculates percentage of
various languages, outputs them and plots bar charts and pie charts
for visualization of results
'''

#TODO: handle und
def analyse_twitter_language_tags(twitter_data):
    tag_counts = dict() #dictionary containing mapping lang -> count

    for tweet in twitter_data:
        lang = tweet['lang']
        tag_counts[lang] = tag_counts.get(lang, 0) + 1

    return tag_counts

#TODO: Analyse differences
def analyse_langid_language_tags(twitter_data):
    tag_counts = dict() #dictionary containing mapping lang -> count

    for tweet in twitter_data:
        lang = langid.classify(tweet['text'])[0]
        tag_counts[lang] = tag_counts.get(lang, 0) + 1

    return tag_counts

def analyse_tag_differences(tag1, tag2):
    all_tags = set(tag1.keys()).union(tag2)
    all_tags = sorted(all_tags)

    print
    print "{0:^20}|{1:^9}|{2:^9}".format("Tag", "# Twitter", "# Langid")
    for tag in all_tags:
        if tag not in tlc.iso_lang_mapping.keys():
            full_lang_name = tag + "(unknown iso)"
        else:
            full_lang_name = tlc.iso_lang_mapping[tag]

        print "{0:^20}|{1:^9}|{2:^9}".format(full_lang_name,
                                             tag1.get(tag, 0),
                                             tag2.get(tag, 0))

def plot_language_rankings(tag_counts, n):
    sorted_tags = sorted(tag_counts.items(), key=operator.itemgetter(1),
                         reverse=True
                        )
    rank_ordered_tags = zip(*sorted_tags)[0]
    rank_ordered_freq = zip(*sorted_tags)[1]

    plt.xlabel("Ranking of languages")
    plt.ylabel("Number of users")

    '''annotating the plot with selected languages defined in
    twitter_lang_config'''
    extra_height = 0
    for tag in tlc.plot_list:
        full_lang = tlc.iso_lang_mapping[tag]
        try:
            rank = rank_ordered_tags.index(tag) + 1
            num_tweets = sorted_tags[rank-1][1]
        except ValueError:
            continue #we don't annotate that tag since it's not present
        plt.annotate(full_lang,
             xy=(rank, num_tweets),
             xytext=(rank, num_tweets+100+(100*extra_height)),
             arrowprops=dict(facecolor="black", shrink=0.05, width=0.1),
            )
        extra_height = 1-extra_height

    plt.plot(range(1, len(sorted_tags)+1), rank_ordered_freq, "ro")
    y_max = (int(max(tag_counts.values())/500 + 1)) * 500
    plt.axis([0, 40, 0, y_max])
    ensure_dir("plot")
    plt.savefig('plot/1_' + str(n) + '.png', bbox_inches='tight')
    plt.close()
    print "Saved plot to plot/1_2.png"
