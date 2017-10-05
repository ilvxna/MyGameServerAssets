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

_STATE_INIT            = 0      #��ʼ״̬
_STATE_MAP_LOADED      = 1      #���е�ͼ�������
_STATE_CITIES_LOADED   = 2      #������ҳ��м������
_STATE_MAP_LOADING     = 3      #���ڼ��ص�ͼ


_TIMER_ID_24_CLOCK = 11      #ÿ��0���timer
_TIMER_ID_EVERY_HOUR = 12    #ÿ��Сʱһ�ε�timer

_INIT_MAP_COUNT = 2000    #��ʼ�����Ŀյ�spaceloader����

_EXTEND_MAP_COUNT = 1    #ÿ����չ����ʱ��Ҫ�����ķ���


class MapMgr(KBEngine.Base,GameObject):
	'''
	�൱��ԭdemo�е�spaces
	'''
	def _init_(self):
		INFO_MSG('MapMgr:__init__')

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

#		#��¼ÿһ�������������ߵ�������
#		self.ScenePlayerCount = {}

		#��ʼ������������Ӧ�ķ�����Ϣ
		MapData = g_map_mgr.getMapData()

		for sceneId, _ in MapData:

			self.SpaceLoaderCount[sceneId] = {}

			self.BusySpecialMapPool[sceneId] = {}

		KBEngine.globalData["MapMgr"] = self

	#�������г���������
	def LoadAllSpace(self):
		INFO_MSG('Map::LoadAllSpace ')

		#Ĭ�ϴ���5000����ͼmap_idΪ�յ�spaceloader
		for i in range(_INIT_MAP_COUNT):
			spaceKey = KBEngine.genUUID64()
			KBEngine.createBaseAnywhere("SpaceLoader", {'map_id':'',"spaceKey" : spaceKey,},
							   Functor.Functor(self.onMapLoaded, spaceKey))

		self.MapCount = _INIT_MAP_COUNT

		#һ����ͼ�������֮��Ļص�����
	def onMapLoaded(self,spaceKey, SpaceLoaderBaseMb):
		"""
		defined method.
		SpaceLoader��cell��������
		"""
		
		loaded_count = self.MapLoadedCount + 1

		all_count = self.MapCount

		self.MapLoadedCount = loaded_count

		self.MapPool[SpaceLoaderBaseMb.id]=SpaceLoaderBaseMb

		self.IdleSpecialMapPool[SpaceLoaderBaseMb.id]=1

		if loaded_count==all_count:

			self.State=_STATE_MAP_LOADED

			INFO_MSG('Map::onMapLoaded:spaceID:%i '%SpaceLoaderBaseMb.id)

			#֪ͨMapMgr�������,Avatar�������֮����UserMgr֪ͨ
			KBEngine.globalData["GameMgr"].OnMgrLoaded('MapMgr')

	def ChangeMapCount(self,flag, scene, line, count):
		pass

	#�ӿ��и����ػ�ȡһ�����ߣ�����ֵ��spaceloader��base mailbox
	def GetIdleMap(self,targetSceneId,targetLine):

		for k,v in self.IdleSpecialMapPool:

			self.BusySpecialMapPool[targetSceneId]=self.BusySpecialMapPool[targetSceneId] or {}

			#targetLine ������ʱ
			if self.BusySpecialMapPool[targetSceneId].get(targetLine,0)==0 :

				DEBUG_MSG("MapMgr:GetAIdleMap:targetSceneId=%i;targetLine=%i"% ( targetSceneId, targetLine))

				return self.MapPool[self.BusySpecialMapPool[targetSceneId][targetLine]]
			else:
				self.BusySpecialMapPool[targetSceneId][targetLine] = k

				self.IdleSpecialMapPool[k] = None

				return self.MapPool[k]
		
		return None

	#���ص�ǰSpace mailbox��base mailbox
	def GetSpaceLoaderMb(self,sceneId,line):

		mbs=self.BusySpecialMapPool[sceneId] or {}

		entityId=mbs[line]

		if entityId:
			return self.MapPool[entityId]
		else:
			DEBUG_MSG("MapMgr:GetSpaceLoaderMb:sceneId=%i;line=%i"%( sceneId, line))


	#��ȡ���и����������������ж��Ƿ���Ҫ�½�����
	def GetIdleMapCount(self):
		i=0
		for k,v in self.IdleSpecialMapPool:
			i=i+1
		return i

	#��չ���еĵ�ͼ
	def ExtendIdleMap(self):
		if self.State==_STATE_MAP_LOADING:
			return

		IdleMapCount=self.GetIdleMapCount()

		if IdleMapCount<=_INIT_MAP_COUNT*0.2:
			#����ǰ���з��ߵ�����С�ڵ���ԭ���з��߸���������80%ʱ����ʼ�´�������
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

           # #�����ҽ���һ����ͨ��ͼ������Ҫѡ��һ�����ߣ�ѡ����߱����ᴥ���´�������
				MapCount = self.SpaceLoaderCount[map_id]
				if MapCount :
					MaxLine = 0    #���ڵ���������

					for imap, count in enumerate(MapCount):

						if imap > MaxLine:
							MaxLine = imap

                  #�ҵ�һ�����ߣ������÷��ߺ�
						if count < mapInfo['maxPlayerNum']:

                       #�ɹ�����һ������
							spaceLoaderMbs = self.GetSpaceLoaderMb(map_id, imap)
							'''
							
    <SelectMapResp>
      <Arg> UINT16 </Arg>    <!# ��ҵ�ʵ�ʵ�ͼID #>
      <Arg> UINT16 </Arg>    <!# ��ҵ�ʵ�ʵ�ͼ����ID #>
      <Arg> LUA_TABLE </Arg> <!# ѡ�е�sp��base��mb #>
      <Arg> LUA_TABLE </Arg> <!# ѡ�е�sp��cell��mb #> #������Ҫ��cell��mailbox����ɾ��
      <Arg> UINT64 </Arg>    <!# ��ҵ�dbid #>
      <Arg> LUA_TABLE </Arg> <!# ���ѡ�����ʱ�������Ĳ�������ʱ�ٷ��ظ��� #>
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

				#�õ�ͼ�����з��߶��Ѿ����ɽ��룬��ӿ��з��߳�������һ������
					sp=self.GetIdleMap(map_id,TargetLine)
				#sp��ΪspaceLoader��base mailbox
					if sp:

						sp.SetMapId(mbStr, targetSceneId, TargetLine, dbid, name, params)

						DEBUG_MSG("MapMgr:SelectMapReq: 2:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

					#�ж��Ƿ���Ҫ����space
						self.ExtendIdleMap()
					else:

					#�޷��ҵ��ɽ��븱������
						ERROR_MSG("MapMgr:SelectMapReq -1:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

				else:
					#�޷��ҵ��ɽ��븱������
					ERROR_MSG("MapMgr:SelectMapReq -2:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])
			
			#�ػ�PvP��ͼѡ
		elif mapInfo['type'] == public_config.MAP_TYPE_DEFENSE_PVP :

            ##�ȴ��Ѿ������ķ�����ѡ�����
				spaceLoaderData = self.SpaceLoaderCount[map_id]

				if spaceLoaderData:

					gameID = line

					if spaceLoaderData[gameID]:

                   #�ؿ������Ѵ��ڣ������ͼ
						spaceLoaderMbs = self.GetSpaceLoaderMb(map_id, gameID)

						Mailbox.SelectMapResp(map_id, gameID, spaceLoaderMbs, dbid, params)
					return

            #�޷��ҵ��ɽ��븱������
				ERROR_MSG("MapMgr:SelectMapReq defense_pvp:map_id=%i;line=%i;dbid=%i;name=%s"%( map_id, line, dbid, name))

		#����boss����ѡ��
		elif mapInfo['type'] == public_config.MAP_TYPE_WB :
            #�ȴ��Ѿ������ķ�����ѡ�����
			MapCount = self.SpaceLoaderCount[map_id]
			MaxLine = 0

			if MapCount :
				for _line, _count in enumerate(MapCount) :
					if _count < mapInfo['maxPlayerNum']:
						targetMapPool = self.BusySpecialMapPool[map_id]

						if targetMapPool:
							sp = targetMapPool[_line]
							if sp :
                                #��ָ���ĸ�������Ƿ��������

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
				#������ߺ�Ϊ0����ʾ��������һ���¸���
				MapCount=self.SpaceLoaderCount[map_id]
				if MapCount:
					Maxline=0 #�������ķ�����

					for imap,count in enumerate(MapCount):
						if imap>MaxLine:
							Maxline=imap

					
					TargetLine=1
					for i in range(MaxLine+1):
						if not MapCount[i]:
							TargetLine=i


					#�õ�ͼ�����з��߶��Ѿ����ɽ��룬��ӿ��з��߳�������һ������
					sp=self.GetIdleMap(map_id,TargetLine)
				#sp��ΪspaceLoader��base mailbox
					if sp:

						sp.SetMapId(mbStr, targetSceneId, TargetLine, dbid, name, params)

						DEBUG_MSG("MapMgr:SelectMapReq: 2:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

					#�ж��Ƿ���Ҫ����space
						self.ExtendIdleMap()
					else:

					#�޷��ҵ��ɽ��븱������
						ERROR_MSG("MapMgr:SelectMapReq -1:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

				else:
					#�޷��ҵ��ɽ��븱������
					ERROR_MSG("MapMgr:SelectMapReq -2:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])


			elif line>0:

				targetMapPool=self.BusySpecialMapPool[map_id]
				
				if targetMapPool:

					spaceLoaderMb=targetMapPool[line]

					if spaceLoaderMb:

						#��ָ���ĸ�������Ƿ��������
						spaceLoaderMb.CheckEnter(Mailbox, dbid, name)

				#�ý�ɫ��Ҫ����ĳ��������Ѿ��������ˣ�ֱ�Ӱ�����ͻ�����
				#todo Ӳ���� ������10004
				targetSceneId=10004

				mapInfo=g_map_mgr.getMapCfgData(targetSceneId)

				MapCount = self.SpaceLoaderCount[targetSceneId]

				if MapCount:
					Maxline=0 #�������ķ�����

					for imap,count in enumerate(MapCount):
						if imap>MaxLine:
							Maxline=imap

					#�ҵ�һ�����ߣ������÷��ߺ�

					if count< mapInfo['maxPlayerNum']:

							#�ɹ�����һ������
						spaceLoaderMbs = self.GetSpaceLoaderMb(targetSceneId, imap)
						Mailbox.SelectMapResp(map_id, imap, spaceLoaderMbs, dbid, params)


						DEBUG_MSG("MapMgr:SelectMapReq: 6:map_id=%i;imap=%i;dbid=%i;name=%s;count=%i"%( map_id, imap, dbid, name, self.SpaceLoaderCount[map_id][imap]))

					
					TargetLine=1
					for i in range(MaxLine+1):
						if not MapCount[i]:
							TargetLine=i

					
			#todo ���ǽ��ظ����뺯���� �õ�ͼ�����з��߶��Ѿ����ɽ��룬��ӿ��з��߳�������һ������
					sp=self.GetIdleMap(map_id,TargetLine)
				#sp��ΪspaceLoader��base mailbox
					if sp:

						sp.SetMapId(mbStr, targetSceneId, TargetLine, dbid, name, params)

						DEBUG_MSG("MapMgr:SelectMapReq: 2:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

					#�ж��Ƿ���Ҫ����space
						self.ExtendIdleMap()
					else:

					#�޷��ҵ��ɽ��븱������
						ERROR_MSG("MapMgr:SelectMapReq -1:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

				else:
					#�޷��ҵ��ɽ��븱������
					ERROR_MSG("MapMgr:SelectMapReq -2:map_id=%i;imap=%i;count=%i;maxPlayerNum=%i", map_id, imap, count, mapInfo['maxPlayerNum'])

	def CheckEnterResp(self,result,playerMb,map_id,line,dbid,name):

		if playerMb:
			if result<0:

				#���Ѵ򿪵ĸ��������ڸ���ң�����Ҫ����Ҵ��͵�����
				if g_map_mgr.IsWBMap(map_id):
					#���������boss�ĳ�����תʧ����Ҫ֪ͨworldbossmgr

					playerMb.SelectMapFailResp(map_id, line)

				spaceLoaderMbs = self.GetSpaceLoaderMb(map_id, line)

				playerMb.SelectMapResp(10004, 1, spaceLoaderMbs,  dbid, {})

			else:
				#�ô򿪵ĸ������ڸ���ң���������½��븱��
				spaceLoaderMbs = self.GetSpaceLoaderMb(map_id, line)

				playerMb.SelectMapResp(map_id, line, spaceLoaderMbs,  dbid, {})





				





