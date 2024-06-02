from bs4 import BeautifulSoup

with open('./Python Files/Input Files/test.html', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
article = soup.find('article', class_='jobs-description__container jobs-description__container--condensed')

if article:
    text = article.get_text(separator='\n', strip=True)  # Get all text within the article, separating by newlines
    print(text)
else:
    print("Article not found")
