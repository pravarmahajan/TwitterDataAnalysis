import json
import langid

import twitterIO
import twitter_lang
import twitter_geo

refresh = False
twitter_count = 10000

def main():

    '''Assigment part one. Get stream of twitter data
    and save it to a file.
    twitter_count specifies number of tweets to be streamed
    '''
    if refresh:
        print "Streaming twitter data...."
        twitterIO.stream_and_save_twitter_data(twitter_count)
    
    print "Loading twitter data....."
    twitter_data = twitterIO.load_twitter_data_from_file(
            twitter_count)
    print "Loaded %d tweets" % twitter_count

    #Some cleanup and remove non text tweets
    twitter_data = twitterIO.process_twitter_data(twitter_data)

    '''Assignment part two. Get lang tags for all text tweets
    and analyse different language tags, get their percentages.
    Plots will be saved in dir plots, labeled 1_2.png
    '''
    
    tag_counts_twitter = \
            twitter_lang.analyse_twitter_language_tags(twitter_data)
    twitter_lang.plot_language_rankings(tag_counts_twitter, 2)

    '''Assignment part three. Get tags using langid package.
    Analyse the differences with twitter's language tag.
    '''
    #TODO: Make comparison table
    tag_counts_langid = \
            twitter_lang.analyse_langid_language_tags(twitter_data)
    twitter_lang.analyse_tag_differences(tag_counts_twitter,
                                         tag_counts_langid)

    twitter_lang.plot_language_rankings(tag_counts_langid, 3)

    '''Assignment part four. Get twitter language tag distribution
    percentage in US.'''

    twitter_geo.analyse_us_twitter_data(twitter_data)

    '''plot language distribution across different countries'''
    twitter_geo.plot_world_lang_dist_hist(twitter_data)


if __name__ == "__main__":
    main()
