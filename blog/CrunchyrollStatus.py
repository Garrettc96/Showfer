from bs4 import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "http://www.crunchyroll.com/oreimo"

def get_status():
 try:
  html = urlopen('http://www.crunchyroll.com/oreimo')
  soup = BeautifulSoup(html, "html.parser")
  name = soup.title.string
  print("HI")
  if name[-1:] == "e":
	return 1;
  
  return 0;
 except Exception:
  return -1;
  pass
value = get_status()
print(value)
