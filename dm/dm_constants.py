'''
	@file dm_constants.py
	@module dm
	@author sb
	@date Fri, 08 May 2020 21:44:05 +0530
	@brief module component containing the dm constants
'''

# configuration constants
GAME_CONF_KEY = "gameconf"

LOGGER_SECTION = "logger"
ENGINE_SECTION = "engine"

LOGFILE_OPTION = "logfile"
LOGDIR_OPTION = "logdir"
LOGTOFILE_OPTION = "logtofile"
LOGTOSTDIO_OPTION = "logtostdio"
ENABLE_DEBUG_OPTION = "enabledebug"

READ_RES_DIR_OPTION = "readresdir"
READ_RES_DBG_DIR_OPTION = "debugdir"
READ_RES_REL_DIR_OPTION = "releasedir"

# default values
LOGFILE_VALUE = "engine"
LOGDIR_VALUE = "logs"
LOGTOFILE_VALUE = 1
LOGTOSTDIO_VALUE = 0
ENABLE_DEBUG_VALUE = 1
READ_RES_DIR_VALUE = "./game-dev"
READ_RES_DBG_DIR_VALUE = "debug"
READ_RES_REL_DIR_VALUE = "release"

# enable/disable constants
ENABLE = 1
DISABLE = 0

# game constants
DEFAULT_FPS = 30

# state identifiers
MENU_STATE_ID = 1000

# resource pattern
PATTERNS = ["*"]
IGNORE_PATTERNS = ""
IGNORE_DIRECTORIES = False
CASE_SENSITIVE = True

# observer settings
GO_RECURSIVELY = True

# main file
DM_JSON = "dm.json"
