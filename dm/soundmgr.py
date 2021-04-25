'''
	@file soundmgr.py
	@module dm
	@author sb
	@date Tue, 13 Apr 2021 22:37:17 +0530
	@brief module component containing the sound mangement functions
'''

# third party libs/modules
from pygame import mixer as pgmixer
from pygame import USEREVENT

class SoundMgr:
	def __init__(self):
		pgmixer.init()
		self._music = dict()

	def load_music(self, fpath, name):
		self._music[name] = pgmixer.music.load(fpath)

	def load_sound(self, fpath, name):
		self._music[name] = pgmixer.Sound(fpath)

	def get_loaded_music(self, name):
		return self._music.get(name)

	def stop_music(self):
		pgmixer.music.stop()

	def get_channels(self):
		return pgmixer.get_num_channels()

	def is_playing(self):
		return pgmixer.Channel(0).get_busy()

	def play_music(self, name):
		if not pgmixer.Channel(0).get_busy():
			self._music.get(name).play()

