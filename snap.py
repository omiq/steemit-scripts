from selenium import webdriver
# Save a screenshot from spotify.com in current directory. “””
DRIVER = 'chromedriver'
driver = webdriver.Chrome(DRIVER)
driver.get('https://www.chrisg.com')
screenshot = driver.save_screenshot('my_screenshot.png')
driver.quit()
