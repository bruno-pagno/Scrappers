from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

# Login into Workana

driver = webdriver.Firefox()
driver.get("https://www.workana.com/login")

driver.execute_script("$('.form-control')[1].value = 'Your Workana Email goes here'");
driver.execute_script("$('.form-control')[2].value = 'Your Workana Password goes here'");
driver.execute_script("document.forms[0].submit()");

pageNo = 1
count = 1
time.sleep(5)

projects = []

# Navigating pages and scrapping 
while True:
	driver.get('https://www.workana.com/jobs?ref=menu_projects_index&language=en%2Cpt&category=it-programming&page=' + str(pageNo))
	time.sleep(2)
	print('actual Page:', pageNo)
	soup = BeautifulSoup(driver.page_source, 'html.parser')

	# Verifying if the scrapper has ended
	if soup.find('img', {"class" : "img-responsive img center-block"}) :
		print('end of the scrapper')
		break

	
	# Scrapping Projects from the page
	project_divs = soup.find_all('div', {"class" : "project-item"})   # Find all div tags for projects
        for project in project_divs:
            print("Project {}".format(count))
            count = count+1

            title = project.find('h2', {"class" : "project-title"}).text
            link = project.find_all('a')[0]['href']
            description = project.find('div', {"class":"project-details"}).text
            author = project.find('span', {"class":"author-info"}).text
            value = project.find('span', {"class":"values"}).text

            data = {
                "title": title.encode('utf-8'),
                "link": 'workana.com' + str(link).encode('utf-8'),
                "description": description.encode('utf-8'),
                "author": author.split(':')[1].encode('utf-8'),
                "value": value.encode('utf-8').encode('utf-8'),
            }

            projects.append(data)


	pageNo+=1;


driver.close()

print("Writing data to Csv file...")

csv_columns = ['title','link', 'description','author', 'value']
csv_file = "./results.csv"

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for p in projects:
            writer.writerow(p)
except IOError:
    print("I/O error")
