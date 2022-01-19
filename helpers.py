from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from email.message import EmailMessage
from twilio.rest import Client
import smtplib
import keys

# Email sender details.
EMAIL_ADDRESS = keys.EMAIL_ADDRESS
EMAIL_PASSWORD = keys.EMAIL_PASSWORD

# Twilio API details.
ACCOUNT_SID = keys.ACCOUNT_SID
AUTH_TOKEN = keys.AUTH_TOKEN
TWILIO_PHONE_NUMBER = keys.PHONE_NUMBER

# Retrieve all months from date-picker and store in array.
def get_all_months(driver):
    dateDropdownOptions = Select(driver.find_element(
        By.XPATH, "//select[@class='ui-datepicker-month']")).options

    for i in range(len(dateDropdownOptions)):
        dateDropdownOptions[i] = dateDropdownOptions[i].text

    return dateDropdownOptions

# Helper function to email notification to subscribers.
def send_email_alert(available_date):

    emails_to_alert = keys.SUBSCRIBER_EMAILS
    msg = EmailMessage()
    msg['Subject'] = 'AVAILABLE APPOINTMENT FOUND - ' + available_date
    msg['From'] = 'Appointment Checker'
    msg['To'] = emails_to_alert
    msg.set_content('Available Appointment Found on ' + available_date + '.\n\n' +
                    'Vist http://sto.imi.gov.my/ATASE/MELBOURNE/permohonan.php to book your appointment.')

    gmailServer = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    gmailServer.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    gmailServer.send_message(msg)
    gmailServer.quit()

# Helper function to sms notification to subscribers.
def send_sms_alert(available_date):
    
    numbers_to_alert = keys.SUBSCRIBER_NUMBERS
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for number in numbers_to_alert:
        client.messages.create(
            body='AVAILABLE APPOINTMENT FOUND - ' + available_date,
            from_=TWILIO_PHONE_NUMBER,
            to=number
        )