import requests
from bs4 import BeautifulSoup
import math

LIMIT = 20


def get_last_page(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    total_count = soup.find(
        "strong", {"class": "dev_tot"}).get_text()
    last_page = math.ceil(int(total_count.replace(',', ""))/LIMIT)
    return last_page


def extract_job(li):
    company = li.find(
        "div", {"class": "post-list-corp"}).find("a")["title"]
    job_name = li.find(
        "div", {"class": "post-list-info"}).find("a")["title"]
    location = li.find("p", {"class": "option"}).find(
        "span", {"class": "loc long"}).get_text(strip=True)
    job_id = li["data-gno"]
    return {"name": job_name, "company": company, "location": location, "link": f"http://www.jobkorea.co.kr/Recruit/GI_Read/{job_id}"}


def extract_jobs(url, last_page):
    extracted_jobs = []
    for page in range(last_page):
        print(f"Scrapping page:{page}")
        request = requests.get(f"{url}&Page_No={page}")
        soup = BeautifulSoup(request.text, "html.parser")
        infos = soup.find("div", {"class": "recruit-info"})
        results = infos.find_all("li", {"class": "list-post"})
        for result in results:
            job = extract_job(result)
            extracted_jobs.append(job)
    return extracted_jobs


def get_jobs(word):
    url = f"http://www.jobkorea.co.kr/Search/?stext={word}"
    last_page = get_last_page(url)
    jobs = extract_jobs(url, last_page)
    return jobs
