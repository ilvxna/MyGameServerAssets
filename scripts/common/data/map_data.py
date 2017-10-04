import py_util
from KBEDebug import *
#import public_config
from config import public_config
import math
import random

class MapDataMgr:
	def __init__(self):
		#--��ͼ��
		self._map_data = _readXml('/data/xml/map_setting.xml', 'id_i')

		self.randomScene = {}
		for k, v in pairs(self._map_data) do
			if v['isRandom'] and v['isRandom'] == 1 then
--            log_game_debug("MapDataMgr:initData random scene", "k=%d", k)
            self.randomScene[k] = true
--            table.insert(self.randomScene, k)
        end
    end

	