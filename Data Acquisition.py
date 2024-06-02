import MyWeb, os, re

'''
Job list column: div class="scaffold-layout__list " tableindex="-1"
Individual job: 
    <li id = "ember[0-9]{4}" class = "ember-view   jobs-search-results__list-item occludable-update p0 relative scaffold-layout__list-item"
    <div data-job-id="3924719779" class="display-flex job-card-container relative job-card-list
Pages:
    <button aria-label="Page 6"
'''

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

def linkedInScraper():

    # Setup chrome driver
    service = MyWeb.Service(executable_path=f'./chromedriver')

    chrome_options = MyWeb.webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--disable-gpu')
    driver = MyWeb.webdriver.Chrome(service=service, options=chrome_options)

    # Login to account
    handleLogin(driver)

    # Search for Job
    pageHTML, pageURL = MyWeb.interactWithTextBoxBySelector(
        selector= 'input[aria-label="Search by title, skill, or company"]', 
        text= 'Data Analyst', 
        driver= driver, 
        pressEnter= True
    )
    
    # Curate list of job URL's (Single Page)
    # &start=25 - Append to URL and up by 25 for each page
    pageText = MyWeb.getHTML(pageURL)
    hyperlinks = pageText.find_all('a')

    regex_pattern = '^\/jobs\/view\/'

    list_of_job_pages = []
    for link in hyperlinks:
        _ = link.get('href')

        # Base Case - No href found
        if _ is None:
            continue

        if re.search(regex_pattern, _) is not None:
            list_of_job_pages.append(f'linkedin.com{_}')
    

# Main Loop
if __name__ == '__main__':
    main()