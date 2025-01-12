# Eml-Email-Backup-Downloader
A Python script to back up emails from your IMAP server. It processes emails from specified folders (e.g., INBOX and Sent), saves them as .eml files, and downloads attachments if available.


Features

Connects to an IMAP server securely.

Downloads emails and attachments.

Organizes emails into folders by mailbox.

Displays real-time progress during download.

Requirements

This script requires Python 3.6 or higher and the following Python libraries:

imaplib (built-in)

email (built-in)

os (built-in)

sys (built-in)

datetime (built-in)

Optional (for development):

colorama for colored terminal output (not required in this simplified version).

Installation

Clone this repository:

git clone https://github.com/your-username/imap-email-downloader.git
cd imap-email-downloader

Create and activate a virtual environment (optional but recommended):

python -m venv env
source env/bin/activate  # On Windows, use `env\Scripts\activate`

Install required libraries:

pip install -r requirements.txt

Configuration

Before running the script, update the main() function in the script with your IMAP server details and credentials:

IMAP_SERVER = "imap.example.com"
EMAIL_ADDRESS = "your-email@example.com"
PASSWORD = "your-password"
IMAP_PORT = 993

Usage

Run the script with:

python main.py

The emails will be saved in the emails/ directory, organized by mailbox name.

Example Output

The script will display the progress of downloaded emails in real time:

Connection successful!
Processing folder: INBOX
INBOX: 1/16000 emails downloaded
INBOX: 2/16000 emails downloaded
...
Processing folder: INBOX.Sent
INBOX.Sent: 1/5000 emails downloaded
...

Notes

Make sure to use demo credentials for public repositories.

Test with a small set of emails before running on a large mailbox.

The script skips emails that fail to download and continues with the next.

License

This project is licensed under the MIT License. See the LICENSE file for details.
