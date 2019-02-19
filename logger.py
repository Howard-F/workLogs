import datetime
import pickle

from constants import *
from prettify_logs import *


class Logger():

	def __init__(self):
		LOGS = self.load_logs("c")
		if not LOGS.get("by_date"): LOGS["by_date"] = {}
		self.LOGS = LOGS
		self.prettify = PrettifyLogs(LOGS)


	def getWorkItem(self, id):
		""" Gets work item

		Args:
			id (str): ID of item to retrieve
		
		Returns:
			Object: Work item object.
		"""
		return self.LOGS.get(id)


	def save_logs(self, mode):
		""" Saves logs object as pickle file in ./logs/file_name

		Args:
			mode (str): Declares which obj to save.
				c - Current LOGS to ./logs/LOGS/pkl
			file_name (str): file_name in logs folder
		"""
		if mode == "c":
			with open('logs/'+ LOGS_FILE_NAME, 'wb') as f:
				pickle.dump(self.LOGS, f, pickle.HIGHEST_PROTOCOL)


	def load_logs(self, mode):
		""" Loads logs object from pickle file in ./logs/file_name

		Args:
			mode (str): Declares which obj to load
				c - Current LOGS from ./logs/LOGS/pkl

		Returns:
			Object: Object created from pickle file
		"""
		if mode == "c":
			try:
				with open('logs/' + LOGS_FILE_NAME, 'rb') as f:
					return pickle.load(f)
			except IOError:
				print("Failed to open " + LOGS_FILE_NAME)
				return {}


	def searchLogs(self, searchTerm):
		""" Searches logs for id by company shorthand or id

			Args:
				searchTerm (str): term to search by

			Returns:
				String; ID of found item
		"""
		ids = list(self.LOGS.keys())
		if "by_date" in ids: ids.remove("by_date")

		for id in ids:
			if searchTerm.lower() == id.lower() or self.LOGS.get(id).get("companyShorthand") == searchTerm.upper():
				return id

		return ""


	def addNewWorkItem(self, id, company, companySH, summary, logData):
		""" Adds a new work item to the logs

			Args:
				id (str): ID of new item
				company (str): Company name of new item
				companySH (str): Shorthand name of company of new item
				summary (str): Summary of new item
				logData (str): Extra log data of new item

			Returns:
				Int: 0 if successful
		"""
		now = datetime.datetime.now()
		data = {"companyName": company, "companyShorthand": companySH, "summary": summary, "log": [[now.strftime(LOG_DATE_FORMAT), logData]]}
		self.LOGS[id] = data
		self.logByDate(now.strftime(CASE_DATE_FORMAT), id)
		self.save_logs("c")
		return 0


	def logByDate(self, timeText, id):
		"""Logs the work item to the special worked on cases per date category

			Args:
				timeText (str): time log was updated in CASE_DATE_FORMAT
				id (str): ID of item
			Returns:
				Int: 0 if successful
		"""
		# Array of IDs for a day
		dayLog = self.LOGS.get("by_date").get(timeText)

		# If day already made
		if dayLog:
			if not id in dayLog:
				dayLog.append(id)
		else:
			self.LOGS.get("by_date")[timeText] = [id]


	def logWork(self, id, logData):
		"""Logs the work item

			Args:
				id (str): ID of item
				logData (str): time log was updated in CASE_DATE_FORMAT
			Returns:
				Int: 0 if successful
		"""
		now = datetime.datetime.now()
		timeText = now.strftime(LOG_DATE_FORMAT)

		logToEdit = self.LOGS.get(id).get("log")
		#If inside this case and there is already a log entry for this time
		alreadyEntryForThisTime = False
		for entry in logToEdit:
			if timeText == entry[0]:
				entry[1] += logData
				alreadyEntryForThisTime = True

		if not alreadyEntryForThisTime:
			logToEdit.append([timeText, logData])
			self.logByDate(now.strftime(CASE_DATE_FORMAT), id)

		self.save_logs("c")
		return 0



	def viewLogs(self, dataMode, timeFilter, outputMode, fileName=None):
		"""Outputs logs

			Args:
				dataMode (str): The data selected to output
					c - current active logs
				timeMode (str): Filter output by time
					abd - All by date
					y - yesterday's logs only
					t - today's logs only
				outputMode (str): The output method
					f - to file
			Returns:
				Int: 0 if successful
		"""
		outputData = ""
		if dataMode == "c":
			if timeFilter == "abd":
				outputData = self.prettify.allLogsByDate()
			elif timeFilter == "y":
				yesterday = datetime.date.today() - datetime.timedelta(1)
				outputData = self.prettify.logsOnDate(yesterday.strftime(CASE_DATE_FORMAT))
			elif timeFilter == "t":
				outputData = self.prettify.logsOnDate(datetime.datetime.now().strftime(CASE_DATE_FORMAT))
		else:
			return 2

		if outputData == "":
			return 1

		if outputMode == "f":
			if fileName is None:
				fileName = DEFAULT_ACTIVE_WORK_LOGS_OUTPUT
			file = open(fileName, "w")
			file.write(outputData)
			file.close
		return 0

