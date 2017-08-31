import py_util
from KBEDebug import *
class HpBottleType:
	#血瓶类型初始化
	def __init__(self):
		cfgData = py_util._readXml('/data/xml/HpTypes.xml', 'id_i')
		self.cfgData = cfgData
	#根据血瓶的类型索引获取血瓶的数值
	def GetBottleData(self,idx):
		if self.cfgData:
			return self.cfgData[idx]