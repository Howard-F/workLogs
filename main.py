from loggerCLI import *
from logger import *

if __name__ == "__main__":
	logger = Logger()

	#if no args received, ie. command line log mode
	interactiveLogging = LoggerCLI(logger)
	#else interactivelogging = loggerArgs() for example

	interactiveLogging.run()
