import imaplib
import ConfigParser
import os
import csv
import time
import getpass


def open_connection(verbose=False):
    # Read the config file and get password
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser('account.txt')])
    hostname = config.get('server', 'hostname')
    username = config.get('account', 'username')
    password = ""
    try:
        password = config.get('account', 'password')[::-1]
    except ConfigParser.NoOptionError:
        pass
    if not password:
        password = getpass.getpass()

    # Connect to the server
    print "hostname = ", hostname
    if verbose:
        print 'Connecting to', hostname
    connection = imaplib.IMAP4_SSL(hostname)

    # Login to our account
    print "account/password = ", username, password
    if verbose:
        print 'Logging in as', username
    connection.login(username, password)
    return connection


def get_summary_info_from_email(msgId, c):
    print "get_summary_info_from_email:", msgId
    emailSubject = ""
    emailDate = ""
    typ, msg_data = c.fetch(msgId, '(BODY.PEEK[HEADER])')
    responseData = msg_data[0][1]
    stringlist = responseData.split('\n')

    # get summary information for message
    for stringElement in stringlist:
        if stringElement[:8] == 'Subject:':
            emailSubject = stringElement[9:].strip()
        if stringElement[:5] == 'Date:':
            emailDate = stringElement[6:].strip()

    return (emailSubject, emailDate)


def get_summary_info_from_mailbox(mailboxName, c):
    mailboxSummary = []
    typ, data = c.select(mailboxName, readonly=True)
    numberOfMsgs = int(data[0])
    print mailboxName, ":", typ, data, numberOfMsgs
    typ, msg_ids = c.search(None, 'ALL')
    listOfIds = msg_ids[0].split(' ')
    for msgId in listOfIds:
        if len(msgId):
            (emailSubject, emailDate) = get_summary_info_from_email(msgId, c)
            if emailSubject and emailDate:
                mailboxSummary.append( (emailSubject, emailDate) )
            
    c.close()
    return mailboxSummary


def ensure_folder_exists(folder_name):
    try:
        os.mkdir(folder_name)
    except OSError:
        pass


def summarise_folder(folderName, connection):
    """
    Creates a CSV file for the folder and puts summary information about each
    message for that folder into the file.
    """
    # get summary information
    mailboxSummary = get_summary_info_from_mailbox(folderName, connection)
    print "mailboxSummary has %d entries" % len(mailboxSummary)
    for emailInfo in mailboxSummary:
        print emailInfo

    # put data in CSV file
    ensure_folder_exists('raw')
    f = open('raw' + '/' + folderName + ".csv", 'wt')
    try:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for emailInfo in mailboxSummary:
            writer.writerow(emailInfo)
    finally:
        f.close()


def main():
    starttime = int(time.time())
    c = open_connection(verbose=True)
    try:
        summarise_folder('INBOX', c)
        summarise_folder('Action I', c)
        summarise_folder('Action II', c)
        summarise_folder('Action III', c)
        summarise_folder('Action IV', c)
    finally:
        c.logout()
    endtime = int(time.time())
    print "Took %d seconds." % (endtime - starttime)


if __name__ == '__main__':
    main()
