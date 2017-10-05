# -*- coding: utf-8 -*-
import KBEngine
import random
import SCDefine
import copy
import math
from KBEDebug import *
from interfaces.GameObject import GameObject
import d_entities
import d_spaces
import d_spaces_spawns
import xml.etree.ElementTree as etree 

class SpaceLoader(KBEngine.Base, GameObject):
	"""
	һ���ɲٿ�cellapp������space��ʵ��
	ע�⣺����һ��ʵ�壬������������space��������space������cellapp���ڴ��У�ͨ�����ʵ����֮�������ٿ�space��
	"""
	def __init__(self):
		KBEngine.Base.__init__(self)
		GameObject.__init__(self)
		self.createInNewSpace(None)

	def onTimer(self, tid, userArg):
		"""
		KBEngine method.
		����ص�timer����
		"""
		#DEBUG_MSG("%s::onTimer: %i, tid:%i, arg:%i" % (self.getScriptName(), self.id, tid, userArg))
		if SCDefine.TIMER_TYPE_SPACE_SPAWN_TICK == userArg:
			self.spawnOnTimer(tid)
		
		GameObject.onTimer(self, tid, userArg)

	def onGetCell(self):
		"""
		KBEngine method.
		entity��cell����ʵ�屻�����ɹ�
		"""
		DEBUG_MSG("Space::onGetCell: %i" % self.id)
		self.addTimer(0.1, 0.1, SCDefine.TIMER_TYPE_SPACE_SPAWN_TICK)
		KBEngine.globalData["MapMgr"].onSpaceGetCell(self.spaceUTypeB, self, self.spaceKey)
		GameObject.onGetCell(self)
		
		