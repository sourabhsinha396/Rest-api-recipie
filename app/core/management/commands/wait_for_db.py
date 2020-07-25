import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

class Command(BaseCommand):
	"""Django command to pause execution untill Databse ready"""
	def handle(self,*args,**options):
		self.stdout.write("Whating for db to start")
		db_conn = None
		while not db_conn:
			try:
				db_conn = connections['default']
			except OperationalError:
				self.stdout.write("Db unavailable waiting for 1 sec")
				time.sleep(1)
		self.stdout.write(self.style.SUCCESS('Database Available'))
