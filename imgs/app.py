from flask import Flask, request, render_template_string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests
import os

app = Flask(__name__)

# Simple HTML form
HTML = """
<!doctype html>
<title>Image Downloader</title>
<h1>Enter your search query</h1>
<form method="POST">
  <input name="query" type="text" placeholder="e.g., cute puppies">
  <input type="submit" value="Download Images">
</form>
<p>{{ message }}</p>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ''
    if request.method == 'POST':
        query = request.form['query'].replace(' ', '+')

        # Set up Chrome driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(f"https://www.google.com/search?q={query}&tbm=isch")

        # Scroll down
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        # Find images
        images = driver.find_elements(By.TAG_NAME, "img")
        print(f"Found {len(images)} images!")
        folder_name = query.replace('+', '_')
        
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        count = 0
        for i, img in enumerate(images):
            try:
                src = img.get_attribute('src')
                if src and "http" in src:
                    img_data = requests.get(src).content
                    with open(f"{folder_name}/image_{i+1}.jpg", 'wb') as handler:
                        handler.write(img_data)
                    count += 1
            except Exception as e:
                print(f"Could not download image {i}: {e}")

        driver.quit()
        message = f"Downloaded {count} images into folder '{folder_name}'."
        app.logger.debug(message)

    return render_template_string(HTML, message=message)

if __name__ == '__main__':
    app.run(debug=True)
