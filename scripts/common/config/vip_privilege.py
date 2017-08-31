import py_util
from KBEDebug import *
class vip_privilege:
	def __init__(self):
		self.vipDatas = {}
		cfgDatas = py_util._readXml("/data/xml/privilege.xml", "id_i")
		for k,v in cfgDatas.items():
			rangeSum = v[accumulatedAmount]
			if rangeSum[0] >rangeSum[1]:
				ERROR_MSG("VipCfgData:GetVipLevel:vip config table error:rangeSum data error")
		self.vipDatas = cfgDatas
	#通过等级获取VIP权限配置属性表
	def GetVipPrivileges(self,level):
		if self.vipDatas:
			vt=self.vipDatas[level]
			if vt:
				return vt
	#根据累计充值金额获取当前所属等级
	def GetVipLevel(self,chrgeSum):
		if chrgeSum<0:
			ERROR_MSG("VipCfgData:GetVipLevel chrgeSum %i illegal"% chrgeSum)
		if self.vipDatas==None:
			ERROR_MSG("VipCfgData:GetVipLevel:vip config table error")
		m=0
		for k,v in self.vipDatas.items():
			rangeSum = v[accumulatedAmount]
			if rangeSum and chrgeSum >= rangeSum[0] and chrgeSum <= rangeSum[1] :
				return k
			elif( rangeSum and chrgeSum > rangeSum[2] and k > m ):
				m = k
		return m


