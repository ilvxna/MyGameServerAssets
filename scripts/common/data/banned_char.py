import py_util
from KBEDebug import *
bannedChars = [
	' ',
	',',
	'`',
	'\'',
	'\\',
	'\"',
	'\t',
	'\r',
	'\n',
	'	',
    '/',
    '[',
    ']',
]
class banned_char:
	def __init__(self):
		self.M_banned={}
		for _,v in enumerate(bannedChars):
			self.M_banned[str(v)]=True
	def Check(self,str):
		for k,_v in self.M_banned:
			if py_util.utfstr_check_char(str,k):
				return False
		return True