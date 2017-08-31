import py_util
from KBEDebug import *
class spiritData:
	def __init__(self):
		SkillLevelUpData = py_util._readXml("/data/xml/SpiritLevelData_Skill.xml", "id_i")
		MarkLevelUpData = py_util._readXml("/data/xml/SpiritLevelData_Mark.xml", "id_i")
		SkillData = py_util._readXml("/data/xml/SpiritSkillData.xml", "id_i")
		MarkData = py_util._readXml("/data/xml/SpiritMarkData.xml", "id_i")
		self.spiritData = {}
		self.spiritData['SkillLevelUpData'] = SkillLevelUpData
		self.spiritData['MarkLevelUpData'] = MarkLevelUpData
		self.spiritData['SkillData'] = SkillData
		self.spiritData['MarkData'] = MarkData
	def GetPointFromId(self,id):
		if self.spiritData["SkillData"][id] :
			return self.spiritData['SkillData'][id]['add_point']

	def  GetCostByLevel_Skill(self,level):
		if self.spiritData["SkillLevelUpData"][level] :
			return self.spiritData['SkillLevelUpData'][level]['cost']

	def  GetCostByLevel_Mark(self,level):
		if self.spiritData["MarkLevelUpData"][level] :
			return self.spiritData['MarkLevelUpData'][level]['cost']
	def GetSlotNum_Skill(self,level):
		data=self.spiritData['SkillLevelUpData'][level]
		if data:
			return data['slot_num']

	def GetSlotNum_Markl(self,level):
		data=self.spiritData['SkillLevelUpData'][level]
		if data:
			return data['slot_num']

