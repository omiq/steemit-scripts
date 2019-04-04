from bs4 import BeautifulSoup
from sys import exit
import re
import urllib.request
import shutil

url = "https://www.instagram.com/unwrappedyarn/"

response = urllib.request.urlopen(url)
html = response.read()
fancyHTML = BeautifulSoup(html, "html.parser")

metaContentTags = fancyHTML.select("meta[content]")
follower = 0
for tags in metaContentTags:
    strContent = tags.get("content").replace(",", "")

    if strContent.find("Follow") != -1:
        follower = int(re.findall(r'\d+', strContent)[0])

print(follower)