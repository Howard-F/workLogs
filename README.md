# Logging Tool for Everyday Work

## Logs Data Structure
{
	'by_date': 
	{
		'Fri Feb 08 2019': [1, 2, 3],
		'Wed Feb 06 2019': [2, 5, 6]
	}
	'2':
	{
		'status': 'open'
		'companyName': 'Some Company',
		'companyShorthand': 'SC',
		'summary': 'someSummary',
		'log': [['Wed Feb 08 2019 - 11:58', 'logEntry1'], ['Fri Feb 08 2019 - 13:52', 'log entry 2 \n']]
	}
}

## Todo

### In Progress
* Refactor to use args as well
	- Able to make new tool that uses logger logic

* Return a message
	- Half implemented

### Not Started
* Delete function
* Can't do accents
* Company Shorthand Duplicates
* Exit out of logging without loggin
* Edit
* Close Case
	on close case, write closed case at end, with resolution
	write to archive file, create a archive pkl item and hide from output (option to show), on progress for each day, just don't show, only show case closed + reso on case close day
	on reopen, write a reopen with reason, and continue logging and unhide (basically a remove). Logs by default show last 2 days of cases that were closed.
	keep progress data for how long?

	create menu option for close (as well as edit?)
	create fancy closed case
	reopen case possbility
	
   Archive?  
   Reopen?
* Configs file, .ini? ex: automatically output the logs after writing,

* view log by specific id
* logger for the logger?
