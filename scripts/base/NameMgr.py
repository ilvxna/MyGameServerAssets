import KBEngine
from KBEDebug import *

from NameData import NameDataMgr

g_name_mgr=NameDataMgr()

class NameMgr(KBEngine.Base,GameObject):
    '''
    名字管理中心，需要在加载在线管理器之后加载
    '''
    def __init__(self):
		KBEngine.Base.__init__(self)
		GameObject.__init__(self)

		KBEngine.globalData["NamgeMgr"] = self

		g_name_mgr.initData()

		sql="SELECT id,sm_name FROM tbl_Avatar"
        #对于方案为MySQL数据库它是一个SQL查询语句。
		KBEngine.executeRawDatabaseCommand(sql,self._onAvatarSelectResp)

    def _onAvatarSelectResp(self,result, rows, insertid, error):
        '''
        result 结果类似:[[b'1',b''],[b'2',b'zhanshi']]

result参数对应的就是“结果集合”，这个结果集合参数是一个行列表。 每一行是一个包含字段值的字符串列表。
命令执行没有返回结果集合（比如说是DELETE命令）， 或者 命令执行有错误时这个结果集合为None。 

rows参数则是“影响的行数”，它是一个整数，表示命令执行受影响的行数。这个参数只和不返回结果结合的命令（如DELETE）相关。
如果有结果集合返回或者命令执行有错误时这个参数为None。 

insertid对应的是“自増长值”，类似于实体的databaseID，当成功的向一张带有自増长类型字段的表中插入数据时，它返回该数据在插入时自増长字段所被赋于的值。
更多的信息可以参阅mysql的mysql_insert_id()方法。另外，此参数仅在数据库类型为mysql时有意义。

error则对应了“错误信息”，当命令执行有错误时，这个参数是一个描述错误的字符串。命令执行没有发生错误时这个参数为None。 
        '''
        names={}
        for id,name_list in enumerate(result):
            names[name_list[1].decode()]=id

        self.OnInited(name)
	def OnInited(self,used_names):
		DEBUG_MSG("NameMgr:OnInited.")

        if not used_names:
            used_names={}

        g_name_mgr.InitByDB(used_names)

        rand_names=self.g_name_mgr.random_n_names(10)

	def GetRandomName(self,account, vocation, accountMailbox):
        #usingPool is list，所以先把usingpool拆开，检查每一个dict,不要有姓名相同的
        #重复点击
		for k,name_dict in enumerate(self.usingPool):
			if name_dict[account]:
				g_name_mgr.BackToUnsed([name,nam_dic[name]])

        [name,name_type]=g_name_mgr.GetRandomName(vocation)

        if not name:
            ERROR_MSG("NameMgr::GetRandomName :run out of name data.")
        
        self.usingPool.append(dict(name=name_type,))

