import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QFormLayout, QHBoxLayout,QMessageBox
from PyQt6.QtGui import QFont, QGuiApplication, QIcon
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QRegularExpressionValidator
from PyQt6.QtCore import QRegularExpression

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.safari.options import Options 
import time
import os



class IBANScraperThread(QThread):
    result = pyqtSignal(str, str)

    def __init__(self, account_number, bank_code):
        super().__init__()
        self.account_number = account_number
        self.bank_code = bank_code

    def run(self):
        options =  Options()
        options.headless = True
        
        driver = webdriver.Safari(options=options)
        driver.get('https://www.cnb.cz/cs/platebni-styk/iban/kalkulator-iban-ceska-republika/')

        # Wait for the form elements to load
        wait = WebDriverWait(driver, 10)
        account_number_input = wait.until(EC.presence_of_element_located((By.NAME, 'acc')))
        bank_code_input = wait.until(EC.presence_of_element_located((By.NAME, 'bnk')))

        # Input the user-provided account number and bank code
        account_number_input.send_keys(self.account_number)
        bank_code_input.send_keys(self.bank_code)

        # Click the "Generate IBAN" button
        generate_iban_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value*="IBAN"]')))
        generate_iban_button.click()

        # Wait for the IBAN to be generated
        time.sleep(3)  # This can be adjusted or replaced with more robust wait conditions

        iban_output = wait.until(EC.presence_of_element_located((By.NAME, 'iban')))
        generated_iban = iban_output.get_attribute('value')

        # Check for error messages
        error_message = ""
        try:
            error_message_element = driver.find_element(By.ID, 'errormessage')
            error_message = error_message_element.text.strip()
        except:
            # If no error message element is found, we assume there's no error
            pass

        # Emit the result
        self.result.emit(generated_iban, error_message)
        driver.quit()


class AccountScraperThread(QThread):
    result = pyqtSignal(str, str)

    def __init__(self, iban):
        super().__init__()
        self.iban = iban

    def run(self):
        options = Options()
        options.headless = True
        
        driver = webdriver.Safari(options=options)
        driver.get('https://www.cnb.cz/cs/platebni-styk/iban/kalkulator-iban-ceska-republika/')
            
        # Wait for the form elements to load
        wait = WebDriverWait(driver, 10)
        iban_input = wait.until(EC.presence_of_element_located((By.NAME, 'iban')))
            
        # Input the IBAN
        iban_input.send_keys(self.iban)
            
        # Click the "Generate IBAN" button
        generate_account_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[value*="Test"]')))
        generate_account_button.click()
            
        # Wait for the response to ensure that the account details are loaded
        time.sleep(3)
            
        # Retrieve the account details
        account_output = wait.until(EC.presence_of_element_located((By.NAME, 'acc')))
        bank_code_output = wait.until(EC.presence_of_element_located((By.NAME, 'bnk')))
        # bic_code_output = wait.until(EC.presence_of_element_located((By.NAME, 'bic')))
        account_first_output = wait.until(EC.presence_of_element_located((By.NAME, 'cur')))
            
        generated_account = account_output.get_attribute('value')
        generated_bank_code = bank_code_output.get_attribute('value')
        #generated_bic_code = bic_code_output.get_attribute('value')
        generate_account_first_output = account_first_output.get_attribute('value')

        error_message2 = ""
        try:
            error_message_element = driver.find_element(By.ID, 'errormessage')
            error_message2 = error_message_element.text.strip()
        except:
        # If no error message element is found, we assume there's no error
            pass

        # Format results
        formated_result = f"{generate_account_first_output} - {generated_account} / {generated_bank_code}"

        # Emit the result
        self.result.emit(formated_result, error_message2)
        driver.quit()

class IBANCalculatorApp(QWidget):
    def __init__(self):
        super().__init__()
        print(f'current working directory: {os.getcwd()}')
        icon_path = 'logo_512x512.png'
        if os.path.exists(icon_path):
            print(f"Icon exists at: {icon_path}")
        else:
            print(f"Icon does not exist at: {icon_path}")

        self.last_calculated_result = None  # Initialize variable to store the last result
        self.init_ui()

         # Apply the stylesheet
        self.setStyleSheet(
            "QWidget { background-color: #fffffb; }"
            "QPushButton { background-color: #005f73; color: white; border-radius: 10px;  padding: 5px 15px; font-weight: bold; border: none;  }"
            "QPushButton:hover { background-color: #0a9396; }"
            "QPushButton:pressed { background-color: #003f5c;}"
            "QLineEdit { border: 1px solid gray; }"
            "QTextEdit { border: 1px solid gray; background-color: #FFFFFF; }"           
        )
        
         # Set the font for the application
        self.setFont(QFont("Arial", 10))

        # Set the application icon
        self.setWindowIcon(QIcon('logo_512x512.png')) 

    def init_ui(self):
        # Section 1: Account to IBAN
        layout_section1 = QFormLayout()
        self.edit_account1 = QLineEdit()
        self.edit_account2 = QLineEdit()
        self.edit_bank_code = QLineEdit()
        layout_section1.addRow(QLabel('First Account Number:'), self.edit_account1)
        layout_section1.addRow(QLabel('Second Account Number:'), self.edit_account2)
        layout_section1.addRow(QLabel('Bank Code:'), self.edit_bank_code)

        # Button for calculating IBAN
        btn_calculate_iban = QPushButton('Calculate IBAN')
        btn_calculate_iban.setFixedSize(150, 30)
        btn_calculate_iban.clicked.connect(self.on_calculate_clicked)

        # Layout for centering the button
        layout_calculate_button = QHBoxLayout()
        layout_calculate_button.addStretch()
        layout_calculate_button.addWidget(btn_calculate_iban)
        layout_calculate_button.addStretch()

        # Section 2: IBAN to Account
        layout_section2 = QFormLayout()
        self.edit_account_to_iban = QLineEdit()
        layout_section2.addRow(QLabel('IBAN:'), self.edit_account_to_iban)
        self.edit_account_to_iban.setFixedWidth(200)

        # Button for calculating account number
        btn_calculate_account = QPushButton('Calculate account number')
        btn_calculate_account.clicked.connect(self.on_calculate_account_clicked)
        layout_section2.addWidget(btn_calculate_account)

        # Error Message Display
        self.error_message = QTextEdit()
        self.error_message.setPlaceholderText('Results will be shown here...')
        self.error_message.setReadOnly(True)

        # Clear and Copy buttons
        self.btn_clear = QPushButton('Clear')
        self.btn_clear.clicked.connect(self.clear_inputs)

        self.btn_copy_result = QPushButton('Copy Result')
        self.btn_copy_result.clicked.connect(self.copy_result_to_clipboard)

        # Layout for buttons
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.btn_clear)
        layout_buttons.addWidget(self.btn_copy_result)

        # Main layout combining all sections
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout_section1)
        main_layout.addLayout(layout_calculate_button)
        main_layout.addLayout(layout_section2)
        main_layout.addWidget(self.error_message)
        main_layout.addLayout(layout_buttons)
        self.setLayout(main_layout)

        # Window configurations
        self.setWindowTitle('IBAN Calculator')
        self.setGeometry(100, 100, 600, 400)

    def on_calculate_clicked(self):
        account_number = self.edit_account1.text() + self.edit_account2.text()
        bank_code = self.edit_bank_code.text()
        self.iban_scraper_thread = IBANScraperThread(account_number, bank_code)
        self.iban_scraper_thread.result.connect(self.on_iban_scraped)
        self.iban_scraper_thread.start()

    def on_iban_scraped(self, iban, error_message):
        if error_message:
            self.error_message.setText(f"Error: {error_message}")
        else:
            self.last_calculated_result = f"Calculated IBAN: {iban}"
            self.error_message.setText(self.last_calculated_result)

    def on_calculate_account_clicked(self):
        iban = self.edit_account_to_iban.text()
        self.account_scraper_thread = AccountScraperThread(iban)
        self.account_scraper_thread.result.connect(self.on_account_scraped)
        self.account_scraper_thread.start()

    def on_account_scraped(self, formatted_result, error_message):
        try:
            generated_account_first_output, rest = formatted_result.split(' - ')
            generated_account, generated_bank_code = rest.split(' / ')
        except ValueError:
            QMessageBox.warning(self, 'Error', 'The formatted result does not contain the expected data.')
            return
        
        if error_message:
            self.error_message.setText(f"Error: {error_message}")
        else:
            self.last_calculated_result = f"Account Number: {generated_account}, Bank Code: {generated_bank_code}"
            self.error_message.setText(self.last_calculated_result)

    def clear_inputs(self):
        self.edit_account1.clear()
        self.edit_account2.clear()
        self.edit_bank_code.clear()
        self.edit_account_to_iban.clear()
        self.error_message.clear()
        self.last_calculated_result = None  # Reset the last result when clearing inputs

    def copy_result_to_clipboard(self):
        if self.last_calculated_result:
            # Check if we're dealing with an account number and bank code
            if "Account Number:" in self.last_calculated_result and "Bank Code:" in self.last_calculated_result:
                # Extract the account number and bank code and format them
                parts = self.last_calculated_result.split(',')
                account_number = parts[0].split(': ')[-1].strip()
                bank_code = parts[1].split(': ')[-1].strip()
                formatted_text = f"{account_number}/{bank_code}"
            else:
                # If it's not an account number and bank code, copy the result as is
                formatted_text = self.last_calculated_result.split(': ')[-1]

            QGuiApplication.clipboard().setText(formatted_text)
            QMessageBox.information(self, 'Copied', 'Result has been copied to clipboard.')
        else:
            QMessageBox.warning(self, 'Error', 'No result to copy.')


    def clear_inputs(self):
        self.edit_account1.clear()
        self.edit_account2.clear()
        self.edit_bank_code.clear()
        self.edit_account_to_iban.clear()
        self.error_message.clear()
        self.last_calculated_result = None  # Reset the last result when clearing inputs

def copy_result_to_clipboard(self):
    if self.last_calculated_result:
        # Check if we're dealing with an account number and bank code
        if "Account Number:" in self.last_calculated_result and "Bank Code:" in self.last_calculated_result:
            # Extract the account number and bank code and format them
            parts = self.last_calculated_result.split(',')
            account_number = parts[0].split(': ')[-1].strip()
            bank_code = parts[1].split(': ')[-1].strip()
            formatted_text = f"{account_number}/{bank_code}"
        else:
            # If it's not an account number and bank code, copy the result as is
            formatted_text = self.last_calculated_result.split(': ')[-1]

        QGuiApplication.clipboard().setText(formatted_text)
        QMessageBox.information(self, 'Copied', 'Result has been copied to clipboard.')
    else:
        QMessageBox.warning(self, 'Error', 'No result to copy.')



if __name__ == '__main__':
    app = QApplication([])
    iban_calculator = IBANCalculatorApp()
    iban_calculator.show()
    sys.exit(app.exec())