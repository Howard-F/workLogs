import datetime
import copy
import pyfiglet
from constants import *

class PrettifyHelper:

	def dayHeader(self, timeText=None):
		""" Creates a formatted day header

		Args:
			timeText (str): A date in the format "3_letter_day_of_week 3_letter_month day year" defaults to current date. e.g. "Mon Feb 04 2019"

		Returns:
			String: Formatted day header

		"""
		if timeText is None:
			now = datetime.datetime.now()
			dayText = now.strftime(CASE_DATE_FORMAT)
		else:
			dayText = timeText

		asciidayText = pyfiglet.figlet_format(dayText)

		formattedText = ""
		longestLine = 0
		for split in asciidayText.split('\n')[:5]:
			formattedText += "|" + (' ' * (96 - len(split) / 2)) + split + (' ' * (96 - len(split) / 2)) + (' ' * (1 - (len(split) % 2))) + "|\n"

		top = SOLID_LINE + BUFFER
		bot = BUFFER + SOLID_LINE + "\n\n\n\n"

		return top + formattedText + bot


	def caseHeader(self, id, companyName, companySH, desc):
		""" Creates a formatted case header for the given case

		Args:
			id (str): ID of the case, max length 174
			companyName (str): Company name of the case, max length 176
			desc (str): Description of the case, max length 181 chars

		Returns:
			String: Formatted case header
		"""
		if(len(id) > 174):
			raise ValueError("ID exceeds 174 charcters")
		elif(len(companyName) > 176):
			raise ValueError("ID exceeds 176 charcters")
		elif(len(desc) > 181):
			raise ValueError("ID exceeds 176 charcters")

		top = SOLID_LINE + BUFFER + BUFFER
		idRow = "| > Case Number/ID: " + id + (' ' * (174 - len(id))) + "|\n"
		companyRow = "| > Company Name: " + companyName + " | " +  "(" + companySH + ")" + (' ' * (171 - (len(companyName) + len(companySH)) )) + "|\n"
		descRow = "| > Summary: " + desc + (' ' * (181 - len(desc))) + "|\n"
		bot = BUFFER + BUFFER + SOLID_LINE

		return top + idRow + companyRow + descRow + bot


	def log(self, timeText, log):
		""" Formats the given log entry

		Args:
			timeText (str): A date in the format "3_letter_day_of_week 3_letter_month day year - hour:minute". e.g. "Tue Jan 22 2019 - 12:02"
			log (str): A string of logs

		Returns:
			String: formatted log entry
		"""
		top = BUFFER + "| > Log Time: " + timeText + (' ' * (180 - len(timeText))) + "|\n" + BUFFER

		logData = ""
		for row in log.split("\n"):
			logData += "| " + row + (' ' * (MAX_INSIDE_TEXT - len(row))) + " |\n"

		bot = BUFFER + DOTTED_LINE

		return top + logData + bot


	def case(self, id, case):
		""" Formats the given case

		Args:
			id (str): id of the case
			case (dict): case information. e.g. {"companyName": "IBM", "companyShorthand": "IBM", "summary": "example summary"}

		Returns:
			String: Formatted case
		"""
		logEntries = case.get("log")

		res = self.caseHeader(id, case.get("companyName"), case.get("companyShorthand"), case.get("summary"))
		for logEntry in logEntries:
			res += self.log(logEntry[0], logEntry[1])

		res = res[:len(res) - 196] + SOLID_LINE

		return res



class Prettify:

	def __init__(self, logs):
		self.prettify = PrettifyHelper()
		self.logs = logs


	def allLogs(self):
		""" Formats all logs without order
		
		Returns:
			String: Formatted string of all logs

		"""
		res = ""
		cases = self.logs.keys()
		if "by_date" in cases: cases.remove("by_date")
		for case in cases:
			res += self.prettify.case(case, self.logs.get(case)) + "\n\n"
		return res


	def logsOnDate(self, timeText):
		""" Formats all logs on specified date

		Args:
			timeText (str): A date in the format "3_letter_day_of_week 3_letter_month day year" defaults to current date. e.g. "Mon Feb 04 2019"

		Returns:
			String: Formatted string of all logs on specified date
		"""
		res = self.prettify.dayHeader(timeText)

		givenDateTimeLogs = datetime.datetime.strptime(timeText, CASE_DATE_FORMAT).replace(hour=23, minute=59, second=59, microsecond=999999)

		if not timeText in self.logs.get("by_date").keys():
			return ""
		else:
			ids = self.logs.get("by_date").get(timeText)

			for id in ids:
				workItem = copy.deepcopy(self.logs.get(id))
				for log in workItem.get("log"):
					currentLogdateTimelogs = datetime.datetime.strptime(log[0],LOG_DATE_FORMAT)
					#if the log time is inside timeText timeframe then write to res
					if givenDateTimeLogs < currentLogdateTimelogs:
						workItem.get("log").remove(log)
				res += self.prettify.case(id, workItem) + "\n"

		return res


	def allLogsByDate(self):
		""" Formats all logs by date. Only showing entries created on or before date

		Returns:
			String: Formatted string of all logs ordered by date
		"""
		dates = self.logs.get("by_date").keys()

		res = ""

		if not dates:
			return ""
		else:
			logsByDate = [datetime.datetime.strptime(date, CASE_DATE_FORMAT) for date in dates]
			logsByDate.sort()
			dates = [datetime.datetime.strftime(datelogs, CASE_DATE_FORMAT) for datelogs in logsByDate]
			
			for date in dates:
				res += self.logsOnDate(date) + "\n\n\n\n"
		return res









































