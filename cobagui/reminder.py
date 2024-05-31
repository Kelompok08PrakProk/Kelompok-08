import smtplib
from email.message import EmailMessage
import csv
import datetime
import os

def send_reminder(to_mail, book_title, due_date, ticket_path):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    
    from_mail = "petibyunsofficial@gmail.com"
    server.login(from_mail, "johl erdn chfr jdgq")
    
    msg = EmailMessage()
    msg["Subject"] = "Book Return Reminder"
    msg["From"] = from_mail
    msg["To"] = to_mail
    msg.set_content(f"""
Dear Valued Patron,

We hope this message finds you well. This is a friendly reminder that the book titled "{book_title}" you borrowed from our library is due on {due_date}.

To ensure that all patrons have fair access to our resources, we kindly ask that you return the book by the due date. Late returns may incur penalties as per our library policy, which is detailed on our website.

Attached to this email is a copy of your borrowing ticket for your reference. Please keep this ticket for your records. If you have any questions or need to extend your borrowing period, do not hesitate to contact us at your earliest convenience. We are here to assist you.

Thank you for your cooperation and continued support of our library. We look forward to serving you again.

Best Regards,
The PETI Library Team

Contact Information:
e-Mail: petibyunsofficial@gmail.com
""")
    
    # Attach the ticket image
    with open(ticket_path, 'rb') as file:
        msg.add_attachment(file.read(), maintype='image', subtype='jpeg', filename=os.path.basename(ticket_path))
    
    server.send_message(msg)
    server.quit()
    print(f"Reminder email sent to {to_mail}")

def send_due_date_reminders():
    try:
        today = datetime.date.today()
        reminder_date = today + datetime.timedelta(days=3)
        
        with open('database/datapinjam.csv', mode='r') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                email = row['email']
                book_title = row['judul']
                due_date = datetime.datetime.strptime(row['tanggalKembali'], "%d-%m-%Y").date()  # Parsing DD-MM-YYYY format
                ticket_path = row['tiket']
                
                if due_date == reminder_date:
                    formatted_due_date = due_date.strftime("%d-%m-%Y")  # Formatting date as MM/DD/YYYY for the email
                    send_reminder(email, book_title, formatted_due_date, ticket_path)
    except Exception as e:
        print(f"An error occurred: {e}")

# Schedule the reminder function
send_due_date_reminders()