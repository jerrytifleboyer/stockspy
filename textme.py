# send emails, SMTP library is just a emailing medium, ssl provide secure certificate to website to access my email 
import smtplib, ssl
import json

with open('config/pw.json') as f:
    data = json.load(f)
    mobile = data["cell"]["mobile"]
    carrier = data["cell"]["carrier"]
    gmail = data["email"]["gmail"]
    token = data["email"]["token"]
    server = data["email"]["server"]
    port = data["email"]["port"]

def send_priceChange_via_email(
    number: str,
    message: str,
    sender_credentials:tuple,
    smtp_server:str= server,
    smtp_port: int= port
):

    sender_email, email_token = sender_credentials
    receiver_email = f'{number}{carrier}'
    email_message =  f'To:{receiver_email}\n{message}'

    with smtplib.SMTP_SSL(smtp_server, smtp_port, context = ssl.create_default_context()) as email:
        email.login(sender_email, email_token)
        email.sendmail(sender_email, receiver_email, email_message)

def textme(message):
    sender_credentials = (gmail,token)
    send_priceChange_via_email(mobile, message, sender_credentials)

if __name__=="__main__":
    textme()