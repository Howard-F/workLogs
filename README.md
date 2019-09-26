# Work Logging Tool

Currently targetted at support cases, but can be used outside of support, future plans to add a more general use.

## Usage
1. Clone the repo
2. Set DEFAULT_ACTIVE_WORK_LOGS_OUTPUT, AUTO_COMMIT, DEFAULT_DISPLAYED_DAYS if desired
3. run "python3 main.py"

## Logs Data Structure
```
{
	'by_date': 
	{
		'Fri Feb 08 2019': [1, 2, 3],
		'Wed Feb 06 2019': [2, 5, 6]
	}
	'workItemIdentifier':
	{
		'status': ['open', 'Wed Feb 08 2019'],
		'resolution': "", //Only exists when case status is closed.
		'companyName': 'Some Company',
		'companyShorthand': 'SC',
		'summary': 'someSummary',
		'log': [
				['Wed Feb 08 2019 - 11:58', 'logEntry1'],
				['Fri Feb 08 2019 - 13:52', 'log entry 2 \n']
		       ]
	}
}
```

## Todo

### In Progress
* Refactor to use args as well
	- Able to make new tool that uses logger logic

* Return a message
	- Half implemented

### Not Started
#### Detect Terminal Size for View
#### View as HTML
#### Validate Settings on startup
#### Easier log searching
#### Change case headers
#### Delete function
#### Show recent and select
* fix the hacky view logs by ID
* Ability to delete by ID
#### Can't do accents
* Accents crash the tool
#### Advanced Searching
* Currently searches by ID (and brokenly company shorthand (cannot handle duplicates)), advanced searching may be to search by anything and list out possibilites and select.
#### Exit out of logging without logging
* Entering the logging section forces you to log an entry, need an escape.
#### Edit
* Edit log information, e.g. meta data, or specific logs.
#### Close Case
	on close case, write closed case at end, with resolution
	replace entry with a case closed entry, default to not show closed case entries
	closed case entries only show on day closed
	write to archive file, create a archive pkl item and hide from output (option to show), on progress for each day, just don't show, only show case closed + reso on case close day
	on reopen, write a reopen with reason, and continue logging and unhide (basically a remove). Logs by default show last 2 days of cases that were closed.
	keep progress data for how long?

	create menu option for close (as well as edit?)
	create fancy closed case
	reopen case possbility
#### Configs file, .ini? ex: automatically output the logs after writing,
* Currently in constants
#### View log by specific id
#### Logger for the logger?
* log actions being performed
#### Tests
