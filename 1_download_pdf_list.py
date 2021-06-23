# You heve to install requests and bs4 modules
# in you envirnment before you precceed the execution of this script

import os, time
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

def downloadFiles(URL=None):
	if URL == None:
		URL = "https://www.google.com/search?q=dummy+pdf+file+list&client=firefox-b-d&sxsrf=ALeKk03Acw61hJpCpB055T4duoPNpTNFEA%3A1624389381542&ei=BTfSYK_YIIr2gAatp7S4BQ&oq=dummy+pdf+file+list&gs_lcp=Cgdnd3Mtd2l6EAM6BwgAEEcQsANKBAhBGABQo01YqlNgo1ZoAnACeACAAYMDiAG3DZIBBTItNC4ymAEAoAEBqgEHZ3dzLXdpesgBCMABAQ&sclient=gws-wiz&ved=0ahUKEwjv7sCA-qvxAhUKO8AKHa0TDVcQ4dUDCA0&uact=5"

	# If there is no such folder, the script will create one automatically
	folder_location = r'pdf_files'
	if not os.path.exists(folder_location):
	    os.mkdir(folder_location)

	response = requests.get(URL)
	soup = BeautifulSoup(response.text, "html.parser")
	for link in soup.select("a[href$='.pdf']"):
	    # Name the pdf files using the last portion of each
	    # link which are unique in this case
	    filename = os.path.join(folder_location, link['href'].split('/')[-1])
	    with open(filename, 'wb') as f:
	        f.write(requests.get(urljoin(url, link['href'])).content)

	print('Done.')
if __name__== "__main__":
	path = input('Enter you link of the page which you want to download pdf files: ')
	downloadFiles(path)
