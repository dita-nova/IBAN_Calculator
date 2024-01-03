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
iban_input = wait.until(EC.presence_of_element_located((By.NAME, 'iban')))

# Input the account number and bank code
iban_input.send_keys('CZ4907100000000000123457')


# Click the "Generate IBAN" button
generate_account_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value*="Test"]')))
generate_account_button.click()

# Add a short sleep to allow time for potential actions triggered by the button click
time.sleep(3)

account_output = wait.until(EC.presence_of_element_located((By.NAME, 'acc')))
bank_code_output = wait.until(EC.presence_of_element_located((By.NAME, 'bnk')))
bic_code_output = wait.until(EC.presence_of_element_located((By.NAME, 'bic')))
account_first_output = wait.until(EC.presence_of_element_located((By.NAME, 'cur')))

# Retrieve the account value
generated_account = account_output.get_attribute('value')
generated_bank_code = bank_code_output.get_attribute('value')
generated_bic_code = bic_code_output.get_attribute('value')
generate_account_first_output = account_first_output.get_attribute('value')
print("account number",  generate_account_first_output, generated_account, generated_bank_code)

# Add a short sleep to observe the result (you can remove this in production)
time.sleep(5)

# Close the browser
driver.quit()
