from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_price(url):
    """
    Scrapes product prices from Amazon, Flipkart, and Myntra.
    Returns price as string or 'Price not found' if unable to extract.
    """
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        # Detect which platform we're scraping
        if "amazon" in url.lower():
            price = _scrape_amazon(driver, wait)
        elif "flipkart" in url.lower():
            price = _scrape_flipkart(driver, wait)
        elif "myntra" in url.lower():
            price = _scrape_myntra(driver, wait)
        else:
            price = "Price not found"

    except Exception as e:
        print(f"Scraping error: {e}")
        price = "Price not found"
    finally:
        driver.quit()

    return price


def _scrape_amazon(driver, wait):
    """Amazon price extraction"""
    try:
        wait.until(
            EC.presence_of_element_located((By.ID, "corePriceDisplay_desktop_feature_div"))
        )
        whole = driver.find_element(By.CLASS_NAME, "a-price-whole").text
        fraction = driver.find_element(By.CLASS_NAME, "a-price-fraction").text
        price = whole.replace(",", "") + "." + fraction
        return price
    except:
        return "Price not found"


def _scrape_flipkart(driver, wait):
    """Flipkart price extraction"""
    try:
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "_30jeq3"))
        )
        price_element = driver.find_element(By.CLASS_NAME, "_30jeq3")
        price = price_element.text.replace("₹", "").replace(",", "").strip()
        return price
    except:
        return "Price not found"


def _scrape_myntra(driver, wait):
    """Myntra price extraction"""
    try:
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "discountedPriceText"))
        )
        price_element = driver.find_element(By.CLASS_NAME, "discountedPriceText")
        price = price_element.text.replace("₹", "").replace(",", "").strip()
        return price
    except:
        return "Price not found"

