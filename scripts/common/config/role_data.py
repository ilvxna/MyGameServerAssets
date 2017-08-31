import py_util
import KBEDebug
class role_data:
	def __init__(self):
		self.role_data = py_util._readXml("/data/xml/role_data.xml", "vocation_i")

	def GetRoleDataByVocation(self,vocation):
		if self.role_data:
			return self.role_data[vocation]
