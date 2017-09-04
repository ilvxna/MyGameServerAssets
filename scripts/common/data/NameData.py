import py_util
from KBEDebug import *
import public_config
import math
import random
Spliter=''

nameType=dict(
    occi_female = 1, #西方
    occi_male = 2, #西方
    cute = 3, #可爱
    orie_female = 4, #东方
    orie_male = 5, #东方
    )

    vocation2Gender = dict(
	[public_config.VOC_WARRIOR] = public_config.GENDER_MALE,
	[public_config.VOC_ASSASSIN] = public_config.GENDER_FEMALE,
	[public_config.VOC_ARCHER] = public_config.GENDER_MALE,
	[public_config.VOC_MAGE] = public_config.GENDER_FEMALE,
)

class NameDataMgr:
    def __init__(self):
         DEBUG_MSG("NameDataMgr:initData begin")

        self.OccidentalLast  = py_util._readXml("/data/xml/NameOccidentalLast.xml", "id_i")
        self.OccidentalFemale = py_util._readXml("/data/xml/NameOccidentalFemale.xml", "id_i")
        self.OccidentalMale = py_util._readXml("/data/xml/NameOccidentalMale.xml", "id_i")

        self.CuteFirst = py_util._readXml("/data/xml/NameCuteFirst.xml", "id_i")
        self.CuteLast = py_util._readXml("/data/xml/NameCuteLast.xml", "id_i")

        self.OrientalLast = py_util._readXml("/data/xml/NameOrientalLast.xml", "id_i")
        self.OrientalFemale = py_util._readXml("/data/xml/NameOrientalFemale.xml", "id_i")
        self.OrientalMale = py_util._readXml("/data/xml/NameOrientalMale.xml", "id_i")

        self.occi_female = [] #西方
        self.occi_male = [ ]#西方
        self.cute = [] #可爱
        self.orie_female = [] #东方
        self.orie_male = [] #东方

        self.count = 0
        DEBUG_MSG("NameDataMgr:initData over.")

    def InitByDB(self,used_names):
#--组合名字
#	--西方,姓在后
        for _,lastname in self.OccidentalLast.items():
            #女生名字
            for _,femalname in self.OccidentalFemale.items():
                name=femalname['name']+Spliter+lastname['name']
                if  used_names.get(name,0)==0: #在Python中，当你使用a[key]这种方式从字典中获取一个值时，若字典中不存在这个此key时就会产生一个KeyError的错误
                    self.occi_female.append(name)
                    self.count = self.count + 1
            for _,malename in self.OccidentalMale.items():
                #男生名字
                name=malename['name']+Spliter+lastname['name']
                if used_names.get(name,0)==0:
                    self.occi_male.append(name)
                    self.count = self.count + 1
#可爱，女性名字，姓在前
        for _,lastname in self.CuteLast.items():
            #姓
            for _,firstname in self.CuteFirst.items():
            #名
                name=lastname['name']+Spliter+firstname['name']
                if used_names.get(name,0)==0:
                    self.cute.append(name)
                    self.count = self.count + 1
   #东方,姓在前
        for _,lastname in self.OrientalLast.items():
            #男名 
            for _,malename in self.OrientalMale.items():
                name=lastname['name']+Spliter+malename['name']
                if used_names.get(name,0)==0:
                    self.orie_male.append(name)
                    self.count = self.count + 1
            #女名
            for _,femalname in self.OrientalFemale.items():
                name=lastname['name']+Spliter+femalname['name']
                if used_names.get(name,0)==0:
                    self.orie_female.append(name)
                    self.count = self.count + 1
        DEBUG_MSG('NameDataMgr::InitByDB: %s' % self.count)
        if self.count==0:
            DEBUG_MSG('NameDataMgr::InitByDB: %s' %  "name space is running out.")

    def GetRandom(self,t):
     # t is list
        m=len(cute)

        if m>0:
            n=random.randint(1,m)
            name=t[n]
            t.remove(name)
            
            self.count=self.count-1

            return name
        else:
            return None
    
    def GetRandomName(self,vocation):
        if self.count==0:
            DEBUG_MSG('NameDataMgr::GetRandomName: %s' % "name space is running out.")
            return
        ts=1

        name=False
        name_type=0

        while not name :
            ts+=1
            if ts<1:
                ts=1
            elif ts>3:
                ts=1

            if  ts==1:
                #根据职业从ma_mc, fa_mc中取
                if vocation2Gender[vocation]==public_config.GENDER_MALE:
                    name=self.GetRandom(self.occi_male)
                    name_type=nameType.occi_male
                else:
                    name=self.GetRandom(self.occi_female)
                    name_type=nameType.occi_female

                    if name:
                        break
            elif ts==2:
                name=self.GetRandom(self.cute)
                name_type=nameType.cute
                if name:
                    break
            elif ts==3:
                #根据职业从ma_mc, fa_mc中取
                if vocation2Gender[vocation]==public_config.GENDER_MALE:
                    name=self.GetRandom(self.orie_male)
                    name_type=nameType.orie_male
                    if name:
                        break
                else:
                    name=self.GetRandom(self.orie_female)
                    name_type=nameType.orie_female
                    if name:
                        break
            else:
                DEBUG_MSG('NameDataMgr:GetRandomName is error')
        if name:
            return [name,name_type]
        else:
            DEBUG_MSG('NameDataMgr:GetRandomName:%s'%'name is none')
    def BackToUnused(self,poolItem):# [name,ty]
        name=poolItem[0]
        ty=poolItem[1]

        if nameType.occi_female==ty:
            self.occi_female.append(name)
        elif nameType.occi_male==ty:
            self.occi_male.append(name)
        elif nameType.cute==ty:
            self.cute.append(name)
        elif  nameType.orie_female==ty:
            self.orie_female.append(name)
        elif nameType.orie_male==ty:
            self.orie_male.append(name)
        else:
            return
        self.count+=1

    def random_n_names(self,n):
        t={}
        for i in range(1,n):
            vocation=math.modf(i/2)
            name=self.GetRandomName(vocation)
            if name:
                t[i]=name
        return t
    def RecoverName(self,name):
        self.cute.append(name)
        

            

            




            

        



                
