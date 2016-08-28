import praw
import re
import OAuth2Util
from praw.helpers import submission_stream
from praw.helpers import flatten_tree
from praw.helpers import  submissions_between
import pprint

SUBREDDIT = "all"

r = praw.Reddit(user_agent='link subreddit in submission title')
o=OAuth2Util.OAuth2Util(r)
o.refresh(force=True) 
    

def get_subredditurls (submission):
    #print (re.findall(r'\sr/\w*', submission.title))
    return re.findall(r'\Wr/\w*', submission.title)
       
        
def has_subredditurl_in_submissiontext(submission,SUBREDDITURL):    
    try:
        if (SUBREDDITURL in submission.selftext.lower()):
            print ("Found url in selftext")
            return True        
    except:
        pass
    
def has_subredditurl_in_comments(submission,SUBREDDITURL):    
    try:
        for comment in  flatten_tree(submission.comments):
            if (SUBREDDITURL in comment.body.lower()):
                print ("Found url in comments")
                return True
    except:
        pass
                
def has_subredditurl_in_link(submission,SUBREDDITURL):    
    try:
        if (SUBREDDITURL in submission.url.lower()):
            print ("Found url in link")
            return True        
    except:
        pass
  
while True:   
    try:    
        for submission in submission_stream(r,SUBREDDIT,1000,1):
        #for submission in submissions_between(r,SUBREDDIT,None,None,False,None,1):
        #for submission in r.get_subreddit(SUBREDDIT).get_new(limit=1000):
            #submission= r.get_submission(submission_id="4w9kzn")
            subredditurls = []
            urlstocomment = ""
            #print (submission.title)
            if submission.over_18 != True:
                subredditurls = get_subredditurls(submission)
                for url in subredditurls:
                    SUBREDDITURL = str(r.get_subreddit(url[3:]).url[1:-1]).lower()
                    if (str(submission.subreddit.url[1:-1]).lower() == SUBREDDITURL):
                            print ("same sub as parent - skipped")
                    elif (has_subredditurl_in_submissiontext(submission,SUBREDDITURL) == True or has_subredditurl_in_comments(submission,SUBREDDITURL) == True or has_subredditurl_in_link(submission,SUBREDDITURL)== True):
                            print ("subreddit url already found - skipped")
                    else:
                            print ("comment added - " + SUBREDDITURL)
                            urlstocomment = urlstocomment + SUBREDDITURL + "\n\n"
        
            if urlstocomment !="":
                submission.add_comment(urlstocomment + "\n\n*I am a bot; I link the subreddits mentioned in the title for easy navigation*")        
    except:
        pass                         