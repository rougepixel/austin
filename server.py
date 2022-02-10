import os
import http.server
import socketserver
import instaloader
from http import HTTPStatus
from collections import Counter
import re
from re import search
import io
from io import BytesIO
import bs4
from bs4 import BeautifulSoup
import requests
import sys
from collections import OrderedDict
import responses
import requests

def do_austin(self):
    self.send_response(HTTPStatus.OK)
    self.end_headers()
        
    #Logs into a burner account
    L = instaloader.Instaloader(download_pictures = False, download_videos = False, download_comments= False, compress_json = False)
    L.login("andrew_ryanne", "$Instagram5")
        
    #Sets your account as the one to find the newest followers
    my_account = "austinjanik"
    my_profile = instaloader.Profile.from_username(L.context, my_account)
        
    #Gets most recent follower and their full name
    for follower in my_profile.get_followers():
        most_recent_follower = follower.username
        follower_full_name = follower.full_name
        msg = '\nMy most recent follower: %s' % (most_recent_follower)
        self.wfile.write(msg.encode())
        msg = '\nTheir name: %s' % (follower_full_name)
        self.wfile.write(msg.encode())
        break
    
    #Gets all posts of most recent follower
    profile_to_scrape = instaloader.Profile.from_username(L.context, most_recent_follower)
    posts = profile_to_scrape.get_posts()

    #Setting up arrays and variables
    usernames = []
    caption_usernames = []
    non_birthday_posts = 0
    birthday_keyword_one = "birth" #these are case insensitive with flags below
    birthday_keyword_two = "born"
    
    #Obtains an array of all tagged users and an array of all captions of most recent follower
    #Also spits out birthday captions, post dates, and tags
    for post in posts: 
        usernames = usernames + post.tagged_users
        caption_usernames = caption_usernames + post.caption_mentions
        if search(birthday_keyword_one, post.caption, flags=re.IGNORECASE) or search(birthday_keyword_two, post.caption, flags=re.IGNORECASE):
            msg = '\n-----------------'
            self.wfile.write(msg.encode())
            msg = '\nPOSSIBLE BIRTHDAY: %s' % (post.date)
            self.wfile.write(msg.encode())
            msg = '\nCaption: %s' % (post.caption)
            self.wfile.write(msg.encode())
            msg = '\nPost Tags: %s' % (post.tagged_users)
            self.wfile.write(msg.encode()) 
            msg = '\nCaption Tags: %s' % (post.caption_mentions)
            self.wfile.write(msg.encode())
            msg = '\n-----------------'
            self.wfile.write(msg.encode())
        else:   
            non_birthday_posts = non_birthday_posts + 1
            
    #Obtains an array of all full NAMES of tagged users. ***************CANNOT DO THIS IF THESE ACCOUNTS ARE PRIVATE***********************
    #names = []
    #for username in usernames:
    #    profile = instaloader.Profile.from_username(L.context, username)
    #    names.append(profile.full_name)
            
    #Obtains an array of all full NAMES of tagged users in CAPTIONS.
    #caption_names = []
    #for caption_username in caption_usernames:
    #    profile = instaloader.Profile.from_username(L.context, caption_username)
    #    caption_names.append(profile.full_name)

    #These print out 5 most common pieces of information per category
    c = Counter(usernames)
    msg = '\n5 most common tagged usernames: \n%s' % (c.most_common(5))
    self.wfile.write(msg.encode())
    #d = Counter(names)
    #msg = '\n5 most common tagged names: \n%s' % (d.most_common(5))
    #self.wfile.write(msg.encode())
    e = Counter(caption_usernames)
    msg = '\n5 most common CAPTION usernames: \n%s' % (e.most_common(5))
    self.wfile.write(msg.encode())
    #f = Counter(caption_names)
    #msg = '\n5 most common CAPTION names: \n%s' % (f.most_common(5))
    #self.wfile.write(msg.encode())
    

def spectator(self):
    note = self.headers.get('note')
    self.send_response(200)
    self.end_headers()
    msg = 'READING '
    self.wfile.write(msg.encode()) 
    f = open("note.txt", "w")
    f.write(note)
    f.close()
    msg = 'DONE'
    self.wfile.write(msg.encode())   

def mirror(self):
    self.send_response(200)
    self.end_headers()
    f = open("note.txt", "r")
    lines = f.read()
    f.close()
    self.wfile.write(lines.encode())

def nameoffunction(self):
    print("Do something here")

def yarn(self):
    print("Insert yarn function here if you'd like--this is just a template")
    
class Handler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self): #THESE ARE THE GET REQUESTS--USED FOR OBTAINING INFORMATION FROM YOUR SERVER AND THEY ARE FASTER THAN POST REQUESTS (BUT YOU CAN USE GET INSTEAD OF POST FOR SMALL INFO FOR SPEED)
        if self.path == '/austin':
            do_austin(self) #NAME OF FUNCTION--MAKE SURE TO PASS IN SELF AS ARGUMENT
        elif self.path == '/mirror':
            mirror(self)
        elif self.path == '/spectator':
            spectator(self)


    def do_POST(self): #THESE ARE POST REQUESTS--USED FOR UPDATING INFO ON SERVER AND THEY ARE SLOWER THAN GET REQUESTS
        if self.path == '/yarn':
            yarn(self) 
        elif self.path == '/nameoffunction':
            nameoffunction(self)

            
port = int(os.getenv('PORT', 80))
print('Listening on port %s' % (port))
httpd = socketserver.TCPServer(('', port), Handler)
httpd.serve_forever()