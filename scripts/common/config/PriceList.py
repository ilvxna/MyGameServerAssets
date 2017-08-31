import py_util
from KBEDebug import *
import public_config
class PriceList:
	#管理物品价格列表
	def __init__(self):
		cfgData = py_util._readXml("/data/xml/PriceList.xml", "id_i")
		self.cfgData = cfgData
		for _,v in self.cfgData.items():
			self.VerifyData(v)

	def VerifyData(self,itemData):
		pass
	#--获取对应类型物品的价格定义
	#--id表示表中物品的索引值
	def GetPriceData(self,idx):
		if self.cfgData:
			return self.cfgData[idx]
	def NeedMoney(self,idx, times):
		cfg=self.cfgData[idx]

		money ={public_config.GOLD_ID:0,public_config.DIAMOND_ID:0}
		if cfg[type]==1:
			#--todo:价格递增
			pass
		elif cfg[type]==2:
			if cfg[currencyType] == 1:
				money[public_config.GOLD_ID] = cfg[priceList][1]
				money[public_config.DIAMOND_ID] = None
			else:
				money[public_config.DIAMOND_ID] = cfg.priceList[1]
				money[public_config.GOLD_ID] = None
		else:
			ERROR_MSG("PriceList:NeedMoney %i, type error."% idx)
		return money
	#按次数计价
	def PriceCheck(self,avatar, idx, times):
		pData = self.GetPriceData(idx)

		if not pData:
			ERROR_MSG("PriceList:PriceCheck idx=%i price data nil"% idx)
		if not times:
			times=1
		if pData[type]==public_config.FIXED_PRICE:
			times=1
		unitPrice = pData[priceList][times]
		if not unitPrice:
			ERROR_MSG("PriceList:PriceCheck idx=%i times=%i priceList error"%(idx, times))
		if pData[currencyType] == public_config.PRICE_GOLD:
			if avatar.gold < unitPrice:
				return False #--金币不足

		elif pData[currencyType] ==public_config.PRICE_DIAMOND:
			if avatar.diamond < unitPrice:
				return False #--钻石不足
		return True

	def DeductCost(avatar, idx, reason, times):
		pData = self.GetPriceData(idx)

		if not pData:
			ERROR_MSG("PriceList:PriceCheck idx=%i price data nil"% idx)
		if not times:
			times=1
		if pData[type]==public_config.FIXED_PRICE:
			times=1
		unitPrice = pData[priceList][times]
		if not unitPrice:
			ERROR_MSG("PriceList:PriceCheck idx=%i times=%i priceList error"%(idx, times))
		if pData[currencyType] == public_config.PRICE_GOLD:
			if avatar.gold >= unitPrice:
				avatar.AddGold(-unitPrice, reason)
				return True #--金币不足

		elif pData[currencyType] ==public_config.PRICE_DIAMOND:
			if avatar.diamond < unitPrice:
				avatar.AddDiamond(-unitPrice, reason)
				return True #--钻石不足
		return False
	#按分钟计价
	def MinitesCostCheck(self,avatar, idx, times, reason):
		pData = self.GetPriceData(idx)
		uPrice = pData[priceList][1]
		if not uPrice:
			ERROR_MSG("PriceList:MinitesCostCheck idx=%i priceList error"% idx)
		if not pData:
			ERROR_MSG("PriceList:PriceCheck idx=%i price data nil"% idx)
		if times<=0:
			ERROR_MSG("PriceList:DeductMinitesCost times=%I error"% times)
		aPrice = uPrice*times 
		unitPrice = pData[priceList][times]
		if not unitPrice:
			ERROR_MSG("PriceList:PriceCheck idx=%i times=%i priceList error"%(idx, times))
		if pData[currencyType] == public_config.PRICE_GOLD:
			if avatar.gold < aPrice:
				return False
				 #--金币不足

		elif pData[currencyType] ==public_config.PRICE_DIAMOND:
			if avatar.diamond < aPrice:
				return False
				 #--钻石不足
		return True
	def DeductMinitesCost(self,avatar, idx, times, reason):
		pData = self.GetPriceData(idx)
		uPrice = pData[priceList][1]
		if not uPrice:
			ERROR_MSG("PriceList:MinitesCostCheck idx=%i priceList error"% idx)
		if not pData:
			ERROR_MSG("PriceList:PriceCheck idx=%i price data nil"% idx)
		if times<=0:
			ERROR_MSG("PriceList:DeductMinitesCost times=%I error"% times)
		aPrice = uPrice*times 
		unitPrice = pData[priceList][times]
		if not unitPrice:
			ERROR_MSG("PriceList:PriceCheck idx=%i times=%i priceList error"%(idx, times))
		if pData[currencyType] == public_config.PRICE_GOLD:
			if avatar.gold >= aPrice:
				avatar.AddGold(-aPrice, reason)
				return True #--金币不足
				 #--金币不足

		elif pData[currencyType] ==public_config.PRICE_DIAMOND:
			if avatar.diamond >= aPrice:
				avatar.AddDiamond(-aPrice, reason)
				return True #--钻石不足
		return False




