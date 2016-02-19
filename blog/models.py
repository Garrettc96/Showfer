from django.db import models
from django.utils import timezone
import datetime
from bs4 import BeautifulSoup
import urllib2
import urllib
import sys
import re
from mechanize import Browser
import cookielib
from tmdb3 import set_key
from tmdb3 import searchMovie
from tmdb3 import searchSeries
from tmdb3 import searchMovieWithYear
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time
from pyvirtualdisplay import Display

now = datetime.datetime.now()
# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Anime(models.Model):
    title = models.TextField()
    crunchy = models.BooleanField()
    hulu = models.BooleanField()
    netflix = models.BooleanField()
    funi = models.BooleanField()
    image = models.ImageField(upload_to = 'blog/media', null = True)

    def __str__(self):
        return self.title
    def similar (self):
      site = "http://usa.netflixable.com/2016/01/complete-alphabetical-list-sat-jan-2.html#uds-search-results"
      hdr = {'User-Agent': 'Mozilla/5.0'}
      req = urllib2.Request(site,headers=hdr)
      page = urllib2.urlopen(req)
      soup = BeautifulSoup(page, "lxml")
      shows = []

      for a in soup.find_all('b'):
        
        text = a.text
        print(text)
        #The text has the year included and some suffixes that follow a '-'. This gets rid of that, leaving only the title
       # if(text.find('(') != -1):
          #text = text[0:text.find('(')]
        if (text.find('-') != -1):
          if (text[text.find('-') + 1] != " "):
            text =text
          else:
            print('hey')
            text = text[0:text.find('-')]
        if (text.find(',') != -1 and text.find(',') != len(text)):
          print(text + "rawr")
          print (text[text.find(','):])
          print (len(text[text.find(','):]))
          if (len(text[text.find(','):]) <= 6):
            
            
            temp = text[text.find(',') + 2: len(text)]
            text = text[0: text.find(',')]
            text = temp + text
            text.strip();
            print(text)
        shows.append(text)
      return shows
      # Downloads the image for a particular title.
    def setImage(self,name):
      print('huh')
      try:
        print('eh')
        driver = webdriver.Firefox()
        print('fh')
        driver.get("https://www.google.com/imghp")
        time.sleep(0.3)
        search = driver.find_element_by_id('lst-ib')
        print('arg')
        search.send_keys(name + " poster")
        print('arg2')
        #search.send_keys(Keys.ENTER)
        print('arg3')
        time.sleep(2.3)
        print('frat')
        image = driver.find_element_by_xpath('/html/body/div[5]/div[4]/div[2]/div[3]/div/div[2]/div[2]/div/div/div/div/div[1]/div[1]/div[1]/div[1]/a/img')
        print('g')
        src = image.get_attribute('src')
        print('gotz')
        urllib.urlretrieve(src, 'blog/media/posters/'+name.replace(" ","")+".jpeg")
        driver.close()
        return 1;
      except Exception:
        print('image failed')
        driver.close()
        return -1;
    """
    def setImage(self, name):
      set_key('c799d173f73d9b215cd654fa87fe9c73')

      try:

       # movie = searchMovieWithYear(name + '(' + year + ')')
        movie = searchMovieWithYear(name)
        print('here1')
        series = searchSeries(name)
        print (series)
        print('here')
        test = movie[0]
        for m in movie:
          if abs(len(m.title) - len(name)) <= 1 :
            test = m
        for s in series:
          if abs(len(s.name) - len(name)) <= 1 :
            test = s
        print (test)
        p = test.poster
        urllib.urlretrieve(p.geturl('w185'), 'blog/media/posters/' + name + ".jpeg")
        print ('here/////////////')
        return 0;
      except:
        print('error getting image')
        return -1;
    """
        #Gets all entries in database with input
    def contains(self, name):
      print("/////")
      all_entries = Anime.objects.filter(title__icontains = name)
      return all_entries
      #Checks if there is an entry with input
    def exists(self, name):
      print(name)
      found = Anime.objects.filter(title = name)
      if (len(found) > 0):
        print('1')
        return true
      print('2')
      return false
    def setCrunch(self):
      crunchy = True
    def setHulu(self):
      hulu = True
    def setNetflix(self):
      netflix = True
    def publish(self):
        self.save()
    def setTitle(self,st):
      self.title = st
    def getTitle(self):
        return self.title
        #Finds if show is on crunchyroll

    def findOnCR(self):
      shows = []
      try:
        r = open('shows', 'ab')
        r.write('crunchyroll\n')
        driver = webdriver.Firefox()
        driver.get("http://www.crunchyroll.com/videos/anime/alpha?group=all")
        time.sleep(0.3)
        #/html/body/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[1]/ul[1]/li/a
        #/html/body/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[1]
        #/html/body/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[1]/ul[4]/li[4]
        left = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[1]')
        right = driver.find_element_by_xpath('/html/body/div/div[2]/div/div[3]/div[2]/div[1]/div[2]/div[2]')        
        children = list(left.find_elements_by_xpath('.//*'))
        rchildren = right.find_elements_by_xpath('.//*')
        #print(children)
        for ul in children:
          children2 = ul.find_elements_by_xpath('.//*')

          for li in children2:

            print("************")
            print(li.text)
            shows.append(li.text)
            temp = li.text + '\n'
            r.write(temp.encode('utf8'))
        for ul in rchildren:
          rchildren2 = ul.find_elements_by_xpath('.//*')
          for li in rchildren2:
            print("************")
            print(li.text)
            temp = li.text + '\n'
            shows.append(li.text)
            r.write(temp.encode('utf8'))
        driver.quit()
        r.close()
        return shows
      except Exception:
        print('I failed :(')
        r.close()
        return shows
     

    def findOnNetflix(self):
      shows = []
      driver = webdriver.Firefox()
     
      try:
        print('eh')
        r = open('shows', 'a')
        r.write("netflix\n")
        driver.get("http://www.allflicks.net/")
        time.sleep(5)
        print('eh2')                            
        nextPage = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/div[3]/div/div[5]/a[3]')      
        print('test')
        driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/div[3]/div/div[1]/label/select/option[4]').click()
        x = 1
        while (x != 57):
          
          for i in range(1,101):
            table = driver.find_element_by_xpath(' /html/body/div[4]/div/div/div[1]/div[1]/div[3]/div/table/tbody/tr[' + str(i) + ']/td[2]/a')
            print(table.text)
            print(i)
            shows.append(table.text)
            temp = table.text + '\n'
            r.write(temp.encode('utf8'))
          print('eh?')
          x+= 1
          nextPage = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/div[3]/div/div[5]/a[3]')
          nextPage.click()
          time.sleep(1)
        driver.quit()
        r.close()
        return shows
      except Exception:
        print('netflix failed')
        driver.quit()
        r.close()
      return shows
    def findOnHulu(self):
     
      #display = Display(visible=0, size=(800, 600))
      #display.start()
      #Shows
      shows = []
      r = open('shows', 'a')
      r.write('hulu\n')
      driver = webdriver.Firefox()
      driver.get("http://somethingtostream.com/hulu/shows/")
      time.sleep(5)
      nextPage = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/div[2]/div/div[5]/a[3]')
      driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/div[2]/div/div[1]/label/select/option[4]').click()
      #time.sleep(5)      
      print('test')
      done = False;
      x = 1
      try:
        while (x != 42):
          
          for i in range(1,101):
            table = driver.find_element_by_xpath(' /html/body/div[4]/div/div/div[1]/div[1]/div[2]/div/table/tbody/tr[' + str(i) + ']/td[2]/a')
            print(table.text)
            print(i)
            shows.append(table.text)
            temp = table.text + '\n'
            r.write(temp.encode('utf8'))
          print('eh?')
          x+= 1
          nextPage = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/div[2]/div/div[5]/a[3]')
          nextPage.click()
          time.sleep(2)
        #movies   
       
        driver.quit()
      except Exception:
       try:
        driver.get("http://somethingtostream.com/hulu/")
        time.sleep(0.3)
        nextPage = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/div[2]/div/div[5]/a[3]')
        driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/div[2]/div/div[1]/label/select/option[4]').click()
        #time.sleep(5)      
        print('test')
        done = False;
        x = 1
        while (x != 78):
          
          for i in range(1,101):
            table = driver.find_element_by_xpath(' /html/body/div[4]/div/div/div[1]/div[1]/div[2]/div/table/tbody/tr[' + str(i) + ']/td[2]/a')
            print(table.text)
            print(i)
            shows.append(table.text)
            temp = table.text + '\n'
            r.write(temp.encode('utf8'))
          print('eh?')
          x+= 1
          nextPage = driver.find_element_by_xpath('/html/body/div[4]/div/div/div[1]/div[1]/div[2]/div/div[5]/a[3]')
          nextPage.click()
          time.sleep(2)      
        r.close()
        driver.quit()
        return shows
       except Exception:
         driver.quit()
         r.close() 
         return shows
      """
      try:
        site = "http://somethingtostream.com/hulu/shows/"
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(site,headers=hdr)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page, "lxml")
        print("eh1")
        br = Browser()
        print("eh2")
        end = False
        br.addheaders = [('User-agent', 'Firefox')]
        br.open("http://somethingtostream.com/hulu/shows/")
        print("eh3")
        while (end == False):
           a = soup.find("a", class_= "paginate_button next")
           print('eh4')
           br.click_link(a)
           print('eh5')
           soup2 = BeautifulSoup(br.response().read())
           test = soup2.findAll('tr')
           print('eh6')
           table = soup.find('table',id = 'shows')
           print(table)
           tablebody = table.find('tbody')
           print('rawr2')
           rows = soup.findAll('tr')
           print('rawr3')
           for row in rows:
              print ("eh7")
              cols =  (row.findAll('td'))
              print(row)
              print("eh8")
           print(soup.findAll("tr"))
           end = True
      except Exception:
        print('Hulu failed :(')
      """
             
    """
    def findOnCR(self,name):
     try:
        
        
        site= "https://www.crunchyroll.com/" + name
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(site,headers=hdr)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page, "lxml")
        name = soup.title.string   
        if (name[-1] == "e"):
          print("CR made it")
          return True;
        return True;
     except Exception:
        return False;
        pass
    def name(self):
        return title
        #Finds if show is on hulu
    def findOnHulu(self, name):
     try:
        
        
        site= "https://www.hulu.com/" + name
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = urllib2.Request(site,headers=hdr)
        page = urllib2.urlopen(req)
        soup = BeautifulSoup(page,"lxml")
        name = soup.title.string   
        if (name[-1] == "u"):
          print("hulu made it")
          return True;
        return True;
     except Exception:
        return False;
        pass
    def name(self):
        return title
    """