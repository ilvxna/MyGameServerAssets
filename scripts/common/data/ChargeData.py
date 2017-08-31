import py_util
from KBEDebug import *
import time
class ChargeData:
	#��ȡ��������
	def __init__(self):
		#ʱ���ǻ����
		self.diamond_mine = py_util._readXml('/data/xml/DiamondMine.xml', 'id_i')
	def GetMineCfg(self):
		t=time.time()
		for id,v in self.diamond_mine.items():
			if t > v[date_open] and t < v[date_end]:
				return v
	def MineCost(self,t):
		cfg = self.GetMineCfg()
		if cfg :
			return cfg[cost][t]
	def MineReward(self,t):
		cfg = self.GetMineCfg()
		if cfg :
			return cfg[reward][t]
	def MineVip(self,t):
		cfg = self.GetMineCfg()
		if cfg:
			vip = cfg[vip_need][t]
		if vip :
			return vip
		else:
			#--������������vip�ȼ�
				m = cfg[vip_need].__len__()
				return cfg[vip_need][m]
#�Ƿ���ȡ�����
	def IfMax(self,t):
		m = 0
		cfg = self.GetMineCfg()
		if cfg :
			for k,v in cfg[cost] :
				if m < k :
					m = k
		
			return m < t

		return true