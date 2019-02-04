import pyfiglet
import datetime
import pickle
import sys
import textwrap
import copy
import os

from constants import *

def createNewDayHeader(timeText=None):
	if timeText is None:
		now = datetime.datetime.now()
		newDayText = now.strftime(CASE_DATE_FORMAT)
	else:
		newDayText = timeText

	asciiNewDayText = pyfiglet.figlet_format(newDayText)

	formattedText = ""
	longestLine = 0
	for split in asciiNewDayText.split('\n')[:5]:
		formattedText += "|" + (' ' * (96 - len(split) / 2)) + split + (' ' * (96 - len(split) / 2)) + (' ' * (1 - (len(split) % 2))) + "|\n"

	TOP = SOLID_LINE + BUFFER
	BOT = BUFFER + SOLID_LINE + "\n\n\n\n"

	return TOP + formattedText + BOT

"""
	String id: max length 174
	String companyName: max length 176
	String desc: max length 181 chars
	Return: String
"""
def prettifyCaseHeader(id, companyName, companySH, desc):
	if(len(id) > 174):
		raise ValueError("ID exceeds 174 charcters")
	elif(len(companyName) > 176):
		raise ValueError("ID exceeds 176 charcters")
	elif(len(desc) > 181):
		raise ValueError("ID exceeds 176 charcters")

	TOP = SOLID_LINE + BUFFER + BUFFER
	ID_ROW = "| > Case Number/ID: " + id + (' ' * (174 - len(id))) + "|\n"
	COMP_ROW = "| > Company Name: " + companyName + " | " +  "(" + companySH + ")" + (' ' * (171 - (len(companyName) + len(companySH)) )) + "|\n"
	DESC_ROW = "| > Summary: " + desc + (' ' * (181 - len(desc))) + "|\n"
	BOT = BUFFER + BUFFER + SOLID_LINE

	return TOP + ID_ROW + COMP_ROW + DESC_ROW + BOT


def prettifyLog(timeText, log):
	TOP = BUFFER + "| > Log Time: " + timeText + (' ' * (180 - len(timeText))) + "|\n" + BUFFER

	logData = ""
	for row in log.split("\n"):
		logData += "| " + row + (' ' * (MAX_INSIDE_TEXT - len(row))) + " |\n"

	BOT = BUFFER + DOTTED_LINE

	return TOP + logData + BOT


def save_logs(logs, file_name):
    with open('logs/'+ file_name + '.pkl', 'wb') as f:
        pickle.dump(logs, f, pickle.HIGHEST_PROTOCOL)


def load_logs(file_name):
	try:
	    with open('logs/' + file_name + '.pkl', 'rb') as f:
	        return pickle.load(f)
	except IOError:
		return {}

"""
Input: String search term
Output: ID key of Logs to edit
"""
def searchLogs(searchTerm, LOGS):
	ids = LOGS.keys()
	if "by_date" in ids: ids.remove("by_date")

	
	for id in ids:
		if searchTerm.lower() == id.lower() or LOGS.get(id).get("companyShorthand") == searchTerm.upper():
			return id
	
	return ""


def createNewWorkItem(LOGS):
	id = raw_input("What is the case number or ID of the work item?\n").upper()

	if LOGS.get(id):
		print("Matching Existing case, returning to main")
		main()

	company = raw_input("What is the company name? (N/A if not applicable)\n")
	companyShorthand = raw_input("What is the shorthand name or acroymn of the company? (N/A if not applicable)\n")
	summary = raw_input("What is the summary of the work item?\n")
	print("Any additional notes? (Press return twice to finish)")
	log = getLogInput("", 0)
	now = datetime.datetime.now()
	timeText = now.strftime(LOG_DATE_FORMAT)

	redirect = 0
	while(True):
		print("Is this correct? 1. (Y)es, 2. (N)o")
		print("ID: %s\nCompany Name: %s\nCompany Shorthand: %s\nSummary: %s\nDescription: \n%s" % (id, company, companyShorthand, summary, log))

		usr_input = raw_input("Enter option: ")

		if(usr_input.lower() == "y" or usr_input.lower() == "yes" or usr_input == "1"):
			data = {"companyName": company, "companyShorthand": companyShorthand, "summary": summary, "log": [[timeText, log]]}
			LOGS[id] = data
			logByDate(LOGS, now.strftime(CASE_DATE_FORMAT), id)

			print("Writing to logs")
			save_logs(LOGS, "LOGS")
			break
		elif(usr_input.lower() == "n" or usr_input.lower() == "no" or usr_input == "2"):
			print("Returning you to main create new work item menu")
			redirect = 1
			break
		else:
			print("Invalid Input")
	
	if redirect == 1:
		return createNewWorkItem(LOGS)
	else:
		return 0

#Log entries is a list of tuples
#Returns the entry for the time given
def getCaseByTime(logEntries, timeText):
	for logEntry in logEntries:
		if logEntry[0] == timeText:
			return logEntry[1]


def prettifyCase(id, case):
	caseLogs = case.get("log")
	logTimes = [x[0] for x in caseLogs]
	res = ""

	res += prettifyCaseHeader(id, case.get("companyName"), case.get("companyShorthand"), case.get("summary"))

	for loggedTime in logTimes:
		res += prettifyLog(loggedTime, getCaseByTime(caseLogs, loggedTime))

	res = res[:len(res) - 196] + SOLID_LINE
	return res


def prettifyAllLogs(LOGS):
	res = ""
	cases = LOGS.keys()
	if "by_date" in cases: cases.remove("by_date")
	for case in cases:
		res += prettifyCase(case, LOGS.get(case)) + "\n\n"
	return res

"""
	input: LOGS, timeText in ("Mon Jan 20 2019") format (CASE_DATE_FORMAT)
"""
def viewLogByDate(LOGS, timeText):
	res = createNewDayHeader(timeText)

	givenDateTimelogs = datetime.datetime.strptime(timeText, CASE_DATE_FORMAT).replace(hour=23, minute=59, second=59, microsecond=999999)

	if not timeText in LOGS.get("by_date").keys():
		return ""
	else:
		ids = LOGS.get("by_date").get(timeText)

		for id in ids:
			workItem = copy.deepcopy(LOGS.get(id))
			for log in workItem.get("log"):
				currentLogdateTimelogs = datetime.datetime.strptime(log[0],LOG_DATE_FORMAT)
				#if the log time is inside timeText timeframe then write to res
				if givenDateTimelogs < currentLogdateTimelogs:
					workItem.get("log").remove(log)
			res += prettifyCase(id, workItem) + "\n"

	return res


def viewAllLogsByDate(LOGS):
	dates = LOGS.get("by_date").keys()

	res = ""

	if not dates:
		return ""
	else:
		dateslogss = [datetime.datetime.strptime(date, CASE_DATE_FORMAT) for date in dates]
		dateslogss.sort()
		dates = [datetime.datetime.strftime(datelogs, CASE_DATE_FORMAT) for datelogs in dateslogss]
		
		for date in dates:
			res += viewLogByDate(LOGS, date) + "\n\n\n\n"
	return res

	


"""
	Takes a continuous stream of input until 2 empty lines
	Input: recursive result, counter for new lines
	Returns: String of input
"""
def getLogInput(res, counter):
	usr_input = raw_input()
	if(usr_input.lower() == "exit"):
		print("Goodbye.")
		sys.exit()

	if not usr_input:
		if counter == 1:
			return res[:-1]
		counter += 1
	else:
		counter = 0

	usr_input = textwrap.fill(usr_input, MAX_INSIDE_TEXT)

	res += usr_input + "\n"

	return getLogInput(res, counter)


def logByDate(LOGS, timeText, id):
	# Array of IDs for a day
	dayLog = LOGS.get("by_date").get(timeText)

	# If day already made
	if dayLog:
		if not id in dayLog:
			dayLog.append(id)
	else:
		LOGS.get("by_date")[timeText] = [id]


def log(LOGS):
	usr_input = menuWritter("Log", "Search by ID or company shorthand (Exact)", None, None, "Search logs for: ")

	#Exit loop
	if(usr_input.lower() == "exit"):
		print("Goodbye.")
		sys.exit()

	searchResult = searchLogs(usr_input, LOGS)
	if(searchResult):
		usr_input = menuWritter("Log", "Found Match: " + searchResult + ", is this correct?", ["Yes", "No"])

		if(usr_input.lower() == "y" or usr_input.lower() == "yes" or usr_input == "1"):
			logToEdit = LOGS.get(searchResult).get("log")

			print("Taking notes now")
			logText = getLogInput("", 0)

			now = datetime.datetime.now()
			timeText = now.strftime(LOG_DATE_FORMAT)

			#If inside this case and there is already a log entry for this time
			alreadyEntryForThisTime = False
			for entry in logToEdit:
				if timeText == entry[0]:
					entry[1] += logText
					alreadyEntryForThisTime = True

			if not alreadyEntryForThisTime:
				logToEdit.append([timeText, logText])

			logByDate(LOGS, now.strftime(CASE_DATE_FORMAT), searchResult)

			print("Writing to logs")
			save_logs(LOGS, "LOGS")


		elif(usr_input.lower() == "n" or usr_input.lower() == "no" or usr_input == "2"):
			print("Returning you to main search")
			log(LOGS)
		else:
			print("Invalid input: " + usr_input)
			log(LOGS)
	else:
		usr_input = menuWritter("Log", "Not found, would you like to create a new work item?", ["Yes", "No"])

		if(usr_input.lower() == "y" or usr_input.lower() == "yes" or usr_input == "1"):
			createNewWorkItem(LOGS)
		elif(usr_input.lower() == "n" or usr_input.lower() == "no" or usr_input == "2"):
			print("Returning you to main search")
			log(LOGS)
		else:
			print("Invalid input: " + usr_input)
			log(LOGS)

def outputToText(output, fileName=None):
	if fileName is None:
		fileName = "output.txt"

	file = open(fileName, "w")
	file.write(output)
	file.close

"""
input: String: title, String: message, List of Strings: options, String: header
Prints the menu
"""
def menuWritter(title, message=None, options=None, header=None, inputMsg=None):
	LINE_LENGTH = 100

	os.system("clear")

	if header is not None:
		print(header)

	TOP = "= " + title + " " + ('=' * (LINE_LENGTH - len(title) - 3)) + "\n"
	BOT = "\n" + ('=' * (LINE_LENGTH)) + "\n"

	print(TOP)

	if message is not None:
		MESSAGE_BUFFER = ' ' * ((LINE_LENGTH - len(message)) / 2)
		MESSAGE = MESSAGE_BUFFER + message + MESSAGE_BUFFER + (' ' * (1 - (len(message) % 2)))
		print(MESSAGE)
		if options is not None:
			print("")

	if options is not None:
		options = [str(i + 1) + ". " + options[i] for i in range(0, len(options))]
		
		# space used by options = for each option: len(option)
		OPTIONS_SPACE = 0
		for option in options:
			OPTIONS_SPACE += len(option)
		
		# space used by dividers = len(options list) - 1
		DIVIDER_SPACE = len(options) - 1

		# space remain = 58 - (space used by options + space used by dividers)
		REMAINING_SPACE = LINE_LENGTH - (OPTIONS_SPACE + DIVIDER_SPACE)

		# space between each option = (space remain / (len(options list) - 1)) / 2
		OPTION_BUFFER = (REMAINING_SPACE / len(options)) / 2

		#If not enough space
		if OPTION_BUFFER < 2 or REMAINING_SPACE < 10:
			raise Exception('Options exceed maximum total character limit')

		#update space left after options buffer
		REMAINING_SPACE = REMAINING_SPACE - ((OPTION_BUFFER * 2) * len(options))

		# if space between each option + (((space remain / (len(options list) - 1)) % 2) / 2) <remainder div 2> is less than 5 # space between each option -= 1
		# and update remaining space
		if OPTION_BUFFER + (REMAINING_SPACE / 2) < 5:
			OPTION_BUFFER -= 1
			REMAINING_SPACE = LINE_LENGTH - (OPTIONS_SPACE + DIVIDER_SPACE + ((OPTION_BUFFER * 2) * len(options)))

		OPTION_BUFFER = ' ' * OPTION_BUFFER

		OPTIONS = ' ' * (REMAINING_SPACE / 2)
		for option in options[:-1]:
			OPTIONS += OPTION_BUFFER + option + OPTION_BUFFER + "|"

		OPTIONS += OPTION_BUFFER + options[-1] + OPTION_BUFFER + (' ' * (REMAINING_SPACE / 2))
		print(OPTIONS)

	print(BOT)
	if inputMsg is None:
		inputMsg = "Enter option: "
	return raw_input(inputMsg)




def main():
	LOGS = load_logs("LOGS")

	if not LOGS.get("by_date"): LOGS["by_date"] = {}

	usr_input = ""
	while(1):
		usr_input = menuWritter("Main Menu", None, ["Log", "New", "View", "Exit"], pyfiglet.figlet_format("Logger . py"))

		#print(load_logs("LOGS"))
		if(usr_input == "1" or usr_input.lower() == "log"):
			log(LOGS)
		elif(usr_input == "2" or usr_input.lower() == "new"):
			createNewWorkItem(LOGS)
		elif(usr_input == "3" or usr_input.lower() == "view"):

			print("View Logs for:")
			print("1. Yesterday, 2. Today, 3. All by date, 4. All by case, 5. Specific ID")
			usr_input = menuWritter("View", "View logs for:", ["Yesterday", "Today", "All by date", "All by case", "Specific ID"])

			viewOutput = ""
			if(usr_input == "1"):
				yesterday = datetime.date.today() - datetime.timedelta(1)
				viewOutput = viewLogByDate(LOGS, yesterday.strftime(CASE_DATE_FORMAT))
			elif(usr_input == "2"):
				viewOutput = viewLogByDate(LOGS, datetime.datetime.now().strftime(CASE_DATE_FORMAT))
			elif(usr_input == "3"):
				viewOutput = viewAllLogsByDate(LOGS)

			if viewOutput != "":
				outputToText(viewOutput)
			else:
				print("Nothing logged or view failed.")

		elif(usr_input.lower() == "exit" or usr_input == "4"):
			print("Goodbye.")
			sys.exit()
		#print(load_logs("LOGS").get("TS001test").get("log").get("Wed Jan 16 - 06:10"))


main()
#Refactor to use args as well
#Delete function
#Can't do accents
#Return a message
#Company Shorthand Duplicates
#Exit out of logging without loggin
#Edit?
#Close Case
	# Archive?
	# Reopen?
# view log by specific id


#print(load_logs("LOGS"))
#print(load_logs("LOGS").get("TS001test".upper()).get("log").get("2017-01-05-15:35"))
#main()

#print(createNewDayHeader())
#print(createCaseHeader("TS0100121", "abc", "test"))

#LOGS = {'1': {'companyShorthand': '3', 'companyName': '2', 'log': [('Mon Jan 21 2019 - 16:39', '5\n'), ('Mon Jan 22 2019 - 16:39', '123123\n')], 'summary': '4'}, 'by_date': {'Mon Jan 21 2019': ['1', '2']}, '2': {'companyShorthand': '4', 'companyName': '3', 'log': [('Mon Jan 21 2019 - 16:39', '6\n')], 'summary': '5'}}





