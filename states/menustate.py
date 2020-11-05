'''
	@file menustate.py
	@module states
	@author sb
	@date Fri, 06 Nov 2020 00:40:32 +0530
	@brief module containing all the states of the state machine to be used by
	dm
'''

# standard libs/modules
from uuid import uuid4

# custom libs/modules
from .state import State

class MenuState(State):
	def __init__(self):
		super().__init__()
		#print("UUID for this object : {}".format(self._uuid))
