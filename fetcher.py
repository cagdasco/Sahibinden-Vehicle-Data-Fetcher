#!/usr/bin/env python
from bs4 import BeautifulSoup
from urllib.request import urlopen
from lxml.html import parse
import sys,os,time,glob,subprocess,re,datetime,hues
import pandas as pd
import csv

ids_real, ids_temp, ids_new = [],[],[]
urls_real, urls_temp, urls_new = [],[],[]
url = 'https://www.sahibinden.com/otomobil?viewType=List&pagingSize=50&sorting=date_desc'

Title = None
ID = None
Price = None
Currency = None
LocationCity = None
LocationCounty = None
LocationDistrict = None
LocationLatitude = None
LocationLongitude = None
Date = None
Brand = None
Series = None
Model = None
Fuel = None
Year = None
Gear = None
Km = None
FrameType =  None
EngineVolume = None
HorsePower = None
DriveType = None
Color = None
Warranty = None
Plate = None
Status = None
SalerType = None
Exchange = None

def clearHTML():
	files = glob.glob(os.path.dirname(os.path.realpath(__file__)) + '/html/*.html')
	for file in files:
		os.remove(file)

	files = glob.glob(os.path.dirname(os.path.realpath(__file__)) + '/html/single/*.html')
	for file in files:
		os.remove(file)

def fetchSinglePage(url):
	now = datetime.datetime.now()
	filename = 'single-' + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond) + '.html'
	filepath = os.path.dirname(os.path.realpath(__file__)) + '/html/single/' + filename
	command = 'wget -O ' + filepath + ' \"' + url + '\"'
	subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
	if os.stat(filepath).st_size == 0:
		hues.error(filename + ' IS NOT DOWNLOADED')
	else:
		pass
		#hues.success(filename + ' DOWNLOADED')
	return

def fetchArchivePage(url):
	now = datetime.datetime.now()
	filename = 'archive-' + str(now.hour) + str(now.minute) + str(now.second) + str(now.microsecond) + '.html'
	filepath = os.path.dirname(os.path.realpath(__file__)) + '/html/' + filename
	#page = urlopen(url).read()
	#soup = BeautifulSoup(page, 'lxml')
	#print(soup)
	command = 'wget -O ' + filepath + ' \"' + url + '\"'
	subprocess.Popen(command,shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.read()
	if os.stat(filepath).st_size == 0:
		hues.error(filename + ' IS NOT DOWNLOADED')
	else:
		pass
		#hues.success(filename + ' DOWNLOADED')
	return

def searchSingle(filepath):
	global Title
	global ID
	global Price
	global Currency
	global LocationCity
	global LocationCounty
	global LocationDistrict
	global LocationLatitude
	global LocationLongitude
	global Date
	global Brand
	global Series
	global Model
	global Fuel
	global Year
	global Gear
	global Km
	global FrameType
	global EngineVolume
	global HorsePower
	global DriveType
	global Color
	global Warranty
	global Plate
	global Status
	global SalerType
	global Exchange

	#files = glob.glob('html/single/*.html')
	#soup = BeautifulSoup(open(files[0],encoding="utf-8"), 'lxml')
	soup = BeautifulSoup(open(filepath,encoding="utf-8"), 'lxml')

	#soup = BeautifulSoup(urlopen(url), 'lxml')
	# Title Div
	rows = soup.findAll("div", { "class" : "classifiedDetailTitle" })
	rows_string = str(rows).split('\n')

	# Data Table
	rows2 = soup.findAll("div", { "class" : "classifiedInfo" })
	rows_string2 = str(rows2).split('\n')

	# Location
	rows3 = soup.find("div", { "id" : "gmap" })
	if rows3:
		LocationLatitude, LocationLongitude = rows3.attrs['data-lat'], rows3.attrs['data-lon']
	else:
		LocationLatitude = 'Unknown'
		LocationLongitude = 'Unknown'

	#Title = soup.title.string
	Title = rows_string[1]
	Price = rows_string2[2]
	LocationCity = rows_string2[6]
	LocationCounty = rows_string2[9]
	LocationDistrict = rows_string2[12]
	ID = rows_string2[16]
	Date = rows_string2[22]
	Brand = rows_string2[26]
	Series = rows_string2[30]
	Model = rows_string2[34]
	Fuel = rows_string2[44]
	Year = rows_string2[39]
	Gear = rows_string2[49]
	Km = rows_string2[54]
	FrameType = rows_string2[59]
	EngineVolume = rows_string2[64]
	HorsePower = rows_string2[69]
	DriveType = rows_string2[74]
	Color = rows_string2[79]
	Warranty = rows_string2[84]
	Plate = rows_string2[89]
	Status = rows_string2[105]
	SalerType = rows_string2[94]
	Exchange = rows_string2[99]

	#hues.info(filepath + ' DELETED')
	#os.remove(filepath)

def searchArchive():
	global ids_temp
	global urls_temp

	hues.info('SCANNING ARCHIVE')

	files = glob.glob(os.path.dirname(os.path.realpath(__file__)) + '/html/*.html')
	soup = BeautifulSoup(open(files[0],encoding="utf-8"), 'lxml')
	rows = soup.findAll("tr", attrs={"class":"searchResultsItem"})

	for row in rows:
		rows_string = str(row).split('\n')

		# Find the ID of the Ad
		id = re.findall('data-id=\"(.*?)\">', rows_string[0], re.DOTALL) 
		ids_cleaned = str(id).replace('[\'', '')
		ids_cleaned = ids_cleaned.replace('\']', '')
		ids_temp.append(int(ids_cleaned))

		# Find & Clear the URL
		url = re.findall('/ilan/(.*?)/detay', rows_string[2], re.DOTALL)
		url_string = str(url[0]).replace('[', '')
		url_string = str(url[0]).replace(']', '')
		#urls = 'https://www.sahibinden.com/ilan/' + url_string + '/detay'
		urls_temp.append('https://www.sahibinden.com/ilan/' + url_string + '/detay')

def clearData():
	global Title
	global ID
	global Price
	global Currency
	global LocationCity
	global LocationCounty
	global LocationDistrict
	global LocationLatitude
	global LocationLongitude
	global Date
	global Brand
	global Series
	global Model
	global Type
	global Fuel
	global Year
	global Gear
	global Km
	global FrameType
	global EngineVolume
	global HorsePower
	global DriveType
	global Color
	global Warranty
	global Plate
	global Status
	global SalerType
	global Status
	global Exchange

	Title = Title.replace(',',' ')
	Title = Title.replace('<h1>', '')
	Title = Title.replace('</h1>', '')
	if '&amp;' in Title:
		Title = Title.replace('&amp;', '&')
	if '\"' in Title:
		Title = Title.replace('\"', ' ')

	ID = ID.replace('<span class="classifiedId" id="classifiedId">', '')
	ID = ID.strip('</span>')
	ID = int(ID.lstrip())

	Price = Price.replace('<a class="emlak-endeksi-link trackClick trackId_emlak-endeksi-link" href="javascript:;" id="emlakEndeksiLink" style="cursor:pointer">Emlak Endeksi</a>', '')
	Price = Price.lstrip()

	if 'TL' in Price:
		Currency = 'Turkish Lira'
	elif '$' in Price:
		Currency = 'US Dollar'
	elif '€' in Price:
		Currency = 'Euro'
	elif '₤' in Price:
		Currency = 'British Pound'

	Price = list(filter(str.isdigit, Price))
	Price = ''.join(Price)

	LocationCity = LocationCity.replace('</a>', '')
	LocationCity = LocationCity.lstrip()

	LocationCounty = LocationCounty.replace('</a>', '')
	LocationCounty = LocationCounty.lstrip()

	LocationDistrict = LocationDistrict.replace('</a>', '')
	LocationDistrict = LocationDistrict.lstrip()

	Date = Date.replace('</span>', '')
	Date = Date.lstrip()
	date_dump = str(Date).split(' ')
	if 'Ocak' in date_dump[1]:
		date_month = '01'
	elif 'Şubat' in date_dump[1]:
		date_month = '02'
	elif 'Mart' in date_dump[1]:
		date_month = '03'
	elif 'Nisan' in date_dump[1]:
		date_month = '04'
	elif 'Mayis' in date_dump[1]:
		date_month = '05'
	elif 'Haziran' in date_dump[1]:
		date_month = '06'
	elif 'Temmuz' in date_dump[1]:
		date_month = '07'
	elif 'Ağustos' in date_dump[1]:
		date_month = '08'
	elif 'Eylül' in date_dump[1]:
		date_month = '09'
	elif 'Ekim' in date_dump[1]:
		date_month = '10'
	elif 'Kasim' in date_dump[1]:
		date_month = '11'
	elif 'Aralik' in date_dump[1]:
		date_month = '12'
	Date = date_dump[2] + '-' + date_month + '-' + date_dump[0]

	Km = Km.replace('</span>', '')
	if 'Belirtilmemiş' in Km:
		Km = 'Unknown'
	else:
		Km = Km.lstrip()
		Km = Km.replace('.','')

	Brand = Brand.replace('<span>', '')
	Brand = Brand.replace('</span>', '')
	Brand = Brand.lstrip()
	Brand = Brand.rstrip()

	Series = Series.replace('<span>', '')
	Series = Series.replace('</span>', '')
	Series = Series.lstrip()
	Series = Series.rstrip()

	Model = Model.replace('<span>', '')
	Model = Model.replace('</span>', '')
	Model = Model.lstrip()
	Model = Model.rstrip()

	Year = Year.replace('</span>', '')
	Year = int(Year.lstrip())

	if 'Benzin' in Fuel:
		Fuel = 'Gas'
	elif 'LPG' in  Fuel:
		Fuel = 'Gas & LPG'
	elif 'Dizel' in Fuel:
		Fuel = 'Diesel'
	elif 'Hybrid' in Fuel:
		Fuel = 'Hybrid'

	if 'Manuel' in Gear:
		Gear = 'Manuel'
	elif 'Yarı Otomatik' in Gear:
		Gear = 'Semi Automatic'
	elif 'Otomatik' in Gear:
		Gear = 'Automatic'

	if 'Cabrio' in FrameType:
		FrameType = 'Cabrio'
	elif 'Coupe' in FrameType:
		FrameType = 'Coupe'
	elif 'Hatchback 3 kapı' in FrameType:
		FrameType = 'Hatchback 3 Doors'
	elif 'Hatchback 5 kapı' in FrameType:
		FrameType = 'Hatchback 5 Doors'
	elif 'Sedan' in FrameType:
		FrameType = 'Sedan'
	elif 'Station Wagon' in FrameType:
		FrameType = 'Station Wagon'
	elif 'Crossover' in FrameType:
		FrameType = 'Crossover'
	elif 'MPV' in FrameType:
		FrameType = 'MPV'
	elif 'Roadster' in FrameType:
		FrameType = 'Roadster'

	EngineVolume = EngineVolume.replace('cc', '')
	EngineVolume = EngineVolume.replace('</span>', '')
	EngineVolume = EngineVolume.lstrip()
	EngineVolume = EngineVolume.rstrip()

	HorsePower = HorsePower.replace('hp', '')
	HorsePower = HorsePower.replace('</span>', '')
	HorsePower = HorsePower.lstrip()
	HorsePower = HorsePower.rstrip()

	if 'Önden' in DriveType:
		DriveType = 'Front Drive'
	elif 'Arkadan' in DriveType:
		DriveType = 'Rear Drive'
	elif '4WD' in DriveType:
		DriveType = 'Four-Wheel Drive (4WD)'
	elif 'AWD' in DriveType:
		DriveType = 'All-Wheel Drive (AWD)'

	if 'Bej' in Color:
		Color = 'Beige'
	elif 'Beyaz' in Color:
		Color = 'White'
	elif 'Bordo' in Color:
		Color = 'Claret Red'
	elif 'Füme' in Color:
		Color = 'Smoked'
	elif 'Gri' in Color:
		Color = 'Grey'
	elif 'Gümüş Gri' in Color:
		Color = 'Silver Grey'
	elif 'Kahverengi' in Color:
		Color = 'Brown'
	elif 'Kırmızı' in Color:
		Color = 'Red'
	elif 'Lacivert' in Color:
		Color = 'Navy Blue'
	elif 'Mavi' in Color:
		Color = 'Blur'
	elif 'Mor' in Color:
		Color = 'Purple'
	elif 'Pembe' in Color:
		Color = 'pink'
	elif 'Sarı' in Color:
		Color = 'Yellow'
	elif 'Siyah' in Color:
		Color = 'Black'
	elif 'Şampanya' in Color:
		Color = 'Champagne'
	elif 'Turkuaz' in Color:
		Color = 'Turquoise'
	elif 'Turuncu' in Color:
		Color = 'Orange'
	elif 'Yeşil' in Color:
		Color = 'Green'

	if 'Evet' in Warranty:
		Warranty = True
	elif 'Hayır' in Warranty:
		Warranty = False

	if 'Türkiye (TR) Plakalı' in Plate:
		Plate = 'Turkish Plate'
	elif 'Yabancı Plakalı' in Plate:
		Plate = 'Foreign Plate'
	elif 'Mavi (MA) Plakalı' in Plate:
		Plate = 'Blue Plate'

	if 'Sahibinden' in SalerType:
		SalerType = 'Owner'
	elif 'Galeriden' in SalerType:
		SalerType = 'Gallery'
	elif 'Yetkili Bayiden' in SalerType:
		SalerType = 'Authorized Dealer'

	if 'Sıfır' in Status:
		Status = 'New'
	elif 'İkinci El' in Status:
		Status = 'Second Hand'

	if 'Hayır' in Exchange:
		Exchange = False
	elif 'Evet' in Exchange:
		Exchange = True

def showData():
	print('Title: ' + Title)
	print('ID: ' + str(ID))
	print('Price: ' + str(Price))
	print('Currency: ' + str(Currency))
	print('City: ' + LocationCity)
	print('County: ' + LocationCounty)
	print('District: ' + LocationDistrict)
	print('Latitude: ' + str(LocationLatitude))
	print('Longitude: ' + str(LocationLongitude))
	print('Date: ' + Date)
	print('Brand: ' + Brand)
	print('Series: ' + Series)
	print('Model: ' + Model)
	print('Year: ' + str(Year))
	print('Fuel: ' + Fuel)
	print('Gear: ' + Gear)
	print('Km: ' + str(Km))
	print('Frame Type: ' + FrameType)
	print('Engine Volume: ' + EngineVolume)
	print('Horse Power: ' + HorsePower)
	print('Drive Type: ' + DriveType)
	print('Color: ' + Color)
	print('Warranty: ' + str(Warranty))
	print('Plate: ' + Plate)
	print('Saler: '+ SalerType)
	print('Status: ' + Status)
	print('Exchange: ' + str(Exchange))

def loadCSV():
	global ids_real
	global urls_real

	# Load real data from id_url
	data_real = pd.read_csv(os.path.dirname(os.path.realpath(__file__)) + '/inc/id_url.csv', names=['id','url'])
	for x in data_real.id:
		ids_real.append(x)
	for x in data_real.url:
		urls_real.append(x)

	#hues.info('REAL DATA LOADED')

def compareCSV():
	global ids_new
	global urls_new
	global ids_temp
	global urls_temp
	global ids_real
	global urls_real

	# Compare _temp and _real
	ids_new = [x for x in ids_temp if x not in ids_real]
	urls_new = [x for x in urls_temp if x not in urls_real]
	if ids_new:
		hues.info('NEW ID COUNT: ' + str(len(ids_new)))
	elif not ids_new:
		hues.warn('NO NEW ID')

def writeToCSV():
	global Title
	global ID
	global Price
	global Currency
	global LocationCity
	global LocationCounty
	global LocationDistrict
	global LocationLatitude
	global LocationLongitude
	global Date
	global Brand
	global Series
	global Model
	global Fuel
	global Year
	global Gear
	global Km
	global FrameType
	global EngineVolume
	global HorsePower
	global DriveType
	global Color
	global Warranty
	global Plate
	global Status
	global SalerType
	global Status
	global Exchange

	WriteMe = Title + ',' + str(ID)+ ',' + str(Price) + ',' + Currency + ',' + LocationCity + ',' + LocationCounty + ',' + LocationDistrict + ',' + str(LocationLatitude) + ',' + str(LocationLongitude) + ',' + Date + ',' + Brand + ',' + Series + ',' + Model + ',' + Fuel + ',' + str(Year) + ',' + Gear + ',' + str(Km) + ',' + FrameType + ',' + EngineVolume + ',' + HorsePower + ',' + DriveType + ',' + Color + ',' + str(Warranty) + ',' + Plate + ',' + SalerType + ',' + Status + ',' + str(Exchange)
	File = open(os.path.dirname(os.path.realpath(__file__)) + '/inc/vehicle_data.csv','a', encoding="utf-8") # 'a' parameter for append, 'w' for overwrite
	File.write(WriteMe + '\n')
	File.close()

	hues.success('VEHICLE DATA HAS BEEN WRITTEN to inc/vehicle_data.csv')

def writeNew():
	global ids_new
	global urls_new

	if ids_new:
		f = open(os.path.dirname(os.path.realpath(__file__)) + '/inc/id_url.csv', 'a')
		for i in range(0,len(ids_new)):
 	  		f.write("{},{}\n".format(ids_new[i], urls_new[i]))
		f.close()
		hues.success('ID URL DATA HAS BEEN WRITTEN to inc/id_url.csv')

def vehicle_data():
	files = glob.glob(os.path.dirname(os.path.realpath(__file__)) + '/html/single/*.html')
	for file in files:
		if os.stat(file).st_size == 0:
			#print(file + ' IS NOT DOWNLOADED')
			pass
		else:
			searchSingle(file)
			clearData()
			showData()
			writeToCSV()

def clearSYSTEM():
	global ids_new
	global ids_temp
	global ids_real
	global urls_new
	global urls_temp
	global urls_real

	clearHTML()
	ids_new.clear()
	ids_temp.clear()
	ids_real.clear()
	urls_new.clear()
	urls_temp.clear()
	urls_real.clear()
	#hues.info('SYSTEM CLEANED')

def automator(url):
	# 0 - Clear html files
	clearHTML()

	# 1 - Load CSV to _real
	loadCSV()

	# 2 - Download archive.html
	fetchArchivePage(url)

	# 3 - Load IDs & URLs to _temp
	searchArchive()

	# 4 - Compare _temp & _real, write new ones to _new
	compareCSV()

	# 5 - Fetch new single pages
	#hues.info('AD PAGES DOWNLOADING')
	for urls in urls_new:
		fetchSinglePage(urls)
		#print('New Ad ID: ' + str(row_temp))
		#print('URL: ' + urls_temp[x])
	
	# 5.1 - IDs & URLs to vehicle_data.csv
	vehicle_data()

	# 5.2 - Write _new to id_url.csv
	writeNew()

	# 6 - Delete archive.html & single.html, Clear _new and _temp
	clearSYSTEM()

if __name__ == '__main__':
	while True:
		#automator(url)
		for x in range(1,951):
			if float(x % 50) == 0:
				hues.info('PAGE: ' + str(int(x / 50)))
				automator('https://www.sahibinden.com/otomobil?viewType=List&pagingOffset=' + str(x) + '&pagingSize=50&sorting=date_desc')
		hues.info('SLEEPING')
		time.sleep(900) # 15 min
