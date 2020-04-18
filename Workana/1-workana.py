import requests
from bs4 import BeautifulSoup

# Workana jobs page url missing page Number 
baseURL = 'https://www.workana.com/jobs?ref=menu_projects_index&language=en%2Cpt&category=it-programming&page=' 

# Auxiliar variables for printing 
count = 1
pageNo = 1

while 1:
    URL = baseURL + str(pageNo)                                  # Creates the URL
    pageNo= pageNo + 1
    page = requests.get(URL)                                     # Request for the site

    if page.status_code != 200:
        print("Something went wrong on the request!: HTTP STATUS: ", end='')
        print(page.status_code)
        exit(1)

    soup = BeautifulSoup(page.content, 'html.parser');
    divs = soup.find_all('div', {"class" : "project-item"})   # Find all div tags for projects

    for div in divs:
        print("Project {}".format(count))
        count = count+1

        title = div.find('h2', {"class" : "project-title"}).text
        desc = div.find('div', {"class":"project-details"}).text
        value = div.find('span', {"class":"values"}).text
        
        # value.split('-')
        # lowerLimit = value[0]
        # upperLimit = value[1]

        print(title)
        print("Description:" + desc + "\n")
        print("Budget: " + value)
        print("\n\n");
        
    
