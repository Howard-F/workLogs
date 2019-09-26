from logger import *
import pprint
import unittest


class manualTest():
	def __init__(self):
		self.pp = pprint.PrettyPrinter(indent=4)
		self.lTogger = Logger()

	def printLogs(self):
		self.pp.pprint(self.logger.LOGS)

	def deleteByID(self, id):

		res = "Delete requested on ID '" + id + "'."

		if self.logger.LOGS.get(id):
			del self.logger.LOGS[id]
			res += " Main logs deleted."
		else:
			res += " ID not found in main logs."

		by_date_flag = False
		for i in list(self.logger.LOGS["by_date"].keys()):
			if id in self.logger.LOGS["by_date"][i]:
				self.logger.LOGS["by_date"][i].remove(id)
				by_date_flag = True

		if by_date_flag:
			res += " by_date entry(s) deleted"
		else:
			res += " ID not found in by_date logs."

		print(res)



class testsomething(unittest.TestCase):
	def setUp(self):
		pass
	def tearDown(self):
		pass
	def test1(self):
		pass

test = manualTest()

test.deleteByID('1')

test.logger.save_logs("c")
