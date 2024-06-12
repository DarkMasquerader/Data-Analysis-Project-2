'''
This Python file is my personal data scraping assistant.
'''
# Web scraping libraries
from bs4 import BeautifulSoup
import requests

# Web interaction/botting libraries 
from selenium import webdriver 
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Threading libraries
from threading import Thread, Lock
mutex = Lock()
threadLimit = 15 
isThreading = False # False = Single Thread | True = Multi-Threaded

# General libraries
import time

# My Functions
def getHTML(url: str):
    '''
        Description
        ------------
        This function is used to acquire the HTML of a specified URL.

        Parameters
        ----------
        url: str
            The URL of the page target.

        Returns
        -------
        BeautifulSoup object containing the rendering of a webpage.

        Raises
        ------
        This function does not raise an exception.
    '''
    page = requests.get(url)
    return BeautifulSoup(page.text, "html")

from typing import Callable
def threadCaller(threadCallee: Callable):
    '''
        Description
        ------------
        This functions is responsible for initiating the threads that are used for botting.

        Before using this function, do the following:
            - Create a global iterable 
            - Place iterable inside mutex controlled function

        Parameters
        ----------
        threadCallee: Callable
            This is the function that is called by each of the threads.
        
        Returns
        -------
        This function does not return a value.

        Raises
        ------
        This function raises any exception thrown inside the passed function.

        Notes
        -----
        When using this function, be sure to implement the following code:
        ###
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
        ###
    '''

    # Recording running time
    start_time = time.time()

    _list = []
    # Initialise threads
    for temp in range(0,threadLimit):
        _ = Thread(target = threadCallee, args = [temp,] )
        _.start()
        _list.append(_)

    # Join threads
    for _ in _list:
        _.join()

    # Display running time
    end_time = time.time()
    print(f'Steam Runtime: {end_time-start_time}')

def interactWithTextBoxByID(id: str, text: str, driver: webdriver, pressEnter: bool):
    '''
        Description
        ------------
        This function is responsible for interacting with a specified textbox that has been identified using its 'ID'.
    
        Parameters
        ----------
        id: str
            The HTML id that is used to identify the textbox.
        
        text: str
            This variable contains the text that is entered into the textbox.

        driver: webdriver
            This variable is the WebDriver object that being used by the calling thread.
        
        pressEnter: bool
            This variable controls whether or not an enter input is pressed
    
        Returns
        -------
        pageHTML: str
            HTML of the page following the interaction with the textbox.

        pageURL: str
            The URL of the page following the interaction with the textbox.
        
        Raises
        ------
        This function does not raise an exception.
    '''

    # Safely confirm presence of textbox before attempting interaction
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, id))
    )

    # Identify and interact with textbox 
    input_element = driver.find_element(By.ID, id)       
    input_element.send_keys(text)
    
    if pressEnter:
        input_element.send_keys(Keys.ENTER)

    # Wait for 3 seconds to load
        time.sleep(3)
        
    pageHTML = driver.page_source
    pageURL = driver.current_url

    return pageHTML, pageURL

def interactWithTextBoxByClass(html_class: str, text: str, driver: webdriver, pressEnter: bool):
    '''
        Description
        ------------
        This function is responsible for interacting with a specified textbox that has been identified using its 'class'.

        Parameters
        ----------
        html_class: str
            The HTML class that is used to identify the textbox.
        
        text: str
            This variable contains the text that is entered into the textbox.

        driver: webdriver
            This variable is the WebDriver object that being used by the calling thread.

        pressEnter: bool
            This variable controls whether or not an enter input is pressed
    
        Returns
        -------
        pageHTML: str
            HTML of the page following the interaction with the textbox.

        pageURL: str
            The URL of the page following the interaction with the textbox.
        
        Raises
        ------
        This function does not raise an exception.
    '''

    # Safely confirm presence of textbox before attempting interaction
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, html_class))
    )

    # Identify and interact with textbox 
    input_element = driver.find_element(By.CLASS_NAME, html_class)       
    input_element.send_keys(text)
    
    if pressEnter:
        input_element.send_keys(Keys.ENTER)

    # Wait for 3 seconds to load
    time.sleep(3)

    pageHTML = driver.page_source
    pageURL = driver.current_url

    return pageHTML, pageURL

def interactWithTextBoxBySelector(selector: str, text: str, driver: webdriver, pressEnter: bool):
    '''
        Description
        ------------
        This function is responsible for interacting with a specified textbox that has been identified using its selector.

        Parameters
        ----------
        selector: str
            The selector that is used to identify the textbox.
        
        text: str
            This variable contains the text that is entered into the textbox.

        driver: webdriver
            This variable is the WebDriver object that being used by the calling thread.

        pressEnter: bool
            This variable controls whether or not an enter input is pressed
    
        Returns
        -------
        pageHTML: str
            HTML of the page following the interaction with the textbox.

        pageURL: str
            The URL of the page following the interaction with the textbox.
        
        Raises
        ------
        This function does not raise an exception.
    '''

    # Safely confirm presence of textbox before attempting interaction
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )

    # Identify and interact with textbox 
    input_element = driver.find_element(By.CSS_SELECTOR, selector)       
    input_element.send_keys(text)
    
    if pressEnter:
        input_element.send_keys(Keys.ENTER)

    # Wait for 3 seconds to load
    time.sleep(3)

    pageHTML = driver.page_source
    pageURL = driver.current_url

    return pageHTML, pageURL 

def isolateHTMLElementByClass(driver: webdriver, element_name: str):
    '''
        Description
        ------------
        This function is responsible for isolating an element by its class and returning it.
    
        Parameters
        ----------
        driver: webdriver
            This variable is the WebDriver object that being used by the calling thread.
        
        element_name: str
            This variable contains the name of the element that's being looked for.
    
        Returns
        -------
        dirtyElement: Element
            The Element object of the searched element.
        
        cleanElement: str
            The contents of the searched element.
        
        Raises
        ------
        NoSuchElementException
            This exception is raised if the element cannot be found.
    '''

    try:

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, element_name))
        )

        dirtyElement = driver.find_element(By.CLASS_NAME, element_name)
        cleanElement = dirtyElement.text.strip()
        return dirtyElement, cleanElement
        
    except NoSuchElementException as e:
        print(f'No such element found: {e}')
        return

from typing import Optional, Dict
def isolateInteractableHTML(page: BeautifulSoup, name: str, findAll: bool, index = -1, attr: Optional[Dict] = None):
    '''
        Description
        ------------
        This function isolates and returns an interactable (i.e. BeautifulSoup object) HTML object.
    
        Parameters
        ----------
        page: BeautifulSoup
            A BeautifulSoup object containing the HTML of a webpage.

        name: str
            The name of the element that's being looked for (e.g. href, a, table).

        findAll: bool 
            A boolean to determine if 'find()' or 'find_all()' if used.

        index: int (Default Value: -1)
            This represents the index of the element that's being used.

        attr: dict
            This contains a dictionary of attributes and values that's used in the isolation of interactable HTML elements.
    
        Returns
        -------
        _list
            A single or list of interactable HTML objects
    
        Raises
        ------
        This function does not raise an exception.
        
    '''

    if findAll:

        if attr is not None:
            _list = page.find_all(name=name, attrs=attr)
        else:
            _list = page.find_all(name=name)
        
        # Return all elements
        if (index == -1):
            return _list
        
        # Return x-th element
        else:
            return _list[index]
    
    else: 

        if attr is not None:
            return page.find(name=name, attrs=attr)
        else:
            return page.find(name=name)

