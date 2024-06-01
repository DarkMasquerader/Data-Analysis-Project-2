import MyWeb 

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
    email = 'zbvd398@live.rhul.ac.uk'
    pwd = 'iushfuish398fs[fsdfs]'

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
    searchBarID = "jobs-search-box-keyword-id-ember27" #TODO: Find the number dynamicall by searching for 'jobs-search-box-keyword-id-ember' and extracting 
    pageHTML, pageURL = MyWeb.interactWithTextBoxByID(searchBarID, "Data Analyst", driver)

    # Isolate list of jobs object
    htmlObject = 'div'
    attr = {"class":"scaffold-layout__list "}
    job_list = MyWeb.isolateInteractableHTML(
        MyWeb.getHTML(pageURL), 
        htmlObject, 
        False, 
        attr= job_list
    )

    # Scroll job object to load all jobs
    ul_element = driver.find_element_by_css_selector("ul.scaffold-layout__list-container")

    initial_height = driver.execute_script("return arguments[0].scrollHeight", ul_element)

    # Handle dynamic HTML
    while True:
        # Scroll the <ul> element
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", ul_element)
        
        # Wait for a short duration to allow the content to load
        MyWeb.time.sleep(2)
        
        # Check if the height of the <ul> element has increased
        new_height = driver.execute_script("return arguments[0].scrollHeight", ul_element)
        if new_height > initial_height:
            initial_height = new_height
        else:
            break


# Main Loop
if __name__ == '__main__':
    main()