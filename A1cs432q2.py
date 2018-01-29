import requests
import urllib.request
import re
import urllib

from bs4 import BeautifulSoup

webb = input('ENTER YOUR LINK:  ')
print('This is your link', webb)

r=requests.get(webb)

r.content

soup = BeautifulSoup(html,"lxml")
print(soup.find_all('a'))
