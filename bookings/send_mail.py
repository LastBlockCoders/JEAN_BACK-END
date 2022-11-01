import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

username = 'psnwaynehartley@gmail.com'
password = 'isxelyoeymywwzpt'


def send_mail_reply(html, text='Email_body', subject='Jeans Beauty and Wellness Service Appointment', from_email=username, to_emails=[]):
    assert isinstance(to_emails, list)

    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)

    html_part = MIMEText(
        f"<p>Good day to you!, Here is an update on your appointment request as of this moment:</p><h2 style='text-transform: capitalize'>{html}</h2>", 'html')
    msg.attach(html_part)
    msg_str = msg.as_string()

    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()


def send_mail_request(text=username, subject='New Appointment Request', from_email=username, to_emails=[]):
    assert isinstance(to_emails, list)

    msg = MIMEMultipart('alternative')
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject
    txt_part = MIMEText(text, 'plain')
    msg.attach(txt_part)

    html_part = MIMEText(
        f"<p>Good day Jean, an account with email {username} has requested a service appointment, head over to the admin dashboard to view it and send them a reply:</p>", 'html')
    msg.attach(html_part)
    msg_str = msg.as_string()

    server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()
