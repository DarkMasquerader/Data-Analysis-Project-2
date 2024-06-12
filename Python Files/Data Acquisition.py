# Imports
import MyWeb, os, re, datetime
from Job import Job
import pandas as pd
from selenium.common.exceptions import TimeoutException

# Global Variables
list_of_job_objects = [] 
url_set = set()

collectNewData = True #Set to false if extracting data from local .html files
no_pages = 100 # No. LinkedIn pages to scrape

specificCountry = False #Set to true to specify the country of the job search
country = 'United States'

basePath = './Python Files/Output Files/Job Pages' # Output path for .html files

collectionDate = datetime.datetime.today()

def main():
    
    ''' 
    These functions are responsible for scraping job-related information from LinkedIn.
    The .html file for each job listing is saved locally with its URL prepended within the document.

    getPreviousJobURLS() creates a set of job URL's from previous data collections.
    The set is used to prevent subsequent scraping attempts including previously recorded jobs.
    '''
    if collectNewData:
        getPreviousJobURLS() # Enables subsequent searches preventing repeated jobs in dataset
        linkedInScraper()
    
    '''
    This function is responsible for extracting, transforming, and structuring the information from the job postings and storing them in objects.
    '''
    extractData()

    '''
    This function is responsible for exporting the job data to a/several .csv file(s) where it can be interacted with in Tableau.
    '''
    exportData()
    
    # Termination notification
    print('******* DONE *******')

# Data Scraping functions
def getPreviousJobURLS():

    for filename in os.listdir(basePath):
        if filename.endswith(".html"):
            filepath = os.path.join(basePath, filename)
            with open(filepath, 'r', encoding='utf-8') as file:
                first_line = file.readline().strip()
                url_set.add(first_line.split('<!-- ')[1].split(' -->')[0].split('?position')[0])

def linkedInScraper():

    # Setup chrome driver
    service = MyWeb.Service(executable_path=f'./Python Files/chromedriver')

    chrome_options = MyWeb.webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    driver = MyWeb.webdriver.Chrome(service=service, options=chrome_options)

    # Login to account
    handleLogin(driver)

    # Acquire list of job postings 
    list_of_job_pages = acquireJobListings(driver)

    # Save HTML 
    file_count = len([name for name in os.listdir(basePath)])
    job_counter = file_count + 1
    for page in list_of_job_pages:
        
        # Base Case - Job already found
        if(page.split('?position')[0] in url_set):
            print('<JOB ALREADY ADDED>')
            continue

        # Get HTML
        driver.get(page)
        # print(page) #Uncomment to show URL in console

        # Click on 'Show More' button
        show_more_button_selector = 'button[aria-label="Click to see more description"]'
        try:
            MyWeb.WebDriverWait(driver, 15).until(
                MyWeb.EC.presence_of_element_located((MyWeb.By.CSS_SELECTOR, show_more_button_selector))
            )
            button = driver.find_element(MyWeb.By.CSS_SELECTOR, show_more_button_selector)

            MyWeb.time.sleep(1)
            button.click()
            MyWeb.time.sleep(1)

        except TimeoutException:
            print('<SHOW MORE BUTTON NOT FOUND>')

        # Save .html file
        path = f'{basePath}/Job{job_counter}.html' 
        with open(path, 'w') as f:
            f.write(f'<!-- {page} -->\n') #Store page URL at top of file
            f.write(driver.page_source)
            job_counter += 1

def handleLogin(driver):
    
    # Open login page
    login_URL = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
    driver.get(login_URL)

    # Acquire login details from text file
    with open(f'/Users/{os.getlogin()}/Desktop/details.txt', 'r') as file:
        email = file.readline().strip()
        pwd = file.readline().strip()

    # Enter details into LinkedIn
    MyWeb.interactWithTextBoxByID('username', 
                                  email, 
                                  driver, 
                                  False)

    MyWeb.interactWithTextBoxByID('password', 
                                  pwd, 
                                  driver, 
                                  True)

    # Go to jobs page post login
    job_URL = 'https://www.linkedin.com/jobs'
    driver.get(job_URL)

def acquireJobListings(driver):
    
    # Search for Job
    if specificCountry:
        MyWeb.interactWithTextBoxBySelector(
            selector= 'input[aria-label="City, state, or zip code"]', 
            text= country,
            driver= driver, 
            pressEnter= True
        )

    pageHTML, pageURL = MyWeb.interactWithTextBoxBySelector(
        selector= 'input[aria-label="Search by title, skill, or company"]', 
        text= 'Data Analyst', 
        driver= driver, 
        pressEnter= True
    )
    
    # Curate list of job page URL's 
    list_of_page_urls = []
    list_of_page_urls.append(pageURL)

    app_str = '&start='
    app_num = 25 
    for x in range(1, no_pages):
        list_of_page_urls.append(f'{pageURL}{app_str}{app_num * x}')

    # Extract all job URL's
    regex_pattern = '^(https:\/\/(www|uk).linkedin.com)\/jobs\/view\/'

    list_of_job_pages = []
    for page_url in list_of_page_urls:

        pageText = MyWeb.getHTML(page_url)
        hyperlinks = pageText.find_all('a')
        for link in hyperlinks:
            _ = link.get('href')

            # Base Case - No href found
            if _ is None:
                continue

            if re.search(regex_pattern, _) is not None: 
                list_of_job_pages.append(_)

    return list_of_job_pages

# Data Extraction Functions
def extractData():
    
    dir = './Python Files/Output Files/Job Pages'
    jobID = 0
    for file_name in os.listdir(dir):

        # Base Case - Not .html file
        if '.html' not in file_name:
            continue

        file_path = os.path.join(dir, file_name)
        jobID += 1

        if os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                
                # Get HTML
                pageText = jobURL = file.read()
                pageText = MyWeb.BeautifulSoup(pageText, 'html')

                # Clean URL
                jobURL = jobURL.splitlines()[0].split('<!-- ')[1].split(' -->')[0]

                # Acquire location, post date, no.applicants
                data_1 = pageText.find('div', 
                                    {'class' : 'job-details-jobs-unified-top-card__primary-description-container'})
                data_1_text = data_1.get_text().strip()
                data_1_split = [_.strip() for _ in data_1_text.split('·')]
                
                # Base Case - No. applicants unspecified
                if len(data_1_split) == 2:
                    data_1_split.append('N/A')

                # Acquire salary, remote/hybrid/in-person, contract type, job level
                LIST_ELEMENTS = pageText.findAll('li', 
                                    {'class' : 'job-details-jobs-unified-top-card__job-insight'})
 
                data_2 = LIST_ELEMENTS[0]
                data_2_text = data_2.get_text().strip()
                _ = [line for line in data_2_text.split('\n') if line.strip()]
                data_2_text = '\n'.join(_)
                data_2_text = data_2_text.lower()

                # Location
                isOnSite = 'on-site' in data_2_text
                isRemote = 'remote' in data_2_text
                isHybrid = 'hybrid' in data_2_text
                isLocationUnspecified = all(location == False for location in [isOnSite, isRemote, isHybrid])
                
                # Contract Type
                isContract = 'contract' in data_2_text
                isFullTime = 'full-time' in data_2_text
                isContractTypeUnspecified = all(contract == False for contract in [isContract, isFullTime])

                # Job Level
                isEntryLevel = 'entry level' in data_2_text
                isMidSeniorLevel = 'mid-senior level' in data_2_text
                isDirector = 'director' in data_2_text
                isAssociate = 'associate' in data_2_text
                isInternship = 'internship' in data_2_text
                isJobLevelUnspecified = all(jobLevel == False for jobLevel in [isEntryLevel, isMidSeniorLevel, isDirector, isAssociate, isInternship])
 
                # Salary
                data_2_split = [_.strip() for _ in data_2.get_text().split('\n')]
                salary = None
                for _ in data_2_split:
                    if '$' in _ or '£' in _ or '€' in _:
                        salary = _
                        break

                # Job description & Skills
                data_3 = pageText.find('article', class_='jobs-description__container jobs-description__container--condensed')
                data_3_text = data_3.get_text(separator='\n', strip=True).lower() # About This Job

                skillSQL = 'sql' in data_3_text
                skillsExcel = 'excel' in data_3_text
                skillsTableau = 'tableau' in data_3_text or 'visualisation tool' in data_3_text
                skillsPowerBi = 'power bi' in data_3_text or 'visualisation tool' in data_3_text
                skillsPython = 'python' in data_3_text
                skillsR = ' r ' in data_3_text

                # No. Employees
                data_4 = LIST_ELEMENTS[1]
                data_4_text = data_4.get_text()
                data_4_split = data_4_text.split('·')
                employeeCount = 'None'

                for _ in data_4_split:
                    if 'employees' in _:
                        employeeCount = _.split('employees')[0].strip()

                # Company Name
                data_5 = pageText.findAll('a', 
                                       {'class' : 'app-aware-link',
                                        'target' : '_self'})
                data_5_text = data_5[5].get_text().strip()

                # Create object
                list_of_job_objects.append(Job(*data_1_split, 
                    isOnSite, isRemote, isHybrid, isLocationUnspecified,
                      isContract, isFullTime, isContractTypeUnspecified,
                        isEntryLevel, isMidSeniorLevel, isDirector, isAssociate, isInternship, isJobLevelUnspecified,
                         skillSQL, skillsExcel, skillsTableau, skillsPowerBi, skillsPython, skillsR,
                          salary,
                           employeeCount, 
                            data_5_text,
                             jobID, 
                                jobURL))
    
# Data Export Functions
def exportData():

    # General 
    general_df = pd.DataFrame(columns= ['Job ID', 'Company Name', 'Location', 'Post Date', 'No. Applicants', 'No. Employees', 'Salary', 'Original Salary', 'URL'])

    # Work Type
    workType_df = pd.DataFrame(columns= ['Job ID', 'On-Site', 'Remote', 'Hybrid', 'Unspecified'])

    # Contract Type
    contractType_df = pd.DataFrame(columns= ['Job ID', 'Contracted', 'Full Time', 'Unspecified'])
    
    # Job Level
    jobLevel_df= pd.DataFrame(columns= ['Job ID', 'Internship', 'Entry Level', 'Mid-Senior Level', 'Associate Level', 'Director Level', 'Unspecified'])

    # Skills
    skills_df= pd.DataFrame(columns= ['Job ID', 'SQL', 'Excel', 'Tableau', 'Power Bi', 'Python', 'R'])

    # Build DataFrame
    for job in list_of_job_objects:
        general_df.loc[len(general_df)] = job.getGeneral()
        workType_df.loc[len(workType_df)] = job.getWorkType()
        contractType_df.loc[len(contractType_df)] = job.getContractType()
        jobLevel_df.loc[len(jobLevel_df)] = job.getJobLevel()
        skills_df.loc[len(skills_df)] = job.getSkills()

    # Export DataFrames
    general_df.to_csv('./Python Files/Output Files/csv/General.csv', index= False)
    workType_df.to_csv('./Python Files/Output Files/csv/Work Type.csv', index= False)
    contractType_df.to_csv('./Python Files/Output Files/csv/Contract Type.csv', index= False)
    jobLevel_df.to_csv('./Python Files/Output Files/csv/Job Level.csv', index= False)
    skills_df.to_csv('./Python Files/Output Files/csv/Skills.csv', index= False)
    
# Main Loop
if __name__ == '__main__':
    main()