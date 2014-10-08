import csv
import sys
import math
from datetime import datetime


def get_dates_from_folder(folderName):
    """
    Opens file containing a list of dates and returns them as datetime objects.
    """
    f = open("threaded" + "/" + folderName + ".csv")
    timeStamps = []
    dateTimeLines = f.readlines()
    for dateEntry in dateTimeLines:
       dt, _, us = dateEntry.partition(".")
       dt = dt.strip()
       dateTimeObj = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")

       timeStamps.append(dateTimeObj)
    f.close()
    return timeStamps


def age_of_msg_in_weeks(date):
    ageInDays = (datetime.now() - date).days
    return ageInDays / 7


def age_of_msg_in_days(date):
    ageInDays = (datetime.now() - date).days
    return ageInDays


def scoreInbox(inboxDates, verbose):
    """
    Score for inbox is based on the sum of message scores, with a bonus for being "clear"
    Metric is:
        for each message older than 1 day: 25.
    In addition there is a bonus for achieving "inbox zero":
        if no messages older than a day (inbox score would be zero): -50
        if no messages at all: -100

    Weighting is 25 (effectively 175 in week terms)
    """
    folderScore = 0
    for date in inboxDates:
        msgScore = 25 * age_of_msg_in_days(date)
        folderScore += msgScore
        if verbose:
            print "Inbox: message is %s. It is %d days old and scores %d" % (date, age_of_msg_in_days(date), msgScore)

    # "inbox zero" rewards:
    if len(inboxDates) == 0:
        folderScore = -100
    elif folderScore == 0:
        folderScore = -50
    return folderScore


def scoreAction1(action1Dates, verbose):
    """
    Score for Action 1 is based on sum of message scores.

    Each message score is: ceil(msg_date(days)).
    Weighting is 5
    (Therefore each message counts immediately and accrues every day.)
    (Rationale: higher urgency so worth something immediately and more as time passes, high value overall).
    """
    folderScore = 0
    for date in action1Dates:
        msgScore = 5 * (age_of_msg_in_days(date) + 1)
        if verbose:
            print "Action I: message is %s. It is %d days old and scores %d" % (date, age_of_msg_in_days(date), msgScore)
        folderScore += msgScore
    return folderScore   # folder scores should be int and we don't need the extra precision!


def scoreAction2(action2Dates, verbose):
    """
    Score for Action 2 is based on sum of message scores.

    Each message score is: 
        5 * floor(msg_date(weeks))
        if msg_date(weeks) > 2:
            += 5 * floor(msg_date(weeks) - 2)
    Weighting is 5.
    (Therefore:     age < 1 week: 0
        1 weeks <= age < 2 weeks: 5
        2 weeks <= age < 3 weeks: 10
        3 weeks <= age < 4 weeks: 20 etc
    """
    folderScore = 0
    for date in action2Dates:
        msgScore = 5 * age_of_msg_in_weeks(date)
        if age_of_msg_in_weeks(date) > 2:
            msgScore = (msgScore - 5) * 2
        if verbose:
            print "Action II: message is %s. It is %d weeks old and scores %d." % (date, age_of_msg_in_weeks(date), msgScore)
        folderScore += msgScore
    return folderScore


def scoreAction3(action3Dates, verbose):
    """
    Score for Action 3 is based on sum of message scores.
    Each message score is:
        ceil(msg_date(days))
    
    Weighting is 1.
    (Therefore each message counts immediately and accrues an extra point every day.)
    (Rationale: higher urgency so worth something immediately and more as time passes, but low value overall).
    """
    folderScore = 0
    for date in action3Dates:
        msgScore = age_of_msg_in_days(date) + 1
        if verbose:
            print "Action III: message is %s. It is %d days old and scores %d." % (date, age_of_msg_in_days(date), msgScore)
        folderScore += msgScore
    return folderScore


def scoreAction4(action4Dates, verbose):
    """
    Score for Action 4 is based on the sum of message scores.
    Each message score is:
        floor(msg_date(weeks))

    Weighting is 1.
    (Therefore there is a 'free' week for each message and thereafter they count as 1 per week)
    (Rationale: lower urgency so no cost at first and gains only per week; lower importance mains the gain is low).
    """
    folderScore = 0
    for date in action4Dates:
        msgScore = age_of_msg_in_weeks(date)
        folderScore += msgScore
        if verbose:
            print "Action IV: message is %s. It is %d weeks old and scores %d." % (date, age_of_msg_in_weeks(date), msgScore)
    return folderScore


def comment_on_score(score):
    # the following are the pass scores
    if score < 250:
        return "(O)utstanding"
    elif score < 500:
        return "(E)xceeds expectation"
    elif score < 1000:
        return "(A)s expected"

    # the following are the fail scores
    elif score < 2000:
        return "(P)oor"
    elif score < 4000:
        return "(D)readful"
    else:
        return "(T)roll"


def create_empty_file_if_needed(fileName):
    try:
        f = open(fileName, "a")
    except IOError:
        # Assume this is because the file doesn't exist. That's fine, create it.
        f = open(fileName, "a")
        writer = csv.writer(f)
        writer.writerow( ('Date', 'Inbox', 'ActionI', 'ActionII', 'ActionIII', 'ActionIV', 'Total', 'Comment') )
    return f


def log_scores(fileName, scoreList):
    """
    Each entry consists of:
        date, time, inbox, a1, a2, a3, a4, total

    @todo: should overwrite the current date if already present
    """
    f = create_empty_file_if_needed(fileName)
    try:
        writer = csv.writer(f)
        writer.writerow( (datetime.now(), scoreList[0], scoreList[1], scoreList[2], scoreList[3], scoreList[4], sum(scoreList), comment_on_score(sum(scoreList))) )
    finally:
        f.close()


def main():
    verbose = True
    scoreList = []

    inboxDates = get_dates_from_folder('INBOX')
    inboxScore = scoreInbox(inboxDates, verbose)
    print "INBOX metric is:", inboxScore
    scoreList.append(inboxScore)

    action1Dates = get_dates_from_folder('Action I')
    action1Score = scoreAction1(action1Dates, verbose)
    print "Action1 metric is:", action1Score
    scoreList.append(action1Score)

    action2Dates = get_dates_from_folder('Action II')
    action2Score = scoreAction2(action2Dates, verbose)
    print "Action2 metric is:", action2Score
    scoreList.append(action2Score)

    action3Dates = get_dates_from_folder('Action III')
    action3Score = scoreAction3(action3Dates, verbose)
    print "Action3 metric is:", action3Score
    scoreList.append(action3Score)

    action4Dates = get_dates_from_folder('Action IV')
    action4Score = scoreAction4(action4Dates, verbose)
    print "Action4 metric is:", action4Score
    scoreList.append(action4Score)

    print 70 * "-"
    print "Total GTD score: %d = %s" % (sum(scoreList), comment_on_score(sum(scoreList))) 

    # Finally, log the scores in the gtdtracker.csv file
    log_scores("gtdtracker.csv", scoreList)


if __name__ == '__main__':
    main()
