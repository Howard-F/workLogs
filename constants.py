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


#Save Location
LOGS_FILE_NAME = "LOGS.pkl"
ARCHIVES_FILE_NAME = "ARCHIVES.pkl"
DEFAULT_ACTIVE_WORK_LOGS_OUTPUT = "active_work_logs.out"
#	center = 97


#Options
AUTO_COMMIT = True
DEFAULT_DISPLAYED_DAYS = 7