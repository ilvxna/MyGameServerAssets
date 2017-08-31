import py_util
from KBEDebug import *
class ActivityData:
	def __init__(self):
		self.activityTime = py_util._readXml('/data/xml/ActivityTime.xml', 'weekDay_i')

		self.activities = py_util._readXml('/data/xml/Activity.xml', 'id_i')

		self.activityReward = {}

#--    local tmp = _readXml('/data/xml/ActivityReward.xml', 'id_i')
#--    for _, v in pairs(tmp) do
		self.activityReward = py_util._readXml('/data/xml/ActivityReward.xml', 'id_i')
	def getActivityTime(self,weekday):
		return self.activityTime[weekday] or {}
	def getActivityLevel(self,ActivityId):
		activity = self.activities[ActivityId] or {}
		return activity['level']
	def getActivity(Aself,ctivityId):
		return self.activities[ActivityId]
	#根据波数和玩家等级获取
	def getTowerDefenceReward(self,wave, level):
	 for _, v in self.activityReward.items():
			if v['wave'] == wave and level >= v['level'][0] and level <= v['level'][1] :
				return v
