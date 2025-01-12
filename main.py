import imaplib
import email
import os
import sys
from email.header import decode_header
from datetime import datetime

def connect_to_imap(server, email_address, password):
    try:
        mail = imaplib.IMAP4_SSL(server)
        mail.login(email_address, password)
        print("Connection successful!")
        return mail
    except Exception as e:
        print(f"Error connecting to IMAP server: {e}")
        return None

def save_email(folder_path, mail_title, mail_content):
    try:
        with open(os.path.join(folder_path, f"{mail_title}.eml"), "wb") as f:
            f.write(mail_content)
    except Exception as e:
        print(f"Error saving email {mail_title}: {e}")

def save_attachment(folder_path, mail_title, attachment):
    try:
        attachment_path = os.path.join(folder_path, f"{mail_title}-attachment")
        with open(attachment_path, "wb") as f:
            f.write(attachment)
    except Exception as e:
        print(f"Error saving attachment for {mail_title}: {e}")

def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '-', '_')).rstrip()

def decode_subject(subject):
    try:
        if isinstance(subject, bytes):
            return subject.decode('utf-8', 'replace')
        return subject
    except Exception as e:
        print(f"Error decoding subject: {e}")
        return "decoded_error"

def process_mailbox(mail, folder_name, base_path):
    status = mail.select(folder_name)
    if status[0] != "OK":
        print(f"Cannot select folder: {folder_name}")
        return

    status, messages = mail.search(None, "ALL")
    if status != "OK":
        print(f"Error fetching emails in folder {folder_name}")
        return

    folder_path = os.path.join(base_path, sanitize_filename(folder_name))
    os.makedirs(folder_path, exist_ok=True)

    message_ids = messages[0].split()
    total_messages = len(message_ids)
    print(f"Total emails in {folder_name}: {total_messages}")

    for idx, msg_id in enumerate(message_ids, start=1):
        try:
            status, data = mail.fetch(msg_id, "(RFC822)")
            if status != "OK":
                print(f"Error fetching email with ID {msg_id}")
                continue

            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject = decode_header(msg.get("Subject"))[0][0]
                    subject = decode_subject(subject)
                    subject = sanitize_filename(subject)

                    date_tuple = email.utils.parsedate_tz(msg.get("Date"))
                    if date_tuple:
                        local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
                        date_str = local_date.strftime("%d-%m-%Y")

                    mail_title = f"{subject}-{date_str}"

                    save_email(folder_path, mail_title, response_part[1])

                    for part in msg.walk():
                        if part.get_content_maintype() == "multipart":
                            continue
                        if part.get("Content-Disposition") is None:
                            continue

                        file_data = part.get_payload(decode=True)
                        if file_data:
                            save_attachment(folder_path, mail_title, file_data)

            # Update the progress on the same line
            sys.stdout.write(f"
{folder_name}: {idx}/{total_messages} emails downloaded")
            sys.stdout.flush()
        except Exception as e:
            print(f"Error processing email {msg_id}: {e}")

    print()  # Move to the next line after processing all emails

def main():
    IMAP_SERVER = "imap.example.com"
    EMAIL_ADDRESS = "demo@example.com"
    PASSWORD = "password123"
    IMAP_PORT = 993

    base_path = "emails"
    os.makedirs(base_path, exist_ok=True)

    mail = connect_to_imap(IMAP_SERVER, EMAIL_ADDRESS, PASSWORD)
    if not mail:
        return

    # Only process INBOX and Sent folders
    folders_to_process = ["INBOX", "INBOX.Sent"]
    for folder_name in folders_to_process:
        print(f"Processing folder: {folder_name}")
        process_mailbox(mail, folder_name, base_path)

    mail.logout()

if __name__ == "__main__":
    main()
