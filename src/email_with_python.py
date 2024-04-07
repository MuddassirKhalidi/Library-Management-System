"""
email_with_python.py

This module provides a class for handling email sending functionality using SMTP.
It includes a class 'EmailSender'.
The 'EmailSender' establishes an SMTP connection, logging in, and sending emails.

Usage:
- Import the 'EmailSender' class into your scripts for email-related functionality.
- Ensure the 'smtplib' library is available in your Python environment.

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
import csv
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
                email = _is_valid_email("Enter your email: ")
                password = getpass.getpass('Enter your password: ')
                self.smtp_object.login(email, password)
            except smtplib.SMTPAuthenticationError:
                print('Invalid combination of email and password!')
            else:
                return email

    def close_connection(self):
        """Close the SMTP connection."""
        self.smtp_object.quit()             

def _get_file_data():
    """
    Read data from a CSV file and return it as a list.

    Returns:
        list: A list containing the data read from the CSV file.
    """
    while True:
        try:
            file_name = input('Enter file path: ')
            with open(file_name, mode='r', encoding='utf-8') as csv_file:
                csv_data = list(csv.reader(csv_file))
        except FileNotFoundError:
            print('File not found. Please try again.')
        else:
            return csv_data

def _get_email_column(data):
    """
    Find the column index containing email addresses in the CSV data.

    Args:
        data (list): The CSV data as a list.

    Returns:
        int or None: The index of the email column, or None if not found.
    """
    email_types = ['emails', 'email address', 'email addresses', 'email']
    for column_number in range(len(data[0])):
        if data[0][column_number].lower().strip() in email_types:
            return column_number
    return None

def _get_name_column(data):
    """
    Find the column index containing names in the CSV data.

    Args:
        data (list): The CSV data as a list.

    Returns:
        int or None: The index of the name column, or None if not found.
    """
    name_types = ['name', 'names']
    for column_number in range(len(data[0])):
        if data[0][column_number].lower().strip() in name_types:
            return column_number
    return None

def _get_mailing_list():
    """
    Extract a mailing list from the CSV data, consisting of name and email pairs.

    Returns:
        list or None: A list of tuples (name, email) or None if no suitable columns are found.
    """
    data = _get_file_data()
    email_column = _get_email_column(data)
    name_column = _get_name_column(data)
    mailing_list = []
    if name_column is not None:
        if email_column is not None:
            # If both name and email columns are found
            for row in range(1, len(data)):
                mailing_list.append((data[row][name_column], data[row][email_column]))
    elif email_column is not None:
        # If only the email column is found
        mailing_list = [data[row][email_column] for row in range(1, len(data))]
    elif name_column is not None:
        # If only the name column is found
        return None
    return mailing_list

def _send_email_with_name(mailing_list):
    """
    Send personalized emails to recipients with names.

    Args:
        mailing_list (list): A list of tuples (name, email).
    """
    subject = input('Enter the subject: ').upper()
    content = input("Enter your message (Press Enter twice to exit): ") + '\n'
    while True:
        line = input()
        if not line:
            break
        line += '\n'
        content += line
    for name, receiver_email in mailing_list:
        message = f'Subject: {subject} \nDear {name} \n{content}'
        admin.smtp_object.sendmail(admin_email, receiver_email, message)
    print('Email sent!')
    print('-' * 50)

def _send_email_without_name(mailing_list):
    """
    Send generic emails to recipients without names.

    Args:
        mailing_list (list): A list of email addresses.
    """
    subject = input('Enter the subject: ').upper()
    content = input("Enter your message (Press Enter twice to exit): ") + '\n'
    while True:
        line = input()
        if not line:
            break
        line += '\n'
        content += line
    message = f'Subject: {subject} \n{content}'
    for receiver_email in mailing_list:
        admin.smtp_object.sendmail(admin_email, receiver_email, message)
    print('Email sent!')
    print('-' * 50)

def _is_valid_email(message):
    """
    Checks the validity of the email using regex.

    Args:
        message (str): The prompt message to get the email.

    Returns:
        str: A valid email address.
    """
    pattern = r'\w+@[A-z]+\.*[a-z]*\.[a-z]*'
    while True:
        try:
            email = input(message)
            if not re.match(pattern, email):
                raise ValueError
        except ValueError:
            print('Enter a valid email')
        else:
            return email


def send_to_one_user():
    """
    Get email content and send it to a specified recipient.

    Args:
        admin (EmailSender): An instance of the EmailSender class.
        admin_email (str): The administrator's email address.
    """
    receivers_email = _is_valid_email("Enter receiver's email: ")
    subject = input('Enter the subject: ').upper()
    content = input('Enter the message (Press Enter twice to exit): ') + '\n'
    while True:
        line = input()
        if not line:
            break
        line += '\n'
        content += line
    message = f'Subject: {subject}\n{content}'
    admin.smtp_object.sendmail(admin_email, receivers_email, message)
    print('Email sent!')
    print('-' * 50)

def send_email_to_group():
    """
    Main function to send emails based on user input.
    """
    mailing_list = _get_mailing_list()

    if mailing_list and isinstance(mailing_list[0], tuple):
        _send_email_with_name(mailing_list)
    elif mailing_list and not isinstance(mailing_list[0], tuple):
        _send_email_without_name(mailing_list)
    else:
        print('No Emails Found!')


if __name__ == '__main__':
    print('Welcome to your personal emailing system!'.center(78))
    admin = EmailSender()
    admin_email = admin.login()
    while True:
        email_type = input('Email to one user [1] or to multiple [2]: ')
        while email_type not in ['1','2']:
            email_type = input('Enter a valid choice: ')
        if email_type == '1':
            send_to_one_user()
        else:
            send_email_to_group()
        choice = input('Do you want to send another email? [y/n]: ').lower().strip()
        while choice not in ['y', 'n']:
            choice = input('Enter a valid choice [y/n]: ')
        if choice == 'n':
            print('Logging out')
            admin.close_connection()
            sys.exit()
