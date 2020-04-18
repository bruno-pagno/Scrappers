import requests
from bs4 import BeautifulSoup

URL = 'https://www.workana.com/jobs?ref=menu_projects_index' # Workana jobs page url
page = requests.get(URL)                                     # Request for the site

if page.status_code != 200:
    print("Something went wrong on the request!")
    exit(1)

soup = BeautifulSoup(page.content, 'html.parser');
divs = soup.find_all('div', {"class" : "project-item"})   # Find all div tags for projects

count = 1
for div in divs:
    print("Project {}".format(count))
    count = count+1

    title = div.find('h2', {"class" : "project-title"}).text
    desc = div.find('div', {"class":"project-details"}).text
    value = div.find('span', {"class":"values"}).text
    
    print(title)
    print("Descrição:" + desc + "\n")
    print("Valor do Projeto: " + value)
    print("\n\n");
    
    
