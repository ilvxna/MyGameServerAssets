from KBEDebug import *
import py_util
CommonXmlConfig = dict(

    EFFECT_PASSIVE_PROPERTY_DATA = {}, #--永久性的属性提升数据
    EFFECT_PASSIVE_SKILL_DATA = {},    #--被动技能影响
)
class CommonXmlConfig_class:
	def __init__(self):
		propEffectData =py_util. _readXml('/data/xml/PropertyEffect.xml', 'id_i')
		self.EFFECT_PASSIVE_PROPERTY_DATA = propEffectData
		passiveSkillData =py_util._readXml('/data/xml/PassiveSkillEffect.xml', 'id_i')
		self.EFFECT_PASSIVE_SKILL_DATA = passiveSkillData
	def GetPassivePropertyEffect(self, effectId ):
		tmp = {}
		if effectId and self.EFFECT_PASSIVE_PROPERTY_DATA[effectId] :
			for key, val in self.EFFECT_PASSIVE_PROPERTY_DATA[effectId].items() :
				if val != 0 :
					tmp[key] = val
	def GetPassiveSkillEffect( self,effectId ):
		return self.EFFECT_PASSIVE_SKILL_DATA[effectId]