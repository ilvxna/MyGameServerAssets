import py_util
from config import error_code
from map_data import MapDataMgr

from config import public_config
import KBEngine
from KBEDebug import *

g_map_mgr=MapDataMgr()

_STATE_INIT            = 0      #��ʼ״̬
_STATE_MAP_LOADED      = 1      #���е�ͼ�������
_STATE_CITIES_LOADED   = 2      #������ҳ��м������
_STATE_MAP_LOADING     = 3      #���ڼ��ص�ͼ


_TIMER_ID_24_CLOCK = 11      #ÿ��0���timer
_TIMER_ID_EVERY_HOUR = 12    #ÿ��Сʱһ�ε�timer

_INIT_MAP_COUNT = 2000    #��ʼ�����Ŀյ�spaceloader����

_EXTEND_MAP_COUNT = 1    #ÿ����չ����ʱ��Ҫ�����ķ���

class MapMgr(KBEngine.Base,GameObject):
	log_game_info('MapMgr:__ctor__', '')

	self.MapCount = 0              #��ͼ������
	self.MapLoadedCount = 0        #�Ѽ��ص�ͼ��
	self.State = _STATE_INIT       #״̬:��ʼ/��ͼ�������/��ҳ��м������

    #����space��entity��Ӧmb�Ĺ�ϣtable
	self.MapPool = {}

    #���еĸ�����
	self.IdleSpecialMapPool = {}   #���ݽṹ��{{base��mb, cell��mb}, ...}

    #�������õĸ�����
	self.BusySpecialMapPool = {}    #���ݽṹ��{��ͼID={����ID={base��mb�� cell��mb}, ...}, ...}

	self.SpaceLoaderCount = {}      #ÿһ�����������ж����ˣ�����һ��table��Ӧ����ʽ��{��ͼID={����ID=����, ...}, ...}

    #��¼ȫ��������
	self.SumPlayerCount = 0

#    #��¼ÿһ�������������ߵ�������
#    self.ScenePlayerCount = {}

    #��ʼ������������Ӧ�ķ�����Ϣ
	MapData = g_map_mgr.getMapData()
	for sceneId, _ in pairs(MapData):
		self.SpaceLoaderCount[sceneId] = {}
		self.BusySpecialMapPool[sceneId] = {}
