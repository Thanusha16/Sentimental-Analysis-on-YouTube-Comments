import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


def mailsend(emailto):
    # Mail details
    emailfrom = "n.thanusha16@gmail.com"
    fileToSend = [
        "Full Comments.csv",
        "Positive Comments.csv",
        "Negative Comments.csv",
        "Spam Comments.csv",
    ]
    password = "pjwrdbvzarsbrrxr"

    # Mail Subject and Body
    subject = "Your YouTube comments file is here - YouTube Comment Scraper"
    body = "Hi,\n\nPlease find attached the CSV files containing the comments from the YouTube video.\n\nBest regards,\nYour Scraper"

    # Creating the email message
    msg = MIMEMultipart("alternative")
    msg["From"] = emailfrom
    msg["To"] = emailto
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # Adding attachments
    for f in fileToSend:
        ctype, encoding = mimetypes.guess_type(f)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"
        maintype, subtype = ctype.split("/", 1)

        with open(f, "rb") as fp:
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=f)
            msg.attach(attachment)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(emailfrom, password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print(
            "Failed to send email: Authentication error. Check your username and password."
        )
    except Exception as e:
        print(f"Failed to send email: {e}")
