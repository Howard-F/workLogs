import datetime
import pickle
import json

from deepdiff import DeepDiff
from pprint import pformat
from constants import *
from prettify_logs import *


class Logger():

	def __init__(self):
		LOGS = self.load_logs("c")
		if not LOGS.get("by_date"): LOGS["by_date"] = {}
		self.LOGS = LOGS
		self.ARCHIVES = self.load_logs("a")
		self.prettify = PrettifyLogs(self.LOGS)
		self.outputDays = DEFAULT_DISPLAYED_DAYS

		if DELETE_OLD_CLOSED_CASES:
			self.deleteOldClosedItems()


	def deleteOldClosedItems(self):
		ids = list(self.LOGS.keys())
		if "by_date" in ids: ids.remove("by_date")

		now = datetime.datetime.now()
		for id in ids:
			# If the case is closed, and if the case is past the number of keep days, removed from logs
			if self.LOGS[id]["status"][0] == "closed" and datetime.datetime.strptime(self.LOGS[id]["status"][1], CASE_DATE_FORMAT) + datetime.timedelta(days=CLOSED_CASE_KEEP_DAYS) < now:
				# If not already archived
				if not self.ARCHIVES.get(id):
					self.ARCHIVES[id] = self.LOGS[id]
					self.save_logs("a")
				
				del self.LOGS[id]
				for date in list(self.LOGS["by_date"].keys()):
					if id in self.LOGS["by_date"][date]:
						self.LOGS["by_date"][date].remove(id)

				self.save_logs("c")


	def autoCommit(self):
		if AUTO_COMMIT:
			self.viewLogs("c", "d", "f")

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
			with open(LOGS_FULL_PATH, 'wb') as f:
				pickle.dump(self.LOGS, f, pickle.HIGHEST_PROTOCOL)
		elif mode == "a":
			with open(ARCHIVES_FULL_PATH, 'wb') as f:
				pickle.dump(self.ARCHIVES, f, pickle.HIGHEST_PROTOCOL)


	def load_logs(self, mode):
		""" Loads logs object from pickle file in ./logs/file_name

		Args:
			mode (str): Declares which obj to load
				c - Current LOGS from ./logs/LOGS.pkl
				a - Archived LOGS from ./logs/ARCHIVE.pkl

		Returns:
			Object: Object created from pickle file
		"""
		try:
			if mode == "c":
				with open(LOGS_FULL_PATH, 'rb') as f:
					return pickle.load(f)
			elif mode == "a":
				with open(ARCHIVES_FULL_PATH, 'rb') as f:
					return pickle.load(f)
		except IOError:
			print("Failed to open logs files")
			return {}
		except EOFError:
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
		data = {"status": ["open", now.strftime(CASE_DATE_FORMAT)], "companyName": company, "companyShorthand": companySH, "summary": summary, "log": [[now.strftime(LOG_DATE_FORMAT), logData]]}
		self.LOGS[id] = data
		self.logByDate(now.strftime(CASE_DATE_FORMAT), id)
		self.save_logs("c")
		self.autoCommit()
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
		self.autoCommit()
		return 0

	def editOpen(self):
		with open(EDIT_FILE, 'w') as f:
			f.write(json.dumps(self.LOGS, indent=4))
		return 0

	def editClose(self):
		with open(EDIT_FILE) as f:
			newLogs = json.load(f)
		diff = pformat(DeepDiff(self.LOGS, newLogs))
		self.LOGS = newLogs
		self.save_logs("c")
		self.prettify.updateLogs(self.LOGS)
		return diff

	def viewLogs(self, dataMode, timeMode, outputMode, id=None, fileName=None):
		"""Outputs logs

			Args:
				dataMode (str): The data selected to output
					c - current active logs
				timeMode (str): Filter output by time
					abd - All by date
					y - yesterday's logs only
					t - today's logs only
					d - default (set in constant/config)
					i - specific id, requires id
				outputMode (str): The output method
					f - to file
					cl - command line
			Returns:
				Int: 0 if successful, 1 if logger error, 2 if input error
		"""
		outputData = ""
		if dataMode == "c":
			if timeMode == "abd":
				outputData = self.prettify.allLogsByDate()
			elif timeMode == "y":
				yesterday = datetime.date.today() - datetime.timedelta(1)
				outputData = self.prettify.logsOnDate(yesterday.strftime(CASE_DATE_FORMAT))
			elif timeMode == "t":
				outputData = self.prettify.logsOnDate(datetime.datetime.now().strftime(CASE_DATE_FORMAT))
			elif timeMode == "d":
				end = datetime.datetime.now()
				start = (end - datetime.timedelta(DEFAULT_DISPLAYED_DAYS)).strftime(CASE_DATE_FORMAT)
				end = end.strftime(CASE_DATE_FORMAT)
				outputData = self.prettify.logsBetweenDates(start, end)
			elif timeMode == "i":
				if id is None or (not self.searchLogs(id)):
					return 1
				else:
					outputData = self.prettify.prettify.case(id, self.LOGS.get(id))
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
		elif outputMode == "cl":
			return outputData

		return 0


	def editStatus(self, id, status):
		workItem = self.getWorkItem(id)

		logData = ">>> Status changed - old: " + workItem["status"] + ", new: " + status + "."

		now = datetime.datetime.now().strftime(CASE_DATE_FORMAT)
		workItem["status"] = [status, now]

		#logs edit status commet
		workItem["log"].append([now.strftime(LOG_DATE_FORMAT), logData])
		self.save_logs("c")
		return 0


	def closeCase(self, id, resolution):
		workItem = self.getWorkItem(id)
		workItem["resolution"] = resolution
		self.editStatus(id, "closed")

		self.ARCHIVES[id] = workItem
		self.save_logs("a")


