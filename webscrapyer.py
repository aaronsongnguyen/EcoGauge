import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def scrape_threads(url):
    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    
    # Initialize the WebDriver
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Navigate to the URL
        driver.get(url)
        
        # Wait for the content to load (adjust the timeout and conditions as needed)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "x1lliihq"))
        )
        
        # Allow some time for dynamic content to load
        time.sleep(5)
        
        # Get the page source and parse it with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Find all thread elements
        thread_elements = soup.find_all('span', class_='x1lliihq')
        
        # Extract the text from each thread element
        threads = [thread.get_text(strip=True) for thread in thread_elements]
        
        return threads
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
    
    finally:
        # Close the browser
        driver.quit()

# URL of the Threads page you want to scrape
url = "https://www.threads.net/search?q=Lebron&serp_type=default"

# Scrape the threads
thread_list = scrape_threads(url)

# Print the scraped threads
print(len(thread_list))
