import py_util
from KBEDebug import *
class arenic_data:
	def __init__(self):
		self.cfgData== py_util._readXml('/data/xml/ArenaLevel.xml', 'id_i')
		
	def GetPropEffect(self,grade):
		if self.cfgData:
			if self.cfgData[grade]:
				return self.cfgData[grade][propEffect]
			else:
				ERROR_MSG("arenic_data::GetPropEffect:self.cfgData[%i] not exist"%(grade))

def GetCredit(self,grade):
		if self.cfgData:
			if self.cfgData[grade]:
				return self.cfgData[grade][credit]
			else:
				ERROR_MSG("arenic_data::GetCredit:self.cfgData[%i] not exist"%(grade))
