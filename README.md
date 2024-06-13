# An Analysis of Data Analyst Jobs in the US

## Table of Contents 
- [Business Problem](#business-problem)
- [Tech Stack](#tech-stack)
- [Project Focus](#project-focus)
- [Data Preparation and Acquisition](#data-preparation-and-acquisition)
- [Results at a Glance](#results-at-a-glance)
- [Insights & Recommendations](#insights-and-recommendations)
- [Limitations and Potential Improvements](#limitations-and-potential-improvements)

## Business Problem 
This project is of personal interest and use to me, as I am looking for data analyst positions in the US. 

The goal of this project is to provide the end user (yours truly) with a high-level insight into the state of data analyst jobs in the USA.

## Tech Stack 
- [Python](Python%20Files/)
    - Data Acquisition: Website Scraping, Website Automation (Selenium, Chrome Driver)
    - Data Processing: Data Cleaning and Transformation
    - Data Visualisation: Numpy, Matplotlib
- [Tableau](Tableau/)

## Project Focus 
This project covers all stages of the data analysis process, with the strong points of this project being the *data collection* and *data processing* stages.

In-depth details on these stages can be found in the [Python](Python%20Files/) directory.

## Data Preparation and Acquisition
The dataset used for this project is generated using data collected first-hand from [LinkedIn](https://linkedin.com).

The collected data is cleaned, transformed, and handled in preparation for subsequent data analysis in Tableau.

The script responsible for data acquisition and preparation is `Data Acquisition.py`, which can be viewed [here](Python%20Files/Data%20Acquisition.py).

## Results at a Glance
Due to the nature of this project collecting data first-hand, there is a `lack' of historical data, which does not leave much room for trend analysis.

This notwithstanding, a couple of insights are provided below:

![](Images/Frequency%20of%20Skills.png)\
Across the 1,169 collected job postings, a significant majority of listings explicitly mention SQL and Excel, highlighting these skills to be of importance to a data analyst.

![alt](Images/Jobs%20per%20State.png)\
This heatmap of the USA shows the majority of data analysis positions are located in the state of New York (317 entries), with the state of California in second place with 51 entries.

[NOTE: The numbers have changed since the writing of this README, though the findings remain the same.]

## Explore the Dashboard (Tableau) 
A dashboard has been put together in Tableau to summarise the findings of this research project.\
For further details and to view the dashboard, go to the [Tableau](Tableau%20Files/) directory.

## Challenges and Limitations

### Data Availability 
The biggest challenge faced regarding data availability is the overwhelming prevalence of qualitative data.

The majority of information about a job posting is contained in its description, the structure of which is **not** standardised.

With each company using its own structure and wording to provide information about the job posting, it is a difficult task to automate the accurate harvesting of this data.

### Historical Data
The lack of available historical data (i.e. previous job postings) places a limitation on the type of analysis that can be conducted.\

One use case of such historical data could be to enable the analysis of the change in average salary over time.

### Data Collection Challenges
Data collection was surprisingly challenging, due to the dynamic nature of LinkedIn.\
This greatly increased the development time of the data acquisition phase of this project.

#### Challenge #1
One consequence of LinkedIn's dynamism results in data that is either visible to a human user or known to be present on the page, not being present in the HTML file (what the scraper looks at).

Let's take a look at the following image:
![alt](Images/Dynamism%201.png)\
In this image, we can see 'About the job' and the start of the job description.

However, in the page's current state, only the 'About the job' can be extracted from the HTML.\
In order for the contents of the job description to be made present in the HTML, the 'See more' button must be interacted with first, adding an extra layer of complexity to the data collection process.

#### Challenge #2
The second challenge, which proved to be a larger hurdle to overcome at the start of the project, is the usage of 'dynamic IDs'.

Depending on the URL used to access LinkedIn, the IDs of the HTML tags (for example, the ID attribute of the search bar) would be dynamic and **not** consistent with each run.

An example of such an ID is `jobs-search-box-keyword-id-ember-28`, where the number '28' would be different with each run, greatly increasing the difficulty of an automated approach to scraping data.

Thankfully, URLs that did not result in such dynamic IDs being used by LinkedIn were found and used for data collection.