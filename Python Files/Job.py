class Job:
    '''
    This class is used to represent and handle the data of the individual job postings extracted from linkedin.

    All information stored in each instance (object) is provided at initialisation.

    Each of the functions in this class facilitate the creation of DataFrame objects, enabling information to be exported (.csv) and analysed in Tableau.
    '''

    # Class attributes
    states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", 
                "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", 
                "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", 
                "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", 
                "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
                "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
                "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", 
                "Wisconsin", "Wyoming"]

    state_abbreviations = {
        'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
        'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
        'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
        'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts',
        'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
        'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
        'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
        'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
        'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
        'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming',
        'DC': 'District of Columbia'
    }

    def __init__(self, location, post_date, no_applicants, on_site, remote, 
                 hybrid, location_unspecified, contract, full_time, contract_unspecified, 
                 entry_level, mid_senior_level, director_level, associate_level, internship_level, job_level_unspecified, 
                 sql, excel, tableau, power_bi, python, r,
                 salary, employee_count, company_name, jobId, jobURL):

        # General
        self.jobId = jobId
        self.company_name = company_name
        self.url = jobURL
        self.employee_count = employee_count
        
        # Applicants
        self.no_applicants = no_applicants
        if 'over' in self.no_applicants.lower(): #Over 100 applicants
            _ = self.no_applicants.split(' ')[1]
            self.no_applicants = _ + '+'
        elif 'early' in self.no_applicants.lower(): #Be an early applicant
            self.no_applicants = 'Early'
        
        if 'applicants' in self.no_applicants.lower():
            self.no_applicant = self.no_applicants.lower().split('applicants')[0]

        if ',' not in location:
            self.location = location

            if location not in Job.states and len(location) != 2: #If not state code and text is not state
                for state in Job.states:
                    if state in self.location:
                        self.location = state
                        break

        else:
            _ = location.split(',')[1].strip()
            if len(_) == 2:
                self.location = Job.state_abbreviations[_]
            else: # Not a state code
                stateSet = False
                for state in Job.states:
                    if state in _:
                        self.location = state
                        stateSet = True
                        break

                if not stateSet:
                    self.location = _

        #Post Date
        self.post_date = post_date.replace('Reposted', '')

        # Handle Salary
        self.salary = salary #Float - This value is used for 'ordering' in Tableau
        self.original_salary = salary #String - This value is used for presentation to the end user

        if salary is not None:
            if 'up to' in salary.lower(): # Remove text
                self.salary = salary.lower().split('up to ')[1]
            elif 'starting at' in salary.lower():
                self.salary = salary.lower().split('starting at ')[1]
            elif ' - ' in salary: #Take lower end of salary range
                self.salary = salary.split(' - ')[0]
                
            # Replace 'k' with ',000'
            if 'k' in self.salary.lower():
                self.salary = self.salary.lower().replace('k', '000.00')

            # Remove 'per hour' or 'per year'
            if '/' in self.salary:
                self.salary = self.salary.split('/')[0]
            
            try:
                self.salary = float(self.salary[1:])
            except ValueError: 
                print(f'Salary Error: {self.salary}')
                self.salary = None
                self.original_salary = None


        # Working Type
        self.on_site = on_site 
        self.remote = remote  
        self.hybrid = hybrid
        self.location_unspecified = location_unspecified

        # Contract Type
        self.contract = contract
        self.full_time = full_time
        self.contract_unspecified = contract_unspecified

        # Job Level
        self.internship_level = internship_level
        self.entry_level = entry_level
        self.mid_senior_level = mid_senior_level
        self.associate_level = associate_level
        self.director_level = director_level
        self.job_level_unspecified = job_level_unspecified

        # Skills
        self.sql = sql
        self.excel = excel
        self.tableau = tableau
        self.power_bi = power_bi
        self.python = python 
        self.r = r

    def getSkills(self):
        return [self.jobId, self.sql, self.excel, self.tableau, self.power_bi, self.python, self.r]

    def getJobLevel(self):
        return [self.jobId, self.internship_level, self.entry_level, self.mid_senior_level, self.associate_level, self.director_level, self.job_level_unspecified]

    def getContractType(self):
        return [self.jobId, self.contract, self.full_time, self.contract_unspecified]
        
    def getWorkType(self):
        return [self.jobId, self.on_site, self.remote, self.hybrid, self.location_unspecified]

    def getGeneral(self):
        return [self.jobId, self.company_name, self.location, self.post_date,  self.no_applicants, self.employee_count, self.salary, self.original_salary, self.url]
