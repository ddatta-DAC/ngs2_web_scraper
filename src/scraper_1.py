# ---------------------------------- #
'''
USAGE:
python scraper_1.py <num_pages to scrape> <keywords>

Data stored in  : Data/<keyword(s)>

'''

# ----------------------------------- #

import requests
import sys
import os
import urllib
import time
import subprocess
import os.path
import urllib
from bs4 import BeautifulSoup
import joblib



# ----------------------------------- #

data_dir = "../Data"
cite_seer_host = 'http://citeseerx.ist.psu.edu'
cwd = None
subdir = '.'
num_parallel_jobs = 40

# ------------------------------------ # 


def parse_query(str):
    return str.replace(' ', "+")


def clean_data(target_url):
    payload = {'url': target_url}
    url = "https://mercury.postlight.com/parser?"
    headers = {'api-key': 'zJzQQRYNqj9XiQTdKax1DxQXQUD9gf96jtAD1w6v'}
    data = requests.get(url, headers=headers, params=payload)
    print data.url
    print data.content


def get_pdf(url):
    data = requests.get(url)
    soup = BeautifulSoup(data.content)

    try:
        links_div = soup.find("ul", {"id": "dlinks"})
        links = links_div.find_all("a")
        for l in links:
            pdf_link = l.get('href')
            if 'pdf' in pdf_link:
                print pdf_link
                return pdf_link;
    except:
        print " 	[ERROR] in getting pdf link!"
        print " url " + url
        return None



def setup_dirs():
	global data_dir,subdir,cwd
	
	cwd = os.getcwd()
		
	if not os.path.exists(data_dir):
		os.makedirs(data_dir)
	os.chdir(data_dir)
	print os.getcwd()
	if not os.path.exists(subdir):
		os.makedirs(subdir)
	os.chdir(subdir)
	print os.getcwd()
	os.chdir(cwd)
	
	return



def process_single_div(div_data):
	global data_dir,cite_seer_hosti,cwd,subdir

	soup = BeautifulSoup('<html>' + str(div_data) + '</html>')
	a = soup.find("a", {"class": "remove doc_details"})
	link = cite_seer_host + a['href']
	pdf_link = get_pdf(link)
    
	print 'PDF LINK ' , pdf_link 
 
    #check link is valid before downloading
	if pdf_link is None:
		return;
	
	try:
		cwd = os.getcwd()
		target_dir = data_dir + '/' + subdir 
		os.chdir(target_dir)
		
		filename = str(time.time()) + '.pdf'
		urllib.urlretrieve(pdf_link, filename)
		print filename
   		
		if os.path.isfile(filename):
			cmd = "pdftotext " + filename
			subprocess.call( cmd, stdout = open(os.devnull, 'wb') )
			os.remove(filename)
		
	except:
		print "		[ERROR] in getting and processing file file!"

	finally:
		os.chdir(cwd)



def getCiteSeerOnePage(query, page=0):
	global cite_seer_host
	try:
		start = page * 10
		url = "http://citeseerx.ist.psu.edu/search?"
		payload = {'t': 'doc', 'sort': 'rlv', 'start': start, 'q': query}
	
		data = requests.get(url, params=payload)
		print 'URL :', data.url
	
		if data.status_code != 200 :
			print '     [ERROR]  non 200 status code!!!! ' , data.url
			return False
	
		soup = BeautifulSoup(data.content)
		div_data = soup.find_all("div", {"class": "result"})
 
		for z in div_data:
			process_single_div(z)
	except:
		print '[ERROR]'
		return False

	return True


# ------------------------ # 


# ------------------------ # 


num_pages = 2
query = "+".join(sys.argv[2:])
subdir = "_".join(sys.argv[2:])
num_pages = int(sys.argv[1])
setup_dirs()

print '-- ', subdir
print 'QUERY :' + query

for i in range(num_pages):
	print '-----> Page :: ', i+1
	boolResult = getCiteSeerOnePage(query,i);
	if not boolResult:
		print '		[ERROR]  non 200 status code!!!! '	
		break;




