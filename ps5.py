#!/usr/bin/env python2
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
    def get_word(self):
        return self.word

    def is_word_in(self, text):
        text = text.lower()                   # turn to lowercase
        word = self.get_word().lower()
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
    def __init__(self, word):
        WordTrigger.__init__(self, word)
    def evaluate(self, story):
        return self.is_word_in(story.get_subject())
    
class SummaryTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_summary())

# Composite Triggers
# Problems 6-8

class NotTrigger(Trigger):
    def __init__(self, trigger):
        self.trig = trigger 
    def evaluate(self, story):
        return not self.trig.evaluate(story)

class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return ( self.trigger1.evaluate(story) and self.trigger2.evaluate(story))
    
class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    def evaluate(self, story):
        return ( self.trigger1.evaluate(story) or self.trigger2.evaluate(story))

# Phrase Trigger
# Question 9

# TODO: PhraseTrigger
class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = phrase
    def get_phrase(self):
        return self.phrase
    
    def evaluate(self, story):
        phrase = self.get_phrase()
        return ( (phrase in story.get_subject()) or (phrase in story.get_title())
                 or (phrase in story.get_summary()) )
                 
#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder (we're just returning all the stories, with no filtering) 
    # Feel free to change this line!
    desire_stories = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                desire_stories.append(story)
                break
    return desire_stories

#======================
# Part 4
# User-Specified Triggers
#======================
def TriggerGenerator(trigger_type, name, param, trigDic):
    """
    Info.: A function to generate Triggers with different type and update the
           trigDic.
    
    trigger_type: a lowercase string
    
    param: parameters to construct a Trigger, e.g. word, trig ....
    
    """
    if trigger_type == 'subject':
        trig = SubjectTrigger(param[0])
    elif trigger_type == 'title':
        trig = TitleTrigger(param[0])
    elif trigger_type == 'summary':
        trig = SummaryTrigger(param[0])
    elif trigger_type == 'phrase':
        trig = PhraseTrigger(" ".join(param))
    elif trigger_type == 'not':
        trig = NotTrigger(trigDic[param[0]])
    elif trigger_type == 'and':
        trig = AndTrigger(trigDic[param[0]], trigDic[param[1]])
    elif trigger_type == 'or':
        trig = OrTrigger(trigDic[param[0]], trigDic[param[1]])
    else:
        raise ValueError("Don't support "+ trigger_type + 'trigger')
    
    trigDic[name] = trig


def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # TODO: Problem 11
    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones
    trigDic = {}
    usedTrigger = []
    
    for line in lines:
        line = line.lower()
        split_line = line.split(' ')
        
        if split_line[0] != 'add':
            TriggerGenerator(split_line[1], split_line[0],
                             split_line[2:], trigDic)
        else:
            for triggerName in split_line[1:]:
                usedTrigger.append(trigDic[triggerName])
    return usedTrigger
    
import thread

def main_thread(p):
    # A sample trigger list - you'll replace
    # this with something more configurable in Problem 11
    t1 = SubjectTrigger("Obama")
    t2 = SummaryTrigger("MIT")
    t3 = PhraseTrigger("Supreme Court")
    t4 = OrTrigger(t2, t3)
    triggerlist = [t1, t4]
    triggerlist = readTriggerConfig('triggers.txt')
    # TODO: Problem 11
    # After implementing readTriggerConfig, uncomment this line 
    #triggerlist = readTriggerConfig("triggers.txt")

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

