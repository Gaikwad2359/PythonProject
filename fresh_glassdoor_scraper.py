from fastapi import FastAPI
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time

app = FastAPI()

@app.get("/scrape/")
def scrape_data(keyword: str):
    try:
        # Initialize Glassdoor jobs list
        glassdoor_jobs = []

        options = uc.ChromeOptions()
        # options.add_argument('--headless')  # Uncomment for headless mode
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')

        # Explicitly specify ChromeDriver version 138 to match Chrome browser version
        # driver = uc.Chrome(options=options, version_main=138)
        driver = uc.Chrome(options=options)
        
        # --- Glassdoor Scraping ---
        glassdoor_url = f"https://www.glassdoor.co.in/Job/jobs.htm?sc.keyword={keyword.replace(' ', '%20')}"
        try:
            print("Navigating to Glassdoor...")
            driver.get(glassdoor_url)
            print("Navigated to Glassdoor.")
        except Exception as e:
            print("Error navigating to Glassdoor:", e)
        time.sleep(10)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        job_cards = soup.select('li[data-test="jobListing"]')
        for job in job_cards:
            title_tag = job.select_one('a.JobCard_jobTitle__GLyJ1[data-test="job-title"]')
            company_tag = job.select_one('span.EmployerProfile_compactEmployerName__9MGcV')
            location_tag = job.select_one('div.JobCard_location__Ds1fM[data-test="emp-location"]')
            apply_link_tag = title_tag
            glassdoor_jobs.append({
                'jobTitle': title_tag.text.strip() if title_tag else '',
                'company': company_tag.text.strip() if company_tag else '',
                'location': location_tag.text.strip() if location_tag else '',
                'experience': '',
                'applyLink': apply_link_tag['href'] if apply_link_tag and apply_link_tag.has_attr('href') else '',
                'platform': 'Glassdoor'
            })

        print(f"Glassdoor jobs found: {len(glassdoor_jobs)}")
        driver.quit()
        
        return glassdoor_jobs
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e)}
