import py_util
from KBEDebug import *
from collections import ChainMap
class ItemDataMagr:
	def __init__(self):
		#解析装备（武器，穿戴等）
		equipment = py_util._readXml("/data/xml/ItemEquipment.xml", "id_i") 
		#解析宝石
		jewel = py_util._readXml("/data/xml/ItemJewel.xml", "id_i")
		#解析普通道具（礼包或材料等）
		comItems = py_util._readXml("/data/xml/ItemCom.xml", "id_i")
		tbl={}
		it={}
		#合并一起，方便循环遍历
		it=ChainMap(equipment,jewel,comItems)
		#将三种道具解析到一个table中
		for _,v in it.items():
			for tk,tv in v.items():
				if tv[itemType]:
					tbl[tk]=tv
		return tbl
	def initForEquipValues(self):
    #--装备属性表
		ev = py_util._readXml("/data/xml/ItemEquipValues.xml", "id_i") 
		tbl={}
		for k,v in ev.items():
			#构建新key值
			t = str(v[quality]) +str( v[vocation]) +str( v[type]) +str( v[level])
			it={}
			for tk,tv in v.items():
				 if tk != "id"  and tk != "vocation" and tk != "type" and tk != "level" and tk != "quality" :
					 it[tk] = tv
			tbl[t] = it
		return tbl
	def initForJewelValues(self):
		propEffects = lua_util._readXml('/data/xml/PropertyEffect.xml', 'id_i') 
		return self.DataFilter(propEffects)


