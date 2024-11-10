import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# Define the directory where queued photos are stored
PHOTO_QUEUE_DIR = "path/to/your/photo_queue"

# Interval in seconds for updating the DP
UPDATE_INTERVAL = 3600  # For example, every hour

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--user-data-dir=path/to/chrome/profile")  # Use a custom profile for logged-in WhatsApp Web
    driver = webdriver.Chrome(executable_path="path/to/chromedriver", options=options)
    return driver

def update_group_dp(driver):
    # Ensure there are images in the queue
    photos = os.listdir(PHOTO_QUEUE_DIR)
    if not photos:
        print("No photos in queue.")
        return
    
    # Select the first photo in the queue
    photo_path = os.path.join(PHOTO_QUEUE_DIR, photos[0])

    # Open WhatsApp Web
    driver.get("https://web.whatsapp.com")
    time.sleep(15)  # Wait for WhatsApp to load and scan QR code if needed
    
    # Locate and click the group for which you want to change the DP
    group_name = "Your Group Name"
    search_box = driver.find_element(By.XPATH, '//*[@title="Search or start new chat"]')
    search_box.click()
    search_box.send_keys(group_name)
    time.sleep(2)
    
    # Click on the group to open chat
    group = driver.find_element(By.XPATH, f'//span[@title="{group_name}"]')
    group.click()
    time.sleep(2)

    # Access group info
    group_info = driver.find_element(By.XPATH, '//*[@title="Group info"]')
    group_info.click()
    time.sleep(2)

    # Click on the DP to edit
    edit_dp = driver.find_element(By.XPATH, '//span[@data-testid="group-photo"]')
    edit_dp.click()
    time.sleep(2)

    # Click on the "Change group icon" button
    change_dp = driver.find_element(By.XPATH, '//span[text()="CHANGE GROUP ICON"]')
    change_dp.click()
    time.sleep(2)

    # Choose "Upload photo"
    upload_option = driver.find_element(By.XPATH, '//input[@type="file"]')
    upload_option.send_keys(photo_path)
    time.sleep(5)

    # Confirm upload
    confirm_button = driver.find_element(By.XPATH, '//span[text()="SAVE"]')
    confirm_button.click()
    time.sleep(3)

    # Delete the used photo from the queue
    os.remove(photo_path)
    print(f"Updated group DP with {photos[0]} and removed from queue.")

def main():
    driver = setup_driver()
    
    try:
        while True:
            update_group_dp(driver)
            time.sleep(UPDATE_INTERVAL)  # Wait until the next update
    except KeyboardInterrupt:
        print("Program stopped.")
    finally:
        driver.quit()

if __name__ == "__main__":
        main()