from KBEDebug import *
import py_util
class npcData:
	def __init__(self):
		cfgData = py_util._readXml('/data/xml/NPCData.xml', 'id_i')
		self.cfgData = cfgData
	def GetNPCDataById(self,id):
		if self.cfgData:
			return self.cfgData[id]