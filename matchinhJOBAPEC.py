from PyPDF2 import PdfReader
import docx
import requests
from bs4 import BeautifulSoup

def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_word(file_path):
    doc = docx.Document(file_path)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

def extract_keywords_from_cv(file_path):
    if file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        text = extract_text_from_word(file_path)
    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")
    
    # This is a simple keyword extraction example
    keywords = set(text.split())
    return keywords

def find_relevant_jobs(keywords):
    url = "https://www.apec.fr/candidat/recherche-emploi.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    jobs = []
    for job in soup.find_all('div', class_='job-card'):
        job_title = job.find('h2').text
        job_description = job.find('p').text
        job_keywords = set(job_description.split())
        
        if keywords & job_keywords:  # Intersection of sets
            jobs.append({
                'title': job_title,
                'description': job_description,
                'link': job.find('a')['href']
            })
            
        if len(jobs) >= 50:
            break
    
    return jobs

def main(cv_file_path):
    keywords = extract_keywords_from_cv(cv_file_path)
    jobs = find_relevant_jobs(keywords)
    
    for i, job in enumerate(jobs, start=1):
        print(f"Job {i}: {job['title']}")
        print(f"Description: {job['description']}")
        print(f"Link: {job['link']}")
        print()

if __name__ == "__main__":
    cv_file_path = "votre_cv.pdf"  # Replace with your CV file path
    main(cv_file_path)