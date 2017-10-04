import py_util
from KBEDebug import *
#import public_config
from config import public_config
import math
import random

class MapDataMgr:
	def __init__(self):
		#地图表
		self._map_data = _readXml('/data/xml/map_setting.xml', 'id_i')

		self.randomScene = {}
		for k, v in pairs(self._map_data):
			if v['isRandom'] and v['isRandom'] == 1:
				INFO_MSG("MapDataMgr:initData random scene k=" % (k))

			self.randomScene[k] = true

		# --读取所有的场景配置表
		self.load_space_data()

	def load_space_data(self):
		tmp={}
		fn_prefix='/data/spaces/'
		bm_fn_prefix='/data/blockmap'

		for map_id,data in self._map_data:
			if data['spaceName'] and data['spaceName']!='':
				fn=fn_prefix+data['spaceName']+'.xml'

	#获取一个map_id的原始map_id(map_id可能是原始map_id+分线数)
	def GetSrcMapId(self,map_id):
		tmp_mid=str(map_id)

		if tmp_mid:
			tmp=tmp_mid.split('_')
			if tmp[0]:
				return tmp[0]

		return map_id
	#获取配置表的地图配置表的数据
	def getMapCfgData(self,map_id):
		return self._map_data[map_id]

	def getMapData(self):
		return self._map_data

	#获取一个entity在场景配置里的信息
	def GetEntityCfgData(self,map_id,eid):
		tmp=self._map_data[map_id]
		if tmp:
			tmp2=tmp['entities']
			if tmp2:
				return emp2[eid]

	#获取指定一个场景的Entity配置数据
	def GetMapEntityCfgData(self,map_id):
		tmp=self._map_data[map_id]
		if tmp:
			tmp2=tmp['entities']
			if tmp2:
				return tmp2

	#WB: world boss 
	def IsWBMap(self,map_id):
		id=self.GetSrcMapId(map_id)
		data=self.getMapCfgData(id)
		if not data:
			ERROR_MSG("MapDataMgr:IsWBMap map_id=" % (map_id))
			return False
		return public_config.MAP_TYPE_WB==data['type']

	#判断玩家是否处于多人副本场景
	def is_in_mpins(self,map_id):
		src_map_id=self.GetSrcMapId(map_id)
		data=self._map_data[src_map_id]
		if data:
			return data['type']==public_config.MAP_TYPE_MUTI_PLAYER_NOT_TEAM
		return False
	#判断玩家是否处于普通场景
	def is_in_normal_map(self,map_id):
		data=self._map_data[map_id]
		if data:
			return data['type']==public_config.MAP_TYPE_NORMAL

		return False

