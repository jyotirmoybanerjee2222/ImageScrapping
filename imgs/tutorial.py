from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os

# Set up Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open Google Images
query = input("Enter your search query: ").replace(' ', '+')
driver.get(f"https://www.google.com/search?q={query}&tbm=isch")

# Scroll down to load more images
for _ in range(4):  # Scroll 3 times
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)

# Find image elements
images = driver.find_elements(By.TAG_NAME, "img")
#print(images)
print(f"Found {len(images)} images!")

# Create folder to save images
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Download images
count = 0
for i, img in enumerate(images):
    try:
        src = img.get_attribute('src')
        if src and "http" in src:
            img_data = requests.get(src).content
            with open(f"downloads/image_{i+1}.jpg", 'wb') as hd:
                hd.write(img_data)
            count += 1
    except Exception as e:
        print(f"Could not download image {i}: {e}")

print(f"Downloaded {count} images.")
driver.quit()
