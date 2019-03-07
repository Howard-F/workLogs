import sys
import textwrap
import os
import datetime
import pyfiglet

from constants import *

class LoggerCLI:


	def __init__(self, logger):
		self.logger = logger
		self.display_logo = True
		self.logo = pyfiglet.figlet_format("Logger . py")
		self.autoCommit = AUTO_COMMIT


	def autoCommitMsg(self):
		""" Creates an autocommit message.

		Returns:
			String: AutoCommit message.

		"""
		if self.autoCommit:
			return " AutoCommit: Wrote to " + str(DEFAULT_ACTIVE_WORK_LOGS_OUTPUT) + " on past " + str(DEFAULT_DISPLAYED_DAYS) + " days."
		else:
			return " AutoCommit: Not activated."

	def getLogInput(self, res, counter):
		""" Recursive function that takes a continuous stream of input until 2 empty lines are seen.

		Args:
			res (str): Total user input.
			counter (int): counter for new lines observed

		Returns:
			String: String of user input

		"""
		usr_input = input()
		if(usr_input.lower() == "exit"):
			print("Exit program request received: Goodbye.")
			sys.exit()

		if not usr_input:
			if counter == 1:
				return res[:-1]
			counter += 1
		else:
			counter = 0

		usr_input = textwrap.fill(usr_input, MAX_INSIDE_TEXT)

		res += usr_input + "\n"

		return self.getLogInput(res, counter)


	def addNewWorkItem(self, id=None):
		""" Adds a new work item to logs

		Args:
			(Optional) id (str): ID of new work item

		Returns:
			String: Return message

		"""
		if id is None:
			id = self.menuWritter("New Item", "What is the case number or ID of the new work item?", None, None).upper()

		if self.logger.searchLogs(id): return "Matching Existing case, returning to main"

		company = input("What is the company name? (N/A if not applicable)\n")
		companyShorthand = input("What is the shorthand name or acroymn of the company? (N/A if not applicable)\n")
		summary = input("What is the summary of the work item?\n")
		print("Any additional notes? (Press return twice to finish)")
		log = self.getLogInput("", 0)

		while(True):
			print("Is this correct? 1. (Y)es, 2. (N)o")
			print("ID: %s\nCompany Name: %s\nCompany Shorthand: %s\nSummary: %s\nDescription: \n%s" % (id, company, companyShorthand, summary, log))
			usr_input = input("Enter option: ")

			if(usr_input.lower() == "y" or usr_input.lower() == "yes" or usr_input == "1"):
				if self.logger.addNewWorkItem(id, company, companyShorthand, summary, log) == 0:
					return "Work item " + id + " successfully added." + self.autoCommitMsg()
			elif(usr_input.lower() == "n" or usr_input.lower() == "no" or usr_input == "2"):
				return "Returned you to main"
			else:
				print("Invalid Input")


	def logWork(self):
		""" Logs work

		Returns:
			String: Return message

		"""

		id_usr_input = self.menuWritter("Log", "Search by ID or company shorthand (Exact), '!m(ain)' to return to main menu", None, None, "Search logs for: ")

		#Exit loop
		if(id_usr_input.lower() == "exit"):
			print("Exit program request received: Goodbye.")
			sys.exit()
		elif(id_usr_input == ""):
			return self.logWork()
		elif(id_usr_input == "!main" or id_usr_input == "!m"):
			return "Returned to main menu"

		id = self.logger.searchLogs(id_usr_input)
		if(id):
			usr_input = self.menuWritter("Log", "Found Match: \"" + self.logger.getWorkItem(id).get("summary") + "\", is this correct?", ["Yes", "No"])

			if(usr_input.lower() == "y" or usr_input.lower() == "yes" or usr_input == "1"):
				print("Enter status update now, hit enter twice to stop")
				logData = self.getLogInput("", 0)
				self.logger.logWork(id, logData)
				return "Work on item " + id + " sucessfully logged." + self.autoCommitMsg()
			elif(usr_input.lower() == "n" or usr_input.lower() == "no" or usr_input == "2"):
				return "Returned you to main menu"
			else:
				print("Invalid input: " + usr_input)
				self.logWork()
		else:
			usr_input = self.menuWritter("Log", "Not found, would you like to create a new work item?", ["Yes", "No"])

			if(usr_input.lower() == "y" or usr_input.lower() == "yes" or usr_input == "1"):
				return self.addNewWorkItem(id_usr_input)
			elif(usr_input.lower() == "n" or usr_input.lower() == "no" or usr_input == "2"):
				return "Returned you to main menu"
			else:
				print("Invalid input: " + usr_input)
				self.logWork()


	def viewLogs(self):
		""" Views log

		Returns:
			String: Result of view log

		"""
		returnCode = 2
		usr_input = self.menuWritter("View", "View logs for:", ["Yesterday", "Today", "All by date", "Default"])
		if(usr_input == "1"):
			returnCode = self.logger.viewLogs("c", "y", "f")
		elif(usr_input == "2"):
			returnCode = self.logger.viewLogs("c", "t", "f")
		elif(usr_input == "3"):
			returnCode = self.logger.viewLogs("c", "abd", "f")
		else:
			return_msg = "Nothing logged or view failed."
		#return "View Logs " + self.returnCodeHandler(returnCode)

	#TODO
	def returnCodeHandler(self, rc):
		if rc == 1:
			return "error on logger"
		elif rc == 2:
			return "error on CLI"
		else:
			return "successful"


	def menuWritter(self, title, message=None, options=None, header=None, inputMsg=None):
		""" Creates a formatted menu output for command line

		Args:
			title (str): Title of the menu. Ex. "Main Menu"
			(optional) message (str): Message for the menu. Ex. "View logs for:"
			(optional) options (list): List of options available for user, automatically numbered. Ex. ["Today", "Yesterday"]
			(optional) header (str): Header in front of menu. Ie. ASCII art program title
			(optional) inputMsg(str): Input message request. Ex. "Search Logs for: ", defaults to "Enter option: "

		Returns:
			String: User input of response to menu

		"""
		os.system("clear")

		if header is not None:
			print(header)

		top = "= " + title + " " + ('=' * (CLI_LINE_LENGTH - len(title) - 3)) + "\n" 
		bot = "\n" + ('=' * (CLI_LINE_LENGTH)) + "\n"

		print(top)

		if message is not None:
			MESSAGE_BUFFER = ' ' * ((CLI_LINE_LENGTH - len(message)) // 2)
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
			REMAINING_SPACE = CLI_LINE_LENGTH - (OPTIONS_SPACE + DIVIDER_SPACE)

			# space between each option = (space remain / (len(options list) - 1)) / 2
			OPTION_BUFFER = (REMAINING_SPACE // len(options)) // 2

			#If not enough space
			if OPTION_BUFFER < 2 or REMAINING_SPACE < 10:
				raise Exception('Options exceed maximum total character limit')

			#update space left after options buffer
			REMAINING_SPACE = REMAINING_SPACE - ((OPTION_BUFFER * 2) * len(options))

			# if space between each option + (((space remain / (len(options list) - 1)) % 2) / 2) <remainder div 2> is less than 5 # space between each option -= 1
			# and update remaining space
			if OPTION_BUFFER + (REMAINING_SPACE // 2) < 5:
				OPTION_BUFFER -= 1
				REMAINING_SPACE = CLI_LINE_LENGTH - (OPTIONS_SPACE + DIVIDER_SPACE + ((OPTION_BUFFER * 2) * len(options)))

			OPTION_BUFFER = ' ' * OPTION_BUFFER

			OPTIONS = ' ' * (REMAINING_SPACE // 2)
			for option in options[:-1]:
				OPTIONS += OPTION_BUFFER + option + OPTION_BUFFER + "|"

			OPTIONS += OPTION_BUFFER + options[-1] + OPTION_BUFFER + (' ' * (REMAINING_SPACE // 2))
			print(OPTIONS)

		print(bot)
		if inputMsg is None:
			inputMsg = "Enter option: "
		return input(inputMsg)


	def run(self):
		""" Runs the CLI main menu of logger

		"""
		usr_input = ""
		return_msg = None
		while(1):
			if not self.display_logo: self.logo = None
			else: self.display_logo = False

			usr_input = self.menuWritter("Main Menu", return_msg, ["Log", "New", "View", "Exit"], self.logo)

			if(usr_input == "1" or usr_input.lower() == "log"):
				return_msg = self.logWork()
			elif(usr_input == "2" or usr_input.lower() == "new"):
				return_msg = self.addNewWorkItem()
			elif(usr_input == "3" or usr_input.lower() == "view"):
				return_msg = self.viewLogs()
			elif(usr_input.lower() == "exit" or usr_input == "4"):
				print("Exit program request received: Goodbye.")
				sys.exit()

