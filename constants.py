#CONSTANTS
LOG_LINE_LENGTH = 195
MAX_INSIDE_TEXT = LOG_LINE_LENGTH - 4 #one space of buffer on each side
SOLID_LINE = " " + ("-" * (LOG_LINE_LENGTH - 2)) + " \n"
DOTTED_LINE = "|" + (" _" * ((LOG_LINE_LENGTH - 3) // 2)) + " |\n"
BUFFER = "| " + (" " * MAX_INSIDE_TEXT) + " |\n"
LOG_DATE_FORMAT = "%a %b %d %Y - %H:%M"
CASE_DATE_FORMAT = "%a %b %d %Y"

#CLI
CLI_LINE_LENGTH = 100


#File Locations
FULL_CODE_PATH = "/Users/howard.fung@ibm.com/Desktop/scripts/workLogs/"
LOGS_DIRECTORY = "logs/"
LOGS_FILE_NAME = "LOGS.pkl"
EDIT_FILE_NAME = "edit.out"
ARCHIVES_FILE_NAME = "ARCHIVES.pkl"

LOGS_FULL_PATH = FULL_CODE_PATH + LOGS_DIRECTORY + LOGS_FILE_NAME
ARCHIVES_FULL_PATH = FULL_CODE_PATH + LOGS_DIRECTORY + ARCHIVES_FILE_NAME
DEFAULT_ACTIVE_WORK_LOGS_OUTPUT = FULL_CODE_PATH + "active_work_logs.out"
EDIT_FILE = FULL_CODE_PATH + EDIT_FILE_NAME
#	center = 97


#Options
AUTO_COMMIT = True
DEFAULT_DISPLAYED_DAYS = 7

DELETE_OLD_CLOSED_CASES = True
CLOSED_CASE_KEEP_DAYS = 14