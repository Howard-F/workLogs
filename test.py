	def logsBetweenDates(self, start, end):
		""" Formats all logs between specified dates, inclusive of that day.

		Args:
			start (str): A start date in the format "3_letter_day_of_week 3_letter_month day year" defaults to current date. e.g. "Mon Feb 04 2019"
			end (str): An end date in the format "3_letter_day_of_week 3_letter_month day year" defaults to current date. e.g. "Tue Feb 05 2019"

		Returns:
			String: Formatted string of all logs on specified date
		"""
		start = datetime.datetime.strptime(start, CASE_DATE_FORMAT).replace(hour=0, minute=0, second=0, microsecond=1)
		end = datetime.datetime.strptime(end, CASE_DATE_FORMAT).replace(hour=23, minute=59, second=59, microsecond=999999)

		dates = self.logs.get("by_date").keys()
		res = ""

		if not dates:
			return ""
		else:
			dates = [datetime.datetime.strptime(date, CASE_DATE_FORMAT) for date in dates]
			validDates = [date for date in dates if (start < date and date > end)]
			validDates.sort()
			dates = [datetime.datetime.strftime(dates, CASE_DATE_FORMAT) for dates in validDates]
			
			for date in dates:
				res += self.logsOnDate(date) + "\n\n\n\n"
		return res