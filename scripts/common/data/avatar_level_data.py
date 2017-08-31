import py_util
class AvatarLevelDataMgr:
	def __init__(self):
		self.data = py_util._readXml("/data/xml/AvatarLevel.xml", "id_i")
	def getCfg(self):
		return self.data
	#取得角色等级的属性效果id
	def GetLevelEffectId(self,level):
    #--重新读取配置计算一级属性
		cfgs = self.data 
		if not cfgs == None :
		 return None
   

		tmpCfgData = cfgs[level]
		if tmpCfgData == None :
			return None
 
		effectId = tmpCfgData['effectId']
		return effectId
	#提供给体力系统
	def GetLevelProps(self,level):
		cfgs = self.data 
		if cfgs == None :
		 return None
   
		tmpCfgData = cfgs[level]
		if tmpCfgData == nil :
			return None
   
		return tmpCfgDat