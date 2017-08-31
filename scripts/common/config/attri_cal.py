import public_config
import py_util
from KBEDebug import *
import error_code

#--道具配置属性索引
ITEM_TYPE_CONFIGURE      = public_config.ITEM_TYPE_CFG_TBL
ITEM_TYPE_ATTRI          = public_config.ITEM_TYPE_EQUIPMENTATTRI
ITEM_TYPE_SUIT           = public_config.ITEM_TYPE_SUITEQUIPMENT
ITEM_TYPE_JEWELATTRI     = public_config.ITEM_TYPE_JEWELATTRI
ITEM_QUALITY_GOLD        = public_config.ITEM_QUALITY_GOLD
AVATAR_ALL_VOC           = public_config.AVATAR_ALL_VOC
#--公式参数索引
PROP_RATE_DEFENCE        = public_config.PROP_RATE_DEFENCE          
PROP_RATE_CRIT           = public_config.PROP_RATE_CRIT             
PROP_RATE_TRUESTRIKE     = public_config.PROP_RATE_TRUESTRIKE       
PROP_RATE_ANTIDEFENSE    = public_config.PROP_RATE_ANTIDEFENSE      
PROP_RATE_PVPADDITION    = public_config.PROP_RATE_PVPADDITION     
PROP_RATE_PVPANTI        = public_config.PROP_RATE_PVPANTI
PROP_RATE_ANTICRITRATE   = public_config.PROP_RATE_ANTICRITRATE   #--抗暴
PROP_RATE_ANTITSTKRATE   = public_config.PROP_RATE_ANTITSTKRATE   #--抗破
#--
INSTANCE_GRIDINDEX       = public_config.ITEM_INSTANCE_GRIDINDEX  #--背包索引
INSTANCE_TYPEID          = public_config.ITEM_INSTANCE_TYPEID     #--道具id
INSTANCE_SLOTS           = public_config.ITEM_INSTANCE_SLOTS      #--宝石插槽
ITEM_INSTANCE_EXTINFO    = public_config.ITEM_INSTANCE_EXTINFO    #--扩展信息

ITEM_ACTIVED_OK          = public_config.ITEM_ACTIVED_OK          #--已激活
ITEM_ACTIVED_NO          = public_config.ITEM_ACTIVED_NO          #--没有激活
ITEM_EXTINFO_ACTIVE      = public_config.ITEM_EXTINFO_ACTIVE      #--道具激活标识

class PropsSystem:
	def GetFightForce(self,baseProps):
		pass
