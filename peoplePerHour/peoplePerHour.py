import requests
from bs4 import BeautifulSoup
import csv
import datetime

projects = []
def scrapper():
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
            price_type = projectSoup.find('div', {"class" : "budget"}).label.text
            experience = projectSoup.find('div', {"class" : "description-experience-level"}).text
            description = projectSoup.find('div', {"class" : "project-description gutter-top"}).text
            
            # Gather author Information
            author = projectSoup.find('div', {"class" : "member-name-container crop"}).h5.text
            projects_involved = projectSoup.find('div', {"class" : "member-stat project-involved-in-stats"}).span.text
            freelancers_worked_with = projectSoup.find('div', {"class" : "member-stat sellers-worked-with-stats"}).span.text
            projects_awarded = projectSoup.find('div', {"class" : "member-stat jobs-awarded-in-stats"}).span.text
            location = projectSoup.find('div', {"class" : "location-container crop"}).text

            # Cleaning the data
            description = description.replace('\n', ' ')
            experience = experience.split(':')[1]
            experience = experience.replace(' ', '')
            

            # Creating data Object
            data = {
                "link": link,
                "price": price,
                "price_type": price_type,
                "experience": experience,
                "description": description,
                "author": author,
                "projects_involved": projects_involved,
                "freelancers_worked_with": freelancers_worked_with,
                "projects_awarded": projects_awarded,
                "location": location,
            }

            # Filters 
            filter1 = experience == "Intermediate" or experience == "Expert"
            filter2 = projects_involved != '-'
            filter3 = freelancers_worked_with != '-'
            filter4 = len(description) > 300

            # Append data with correct filters
            if (filter1 and filter2 and filter3 and filter4):
                projects.append(data)
                print("Found a project")

            print("In progress ...")

    print("Scrapper Finished.")

def writeToCsv():
    print("Writing data to Csv file...")

    csv_columns = ['link', 'price', 'price_type', 'experience','description', 'author','projects_involved','freelancers_worked_with', 'projects_awarded','location']
    csv_file = "./results.csv"

    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for project in projects:
                writer.writerow(project)

    except IOError:
        print("I/O error")

def main():
    scrapper()
    writeToCsv()
    
    print("Number of Projects Found: " + str(len(projects)))

main()

