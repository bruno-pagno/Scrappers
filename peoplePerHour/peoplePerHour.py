import requests
from bs4 import BeautifulSoup

baseURL = "https://www.peopleperhour.com/freelance-jobs/software-development?page="
pageNo = 1


lastPage = None
while True:
    URL = baseURL + str(pageNo) # Creates the URL
    pageNo+=1

    page = requests.get(URL)  
    soup = BeautifulSoup(page.content, 'html.parser')

    selectedPage = soup.find('a', {"class" : " selected"}).text
    if selectedPage == lastPage:
        break

    lastPage = selectedPage

    project_links = soup.find_all('a', {"class" : "job js-paragraph-crop"})
    for project_link in project_links:
        link = project_link['href']
        
        link_page = requests.get(link)
        projectSoup = BeautifulSoup(link_page.content, 'html.parser')

        # Gathering the Project Information
        price =  projectSoup.find('div', {"class" : "value price-tag"}).text
        experience = projectSoup.find('div', {"class" : "description-experience-level"}).text
        description = projectSoup.find('div', {"class" : "project-description gutter-top"}).text
        
        # Gather author
        author = projectSoup.find('div', {"class" : "member-name-container crop"}).h5.text
        projects_involved = projectSoup.find('div', {"class" : "member-stat project-involved-in-stats"}).span.text
        freelancers_worked_with = projectSoup.find('div', {"class" : "member-stat sellers-worked-with-stats"}).span.text
        projects_awarded = projectSoup.find('div', {"class" : "member-stat jobs-awarded-in-stats"}).span.text
        location = projectSoup.find('div', {"class" : "location-container crop"}).text
        
        print(link)
        print(price)
        print(experience)
        print(description)
        print(author)
        print(projects_involved)
        print(freelancers_worked_with)
        print(projects_awarded)
        print(location)
        print("\n\n")
