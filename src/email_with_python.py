"""
email_with_python.py

This module provides a class for handling email sending functionality using SMTP.
It includes a class 'EmailSender'.
The 'EmailSender' establishes an SMTP connection, logging in, and sending emails.

Usage:
- Import the 'EmailSender' class into your scripts for email-related functionality.
- Ensure the 'smtplib' library is available in your Python environment.
- When logging in, use the App password to your Gmail
Example:
    from email_with_python import EmailSender

    admin = EmailSender()
    admin_email = admin.login()
    admin.close_connection()

Requirements:
- Python 3.x
- 'smtplib' library

Author: Muddassir Khalidi
Date: 15 January 2024
"""

import smtplib
import getpass
import re
import sys

class EmailSender:
    """
    A class for handling email sending functionality using SMTP.

    Attributes:
        smtp_object (smtplib.SMTP): An SMTP connection object.
    """

    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587):
        """
        Initializes the EmailSender object.

        Args:
            smtp_server (str): SMTP server address.
            smtp_port (int): SMTP server port.
        """
        self.smtp_object = smtplib.SMTP(smtp_server, smtp_port)
        self.smtp_object.ehlo()
        self.smtp_object.starttls()

    def login(self):
        """
        Log in to the SMTP server.

        Returns:
            str: The email address used for login.
        """
        while True:
            try:
                email = get_email()
                password = getpass.getpass('Enter your password: ')
                self.smtp_object.login(email, password)
            except smtplib.SMTPAuthenticationError:
                print('Invalid combination of email and password!')
            else:
                return email

    def close_connection(self):
        """Close the SMTP connection."""
        self.smtp_object.quit() 

def is_valid_email(email):
    """
    Validate the format of the email using regular expressions.
    """
    # Regular expression pattern for validating email
    pattern = r'^\w+@[a-zA-Z]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

def send_to_one_user(admin, admin_email, email: str):
    """
    Sends an email to one recipient
    """
    subject = get_subject()
    content = get_content_for_one_user()
    message = f'Subject: {subject} \n{content}'
    admin.smtp_object.sendmail(admin_email, email, message)
    print('Email sent!')


def send_to_group(admin, admin_email, name_list: list, email_list: list, *custom_lists: list):
    """
    Instructions for Entering Email Message:

When composing your email message, follow this format:

1. Start your message with a salutation, addressing the recipient by name:
   Example: Dear {name},

2. Use placeholders enclosed in curly braces {} to represent dynamic content.
   - Replace "{name}" with the recipient's name.
   - Use "{custom1}", "{custom2}", etc., to denote custom values from your provided lists.

3. Ensure that each placeholder corresponds to an item in the respective lists:
   - {name}: Refers to the recipient's name from the provided 'names' list.
   - {custom1}, {custom2}, etc.: Correspond to values from the custom lists provided.

4. Maintain clear and concise wording for clarity and professionalism.
   - Avoid excessive formatting or unnecessary details.

5. Conclude your message with a polite closing, such as "Thank you!" or "Best regards,".

Example Email Message Format:
---------------------------------
Dear {name},

This is your {custom1} for your {custom2} and this will be your {custom3}.

Thank you!
---------------------------------

Follow these instructions to create personalized email messages using the provided lists effectively.
"""
    input_lengths = [len(name_list), len(email_list)] + [len(lst) for lst in custom_lists]
    if len(set(input_lengths)) != 1:
        raise ValueError("Input lists must have the same length.")
    print("Enter your message below (Press Enter twice to finish):")
    message_lines = []
    while True:
        line = input()
        if not line:
            break
        message_lines.append(line)

    # Combine the lines into a single message
    message = '\n'.join(message_lines)

    messages = []
    try:
        for items in zip(name_list, *custom_lists):
            # Format the message template with the current items
            name = items[0]
            custom_items = {f'custom{i+1}': item for i, item in enumerate(items[1:])}

            formatted_message = message.format(name=name, **custom_items)
            messages.append(formatted_message)

    except KeyError as error:
        print(f"Error: Placeholder {error} is missing from the message template.")
    subject = get_subject()
    for email, message in zip(email_list, messages):
        final_message = f'Subject: {subject} \n{message}'
        admin.smtp_object.sendmail(admin_email, email, final_message)
        print('Email sent!')
        
def get_email():
    """
    Gets the email of the user, validates it and returns it
    """
    email = input('Enter email: ')
    while not is_valid_email(email):
        print('Enter a valid email')
        print('-'*50)
        email = input('Enter email')
    
    return email

def get_subject():
    """"
    Returns the subject of the email
    """
    subject = input('Enter subject: ')
    return subject

def get_content_for_one_user():
    """
    Returns the content of the email
    """
    content = input('Enter message: ') + '\n'
    while True:
        line = input()
        if not line:
            break
        line += '\n'
        content += line
    
    return content


if __name__ == '__main__':
    print('Welcome to your personal emailing system!'.center(78))
    admin = EmailSender()
    admin_email = admin.login()
    while True:
        email_type = input('Email to one user [1] or to multiple [2]: ')
        while email_type not in ['1','2']:
            email_type = input('Enter a valid choice: ')
        if email_type == '1':
            send_to_one_user(admin, admin_email, 'muddassirnawazkhan@gmail.com')
        else:
            names = ['Muddassir', 'Andre Stephens']
            emails = ['muddassirnawazkhan@gmail.com', 'andrestephens2604@gmail.com']
            penalties = [100, 200]
            released = ['Released','Not Released']
            send_to_group(admin, admin_email, names, emails, penalties, released)
        choice = input('Do you want to send another email? [y/n]: ').lower().strip()
        while choice not in ['y', 'n']:
            choice = input('Enter a valid choice [y/n]: ')
        if choice == 'n':
            print('Logging out')
            admin.close_connection()
            sys.exit()
