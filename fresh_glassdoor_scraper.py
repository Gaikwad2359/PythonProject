from fastapi import FastAPI
from fastapi.responses import JSONResponse
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import os

app = FastAPI(title="Glassdoor Scraper API", version="1.0.0")

@app.get("/")
def read_root():
    return {"message": "Glassdoor Scraper API is running!", "status": "active"}

@app.get("/scrape/")
def scrape_data(keyword: str):
    try:
        # Initialize Glassdoor jobs list
        glassdoor_jobs = []

        options = uc.ChromeOptions()
        options.add_argument('--headless')  # Enable headless for Render
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Additional options for better compatibility
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        driver = None
        try:
            driver = uc.Chrome(options=options)
            driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            # --- Glassdoor Scraping ---
            glassdoor_url = f"https://www.glassdoor.co.in/Job/jobs.htm?sc.keyword={keyword.replace(' ', '%20')}"
            print(f"Navigating to Glassdoor with keyword: {keyword}")
            driver.get(glassdoor_url)
            print("Page loaded, waiting for content...")
            
            time.sleep(8)  # Increased wait time for Render
            
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            job_cards = soup.select('li[data-test="jobListing"]')
            
            print(f"Found {len(job_cards)} job cards")
            
            for job in job_cards:
                title_tag = job.select_one('a.JobCard_jobTitle__GLyJ1[data-test="job-title"]')
                company_tag = job.select_one('span.EmployerProfile_compactEmployerName__9MGcV')
                location_tag = job.select_one('div.JobCard_location__Ds1fM[data-test="emp-location"]')
                apply_link_tag = title_tag
                
                if title_tag and company_tag:  # Only add if we have basic info
                    glassdoor_jobs.append({
                        'jobTitle': title_tag.text.strip() if title_tag else '',
                        'company': company_tag.text.strip() if company_tag else '',
                        'location': location_tag.text.strip() if location_tag else '',
                        'experience': '',
                        'applyLink': f"https://www.glassdoor.co.in{apply_link_tag['href']}" if apply_link_tag and apply_link_tag.has_attr('href') else '',
                        'platform': 'Glassdoor'
                    })

            print(f"Successfully scraped {len(glassdoor_jobs)} jobs from Glassdoor")
            
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            return JSONResponse(
                status_code=500,
                content={"error": f"Scraping failed: {str(e)}", "jobs": []}
            )
        finally:
            if driver:
                driver.quit()
                print("Browser closed")
        
        return {
            "keyword": keyword,
            "total_jobs": len(glassdoor_jobs),
            "jobs": glassdoor_jobs
        }
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"Unexpected error: {error_details}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Unexpected error: {str(e)}", "jobs": []}
        )

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Glassdoor Scraper"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
