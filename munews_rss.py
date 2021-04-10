#Naser Haroon 
import requests
from bs4 import BeautifulSoup as bs
import datetime
import time
from email import utils


print("Naser Haroon")
link = input("Enter link : ")
page = requests.get(link) # requesting page
soup = bs(page.content, "html.parser")

title = soup.find("title").text
# to get all article element
articles = soup.find_all("article")



rss = soup.new_tag("rss", version="2.0") # creating new element
channel  = soup.new_tag("channel") # creating channel element

# create title element
title_tg = soup.new_tag("title")
title_tg.string = title

# create a link tag
link_tg = soup.new_tag("link")
link_tg.string = link

# create description for channel
description = soup.new_tag("description")

# creat atom:link for channel
#atom_link = soup.new_tag("atom:link", rel="self")


# add title and current link to channel
channel.append(title_tg)
channel.append(link_tg)
channel.append(description)
#channel.append(atom_link)


for article in articles:
	# creating item element
	item = soup.new_tag("item")
	# getting title
	title = article.find(class_="article-header").text
	# getting link
	link = article.find("a")["href"]
	# creating title element
	title_tg = soup.new_tag("title")
	# value to title element
	title_tg.string = title
	# link element
	link_tg = soup.new_tag("link")
	# value to link
	link_tg.string = link
	# attaching to item
	item.append(title_tg); 
	guid_tg = soup.new_tag("guid") # guid element
	guid_tg.string = link # link for value
	description_tg = soup.new_tag("description"); item.append(description_tg) # another tag
	pubDate = article.find(class_="article-meta").text # another date tag value from page
	y = datetime.datetime.strptime(pubDate.replace("\t","").replace("\r","").replace("\n",""), "%A, %B %d, %Y") # convert date to datetime
	pubDate = utils.format_datetime(y) # convert to RFC 822
	pubDate_tg = soup.new_tag("pubDate") # tag for date
	pubDate_tg.string = pubDate # value to tag
	item.append(guid_tg) # attach guid to item
	item.append(link_tg) # attach link to item
	item.append(pubDate_tg) # attach date to item
	channel.append(item) # attach item to channel



# add channel to rss
rss.append(channel)

# write to file
f = open("file.xml", "w")
f.write("<?xml version=\"1.0\"?>\n"+str(rss.prettify()))
f.close()
