'''
	@file titlestate.py
	@module states
	@author sb
	@date Wed, 07 Apr 2021 08:44:14 +0530
	@brief module to show the title of the game. This is the initial state in
	which the game would be starting
'''

# standard libs/modules
from uuid import uuid4

# custom libs/modules
from .state import State
from .stateconstants import (ENGINE_BG_RESOURCE_DIR,
		ENGINE_BG_ENGINE_TITLE_STATE_MUS,
		TAG_ENGINETITLESTATE)

class EngineTitleState(State):
	def __init__(self):
		super(EngineTitleState, self).__init__()
		self._set_uuid_()

		# load the initial background images
		self.set_dir(dirname=ENGINE_BG_RESOURCE_DIR)

		# save the path of the music to be played in the background
		self.bg_path = ENGINE_BG_ENGINE_TITLE_STATE_MUS

	def _set_uuid_(self):
		self.__uuid = TAG_ENGINETITLESTATE

	def get_mus(self):
		return self.bg_path

