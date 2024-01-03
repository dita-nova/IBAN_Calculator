Introduction
This repository contains a Python-based application designed as part of a portfolio to demonstrate web scraping and automation skills. The application provides a user-friendly interface for converting account numbers to IBANs and vice versa, leveraging web scraping techniques.

Files Description
application.py
Description: The main application file, built using PyQt6. It offers a graphical user interface to interact with the application's features.
Functionality: Integrates with other scripts to provide functionalities like account number to IBAN conversion and vice versa.

acount_to_iban.py
Description: A script utilizing Selenium for automating the conversion of account numbers to IBANs.
Functionality: Automates a web browser to input an account number into a web form and retrieve the corresponding IBAN.

iban_to_account.py
Description: Similar to acount_to_iban.py, this script uses Selenium to convert IBANs back to account numbers.
Functionality: Interacts with a web form to perform the reverse operation of acount_to_iban.py.

prep.py
Description: A basic web scraping script using BeautifulSoup and requests.
Functionality: Fetches and parses HTML content from a specific URL, demonstrating basic web scraping capabilities.

testing.txt
Description: Contains test data including an account number and an IBAN.
Functionality: Used for testing the application's conversion functionalities.

Installation
Ensure Python 3.x is installed on your system.
Install required packages using pip install -r requirements.txt.
Run python3 application.py to launch the application.

Usage
The main application (aplication.py) provides a user-friendly GUI.
Enter an account number to convert it to an IBAN or an IBAN to convert it back to an account number.
Utilize prep.py for basic web scraping demonstrations.

Technical Details of the IBAN Calculator Application

Programming Languages and Frameworks:
Python: The core programming language used, known for its simplicity and versatility.
PyQt6: A set of Python bindings for the Qt application framework, used for creating the graphical user interface (GUI).
Selenium: A suite of tools for automating web browsers, used for scraping necessary data from a web page.

Application Architecture:
Class-Based Design: The application employs a class-based design, with key classes like IBANScraperThread and AccountScraperThread for handling different functionalities.
Multithreading: Utilizes Python's QThread for running web scraping operations in separate threads, preventing the GUI from becoming unresponsive during long-running tasks.

Key Functionalities:
IBAN Generation: Converts Czech bank account numbers to IBANs by automating interaction with a specific web page using Selenium.
Account Number Conversion: Reverts IBANs back to standard Czech account number format, providing a comprehensive tool for financial conversions.

User Interface Components:
Form Layout: Utilizes QFormLayout for structuring the input fields and labels in an organized manner.
Interactive Elements: Includes QLineEdit for input fields, QPushButton for actions like calculation and clearing inputs, and QTextEdit for displaying results or error messages.
Styling and Theming: Applies custom stylesheets for widget styling, enhancing the visual appeal and user experience.

Error Handling and User Input Validation:
Error Messaging: Implements try-except blocks to handle potential errors during web scraping.
Regular Expression Validator: Employs QRegularExpressionValidator to ensure that user inputs adhere to expected formats, enhancing data integrity.

Performance Considerations:
Efficient Web Scraping: Uses headless browser options in Selenium to improve the speed and efficiency of web scraping operations.
Optimized Wait Conditions: Incorporates WebDriverWait and expected_conditions in Selenium to dynamically wait for page elements, ensuring reliable data retrieval without unnecessary delays.

Additional Features:
Clipboard Integration: Provides functionality to copy the results directly to the clipboard, facilitating easy use of the output.
Error Message Handling and Display: The application is designed to interact with a specific web page for IBAN conversions. If the web page provides error messages (e.g., due to incorrect input or server-side issues), these messages are captured by the application's web scraping mechanism. The application then displays these error messages to the user through a QTextEdit component in the GUI. This feature ensures that users are promptly informed of any issues during the conversion process, enhancing the usability and reliability of the application.

Acknowledgments
This project uses Selenium and BeautifulSoup for web automation and scraping, respectively.
PyQt6 is used for the graphical user interface.
The application interacts with a specific web service for conversion purposes.
