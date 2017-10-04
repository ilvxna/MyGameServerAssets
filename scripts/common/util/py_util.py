#coding=utf-8
import time

import math
import random
from KBEDebug import *
import xml.etree.ElementTree as ET
_ONEDAY_SECONDS = 24*60*60
#生成一个日期的整数，默认以凌晨4:00为界
#ToDo 时间time.struct_time有问题
def get_number_date(from_time,from_clock):
	now_time=from_time or time.time()
	_from_clock=from_clock or 4
	now_time_table=time.struct_time(now_time)
	if now_time_table==None:
		return 0
	if now_time_table[0]<from_clock :
		now_time_table_2=time.struct_time(now_time-_ONEDAY_SECONDS)
		return now_time_table_2[0]*1000+now_time_table_2[1]*100+now_time_table_2[2]
	else:
		return now_time_table[0]*1000+now_time_table[1]*100+now_time_table[2]

#获得某日某个时刻点对应的秒数
def get_number_secs(from_time,from_clock):
	now_time=from_time or time.time()
	_from_clock=from_clock or 4
	now_time_table=time.struct_time(now_time)
	if now_time==None:
		return 0
	if now_time_table[0]<from_clock:
		now_time_table_2=time.struct_time(now_time-_ONEDAY_SECONDS)
		now_time_table_2[3]=from_clock
		now_time_table_2[4]=0
		now_time_table_2[5]=0
		return now_time_table_2
	else:
		now_time_table[3]=from_clock
		now_time_table[4]=0
		now_time_table[5]=0
		return now_time_table

#从M个数里(等概率)随机出N个不重复的数
def choose_n_norepeated(t,n):
	m=t
	if m<=n:
		return t
	t2={}
	i=0
	while True:
		r=random.randint(1,m)
		if t2[r]==None:
			t2[r]=1
			i=i+1
			if i>=n:
				return t2

#从{k = prob}表里挑选一个满足概率的k
def choose_prob(t,min_prob,max_prob):
	if min_prob and max_prob:
		ram=random.uniform(min_prob,max_prob)
	else:
		ram=random.random()
	prob=0
	for k,prob1 in t:
		prob=prob+prob1
		if ram<=prob:
			return k

#从格式"道具id1,数量1,概率1,道具id2,数量2,概率2,..."中随机出一个道具id和数量
def choose_random_item(drop):
	if drop:
		ram=random.random()
		n=len(drop)
		prop=0
		for i in range(3,n,3):
			p=drop[i]
			if p:
				prop=prop+p
				if ram<prop:
					return [drop[i-2],drop[i-1]]

#x=0.3 0.3概率发生
def prob(x):
	if x<=0:
		return False
	return random.random()<x
#{0.2,0.3,0.5}，总和1,返回按各自概率返回索引20%返回1，30%返回2,50%返回3
def choice(x):
	d=random.random()
	sum=0
	for k,v in enumerate(x):
		if d<v+sum:
			return k
		sum=sum+v
	return sum
#从一个列表中随机一个值
def choose_1(t):
	n=len(t)
	if n==0:
		return None
	return t[random.randint(1,n)]
#从一个列表中随机一个值,从其关联列表也返回一个值
def choose_2(t,t2):
	n=len(t)
	if n==0:
		return None
	idx=random.random(1,n)
	return[t[idx],t2[idx]]
#-从不等概率的一组值里面随机选择个
#--table格式如：{[值]=概率}；函数返回 值，概率
def getrandomseed(a):
	if type(a)==dict:
		max=0
		for k,v in a:
			max=max+v
		seed=random.randint(1,max)
		sumvv=0
		for k,v in a:
			sumvv=sumvv+sumvv
			if seed<=sumvv:
				return {k:v}

def _format_key_value(key,value):
	nKeyLen=len(key)
	
	prefix=key[-2:]
	key2=key[:-2]
	if prefix=='_i' :
		return [key2,int(value)]
	elif prefix=='_f':
		return [key2,int(value)]
	elif prefix=='_s':
		return [key2,int(value)]
	elif prefix=='_l':
		return[key2,value.split(',')]
	elif prefix=='_k':
		tmp=value.split(',')
		tmp2={}
		for _,k in enumerate(tmp):
			tmp2[k]=1
		return[key2,tmp2]
	elif prefix=='_t':
		tmp=value.split(":")
		sec=0
		for i,v in enumerate(tmp):
			t=int(v)
			if t:
				sec=t+sec*60
		return [key2,sec]
	elif prefix=='_y':
		i=value.find(' ')
		str_data=value[1:i-1]
		str_time=value[i+1:]
		dd=value.split('-')
		tt=value.split('-')
		return [key2,time.struct_time(year=dd[0],month=dd[1],day=dd[2],hour=dd[3],minute=dd[4],second=dd[5])]
	elif prefix=='_m':
		tmp=value.split(',')
		tmp2={}
		for _,v in enumerate(tmp):
			tp=v.split(':')
			id=int(tp[0]) or  (tp[0])
			num=int(tp[1]) or tp[1]
			tmp2[id]=num
		return [key2,tmp2]
	else:
		return [key,value]
def format_key_value(key,value):
	return _format_key_value(key,value)

#格式化一个table,该table只有一层关系
def _format_table(t):
	v2={}
	if isinstance(t,dict):
		for key,value in t.items():
			key2=_format_key_value(key,value)[0]
			value2=_format_key_value(key,value)[1]
			v2[key2]=value2
	return v2

#根据字段名后缀的含义修改从xml读取的数据类型
def format_xml_table(t):
	p_type=type(t)
	if isinstance(t,int):
		for k,v in enumerate(t):
			v2=_format_table(v)
		
			t2[k]=v2
	elif isinstance(t,dict):
		t2={}
		for k,v in t.items():
			v2=_format_table(v)
		
			t2[k]=v2
	return t2
PATH=r"scripts\data\%s"

#读取xml文件
def _readXml(path,key):
	new_path=(PATH % (path)).replace("\\", "/")

	#path 即是路径的名字
	tree=ET.parse(new_path)

	key_path=('./'+path.title())
	p=tree.findall(key_path)
	# 这儿意味着XML文件的关键字与路径有关系，因此需要处理XML与路径的不一致的问题。
	#将XML
	d={}
	for v in p:
		for child in v.getchildren():
			if child.tag==key:
				tmp=int(child.text)
				d[tmp]={}
			else:
				d[tmp][child.tag]=child.text
	e=d
	d=format_xml_table(e)
	

	e={}
	for i,j in d.items():
		e[i]={}
		for key,value in  j.items():
			prefix=key[-2:]
			key2=key[:-2]
			if prefix=='_i' :
				e[i][key2]=int(value)
			elif prefix=='_f':
				e[i][key2]=int(value)
			elif prefix=='_s':
				if type(value)==int:
					e[i][key2]=int(value)
				else:
					e[i][key2]=value

			elif prefix=='_l':
				#list
				s=value.split(',')
				t=[]
				for k,v in enumerate(s):
					if type(v)==int:
						t.append(int(v))
					else:
						t.append(float(v))
				e[i][key2]=t

			elif prefix=='_k':
				tmp=value.split(',')
				tmp2={}
				for _,k in enumerate(tmp):
					tmp2[k]=1
				#return[key2,tmp2]
				e[i][key2]=tmp2
			elif prefix=='_t':	
				tmp=value.split(":")
				sec=0
				for i,v in enumerate(tmp):
					t=int(v)
					if t:
						sec=t+sec*60
				e[i][key2]=sec

			elif prefix=='_y':
				e[i][key2]= time.mktime(time.strptime(value, '%Y-%m-%d %X'))
			elif prefix=='_m':
				tmp=value.split(',')
				tmp2={}
				for _,v in enumerate(tmp):
					tp=v.split(':')
					id=str(tp[0])
					if type(tp[1])==int:
						num=int(tp[1]) or tp[1]
					else:
						num=tp[1]
					tmp2[id]=num
				e[i][key2]=tmp2
			else:
				if type(value)==int:
					e[i][key2]=int(value)
				else:
					e[i][key2]=value
	return e
#--根据两个关键字来读xml文件,例如科技表根据科技id和科技等级来决定相关的数据
#--注意,这里的key和key2不能带后缀
def _readXmlBy2Key(path,key1,key2):
	d=_readXml(path,'id_i')
	len=d.__len__()

	#--计算utf编码字符串的长度
_utf_arr = [0, 0xc0, 0xe0, 0xf0, 0xf8, 0xfc]
_utf_arr_len = _utf_arr.__len__()
#检查utf字符串是否含有char(< 0xc0)字符
def utfstr_check_char(str, char):
	if char<0 or char>=0xc0 :
		ERROR_MSG("utfstr_check_char")
	
	left=len(str)
	cnt=0
	while left>0:
		tmp=ord(str[-left])
		if tmp==char:
			return True
		i = _utf_arr_len
		while _utf_arr[i-1]:
			if tmp >= _utf_arr[i]:
				left=left-i
			i=i-1
			cnt=cnt+1
	return cnt




	