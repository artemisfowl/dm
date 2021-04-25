'''
	@file dm.py
	@module dm
	@author sb
	@date Fri, 08 May 2020 13:00:14 +0530
	@brief module component containing the main dm functions
'''

# standard libs/modules
from os import (environ, sep)
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from random import randint

# third-party libs/modules
from pygame import (init as pginit,
		quit as pgquit,
		display as pgdisplay,
		event as pgevent,
		image as pgimage,
		transform as pgtransform,
		mixer as pgmixer)
from pygame import (QUIT)
from pygame.time import Clock as pgclock
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

# custom libs/modules
from .dm_constants import (DEFAULT_FPS)
from .dm_constants import (PATTERNS, IGNORE_PATTERNS, IGNORE_DIRECTORIES,
		CASE_SENSITIVE)
from .dm_constants import (GO_RECURSIVELY)
from .dm_constants import (DM_JSON)
from .dm_exception import ResourceDirException
from .soundmgr import SoundMgr
from states.enginetitlestate import EngineTitleState
from states.stateconstants import (ENGINE_BG_ENGINE_TITLE_STATE_MUS,
		TAG_ENGINETITLESTATE)

class Dm:
	'''
		@class Dm
		@date Thu, 21 May 2020 18:23:05 +0530
		@brief Class acting as the Dungeon Master - setting up the view for the
		players
	'''
	def __init__(self, readdir : str, logger = None):
		# create a function to set up the state machine
		# also create a function to pre-configure the right options

		# Wed, 19 Aug 2020 09:36:03 +0530 - start working on the code here

		self._logger = None
		if logger is not None:
			self._logger = logger

		self.rdir = None
		if readdir is not None:
			self.rdir = readdir
		else:
			# go to the default location
			self.rdir = None

		# setup the pygame environment
		pgmixer.init()
		pginit()

		# setting up the clock
		self._clock = pgclock()

		# setting up the mixer
		self._soundmgr = SoundMgr()

		# pygame essentials
		self._screen = None	# in this one the mode will be set
		self.__set_mode()

		self._mode = None # windowed or fullscreen
		self._fps = DEFAULT_FPS	# default support is allowed for 30 fps

		self._resolutions = list()
		self.__get_resolutions()

		# state machine
		# Thu, 01 Apr 2021 00:36:24 +0530 : the first state will be that of the
		# title state - create title state
		self._state = dict()
		self._state[TAG_ENGINETITLESTATE] = EngineTitleState()

		# sound should be loaded from the state - this needs to be handled from
		# the state
		#self._bg_sound = pgmixer.Sound(ENGINE_BG_ENGINE_TITLE_STATE_MUS)
		# classes is not working

		# need to register the states to the statemachine - first set the
		# variable with the project directory information
		#self._cur_stm.set_projects(self.__monitor_res())

		# watchdog observer
		self.observer = Observer()
		# Sat, 24 Oct 2020 00:27:27 +0530 : provide the right options in this
		# section
		self._res_evt_handler = PatternMatchingEventHandler(PATTERNS,
				IGNORE_PATTERNS, IGNORE_DIRECTORIES, CASE_SENSITIVE)

		# binding the functions
		self._res_evt_handler.on_created = self._on_created
		self._res_evt_handler.on_deleted = self._on_deleted
		self._res_evt_handler.on_modified = self._on_modified
		self._res_evt_handler.on_moved = self._on_moved

	def stop_observer(self):
		'''
			@function stop_observer
			@brief function to stop the observer at while exiting the engine
		'''
		self.observer.stop()
		self.observer.join()

	def set_observer_scheduler(self):
		if self._logger is not None:
			self._logger.debug("Monitor path : {}".format(self.rdir))

		# need to raise an exception if the resource directory is not set
		if self.rdir is None:
			raise ResourceDirException("Resource Directory path not provided")

		self.observer.schedule(self._res_evt_handler,
				self.rdir, recursive = GO_RECURSIVELY)

	def _on_created(self, event):
		# Sun, 25 Oct 2020 19:21:05 +0530 : write in the logger for now
		if self._logger is not None:
			self._logger.debug(f"{event.src_path} has been created")

	def _on_deleted(self, event):
		# Sun, 25 Oct 2020 19:21:05 +0530 : write in the logger for now
		# should I be doing something in this case? Maybe, just empty the
		# memory which contains the data read from the file(s) removed
		if self._logger is not None:
			self._logger.debug(f"{event.src_path} has been deleted")

	def _on_modified(self, event):
		# Sun, 25 Oct 2020 19:21:05 +0530 : write in the logger for now
		if self._logger is not None:
			self._logger.debug(f"{event.src_path} has been modified")
			self._logger.debug(f"Directory changed : {event.is_directory}")

		if not event.is_directory:
			filename = event.src_path
			filename = filename[filename.rfind(sep)+1:]

			# populate the data in the DM model - and the model needs to be
			# updated based on the input set up by the author
			if self._logger is not None and filename == DM_JSON:
				self._logger.debug("Main DM file changed, reloading data")

	def _on_moved(self, event):
		# Sun, 25 Oct 2020 19:21:05 +0530 : write in the logger for now
		# this will be tricky to handle
		if self._logger is not None:
			self._logger.debug(f"{event.src_path} has been moved")

	def _check_state(self):
		# need to check which state is being run at this moment - basically
		# current state would be returned from this function
		pass

	def set_initial_bg(self):
		# rather than selecting any one of the images, just fade out and fade
		# in the images - keep the same images for the current version
		bg_files = self._state.get(TAG_ENGINETITLESTATE).get_files()
		if self._logger is not None:
			self._logger.debug(
					f'Random integer : {randint(0, len(bg_files))}')
		bg = pgimage.load(bg_files[randint(0, len(bg_files)-1)])

		# set up the music as well
		#self._soundmgr.load_music(self._state.get_mus(), "bg")
		# scale the background image to match the one with the screen width and
		# height
		self._scale_img(self._screen, bg, (pgdisplay.Info().current_w,
			pgdisplay.Info().current_h), (0, 0))

	def _scale_img(self, surface, img, disp_wh: tuple, pos: tuple):
		surface.blit(pgtransform.scale(img, (disp_wh[0], disp_wh[1])),
				pos)

	def show(self):
		'''
			@function show
			@date Thu, 21 May 2020 18:07:35 +0530
			@brief member function to show the items on the screen
		'''
		pass

	def update(self):
		'''
			@function update
			@date Thu, 21 May 2020 18:16:12 +0530
			@brief member function to update the main screen
		'''
		pgdisplay.flip()

	def cleanup(self):
		'''
			@function cleanup
			@date Thu, 21 May 2020 18:08:08 +0530
			@brief member function to be called when the engine is exiting
		'''
		#self._soundmgr.stop_music()
		pgquit()

	def manage(self):
		'''
			@function manage
			@date Fri, 22 May 2020 12:42:58 +0530
			@brief function handling all the events and the other things
			happening in the game - the dungeon master itself impersonated
		'''
		# Sat, 24 Apr 2021 14:30:08 +0530 : this is where the music playing and
		# all the other codes should be going in.
		for event in pgevent.get():
			# check state and load the respective background image	- this
			# check also needs to be done so that at one loading time, only one
			# image is shown - working on this one later
			#self.set_initial_bg()
			# for the first state get the music and play
			self.__handle_events(event)

	def init_watch(self):
		'''
			@function init_watch
			@date Thu, 19 Nov 2020 09:18:58 +0530
			@brief function to start the watch for the filesystem watches
		'''
		self.set_observer_scheduler()
		self.observer.start()

	def __handle_events(self, event = None):
		'''
			@function __handle_events
			@date Thu, 21 May 2020 19:53:34 +0530
			@brief internal member function to handle the events happening on
			the screen from the user
		'''
		if event == None:
			return

		if event.type == QUIT:
			if self._logger is not None:
				self._logger.debug("quit event received - doing nothing")

	def __set_mode(self):
		'''
			@function __set_mode
			@date Thu, 21 May 2020 20:18:05 +0530
			@brief internal function to set the default setting resolution
		'''
		tmp = pgdisplay.Info()
		self._screen = pgdisplay.set_mode((tmp.current_w, tmp.current_h))

		# temporary for testing purposes
		#self._screen = pgdisplay.set_mode((1366, 768))

	def __get_resolutions(self):
		'''
			@function __get_resolutions
			@date Thu, 21 May 2020 18:32:01 +0530
			@brief internal member function to get the resolutions supported by
			the system running this engine
		'''
		self._resolutions = pgdisplay.list_modes()

	def run(self):
		'''
			@function run
			@date Tue, 13 Apr 2021 11:43:01 +0530
			@brief function to run the main loop of the game
		'''
		self.set_initial_bg()
		#self._bg_sound.play()
		while True:
			if self._soundmgr.get_loaded_music("engine-bg") is None:
				self._soundmgr.load_sound(
						self._state[TAG_ENGINETITLESTATE].get_mus(),
						'engine-bg')
			if self._logger is not None:
				self._logger.debug(
				f'Is Music playing :{self._soundmgr.is_playing()}')
			self._soundmgr.play_music("engine-bg")
			self.manage()
			self.update()
			self._clock.tick(self._fps)
