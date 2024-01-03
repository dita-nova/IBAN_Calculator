from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # Import the time module

# Initialize the WebDriver
driver = webdriver.Safari()

# Navigate to the website
driver.get('https://www.cnb.cz/cs/platebni-styk/iban/kalkulator-iban-ceska-republika/')

# Wait for the form elements to load
wait = WebDriverWait(driver, 10)
account_number_input = wait.until(EC.presence_of_element_located((By.NAME, 'acc')))
bank_code_input = wait.until(EC.presence_of_element_located((By.NAME, 'bnk')))

# Input the account number and bank code
account_number_input.send_keys('0000123457')
bank_code_input.send_keys('0710')

# Click the "Generate IBAN" button
generate_iban_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value*="IBAN"]')))
generate_iban_button.click()

# Add a short sleep to allow time for potential actions triggered by the button click
time.sleep(3)

iban_output = wait.until(EC.presence_of_element_located((By.NAME, 'iban')))

# Retrieve the IBAN value
generated_iban = iban_output.get_attribute('value')
print("Generated IBAN:", generated_iban)

error_message_element = driver.find_element(By.ID, 'errormessage')
error_message = error_message_element.text.strip()
print("Error Message:", error_message)

# Add a short sleep to observe the result (you can remove this in production)
time.sleep(5)

# Close the browser
driver.quit()
