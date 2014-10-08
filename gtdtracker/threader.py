"""
Todo:
- threading is crude bit works quite well. What I currently see is that it is slightly over-aggressive. You can get multiple emails which are unrelated but which get grouped. However as of 15/9/2010 I've only seen it on lower priority Action IV items which I don't mind. No doubt it will occur elsewhere though.
- not just threading but I mention it here: we should be scoring the 'Hold' folder.
"""

import csv
import os
from datetime import datetime


def get_sanitised_msg_title(raw_title):
    if raw_title[0:4].lower() == 're: ':
        return raw_title[4:]
    elif raw_title[0:4].lower() == 'fw: ':
        return raw_title[4:]
    else:
        return raw_title


def calc_mean_datetime(dateTimes):
    if len(dateTimes) == 1:
        return dateTimes[0]
    oldest = min(dateTimes)
    newest = max(dateTimes)
    midpoint = (newest - oldest) // 2
    meanDate = oldest + midpoint
    return meanDate


def thread_and_date_folder(folderName):
    """
    Opens folder and processes date.
    """
    folderDateStrings = []

    # experimental: dictionary of messages:
    #     key = message title
    #     value = list of dates
    folderDict = {}

    f = open("raw" + "/" + folderName + ".csv")
    try:
        reader = csv.reader(f)
        for row in reader:
#           print row
            parsedDate = parse_date(row[1])
            folderDateStrings.append(parsedDate.isoformat(' '))

            # experimental:
            msgTitle = get_sanitised_msg_title(row[0])
            if msgTitle in folderDict:
                folderDict[msgTitle].append(parsedDate)
            else:
                folderDict[msgTitle] = [parsedDate]
    finally:
        f.close()

    # Any duplicates? i.e. threads
    print "%s: raw item count = %d. dict count = %d" % (folderName, len(folderDateStrings), len(folderDict))

    for k, v in folderDict.iteritems():
        print "(%d) %s" % (len(v), k)
        print "    ->", v
        if len(v) > 1:
            print "    ", calc_mean_datetime(v)

    # Now write the date out in ISO format to the output CSV file
    ensure_folder_exists("threaded")
    f = open("threaded" + "/" + folderName + ".csv", "wt")
    try:
        # for dateString in folderDateStrings:
        #     f.write(dateString)
        for k, v in folderDict.iteritems():
            f.write(calc_mean_datetime(v).isoformat(' '))
            f.write("\n")
    finally:
        f.close()


def chop_off_last_bit_of_datestring(dateString):
    endPos = dateString.rfind(' ')
    newString = dateString[0:endPos]
    return newString


def parse_date(dateString):
    """
    Tries to extract the date from the supplied string and returns it as a datetime object.
    If the date cannot be parsed then it returns the current datetime.
    """
    #set a default return value in case we cannot parse it
    dt = datetime.today()

    trimmedDateString = chop_off_last_bit_of_datestring(dateString)
    try:
	dt = datetime.strptime(trimmedDateString, "%a, %d %b %Y %H:%M:%S")
        return dt
    except ValueError:
        print "Error! Trying again..."
        try:
            tds2 = chop_off_last_bit_of_datestring(trimmedDateString)
            dt = datetime.strptime(tds2, "%a, %d %b %Y %H:%M:%S")
        except ValueError:
            print "Error 2!! Trying again..."
            try:
                dt = datetime.strptime(trimmedDateString, "%d %b %Y %H:%M:%S")
            except:
                print "Argh! Another error, give up!"
    finally:
        return dt

def ensure_folder_exists(folder_name):
    try:
        os.mkdir(folder_name)
    except OSError:
        pass


def main():
    thread_and_date_folder('INBOX')
    thread_and_date_folder('Action I')
    thread_and_date_folder('Action II')
    thread_and_date_folder('Action III')
    thread_and_date_folder('Action IV')


if __name__ == '__main__':
    main()
