arenicDataKey=dict(
    #-->begin:arenaSystem m_systemData ��key
    tmp_scoresOfDay = 1,
    tmp_rewardOfDay  = 2,
    tmp_scoresOfWeek = 3,
    tmp_rewardOfWeek = 4,
    tmp_challengeTimes = 5,
    tmp_weakFoes = 6,
    #--tmp_theWeakFoe = 7,
    tmp_strongFoes = 8,
    #--tmp_theStrongFoe = 9,
    tmp_theEnemy = 10,
    tmp_beatEnemy = 11,
    tmp_weakFoesRange = 12,
    tmp_strongFoesRange = 13,
    tmp_dayLevel = 14,
    tmp_weekLevel = 15,
    #--<end


    #-->begin: avatar arenicData ��key
    avatar_cdEndTime = 1,
    avatar_buyTimes = 2,
    #--avatar_bufAtk = 3,
    #--avatar_bufHp = 4,
    avatar_weak = 5,
    avatar_strong = 6,
    avatar_inspire_buf = 7,
    avatar_weakRange = 8,
    avatar_strongRange = 9,
    avatar_DailyBuys = 10, #--���칺�����
    avatar_DailyBuyCd = 11, #--�´��幺�����cd
    #--<end
)

arena_text_id = dict(
	NO_MONEY = 25000,
	CLEAR_CD_NO_NEED = 25001,
	CLEAR_CD_SUC = 25002,
	BUY_ARENA_TIME_SUC = 25003,
	SCORS_REWARD_RECV_ED = 25004,
	SCORS_REWARD_RECV_SUC = 25005,

	ENEMY_BEATED = 25006,
	NO_ENEMY     = 25007,

	#--��ս
	CHALLENGE_CDING = 25017,
	NO_ENTER_TIMES = 25018,
    NO_WEAK_FOE = 25019,
    NO_STRONG_FOE = 25020,
    MAP_CHANGE_FAILED = 25021,
    NEED_LEVEL = 25022,
    NO_DIAMOND = 25023,

    #--
    SCORS_REWARD_RECV_LV = 25024,
    SCORS_REWARD_RECV_DAY = 25025,
    SCORS_REWARD_RECV_WEEK = 25026,

    #--
    REWARDS_TITLE_WIN = 25030,
    REWARDS_TEXT_WIN = 25031,
    REWARDS_TITLE_LOSS = 25032,
    REWARDS_TEXT_LOSS = 25033,

    REFRESH_SUC = 25035,

    #--�������
    INSPIRE_SUC = 25037, #--����ɹ�
    INSPIRE_ED  = 25038, #--�Ѿ��������

    VIP_BUY_FULL = 25039, #--�Ѵ���������
)

#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--- ���� #--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#--#---
#--Ĭ������
arena_config_default=dict (
	#--INIT_NUM = 1000,
	OPEN_LV = 20,
	CHALLENGE_CD = 300, 

	CHALLENGE_TIME_PER_DAY = 15,

	WEAK_FOE_PICK_PARAM = {90,50,50,10},
	STRONG_FOE_PICK_PARAM = {150,90,90,50,50,10},
	ENEMY_PICK_PARAM = {150,50},
	FOES_NUM_FOR_RAND = 15,

	BUF_ATK_PER = 10,
	BUF_HP_PER = 10,

	CLEAR_CD_PRICE_ID = 5,
	REFRESH_WEAK_PRICE_ID = 6,
	REFRESH_STRONG_PRICE_ID = 7,
	BUY_ARENA_TIME_PRICE_ID = 8,
	BUF_PRICE_ID = 9,
	INSPIRE_BUF_ID = 41,
	#--BUF_PRICE_PER = {[2] = 200,},
	#--REFRESH_WEAK_PRICE = {[2] = 200,},
	#--REFRESH_STRONG_PRICE = {[2] = 200,},
	)
import py_util
import KBEDebug
class arena_config:
	def __init__(self,a,b):
		tmp=py_util._readXml('/data/xml/ArenaConfig.xml', 'key')

		def less(a,b):
			return a<b

		for key,value in tmp.items():
			if value['value']:
				k=py_util.format_key_value(key,value['value'])[0]
				v=py_util.format_key_value(key,value['value'])[1]
	#TODO ������

		self.m_scoreRewards = py_util._readXml('/data/xml/ArenaScoreReward.xml', 'id_i')

		self.m_creditRewards4Challenge = py_util._readXml('/data/xml/ArenaCreditReward4Challenge.xml', 'id_i')
		self.m_typeAndlevel2CreditRewards = {}
		for id,v in self.m_creditRewards4Challenge.items():
			t=v[type]
			if self.m_creditRewards4Challenge[t] is None:
				self.m_creditRewards4Challenge[t]={}
