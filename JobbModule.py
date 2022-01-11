import requests
import time
import os
import config
from bs4 import BeautifulSoup
from selenium import webdriver


class Academicwork:
	def __init__(self):
		self.email = config.AcademicWork.username
		self.password = config.AcademicWork.password

	def send_cv(self, href):
		ff = webdriver.Firefox()
		ff.get(href)
		time.sleep(4)

		#gör kontroll ifall cv ska vara på svenska eller engelska
		cv = os.getcwd()+"\\cv-svenska.pdf"
		print(cv)

		#klicka på acceptera cookies
		ff.find_element_by_css_selector('#onetrust-accept-btn-handler').click()

		time.sleep(1)

		#klicka på ansök
		ff.find_elements_by_css_selector('.aw-block-button')[1].click()

		#log in
		ff.find_element_by_name('Username').send_keys(self.email)
		ff.find_element_by_name('Password').send_keys(self.password)
		ff.find_element_by_css_selector('#login-btn').click()
		time.sleep(3)
		#lägg till cv
		ff.find_element_by_name('UploadCv').send_keys(cv)


class Blocketjobb:
	def __init__(self):
		self.page = 1
		#skapa fil ifall den inte finns
		self.write_to_files("", "")

	#kontrollerar ifall jobbansökan redan har gjorts
	def check_id(self, id):
		with open('id.txt') as f:
			return id in f.read()
	
	#Spara id och jobbets url
	def write_to_files(self, id, href):
		file_id = open('id.txt','a+')
		file_id.write(id+"\n")
		file_id.close()
		file_id = open('href.txt','a+')
		file_id.write(href+"\n")
		file_id.close()

	def send_cv(self, href, id):
		#hämta ansöknins sida länk från blocket
		get = requests.get(href)
		html = BeautifulSoup(get.text,'html.parser')
		href_cv = "https://jobb.blocket.se" + html.find(class_=("ui column less-margin-top adwatch-container no-margin-bottom")).a.get('href')

		#Kontroll för vilken rykreterare det är för att veta hur den ska skicka in cv:et
		if href_cv.find('academic-work') != -1:
			Academicwork().send_cv(href_cv)
			#sparar id och länk
			self.write_to_files(id, href)

		#tests


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
			for job in jobitem:
				#leta efter id 
				id = job.find(class_="save_item")['data-id']
				if (not self.check_id(id)):
					href = job.find(class_="content").a.get('href')
					#skicka cv
					#self.send_cv(href, id)
					self.write_to_files(id, href)
					print(href)

			#gå till nästa sida
			self.page += 1
