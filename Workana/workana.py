import requests
from bs4 import BeautifulSoup
from credentials import * # Import your credentials from credentials.py to be able to Login (Variables are login and password)

def login(): # Login on the site, to be able to gather more information
    URL = "https://www.workana.com/login"

    headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}

    data = {
        'email': login,
        'password': password,
        'remember': 1
    }

    page = requests.post(URL, data=data, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser');
    
    print(page.status_code)
    print(soup.prettify())


def scrapper():
    baseURL = 'https://www.workana.com/jobs?ref=menu_projects_index&language=en%2Cpt&category=it-programming&page=' 
    count = 1
    pageNo = 1

    while True:
        URL = baseURL + str(pageNo) # Creates the URL
        pageNo= pageNo + 1
        page = requests.get(URL)    # Request for the site                                     

        if page.status_code != 200: # While it find valid pages
            break

        soup = BeautifulSoup(page.content, 'html.parser');
        divs = soup.find_all('div', {"class" : "project-item"})   # Find all div tags for projects
        
        for div in divs:
            print("Project {}".format(count))
            count = count+1

            title = div.find('h2', {"class" : "project-title"}).text
            desc = div.find('div', {"class":"project-details"}).text
            value = div.find('span', {"class":"values"}).text

            print(title)
            print("Description:" + desc + "\n")
            print("Budget: " + value)
            print("\n\n");
            
    print("End of the Scrapper.")

def main():
    # scrapper()
    login()

main()