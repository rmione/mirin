import requests
import json 
from bs4 import BeautifulSoup
from xml.dom import minidom
import xmltodict 
from selenium import webdriver
from requests_html import HTMLSession
"""
For now we are going to use Romaji titles for the anime and search the database that we are going to use (for now, kitsuneko.)
Kitsuneko uses a pretty simplistic URL structure so I think that this will be pretty simple to work with. Let's get going! 
"""

# headers = """GET /dirlist.php?dir=subtitles%2Fjapanese%2F07-Ghost%2F HTTP/2
# Host: kitsunekko.net
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0
# Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
# Accept-Language: en-US,en;q=0.5
# Accept-Encoding: gzip, deflate, br
# Referer: https://kitsunekko.net/dirlist.php?dir=subtitles%2Fjapanese
# DNT: 1
# Connection: keep-alive
# Cookie: G_ENABLED_IDPS=google
# Upgrade-Insecure-Requests: 1
# Cache-Control: max-age=0
# TE: Trailers
#             """

base_url = 'https://kitsunekko.net/dirlist.php?dir=subtitles\%2Fjapanese\%2FAjin+S2\%2F'
headers = {'Host': 'kitsunekko.net',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:79.0) Gecko/20100101 Firefox/79.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'DNT': '1',
'Connection': 'keep-alive',
'Referer': 'https://kitsunekko.net/dirlist.php?dir=subtitles\%2Fjapanese\%2F',
'Cookie': 'G_ENABLED_IDPS=google',
'Upgrade-Insecure-Requests': '1',
'TE': 'Trailers'} 
# cookies = {'G_ENABLED_IDPS': 'google'}
# r = requests.get(base_url, headers=headers, params={'Scheme': 'https', 'Host': 'kitsunekko.net', 'Filename':'/dirlist.php'} )

# soup  = BeautifulSoup(r.text, 'html.parser')
# print(soup.prettify())

session = HTMLSession()

r = session.get(base_url, headers=headers) 
bruh = r.html.find('#dirlist', first=True)
#print(r.html.render())
print(bruh)