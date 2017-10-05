# -*- coding: utf-8 -*-
import py_util
from config import error_code
from map_data import MapDataMgr
from interfaces.GameObject import GameObject
from config import public_config
import KBEngine
from KBEDebug import *
import Functor
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
	'''
	相当于原demo中的spaces
	'''
	def _init_(self):
		INFO_MSG('MapMgr:__init__')

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

#		#记录每一个场景各个分线的总人数
#		self.ScenePlayerCount = {}

		#初始化各个场景对应的分线信息
		MapData = g_map_mgr.getMapData()

		for sceneId, _ in MapData:

			self.SpaceLoaderCount[sceneId] = {}

			self.BusySpecialMapPool[sceneId] = {}

		KBEngine.globalData["MapMgr"] = self

	#加载所有场景管理器
	def LoadAllSpace(self):
		INFO_MSG('Map::LoadAllSpace ')

		#默认创建5000个地图map_id为空的spaceloader
		for i in range(_INIT_MAP_COUNT):
			spaceKey = KBEngine.genUUID64()
			KBEngine.createBaseAnywhere("SpaceLoader", {'map_id':'',"spaceKey" : spaceKey,},
							   Functor.Functor(self.onMapLoaded, spaceKey))

		self.MapCount = _INIT_MAP_COUNT

		#一个地图加载完成之后的回调方法
	def onMapLoaded(self,spaceKey, SpaceLoaderBaseMb):
		"""
		defined method.
		SpaceLoader的cell创建好了
		"""
		
		loaded_count = self.MapLoadedCount + 1

		all_count = self.MapCount

		self.MapLoadedCount = loaded_count

		self.MapPool[SpaceLoaderBaseMb.id]=SpaceLoaderBaseMb

		self.IdleSpecialMapPool[SpaceLoaderBaseMb.id]=1

		if loaded_count==all_count:

			self.State=_STATE_MAP_LOADED

			INFO_MSG('Map::onMapLoaded:spaceID:%i '%SpaceLoaderBaseMb.id)

			#通知MapMgr加载完毕,Avatar加载完毕之后由UserMgr通知
			KBEngine.globalData["GameMgr"].OnMgrLoaded('MapMgr')

	def ChangeMapCount(self,flag, scene, line, count):
		pass

	#从空闲副本池获取一个分线，返回值是spaceloader的base mailbox
	def GetIdleMap(self,targetSceneId,targetLine):

		for k,v in self.IdleSpecialMapPool:

			self.BusySpecialMapPool[targetSceneId]=self.BusySpecialMapPool[targetSceneId] or {}

			#targetLine 不存在时
			if self.BusySpecialMapPool[targetSceneId].get(targetLine,0)==0 :

				DEBUG_MSG("MapMgr:GetAIdleMap:targetSceneId=%i;targetLine=%i"% ( targetSceneId, targetLine))

				return self.MapPool[self.BusySpecialMapPool[targetSceneId][targetLine]]
			else:
				self.BusySpecialMapPool[targetSceneId][targetLine] = k

				self.IdleSpecialMapPool[k] = None

				return self.MapPool[k]
		
		return None

	#返回当前Space mailbox的base mailbox
	def GetSpaceLoaderMb(self,sceneId,line):

		mbs=self.BusySpecialMapPool[sceneId] or {}

		entityId=mbs[line]

		if entityId:
			return self.MapPool[entityId]
		else:
			DEBUG_MSG("MapMgr:GetSpaceLoaderMb:sceneId=%i;line=%i"%( sceneId, line))


	#获取空闲副本的数量，用于判断是否需要新建副本
	def GetIdleMapCount(self):
		i=0
		for k,v in self.IdleSpecialMapPool:
			i=i+1
		return i

	#扩展空闲的地图
	def ExtendIdleMap(self):
		if self.State==_STATE_MAP_LOADING:
			return

		IdleMapCount=self.GetIdleMapCount()

		if IdleMapCount<=_INIT_MAP_COUNT*0.2:
			#当当前空闲分线的数量小于等于原空闲分线副本数量的80%时，开始新创建分线
			for i in range(_EXTEND_MAP_COUNT):

				spaceKey = KBEngine.genUUID64()

			KBEngine.createBaseAnywhere("SpaceLoader", {'map_id':'',"spaceKey" : spaceKey,},
							   Functor.Functor(self.onMapLoaded, spaceKey))

			self.State=_STATE_MAP_LOADING

			self.MapCount=self.MapCount+_EXTEND_MAP_COUNT

			DEBUG_MSG("MapMgr:ExtendIdleMap:self.MapCount=%i"% self.MapCount)

	def SelectMap(self,Mailbox,map_id,line,dbid,name,params):

		mapInfo=g_map_mgr.getMapCfgData(map_id)

		INFO_MSG("MapMgr:SelectMapReq:map_id=%i;line=%i;dbid=%i;name=%s;params=%s"%(map_id, line, dbid, name, params))

		if Mailbox and mapInfo:
			if mapInfo['type'] == public_config.MAP_TYPE_NORMAL or mapInfo['type'] == public_config.MAP_TYPE_MUTI_PLAYER_NOT_TEAM :

           # #如果玩家进入一个普通地图，则需要选择一个分线，选择分线本身不会触发新创建分线
				MapCount = self.SpaceLoaderCount[map_id]
				if MapCount :
					MaxLine = 0    #现在的最大分线数

					for imap, count in enumerate(MapCount):

						if imap > MaxLine:
							MaxLine = imap

                  #找到一条分线，则分配该分线号
						if count < mapInfo['maxPlayerNum']:

                       #成功进入一条分线
							spaceLoaderMbs = self.GetSpaceLoaderMb(map_id, imap)
							'''
							
    <SelectMapResp>
      <Arg> UINT16 </Arg>    <!# 玩家的实际地图ID #>
      <Arg> UINT16 </Arg>    <!# 玩家的实际地图分线ID #>
      <Arg> LUA_TABLE </Arg> <!# 选中的sp的base的mb #>
      <Arg> LUA_TABLE </Arg> <!# 选中的sp的cell的mb #> #将来需要将cell的mailbox参数删除
      <Arg> UINT64 </Arg>    <!# 玩家的dbid #>
      <Arg> LUA_TABLE </Arg> <!# 玩家选择分线时穿进来的参数，此时再返回给他 #>
    </SelectMapResp>

							'''
							Mailbox.SelectMapResp(map_id, imap, spaceLoaderMbs, dbid, params)


							DEBUG_MSG("MapMgr:SelectMapReq: 1:map_id=%i;imap=%i;dbid=%i;name=%s;count=%i"%( map_id, imap, dbid, name, self.SpaceLoaderCount[map_id][imap]))

							return
					else:
						DEBUG_MSG("MapMgr:SelectMapReq full:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])
					
					TargetLine=1
					for i in range(MaxLine+1):
						if not MapCount[i]:
							TargetLine=i

				#该地图的所有分线都已经不可进入，则从空闲分线池里面拿一个出来
					sp=self.GetIdleMap(map_id,TargetLine)
				#sp即为spaceLoader的base mailbox
					if sp:

						sp.SetMapId(mbStr, targetSceneId, TargetLine, dbid, name, params)

						DEBUG_MSG("MapMgr:SelectMapReq: 2:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

					#判断是否需要创建space
						self.ExtendIdleMap()
					else:

					#无法找到可进入副本分线
						ERROR_MSG("MapMgr:SelectMapReq -1:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

				else:
					#无法找到可进入副本分线
					ERROR_MSG("MapMgr:SelectMapReq -2:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])
			
			#守护PvP地图选
		elif mapInfo['type'] == public_config.MAP_TYPE_DEFENSE_PVP :

            ##先从已经创建的分线中选择分线
				spaceLoaderData = self.SpaceLoaderCount[map_id]

				if spaceLoaderData:

					gameID = line

					if spaceLoaderData[gameID]:

                   #关卡分线已存在，切入地图
						spaceLoaderMbs = self.GetSpaceLoaderMb(map_id, gameID)

						Mailbox.SelectMapResp(map_id, gameID, spaceLoaderMbs, dbid, params)
					return

            #无法找到可进入副本分线
				ERROR_MSG("MapMgr:SelectMapReq defense_pvp:map_id=%i;line=%i;dbid=%i;name=%s"%( map_id, line, dbid, name))

		#世界boss分线选择
		elif mapInfo['type'] == public_config.MAP_TYPE_WB :
            #先从已经创建的分线中选择分线
			MapCount = self.SpaceLoaderCount[map_id]
			MaxLine = 0

			if MapCount :
				for _line, _count in enumerate(MapCount) :
					if _count < mapInfo['maxPlayerNum']:
						targetMapPool = self.BusySpecialMapPool[map_id]

						if targetMapPool:
							sp = targetMapPool[_line]
							if sp :
                                #到指定的副本检查是否允许进入

								DEBUG_MSG("MapMgr:SelectMapReq 1:map_id=%i;line=%i;dbid=%i;name=%s"%( map_id, _line, dbid, name))

								KBEngine.globalData["WorldBossMgr"].CheckEnter( mbStr, map_id, _line, dbid, name)
								return
							else:
								ERROR_MSG("MapMgr:SelectMapReq:have count data but BusySpecialMapPool data.[%i][%i]"%( map_id, _line))
						
						else:
							ERROR_MSG("MapMgr:SelectMapReq:have count data but BusySpecialMapPool data.[%i][%i]"%( map_id, _line))


					if _line > MaxLine : MaxLine = _line 

					else:
						self.SpaceLoaderCount[map_id] = {}

			TargetLine = MaxLine + 1


		else:
			if line==0:
				#如果分线号为0，表示玩家想进入一个新副本
				MapCount=self.SpaceLoaderCount[map_id]
				if MapCount:
					Maxline=0 #现在最大的分线数

					for imap,count in enumerate(MapCount):
						if imap>MaxLine:
							Maxline=imap

					
					TargetLine=1
					for i in range(MaxLine+1):
						if not MapCount[i]:
							TargetLine=i


					#该地图的所有分线都已经不可进入，则从空闲分线池里面拿一个出来
					sp=self.GetIdleMap(map_id,TargetLine)
				#sp即为spaceLoader的base mailbox
					if sp:

						sp.SetMapId(mbStr, targetSceneId, TargetLine, dbid, name, params)

						DEBUG_MSG("MapMgr:SelectMapReq: 2:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

					#判断是否需要创建space
						self.ExtendIdleMap()
					else:

					#无法找到可进入副本分线
						ERROR_MSG("MapMgr:SelectMapReq -1:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

				else:
					#无法找到可进入副本分线
					ERROR_MSG("MapMgr:SelectMapReq -2:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])


			elif line>0:

				targetMapPool=self.BusySpecialMapPool[map_id]
				
				if targetMapPool:

					spaceLoaderMb=targetMapPool[line]

					if spaceLoaderMb:

						#到指定的副本检查是否允许进入
						spaceLoaderMb.CheckEnter(Mailbox, dbid, name)

				#该角色想要进入的场景分线已经不存在了，直接把玩家送回王城
				#todo 硬编码 王城是10004
				targetSceneId=10004

				mapInfo=g_map_mgr.getMapCfgData(targetSceneId)

				MapCount = self.SpaceLoaderCount[targetSceneId]

				if MapCount:
					Maxline=0 #现在最大的分线数

					for imap,count in enumerate(MapCount):
						if imap>MaxLine:
							Maxline=imap

					#找到一条分线，则分配该分线号

					if count< mapInfo['maxPlayerNum']:

							#成功进入一条分线
						spaceLoaderMbs = self.GetSpaceLoaderMb(targetSceneId, imap)
						Mailbox.SelectMapResp(map_id, imap, spaceLoaderMbs, dbid, params)


						DEBUG_MSG("MapMgr:SelectMapReq: 6:map_id=%i;imap=%i;dbid=%i;name=%s;count=%i"%( map_id, imap, dbid, name, self.SpaceLoaderCount[map_id][imap]))

					
					TargetLine=1
					for i in range(MaxLine+1):
						if not MapCount[i]:
							TargetLine=i

					
			#todo 考虑将重复代码函数化 该地图的所有分线都已经不可进入，则从空闲分线池里面拿一个出来
					sp=self.GetIdleMap(map_id,TargetLine)
				#sp即为spaceLoader的base mailbox
					if sp:

						sp.SetMapId(mbStr, targetSceneId, TargetLine, dbid, name, params)

						DEBUG_MSG("MapMgr:SelectMapReq: 2:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

					#判断是否需要创建space
						self.ExtendIdleMap()
					else:

					#无法找到可进入副本分线
						ERROR_MSG("MapMgr:SelectMapReq -1:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

				else:
					#无法找到可进入副本分线
					ERROR_MSG("MapMgr:SelectMapReq -2:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

	def CheckEnterResp(self,result,playerMb,map_id,line,dbid,name):

		if playerMb:
			if result<0:

				#该已打开的副本不属于该玩家，则需要把玩家传送到王城
				if g_map_mgr.IsWBMap(map_id):
					#如果是世界boss的场景跳转失败需要通知worldbossmgr

					playerMb.SelectMapFailResp(map_id, line)

				spaceLoaderMbs = self.GetSpaceLoaderMb(map_id, line)

				playerMb.SelectMapResp(10004, 1, spaceLoaderMbs,  dbid, {})

			else:
				#该打开的副本属于该玩家，则玩家重新进入副本
				spaceLoaderMbs = self.GetSpaceLoaderMb(map_id, line)

				playerMb.SelectMapResp(map_id, line, spaceLoaderMbs,  dbid, {})





				





