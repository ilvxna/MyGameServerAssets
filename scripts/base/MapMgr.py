import py_util
from config import error_code
from map_data import MapDataMgr

from config import public_config
import KBEngine
from KBEDebug import *

g_map_mgr=MapDataMgr()

_STATE_INIT            = 0      #初始状态
_STATE_MAP_LOADED      = 1      #所有地图加载完毕
_STATE_CITIES_LOADED   = 2      #所有玩家城市加载完毕
_STATE_MAP_LOADING     = 3      #正在加载地图


_TIMER_ID_24_CLOCK = 11      #每日0点的timer
_TIMER_ID_EVERY_HOUR = 12    #每个小时一次的timer

_INIT_MAP_COUNT = 2000    #初始创建的空的spaceloader数量

_EXTEND_MAP_COUNT = 1    #每次扩展场景时需要创建的分线

class MapMgr(KBEngine.Base,GameObject):
	log_game_info('MapMgr:__ctor__', '')

	self.MapCount = 0              #地图的总数
	self.MapLoadedCount = 0        #已加载地图数
	self.State = _STATE_INIT       #状态:初始/地图加载完毕/玩家城市加载完毕

    #所有space的entity对应mb的哈希table
	self.MapPool = {}

    #空闲的副本区
	self.IdleSpecialMapPool = {}   #数据结构：{{base的mb, cell的mb}, ...}

    #正在启用的副本区
	self.BusySpecialMapPool = {}    #数据结构：{地图ID={分线ID={base的mb， cell的mb}, ...}, ...}

	self.SpaceLoaderCount = {}      #每一个分线里面有多少人，做成一个table对应，格式：{地图ID={分线ID=人数, ...}, ...}

    #记录全服总人数
	self.SumPlayerCount = 0

#    #记录每一个场景各个分线的总人数
#    self.ScenePlayerCount = {}

    #初始化各个场景对应的分线信息
	MapData = g_map_mgr.getMapData()
	for sceneId, _ in pairs(MapData):
		self.SpaceLoaderCount[sceneId] = {}
		self.BusySpecialMapPool[sceneId] = {}
