import MyWeb
import re

with open('test.html') as f:
    html = f.read()
pageText = MyWeb.BeautifulSoup(html, 'html')
hyperlinks = pageText.find_all('a')

# Curate list of job URL's
list_of_job_pages = []
regex_pattern = '^\/jobs\/view\/'
for link in hyperlinks:
    _ = link.get('href')
    if re.search(regex_pattern, _) is not None:
        list_of_job_pages.append(f'linkedin.com{_}')

print('Done')