# import requests
# from bs4 import BeautifulSoup
# import csv
# import schedule
# import time
# from datetime import datetime

# def scrape_jobs():
#     print(f"\n⏰ Starting job scraping at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

#     url = 'https://vacancymail.co.zw/jobs/'
#     print("📡 Sending request to the VacancyMail jobs page...")
#     response = requests.get(url)

#     if response.status_code == 200:
#         print("✅ Successfully fetched the page!")
#         soup = BeautifulSoup(response.text, 'html.parser')

#         print("🔍 Parsing job listings...")
#         job_listings = soup.find_all('a', class_='job-listing')

#         if not job_listings:
#             print("⚠️ No job listings found. Check the structure or class names.")
#             return

#         filename = 'scraped_jobs.csv'
#         print(f"📁 Creating CSV file: {filename}")
#         with open(filename, mode='w', newline='', encoding='utf-8') as file:
#             writer = csv.writer(file)
#             writer.writerow(['Job Title', 'Company', 'Location', 'Expiry Date', 'Job Description'])

#             print("✍️ Writing job listings to CSV...")
#             for i, job in enumerate(job_listings[:10], start=1):
#                 try:
#                     title_tag = job.find('h3', class_='job-listing-title')
#                     title = title_tag.text.strip() if title_tag else "N/A"

#                     company_tag = job.find('h4', class_='job-listing-company')
#                     company = company_tag.text.strip() if company_tag else "N/A"

#                     description_tag = job.find('p', class_='job-listing-text')
#                     description = description_tag.text.strip() if description_tag else "N/A"

#                     footer = job.find('div', class_='job-listing-footer')
#                     footer_items = footer.find_all('li') if footer else []

#                     location = footer_items[0].text.strip() if len(footer_items) > 0 else "N/A"
#                     expiry = footer_items[1].text.replace("Expires", "").strip() if len(footer_items) > 1 else "N/A"

#                     writer.writerow([title, company, location, expiry, description])
#                     print(f"   ✅ Job #{i} written to file.")
#                 except Exception as e:
#                     print(f"   ❌ Error writing job #{i}: {e}")

#         print(f"🎉 Finished! CSV file '{filename}' has been updated.\n")

#     else:
#         print(f"❌ Failed to fetch the page. Status code: {response.status_code}")

# # 🔁 Schedule the job
# print("📅 Setting up schedule...")
# schedule.every().day.at("09:15").do(scrape_jobs)

# # 🚀 Run immediately for testing
# scrape_jobs()

# print("🕒 Job scheduler is running. Press Ctrl+C to stop.")
# while True:
#     schedule.run_pending()
#     time.sleep(1)

import requests
from bs4 import BeautifulSoup
import csv
import schedule
import time
import logging
from datetime import datetime

# Set up logging configuration
logging.basicConfig(
    filename='scraping.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def setup_logging():
    """Initialize logging with console and file handlers"""
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter and attach to handlers
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    # Get root logger and add handlers
    logger = logging.getLogger()
    logger.addHandler(console_handler)
    
    logging.info("📝 Logging system initialized successfully")

class ScraperException(Exception):
    """Custom exception class for scraper-related errors"""
    pass

def scrape_jobs():
    """
    Scrape job listings from VacancyMail website.
    
    Handles:
    - Webpage fetching
    - HTML parsing
    - CSV writing
    - Error cases
    """
    try:
        logging.info("⏰ Starting job scraping...")
        print(f"\n⏰ Starting job scraping at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Input Phase
        url = 'https://vacancymail.co.zw/jobs/'
        headers = {'User-Agent': 'Mozilla/5.0'}
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            logging.info("✅ Successfully fetched the webpage")
            print("✅ Successfully fetched the webpage")
            
        except requests.exceptions.Timeout:
            logging.error("⌛ Request timed out")
            print("⌛ Request timed out")
            return
            
        except requests.exceptions.ConnectionError:
            logging.error("❌ Failed to connect to server")
            print("❌ Failed to connect to server")
            return
            
        except Exception as e:
            logging.error(f"❌ Unexpected request error: {str(e)}")
            print(f"❌ Unexpected request error: {str(e)}")
            return
        
        # Parsing Phase
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            logging.info("🔍 Parsing job listings...")
            print("🔍 Parsing job listings...")
            
            job_listings = soup.find_all('a', class_='job-listing')
            
            if not job_listings:
                logging.warning("⚠️ No job listings found")
                print("⚠️ No job listings found")
                return
                
        except Exception as e:
            logging.error(f"❌ Parsing error: {str(e)}")
            print(f"❌ Parsing error: {str(e)}")
            raise ScraperException(f"Parsing error: {str(e)}")
        
        # Storage Phase
        filename = 'scraped_jobs.csv'
        logging.info(f"📁 Creating CSV file: {filename}")
        print(f"\n📁 Creating CSV file: {filename}")
        
        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Job Title', 'Company', 'Location', 'Expiry Date', 'Job Description'])
                
                logging.info("✍️ Writing job listings to CSV...")
                print("✍️ Writing job listings to CSV...")
                
                for i, job in enumerate(job_listings[:10], start=1):
                    try:
                        # Extract job details with error handling
                        job_data = {
                            'title': '',
                            'company': 'Unknown Company',
                            'location': 'Unknown Location',
                            'expiry_date': 'No expiry date',
                            'description': 'No description available'
                        }
                        
                        # Extract title
                        title_element = job.find('h3', class_='job-listing-title')
                        if title_element:
                            job_data['title'] = title_element.text.strip()
                            
                        # Extract company
                        company_element = job.find('h4', class_='job-listing-company')
                        if company_element:
                            job_data['company'] = company_element.text.strip()
                            
                        # Extract description
                        description_element = job.find('p', class_='job-listing-text')
                        if description_element:
                            job_data['description'] = description_element.text.strip()
                            
                        # Extract footer information
                        footer = job.find('div', class_='job-listing-footer')
                        if footer:
                            footer_items = footer.find_all('li')
                            if len(footer_items) >= 2:
                                job_data['location'] = footer_items[0].text.strip()
                                job_data['expiry_date'] = footer_items[1].text.replace("Expires", "").strip()
                        
                        writer.writerow([
                            job_data['title'],
                            job_data['company'],
                            job_data['location'],
                            job_data['expiry_date'],
                            job_data['description']
                        ])
                        
                        logging.info(f"✅ Job #{i} processed successfully")
                        print(f"   ✅ Job #{i} written to file.")
                        
                    except Exception as e:
                        logging.error(f"❌ Error processing job #{i}: {str(e)}")
                        print(f"   ❌ Error writing job #{i}: {str(e)}")
                        continue
                        
            logging.info("🎉 Finished scraping! CSV file has been updated successfully!")
            print("\n🎉 Finished! CSV file has been updated successfully.\n")
            
        except IOError as e:
            logging.error(f"❌ Failed to write to CSV file: {str(e)}")
            print(f"❌ Failed to write to CSV file: {str(e)}")
            raise ScraperException(f"CSV write error: {str(e)}")
            
    except ScraperException as se:
        logging.error(f"Scraper exception: {str(se)}")
        print(f"❌ Scraper exception: {str(se)}")
        
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        print(f"❌ Unexpected error: {str(e)}")

def schedule_scraping():
    """Set up scheduled tasks"""
    try:
        # Schedule daily task at 10:30 AM
        schedule.every().day.at("10:30").do(scrape_jobs)
        logging.info("📅 Scheduled daily scraping at 10:30 AM")
        print("📅 Scheduled daily scraping at 10:30 AM")
        
        # Run immediately for testing
        print("🚀 Running initial scrape...")
        scrape_jobs()
        
        # Start scheduler loop
        print("\n🕒 Job scheduler is running. Press Ctrl+C to stop.")
        logging.info("🕒 Scheduler initialized and running")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Wait one minute
            
    except KeyboardInterrupt:
        logging.info("👋 Stopping the scheduler...")
        print("\n👋 Stopping the scheduler...")
        
    except Exception as e:
        logging.error(f"❌ Scheduler error: {str(e)}")
        print(f"❌ Scheduler error: {str(e)}")

if __name__ == "__main__":
    setup_logging()
    schedule_scraping()