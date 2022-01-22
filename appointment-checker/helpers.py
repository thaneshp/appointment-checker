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

TARGET_WEBSITE = keys.TARGET_WEBSITE

# Helper function to retrieve all months from UI and store in array.
def get_all_months(driver):
    list_of_months = Select(driver.find_element(
        By.XPATH, "//select[@class='ui-datepicker-month']")).options

    for i in range(len(list_of_months)):
        list_of_months[i] = list_of_months[i].text

    return list_of_months

# Helper function to email subcribers with available date.
def send_email_alert(available_date):

    message = "Available Appointment Found on {date}.\n\nVist {link} to book your appointment.".format(date=available_date, link=TARGET_WEBSITE)

    emails_to_alert = keys.SUBSCRIBER_EMAIL_LIST
    msg = EmailMessage()
    msg['Subject'] = 'AVAILABLE APPOINTMENT FOUND - ' + available_date
    msg['From'] = 'Appointment Checker'
    msg['To'] = emails_to_alert
    msg.set_content(message)

    gmailServer = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    gmailServer.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    gmailServer.send_message(msg)
    gmailServer.quit()

# Helper function to sms notification with available date.
def send_sms_alert(available_date):

    message = "AVAILABLE APPOINTMENT FOUND - {date} - {link}".format(date=available_date, link=TARGET_WEBSITE)
    
    numbers_to_alert = keys.SUBSCRIBER_PHONE_LIST
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    for number in numbers_to_alert:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=number
        )