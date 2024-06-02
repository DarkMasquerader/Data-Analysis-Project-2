import MyWeb, os, re
from Job import Job

list_of_job_objects = []
def main():
    linkedInScraper()

threadCounter = 0
def getNextThing():
    with MyWeb.mutex:
        global threadCounter
        threadCounter += 1
        # return next(<ITERABLE>)

def threadCallee(num):
    print(f'Thread #{num} started')
    
    # Setup chrome driver
    service = MyWeb.Service(executable_path=f'./chromedriver')

    chrome_options = MyWeb.webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = MyWeb.webdriver.Chrome(service=service, options=chrome_options)

    while True:
        try:
            pass
        except StopIteration:
            print('End of list')
            driver.quit()
            break
        except Exception as e:
            print(f'Exception Occurred: {e}')
            continue
            
def handleLogin(driver):
    # Open Login Page
    login_URL = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
    driver.get(login_URL)

    # Enter Login Details
    with open(f'/Users/{os.getlogin()}/Desktop/details.txt', 'r') as file:
        email = file.readline().strip()
        pwd = file.readline().strip()

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
    for x in range(1, 10):
        list_of_page_urls.append(f'{pageURL}{app_str}{app_num * x}')

    # Extract all job URL's
    regex_pattern = '^https:\/\/www.linkedin.com\/jobs\/view\/'

    list_of_job_pages = []
    for page_url in list_of_page_urls:

        # driver.get(page_url)
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

def extractData():
    pass
    # global list_of_job_objects
    # for job in list_of_job_pages:
        
    #     # Get HTML
    #     driver.get(job)
    #     pageText = MyWeb.BeautifulSoup(driver.page_source, 'html')

    #     # Acquire location, post date, no.applicants
    #     data_1 = pageText.find('div', 
    #                            {'class' : 'job-details-jobs-unified-top-card__primary-description-container'})
    #     data_1_text = data_1.get_text()
    #     print(data_1_text)

    #     # Acquire salary, remote/hybrid/in-person, contract type, level
    #     data_2 = pageText.find('li', 
    #                            {'class' : 'job-details-jobs-unified-top-card__job-insight job-details-jobs-unified-top-card__job-insight--highlight'})
    #     data_2_text = data_2.get_text().strip()
    #     _ = [line for line in data_2_text.split('\n') if line.strip()]
    #     data_2_text = '\n'.join(_)
    #     print(data_2_text)

    #     # Job description
    #     data_3 = pageText.find('article', class_='jobs-description__container jobs-description__container--condensed')
    #     data_3_text = data_3.get_text(separator='\n', strip=True) # About This Job
    #     print(data_3_text)

    #     # Create object
    #     list_of_job_objects.append(Job(data_1_text, data_2_text, data_3_text))

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
    job_counter = 1
    for page in list_of_job_pages:
        driver.get(page)
        
        path = f'./Python Files/Output Files/Job{job_counter}.html' 
        with open(path, 'w') as f:
            f.write(driver.page_source)
            job_counter += 1
        
        MyWeb.time.sleep(3)

    # Extract data
    # extractData()

    print('Done')

# Main Loop
if __name__ == '__main__':
    main()