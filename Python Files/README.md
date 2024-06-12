# Python (Data Acquisition & Transformation)
This directory contains four files and one sub-directory.

### Executables
`chromedriver` is the Mac/Linux executable required for website automation.

### Python Files
`Data Acquisition.py` is the script responsible for data collection, transformation, and handling.

`Job.py` contains the class used to represent and store the data for each job listing included in the analysis. This class is also responsible for a significant amount of data transformation and handling.

`MyWeb.py` is my library which contains tailor-made, frequently performed actions, regarding website scraping.

All Python files are thoroughly documented and commented.

### Directories
`Output Files/` is the directory where all output from *Data Acquisition.py* is stored; it contains two sub-directories:
- `csv/` -> This sub-directory contains the tables generated using the data collected from LinkedIn. The files in this sub-directory are used as input into Tableau.
- `Job Pages/` -> This sub-directory contains the .html files of the job listings included in the analysis.

## Script Structure (Data Acquisition.py)
The main loop is well-commented, providing a high-level explanation of the script.\
The main loop is included in-line, below:

```python
    ''' 
    These functions are responsible for scraping job-related information from LinkedIn.
    The .html file for each job listing is saved locally with its URL prepended within
    the document.
    '''
    if collectNewData:
        getPreviousJobURLS() # Prevents repeated jobs in dataset
        linkedInScraper()
    
    '''
    This function is responsible for extracting, transforming, and
    structuring the information from the job postings and storing
    them in objects.
    '''
    extractData()

    '''
    This function is responsible for exporting the job data to
    a/several .csv file(s) where it can be interacted with in Tableau.
    '''
    exportData()
```