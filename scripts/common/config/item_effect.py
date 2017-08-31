import py_util
from KBEDebug import *
import random
class item_effect:
	#初始化道具配置效果配置表
	def __init__(self):
		ieffect = py_util._readXml("/data/xml/ItemEffect.xml", "id_i")
		self.EData = ieffect
	#根据效果tbl，通过随机值获取对应的奖励
	def GetReward(self,itb) :
		prob=[]
		if random.randint(1,itb)==None:
			ERROR_MSG("ItemEffect:GetReward:random data error")
		for k,v in enumerate(random.randint(1,itb)):
			prob.append(v/100)
		rtn = py_util.choice(prob)
		if rtn==1:
			return itb[reward1]
		elif rtn==2:
			return itb[reward2]
		elif rtn==3:
			return itb[reward3]
	#根据效果eId获取对应的配置项
	def GetEffect(self,eId):
		itbl = self.EData[eId]
		if itbl==None:
			ERROR_MSG("ItemEffect:GetEffect:effect id = %i error"%eId)
		return itbl

