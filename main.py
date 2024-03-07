import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from fpdf import FPDF

def send_email(pdf_filename, recipient_email):
    # Mailgun configuration
    mailgun_api_key = "your_mailgun_api_key"  # Replace with your Mailgun API key
    mailgun_domain = "your_mailgun_domain"  # Replace with your Mailgun domain
    sender_email = "your_email@your_domain.com"  # Replace with your sender email

    # Mailgun API endpoint
    mailgun_url = f"https://api.mailgun.net/v3/{mailgun_domain}/messages"

    # Email parameters
    email_data = {
        "from": f"NextFit Report <{sender_email}>",
        "to": recipient_email,
        "subject": "NextFit PDF Report",
        "text": "Please find the NextFit PDF report attached."
    }

    # Attach PDF
    with open(pdf_filename, "rb") as attachment:
        files = [("attachment", (pdf_filename, attachment))]
        response = requests.post(
            mailgun_url,
            auth=("api", mailgun_api_key),
            files=files,
            data=email_data
        )

    if response.status_code == 200:
        print("Email sent successfully!")
    else:
        print("Failed to send email. Status code:", response.status_code)

# Generate PDF
# (Assuming you have already generated the PDF and saved it as 'nextfit.pdf')
pdf_filename = "nextfit.pdf"

# Send email
recipient_email = "recipient_email@example.com"  # Update with recipient's email
send_email(pdf_filename, recipient_email)

# Set up the web driver (make sure you have chromedriver installed)
chrome_options = Options()
chrome_options.add_argument("--headless")  # To run Chrome in headless mode
service = Service('path_to_chromedriver')  # Update 'path_to_chromedriver' with the path to your chromedriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Navigate to the login page
driver.get("https://app.nextfit.com.br/")
time.sleep(2)

# Fill in the login form
username = driver.find_element(By.NAME, "usuario")
username.send_keys("your_username")
password = driver.find_element(By.NAME, "senha")
password.send_keys("your_password")
password.send_keys(Keys.RETURN)

# Wait for the page to load after login
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "financeiro-receber")))
except TimeoutException:
    print("Timed out waiting for page to load")

# Navigate to the desired page
driver.get("https://app.nextfit.com.br/financeiro/receber")

# Wait for the page to load
time.sleep(5)  # Adjust timing as necessary

# Extract HTML content
html_content = driver.page_source

# Parse HTML content
soup = BeautifulSoup(html_content, "html.parser")

# Close the browser
driver.quit()

# Extract necessary data and generate PDF (You'll need to customize this part)
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt="NextFit - Recebíveis", ln=True, align="C")
pdf.cell(200, 10, txt="Your data goes here", ln=True, align="L")
pdf_filename = "nextfit.pdf"
pdf.output(pdf_filename)

# Send email
recipient_email = "recipient_email@example.com"  # Update with recipient's email
send_email(pdf_filename, recipient_email)