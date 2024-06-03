class Job:

    def __init__(self, location, post_date, no_applicants, on_site, remote, 
                 hybrid, location_unspecified, contract, full_time, contract_unspecified, 
                 entry_level, mid_senior_level, director_level, associate_level, internship_level, job_level_unspecified, 
                 sql, excel, tableau, power_bi, python, r,
                 salary, employee_count):

        # General
        self.location = location
        self.post_date = post_date
        self.no_applicants = no_applicants 
        self.salary = salary #todo
        self.employee_count = employee_count

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
        self.entry_level = entry_level
        self.mid_senior_level = mid_senior_level
        self.director_level = director_level
        self.associate_level = associate_level
        self.internship_level = internship_level
        self.job_level_unspecified = job_level_unspecified

        # Skills
        self.sql = sql
        self.excel = excel
        self.tableau = tableau
        self.power_bi = power_bi
        self.python = python 
        self.r = r

    def __str__(self) -> str:
        return [self.location, self.post_date, self.no_applicants, self.on_site, self.remote, self.hybrid, self.location_unspecified, self.contract, self.full_time, self.contract_unspecified, self.entry_level, self.mid_senior_level, self.director_level, self.associate_level, self.internship_level, self.job_level_unspecified, self.sql, self.excel, self.tableau, self.power_bi, self.python, self.r, self.salary, self.employee_count]