import py_util
class BodyDataMgr:
	def __init__(self):
		self.bodyData = py_util._readXmlBy2Key('/data/xml/BodyEnhanceData.xml', 'pos', 'level')
		#ʵ�ֲ��