import py_util
from KBEDebug import *
class FormularMgr:
	#读取配置数据
	def __init__(self):
		cfgDatas = py_util._readXml("/data/xml/FormulaParameters.xml", "id_i")
		if cfgDatas:
			self.cfgdatas = cfgDatas or {}
	#取得二级属性计算公式所需参数
	def GetFormulaCfg(self,propType):
		if not self.cfgdatas:
			ERROR_MSG("FormularMgr:GetFormulaCfg:cfg nil")
		paras=self.cfgdatas[propType]
		return paras


