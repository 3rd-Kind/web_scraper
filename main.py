import os
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create Path to store images.
path = "C:\\Users\\3rdki\\OneDrive\\Desktop"

# Instantiate an Options object
options = Options()

# Set the path to the Chrome driver executable
options.binary_location = path

# Pass the Options object to the webdriver.Chrome() method
driver = webdriver.Chrome()
# The default page which should be bought up.
google_search = 'https://www.google.com/imghp?hl=en&authuser=0&ogbl'

# Prompt user for search term.
search_term = input('What would you like to scrape? ')
# Set search_term to saved_term.
saved_term = search_term
# Name of directory, where images will be saved.
image_directory = f"{saved_term}_images"


def scraping_images_from_google(driver, max_images):
    # If there is a search term.
    if search_term:
        # Pull up the default google page.
        driver.get(google_search)
        # Find the accept button and enter.
        accept_button = driver.find_element(By.ID, 'L2AGLb')
        accept_button.send_keys(Keys.RETURN)
        # Wait for 2 seconds.
        driver.implicitly_wait(2)
        # Find the search box.
        search_box = driver.find_element(By.ID, 'APjFqb')
        # Clear the search box incase anything is inside it.
        search_box.clear()
        # Send the users search term to the search box and enter.
        search_box.send_keys(saved_term)
        search_box.send_keys(Keys.RETURN)
        # Wait for 2 seconds.
        driver.implicitly_wait(2)
    # Within the range of max_images.
    for _ in range(max_images):
        # Scroll down the page.
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    # Wait until the picture element becomes available & then find those elements.
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.Q4LuWd')))
    image_elements = driver.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")

    # If the folder does not exist for the desired search term, create directory.
    if not os.path.exists(image_directory):
        os.makedirs(image_directory)
        print('Directory created successfully')
    else:
        # Show directory already exists.
        print("Directory already exists!")

    # For image & image_element in images up till max_images.
    for image, image_element in enumerate(image_elements[:max_images]):
        try:
            # Click on each image_element.
            image_element.click()
            # Wait and find the css_selector, for images.
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((
                By.CSS_SELECTOR, 'img.sFlh5c.pT0Scc.iPVvYb')))

            # Set image_url_element to the css_selector.
            img_url_element = driver.find_element(By.CSS_SELECTOR, 'img.sFlh5c.pT0Scc.iPVvYb')
            # Set img_url to the source of img_url_element.
            img_url = img_url_element.get_attribute("src")
            # Set each image name and increment by 1.
            image_name = f"{search_term}_{image+1}.jpg"
            # Set image_path by joining image_directory, image_name.
            image_path = os.path.join(image_directory, image_name)
            # Request the img_url use stream to get pictures individually.
            image_content = requests.get(img_url, stream=True)
            # Download the image in chunks.
            with open(image_path, "wb") as file:
                for chunk in image_content.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            # Show image has been saved.
            print(f"Image {image+1} download successfully")
        # If an error occurs display exception.
        except Exception as e:
            print(f"ERROR - Could not save {image+1}: {e}")


# Call the function passing the options object
scraping_images_from_google(driver, 20)

# Quit after code has executed.
driver.quit()
