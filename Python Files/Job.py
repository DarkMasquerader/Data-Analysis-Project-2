class Job:
    '''
    This class is used to represent and handle the data of the individual job postings extracted from linkedin.

    All information stored in each instance (object) is provided at initialisation.

    Each of the functions in this class have been created to facilitate the creation of DataFrame objects, which allows information to be exported and analysed in Tableau.
    '''

    def __init__(self, location, post_date, no_applicants, on_site, remote, 
                 hybrid, location_unspecified, contract, full_time, contract_unspecified, 
                 entry_level, mid_senior_level, director_level, associate_level, internship_level, job_level_unspecified, 
                 sql, excel, tableau, power_bi, python, r,
                 salary, employee_count, company_name, jobId):

        # General
        self.jobId = jobId
        self.company_name = company_name
        self.location = location
        self.post_date = post_date
        self.no_applicants = no_applicants 
        self.employee_count = employee_count


        self.salary = salary #todo
        if 'up to' in salary.lower(): # Remove text
            self.salary = salary.lower().split('up to ')[1]
        elif ' - ' in salary: #Take lower end of salary range
            self.salary = salary.split(' - ')[0]
            
        # Replace 'k' with ',000'
        if 'k' in self.salary.lower():
            self.salary = self.salary.lower().replace('k', ',000')

        # Remove 'per hour' or 'per year'
        if '/' in self.salary:
            self.salary = self.salary.split('/')[0]

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
        return [self.jobId, self.company_name, self.location, self.post_date,  self.no_applicants, self.employee_count, self.salary]

    def __str__(self) -> str:
        return [self.jobId, self.location, self.post_date, self.no_applicants, self.on_site, self.remote, self.hybrid, self.location_unspecified, self.contract, self.full_time, self.contract_unspecified, self.entry_level, self.mid_senior_level, self.director_level, self.associate_level, self.internship_level, self.job_level_unspecified, self.sql, self.excel, self.tableau, self.power_bi, self.python, self.r, self.salary, self.employee_count, self.company_name]