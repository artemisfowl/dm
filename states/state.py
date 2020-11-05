'''
	@file state.py
	@module dm
	@author sb
	@date Fri, 06 Nov 2020 00:42:26 +0530
	@brief module component containing the menu state details
'''

# standard libs/modules
from uuid import uuid4
from abc import abstractmethod

class State:
	def __init__(self):
		self._uuid = uuid4()
		self._logger = None

	@abstractmethod
	def get_uuid(self):
		return self._uuid
