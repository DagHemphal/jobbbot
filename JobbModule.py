import requests
import time
import os
import config
from bs4 import BeautifulSoup
from selenium import webdriver

cv_svenska = os.getcwd()+"\\cv-svenska.pdf"

class Academicwork:
	def __init__(self, driver):
		self.driver = driver
		self.logged_in = False

	def send_cv(self, href, title):
		self.driver.get(href)
		time.sleep(4)

		#todo: gör kontroll ifall cv ska vara på svenska eller engelska

		#klicka på acceptera cookies
		if (not self.logged_in):
			self.driver.find_element_by_css_selector('#onetrust-accept-btn-handler').click()

		time.sleep(1)

		#klicka på ansök
		self.driver.find_elements_by_css_selector('.aw-block-button')[1].click()

		#log in
		if (not self.logged_in):
			self.driver.find_element_by_name('Username').send_keys(config.email)
			self.driver.find_element_by_name('Password').send_keys(config.AcademicWork.password)
			self.driver.find_element_by_css_selector('#login-btn').click()
			self.logged_in = True
		time.sleep(3)
		#lägg till cv
		self.driver.find_element_by_name('UploadCv').send_keys(cv_svenska)

class Skill:
	def __init__(self, driver):
		self.driver = driver
		self.cookies_clicked = False

	def send_cv(self, href, title):
		self.driver.get(href)
		if not self.cookies_clicked:
			self.driver.find_element_by_css_selector(".coi-banner__accept").click()
			self.cookies_clicked = True
		time.sleep(1)


class Other:
	def __init__(self, driver):
		self.driver = driver
		self.skill = Skill(self.driver)

	def send_cv(self, href, title):
		self.driver.get(href)	
		time.sleep(1)
		#skill
		if self.driver.find_elements_by_css_selector(".col-6.text-right a"):
			print("skill")
			a = self.driver.find_element_by_css_selector(".col-6.text-right a")
			self.skill.send_cv(a.get_attribute('href'), title)

		#varbi
		if self.driver.find_elements_by_css_selector(".apply-button"):
			if self.driver.find_elements_by_css_selector(".btn-cookie-warning"):
				self.driver.find_element_by_css_selector(".btn-cookie-warning").click()
			print(self.driver.find_elements_by_css_selector(".apply-button")[0])
			(self.driver.find_elements_by_css_selector(".apply-button")[1]).click()
			

		#lägg till cv
		if self.driver.find_elements_by_css_selector("input[type='file']"):
			print("cv input found!")
			self.driver.find_element_by_css_selector("input[type='file']").send_keys(cv_svenska)

		#Kontroll för automatiskt cv
		if self.driver.find_elements_by_name('resume'):
			time.sleep(4)
			self.driver.find_element_by_name('name').clear()
			self.driver.find_element_by_name('email').clear()
			self.driver.find_element_by_name('org').clear()
			self.driver.find_element_by_name('phone').clear()
			self.driver.find_element_by_name('urls[GitHub]').clear()
			self.driver.find_element_by_name('urls[GitHub]').send_keys(config.github)

		#lägg till namn om det finns
		if self.driver.find_elements_by_name('name'):
			self.driver.find_element_by_name('name').send_keys(config.first_name + " " + config.last_name)
		#lägg till förnamn om det finns input[name="goButton"]
		if self.driver.find_elements_by_css_selector('input[name=first_name]'):
			print("first_name")
			self.driver.find_element_by_css_selector('input[name=first_name]').send_keys(config.first_name)
		elif self.driver.find_elements_by_css_selector('input[name=firstname]'):
			print("firstname")
			self.driver.find_element_by_css_selector('input[name=firstname]').send_keys(config.first_name)
		elif self.driver.find_elements_by_css_selector('input[name=firstName]'):
			print("firstName")
			self.driver.find_element_by_css_selector('input[name=firstName]').send_keys(config.first_name)
		elif self.driver.find_elements_by_css_selector('input[name="candidate[first_name]"]'):
			self.driver.find_element_by_css_selector('input[name="candidate[first_name]"]').send_keys(config.first_name)
		

		#lägg till efternamn om det finns
		if self.driver.find_elements_by_css_selector('input[name=surname]'):
			self.driver.find_element_by_css_selector('input[name=surname]').send_keys(config.last_name)
		elif self.driver.find_elements_by_css_selector('input[name=surName]'):
			self.driver.find_element_by_css_selector('input[name=surName]').send_keys(config.last_name)
		elif self.driver.find_elements_by_css_selector('input[name=last_name]'):
			self.driver.find_element_by_css_selector('input[name=last_name]').send_keys(config.last_name)
		elif self.driver.find_elements_by_css_selector('input[name=lastname]'):
			self.driver.find_element_by_css_selector('input[name=lastname]').send_keys(config.last_name)
		elif self.driver.find_elements_by_css_selector('input[name="candidate[last_name]"]'):
			self.driver.find_element_by_css_selector('input[name="candidate[last_name]"]').send_keys(config.last_name)
			

		#lägg till email
		if self.driver.find_elements_by_css_selector('input[name=email]'):
			self.driver.find_element_by_css_selector('input[name=email]').send_keys(config.email)
		elif self.driver.find_elements_by_css_selector('input[name="candidate[email]"]'):
			self.driver.find_element_by_css_selector('input[name="candidate[email]"]').send_keys(config.email)
		

		#lägg till telefon
		if self.driver.find_elements_by_css_selector('input[name=mobile_phone]'):
			self.driver.find_element_by_css_selector('input[name=mobile_phone]').send_keys(config.phone)
		elif self.driver.find_elements_by_css_selector('input[name=mobilePhone]'):
			self.driver.find_element_by_css_selector('input[name=mobilePhone]').send_keys(config.phone)
		elif self.driver.find_elements_by_css_selector('input[name=phone]'):
			self.driver.find_element_by_css_selector('input[name=phone]').send_keys(config.phone)
		elif self.driver.find_elements_by_css_selector('.js-phone_number'):
			self.driver.find_element_by_css_selector('.js-phone_number').send_keys(config.phone)
		elif self.driver.find_elements_by_css_selector('input[name="candidate[phone]"]'):
			self.driver.find_element_by_css_selector('input[name="candidate[phone]"]').send_keys(config.phone)


class Blocketjobb:
	def __init__(self):
		self.page = 1
		#skapa fil ifall den inte finns
		self.write_to_files("", "")
		self.driver = webdriver.Firefox()
		self.academicwork = Academicwork(self.driver)
		self.other = Other(self.driver)

	#kontrollerar ifall jobbansökan redan har gjorts eller ska skippas
	def check_title(self, title):
		with open('title.txt') as f:
			return title in f.read()

	#Spara title och jobbets url
	def write_to_files(self, title, href):
		file = open('title.txt','a+')
		file.write(title+"\n")
		file.close()
		file = open('href.txt','a+')
		file.write(href+"\n")
		file.close()

	#funktion som kollar vad som ska göras med ansökan.
	def Ansokan(self, title, href):
		while(True):
			print("Ansökan skickad, skipad eller rejected")
			x = input("y = skickad, n = skip, x = reject\n")
			if (x == "y" or x == "Y"):
				self.write_to_files(title, href)
				break
			elif (x == "n" or x == "N"):
				break
			elif (x == "x" or x == "X"):
				self.write_to_files(title, href + " XXX")
				break
			print("skriv y, n eller x")


	def send_cv(self, href, title):
		#hämta ansöknins sida länk från blocket
		get = requests.get(href)
		html = BeautifulSoup(get.text,'html.parser')
		href_cv = "https://jobb.blocket.se" + html.find(class_=("ui column less-margin-top adwatch-container no-margin-bottom")).a.get('href')

		#Kontroll för vilken rykreterare det är för att veta hur den ska skicka in cv:et
		'''if href_cv.find('academic-work') != -1:
			self.academicwork.send_cv(href_cv)
			#sparar id och länk
			self.write_to_files(title, href)'''
			
		if href_cv.find('academic-work') == -1:
			self.other.send_cv(href_cv, title)
			#fråga vad som gjordes med ansökan
			self.Ansokan(title, href)
			

		

	def run(self):
		last = False
		while(not last):
			#get html sidan
			get = requests.get('https://jobb.blocket.se/lediga-jobb-i-linkoping/data-it:back-end-utvecklare/sida'+str(self.page)+'/?ks=regions.11&ks=scg.9033&ks=scg.9231&ks=scg.9236')
			html = BeautifulSoup(get.text,'html.parser')
			#hämta jobben
			jobitem = html.find_all(class_='job-item')

			#kollar ifall den inte hittade några job-item, därmed på sista sidan.
			if not jobitem:
				last = True 

			#gå igenom alla jobb
			#todo sortera bättre, tex ta bort chef roller, spel bolag med mera
			for job in jobitem:
				#leta efter title
				atag = job.find(class_="content").a
				title = atag.text
				if (not self.check_title(title)):
					href = atag.get('href')
					#print(title)
					#print(href)
					#skicka cv
					self.send_cv(href, title)
					
					
					
			#gå till nästa sida
			self.page += 1


#hjälp funktioner



