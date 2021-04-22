'''
	@file state.py
	@module states
	@author sb
	@date Fri, 06 Nov 2020 00:42:26 +0530
	@brief module component containing the base state details
'''

# standard libs/modules
from abc import ABC, abstractmethod
from glob import glob
from os import sep

class Resource:
	def __init__(self):
		super(Resource, self).__init__()
		self.__dir = None
		self.__files = None

	def set_dir(self, dirname):
		self.__dir = dirname
		self.__files = self._load_resources()

	def get_dir(self):
		return self.__dir

	def get_files(self):
		return self.__files

	def _load_resources(self):
		return glob(f'{self.__dir}{sep}*.*')

class State(ABC):
	def __init__(self):
		self.__resource = Resource()
		self.__uuid = None

	@abstractmethod
	def _set_uuid_(self):
		pass

	def get_uuid(self):
		return self.__uuid

	def set_dir(self, dirname):
		self.__resource.set_dir(dirname)

	def get_dir(self):
		return self.__resource.get_dir()

	def get_files(self):
		return self.__resource.get_files()
