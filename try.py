# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid

    def get_title(self):
        return self.title

    def get_subject(self):
        return self.subject

    def get_summary(self):
        return self.summary

    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

class WordTrigger(Trigger):
    import string
    def __init__(self, word):
        self.word = word

    def is_word_in(self, text):
        text = text.lower()                   # turn to lowercase
        word = self.word.lower()
        
        for punc in string.punctuation:                   # Replace Punctuation to Space
            text = text.replace(punc, " ") 
        Voc = text.split()                    # Split if any space there
        
        pureVoc = []
        for eachVoc in Voc:
            if eachVoc.endswith('ed') and (not self.word.endswith('ed')):
                pureVoc.append( eachVoc[:-2] )
            elif eachVoc.endswith('es') and ( not self.word.endswith('es')):
                pureVoc.append( eachVoc[:-2] )
            elif eachVoc.endswith('s') and (not self.word.endswith('s')):
                pureVoc.append( eachVoc[:-1] )
            else:
                pureVoc.append(eachVoc)
                
        return ( word in pureVoc )
    
        

class TitleTrigger(WordTrigger):
    def __init__(self, word):
        WordTrigger.__init__(self, word)
    def evaluate(self, story):
        return self.is_word_in(story.get_title())
        
class SubjectTrigger(WordTrigger):
    def evaluate():
        pass
