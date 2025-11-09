#!/usr/bin/env python3
"""
LinkedIn Profile Scraper
Scrapes public LinkedIn profiles and saves data to CSV.
WARNING: LinkedIn scraping may violate their Terms of Service.
Use only for educational purposes with test accounts and public data.
"""

import os
import sys
import time
import logging
import random
import argparse
from datetime import datetime
from typing import List, Dict, Optional

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class LinkedInScraper:
    """Scraper for LinkedIn public profiles"""
    
    def __init__(self, headless: bool = False):
        """Initialize the scraper with Chrome driver"""
        self.headless = headless
        self.driver = None
        self.is_logged_in = False
        self.profiles_data = []
        
    def setup_driver(self) -> None:
        """Set up Chrome WebDriver with appropriate options"""
        chrome_options = Options()
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        # Anti-detection measures
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument(f'user-agent={UserAgent().random}')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        try:
            # Try to use custom chromedriver path if provided
            chrome_driver_path = os.getenv('CHROME_DRIVER_PATH')
            if chrome_driver_path and os.path.exists(chrome_driver_path):
                service = Service(chrome_driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info(f"Using ChromeDriver from: {chrome_driver_path}")
            else:
                # Use webdriver-manager to auto-download driver
                driver_path = ChromeDriverManager().install()
                
                # Fix: webdriver-manager sometimes returns wrong file (THIRD_PARTY_NOTICES.chromedriver)
                # We need to find the actual chromedriver executable
                if not os.path.isfile(driver_path) or not os.access(driver_path, os.X_OK) or 'THIRD_PARTY' in driver_path:
                    # If path is invalid or points to wrong file, search for actual chromedriver
                    base_dir = driver_path
                    if os.path.isfile(driver_path):
                        base_dir = os.path.dirname(driver_path)
                    elif not os.path.isdir(driver_path):
                        base_dir = os.path.dirname(os.path.dirname(driver_path))
                    
                    # Search for chromedriver executable
                    possible_paths = [
                        os.path.join(base_dir, 'chromedriver'),
                        os.path.join(base_dir, 'chromedriver-mac-arm64', 'chromedriver'),
                        os.path.join(base_dir, 'chromedriver-mac-x64', 'chromedriver'),
                    ]
                    
                    # Also check parent directories
                    parent_dir = os.path.dirname(base_dir) if os.path.isdir(base_dir) else base_dir
                    possible_paths.extend([
                        os.path.join(parent_dir, 'chromedriver'),
                        os.path.join(parent_dir, 'chromedriver-mac-arm64', 'chromedriver'),
                        os.path.join(parent_dir, 'chromedriver-mac-x64', 'chromedriver'),
                    ])
                    
                    driver_found = False
                    for path in possible_paths:
                        if os.path.isfile(path) and os.access(path, os.X_OK) and 'THIRD_PARTY' not in path:
                            driver_path = path
                            driver_found = True
                            break
                    
                    # If still not found, search recursively
                    if not driver_found:
                        search_dirs = [base_dir, parent_dir] if os.path.isdir(base_dir) else [os.path.dirname(base_dir)]
                        for search_dir in search_dirs:
                            if os.path.isdir(search_dir):
                                for root, dirs, files in os.walk(search_dir):
                                    for file in files:
                                        if file == 'chromedriver' and 'THIRD_PARTY' not in root:
                                            candidate = os.path.join(root, file)
                                            if os.access(candidate, os.X_OK):
                                                driver_path = candidate
                                                driver_found = True
                                                break
                                    if driver_found:
                                        break
                            if driver_found:
                                break
                    
                    if not driver_found:
                        raise FileNotFoundError(f"Could not find chromedriver executable. Searched in: {base_dir}")
                
                service = Service(driver_path)
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
                logger.info(f"Using auto-managed ChromeDriver: {driver_path}")
                
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            logger.info("Chrome WebDriver initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise
    
    def login(self, email: str = None, password: str = None) -> bool:
        """
        Log in to LinkedIn (optional, for accessing more profile data)
        Note: Login may not be necessary for public profiles
        """
        if not email or not password:
            email = os.getenv('LINKEDIN_EMAIL')
            password = os.getenv('LINKEDIN_PASSWORD')
        
        if not email or not password:
            logger.warning("LinkedIn credentials not provided. Skipping login.")
            return False
        
        try:
            logger.info("Attempting to log in to LinkedIn...")
            self.driver.get('https://www.linkedin.com/login')
            time.sleep(random.uniform(2, 4))
            
            # Enter email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.send_keys(email)
            time.sleep(random.uniform(0.5, 1))
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(password)
            time.sleep(random.uniform(0.5, 1))
            
            # Click sign in
            sign_in_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            sign_in_button.click()
            
            # Wait for redirect
            time.sleep(random.uniform(3, 5))
            
            # Check if login successful
            if 'feed' in self.driver.current_url or 'checkpoint' not in self.driver.current_url:
                logger.info("Successfully logged in to LinkedIn")
                self.is_logged_in = True
                return True
            else:
                logger.warning("Login may have failed or requires verification")
                return False
                
        except Exception as e:
            logger.error(f"Login failed: {e}")
            return False
    
    def scrape_profile(self, profile_url: str) -> Optional[Dict]:
        """Scrape a single LinkedIn profile"""
        try:
            logger.info(f"Scraping profile: {profile_url}")
            self.driver.get(profile_url)
            
            # Random delay to appear human-like
            time.sleep(random.uniform(3, 6))
            
            # Wait for the page to load
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
            except TimeoutException:
                logger.warning(f"Timeout waiting for profile page: {profile_url}")
                return None
            
            # Scroll down to load more content
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(random.uniform(1, 2))
            
            # Parse page with BeautifulSoup
            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            
            # Extract profile data with fallbacks
            profile_data = {
                'profile_url': profile_url,
                'name': self._extract_name(soup),
                'headline': self._extract_headline(soup),
                'location': self._extract_location(soup),
                'current_company': self._extract_current_company(soup),
                'experience_summary': self._extract_experience_summary(soup),
                'education': self._extract_education(soup),
                'skills': self._extract_skills(soup),
                'extraction_timestamp': datetime.now().isoformat()
            }
            
            logger.info(f"Successfully scraped profile: {profile_data['name']}")
            return profile_data
            
        except Exception as e:
            logger.error(f"Error scraping profile {profile_url}: {e}")
            return None
    
    def _extract_name(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract profile name"""
        try:
            # Try multiple selectors
            selectors = [
                'h1.text-heading-xlarge',
                'h1.inline.t-24.v-align-middle.break-words',
                'h1.top-card-layout__title'
            ]
            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    return element.get_text(strip=True)
            return None
        except:
            return None
    
    def _extract_headline(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract profile headline"""
        try:
            selectors = [
                'div.text-body-medium.break-words',
                'div.top-card-layout__headline',
                'h2.mt1.t-18.t-black.t-normal.break-words'
            ]
            for selector in selectors:
                element = soup.select_one(selector)
                if element:
                    return element.get_text(strip=True)
            return None
        except:
            return None
    
    def _extract_location(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract location"""
        try:
            selectors = [
                'span.text-body-small.inline.t-black--light.break-words',
                'div.top-card__subline-item',
                'span.top-card-layout__first-subline'
            ]
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(strip=True)
                    # Location usually doesn't have numbers
                    if not any(char.isdigit() for char in text) and len(text) > 3:
                        return text
            return None
        except:
            return None
    
    def _extract_current_company(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract current company from experience section"""
        try:
            experience_section = soup.find('section', {'id': 'experience'})
            if not experience_section:
                # Try alternative selector
                experience_section = soup.find('div', {'id': 'experience'})
            
            if experience_section:
                # Get first experience item (most recent)
                experience_items = experience_section.find_all('li', class_='artdeco-list__item')
                if experience_items:
                    first_item = experience_items[0]
                    company_elem = first_item.find('span', class_='t-14')
                    if company_elem:
                        return company_elem.get_text(strip=True)
            return None
        except:
            return None
    
    def _extract_experience_summary(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract experience summary (first 200 chars)"""
        try:
            experience_section = soup.find('section', {'id': 'experience'})
            if experience_section:
                text = experience_section.get_text(separator=' ', strip=True)
                return text[:200] + '...' if len(text) > 200 else text
            return None
        except:
            return None
    
    def _extract_education(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract education (first school)"""
        try:
            education_section = soup.find('section', {'id': 'education'})
            if not education_section:
                education_section = soup.find('div', {'id': 'education'})
            
            if education_section:
                school_elem = education_section.find('h3', class_='t-16')
                if not school_elem:
                    school_elem = education_section.find('span', class_='t-16')
                if school_elem:
                    return school_elem.get_text(strip=True)
            return None
        except:
            return None
    
    def _extract_skills(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract skills (top 5, comma-separated)"""
        try:
            skills_section = soup.find('section', {'id': 'skills'})
            if skills_section:
                skill_elements = skills_section.find_all('span', class_='t-bold')[:5]
                skills = [skill.get_text(strip=True) for skill in skill_elements]
                return ', '.join(skills) if skills else None
            return None
        except:
            return None
    
    def scrape_multiple_profiles(self, profile_urls: List[str]) -> List[Dict]:
        """Scrape multiple profiles with polite delays"""
        self.profiles_data = []
        
        for idx, url in enumerate(profile_urls, 1):
            logger.info(f"Processing profile {idx}/{len(profile_urls)}")
            
            profile_data = self.scrape_profile(url)
            if profile_data:
                self.profiles_data.append(profile_data)
            
            # Polite delay between requests (2-6 seconds)
            if idx < len(profile_urls):
                delay = random.uniform(2, 6)
                logger.info(f"Waiting {delay:.1f} seconds before next profile...")
                time.sleep(delay)
        
        return self.profiles_data
    
    def save_to_csv(self, output_file: str = 'profiles.csv') -> None:
        """Save scraped data to CSV"""
        if not self.profiles_data:
            logger.warning("No profile data to save")
            return
        
        df = pd.DataFrame(self.profiles_data)
        df.to_csv(output_file, index=False, encoding='utf-8')
        logger.info(f"Saved {len(self.profiles_data)} profiles to {output_file}")
        
        # Print summary
        print("\n" + "="*50)
        print(f"SCRAPING SUMMARY")
        print("="*50)
        print(f"Total profiles scraped: {len(self.profiles_data)}")
        print(f"Output file: {output_file}")
        print(f"Columns: {', '.join(df.columns)}")
        print("="*50 + "\n")
    
    def close(self) -> None:
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")


def load_urls_from_file(file_path: str) -> List[str]:
    """Load LinkedIn profile URLs from a text file"""
    try:
        with open(file_path, 'r') as f:
            urls = [line.strip() for line in f if line.strip() and line.strip().startswith('http')]
        logger.info(f"Loaded {len(urls)} URLs from {file_path}")
        return urls
    except FileNotFoundError:
        logger.error(f"URL file not found: {file_path}")
        return []


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Scrape LinkedIn profiles to CSV')
    parser.add_argument('--urls', type=str, default='urls.txt', 
                        help='Path to file containing LinkedIn profile URLs')
    parser.add_argument('--output', type=str, default='profiles.csv',
                        help='Output CSV file path')
    parser.add_argument('--headless', action='store_true',
                        help='Run browser in headless mode')
    parser.add_argument('--login', action='store_true',
                        help='Attempt to login to LinkedIn (requires credentials in .env)')
    
    args = parser.parse_args()
    
    # Load URLs
    profile_urls = load_urls_from_file(args.urls)
    if not profile_urls:
        logger.error("No valid URLs found. Exiting.")
        return
    
    # Initialize scraper
    scraper = LinkedInScraper(headless=args.headless)
    
    try:
        # Setup driver
        scraper.setup_driver()
        
        # Optional login
        if args.login:
            scraper.login()
        
        # Scrape profiles
        logger.info(f"Starting to scrape {len(profile_urls)} profiles...")
        scraper.scrape_multiple_profiles(profile_urls)
        
        # Save results
        scraper.save_to_csv(args.output)
        
    except KeyboardInterrupt:
        logger.info("Scraping interrupted by user")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
    finally:
        scraper.close()


if __name__ == '__main__':
    main()

