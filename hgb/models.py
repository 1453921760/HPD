from sqlalchemy import  create_engine,Column,Integer,String,Float,Text,Enum,DateTime,PickleType,JSON,Table,ForeignKey,and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy.sql.expression import func
from datetime import datetime,timedelta
from time import sleep
from test_data import *
import memcache
import cv2
from x import *
from gg import*
mc=memcache.Client(['127.0.0.1:11211'],debug=True)

HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'test'
USERNAME = 'root'
PASSWORD = 'root'
db_uri="mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD,host=HOST,port=PORT,db=DATABASE)

engine=create_engine(db_uri,encoding='utf-8')
Base=declarative_base(engine)
session=sessionmaker(engine)()

goods_and_admin=Table(
    'goods_and_users',
    Base.metadata,
    Column('user_id',Integer,ForeignKey('users.id')),
    Column('goods_id',Integer,ForeignKey('goods.id'))
)

class Goods(Base):
    __tablename__='goods'
    id=Column(Integer,primary_key=True,autoincrement=True)
    picture=Column(Text,default='default.jpg')
    description=Column(Text,default='this is default description')
    name=Column(String(20),nullable=False)
    price=Column(Float,nullable=False)
    goods_id=Column(String(50),primary_key=True)
    num=Column(Integer)
    kind1=Column(String(20))
    kind2=Column(String(20))
    admin=relationship('Users',backref='goods_sold',secondary=goods_and_admin)
    __table_args__ = {
        "mysql_charset" : "utf8"
}


class Users(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,autoincrement=True)
    openid=Column(Text)
    goods_on_sell=Column(PickleType(),default=[])
    buy_history=Column(PickleType(),default=[])
    buy_car=Column(PickleType(),default=[])
    browse_history=Column(PickleType())
    like_matrix=Column(PickleType(),default=[])
    __table_args__ = {
        "mysql_charset" : "utf8"
}




Base.metadata.drop_all()
Base.metadata.create_all()
# def buyGoods(goods_id,num,openid):
#     goods=session.query(Goods).filter(Goods.goods_id==goods_id).first()
#     if goods.num<num:
#         print(0) 
#     else :
#         goods.num=goods.num-num
#         new_history={
#             'goods_id':goods_id,
#             'kind1':goods.kind1,
#             'kind2':goods.kind2,
#             'num':num
#         }
#         user=session.query(Users).filter(Users.openid==openid).first()
#         old_history=user.buy_history
#         old_history.append(new_history)
#         session.query(Users).filter(Users.openid=='openid').update({'buy_history':old_history})
#         session.commit()


def add_user(openid):
    new_custom=Custom()
    user=Users(openid=openid,like_matrix=new_custom.matrix)
    session.add(user)
    session.commit()
add_user('test_user')



def getGoodsInfo(goods_id):
    goods=session.query(Goods).filter(Goods.goods_id==goods_id).first()
    return goods

def addBuyCar(openid,goods_id,num,checked):
    user=get_user_from_openid(openid)
    goods=getGoodsInfo(goods_id)
    new_buy_car={
        'goods_id':goods_id,
        'kind1':goods.kind1,
        'kind2':goods.kind2,
        'num':num,
        'price':goods.price,
        'description':goods.description,
        'picture':goods.picture,
        'name':goods.name,
        'checked':checked
    }
    old_buy_car=user.buy_car
    for i in range(0,len(old_buy_car)):
        if old_buy_car[i].get('goods_id')==goods_id:
            old_buy_car[i]['num']=int(old_buy_car[i].get('num'))+int(num)
            session.query(Users).filter(Users.openid==openid).update({'buy_car':old_buy_car})
            session.commit()
            return 0
    old_buy_car.append(new_buy_car)
    session.query(Users).filter(Users.openid==openid).update({'buy_car':old_buy_car})
    session.commit()

def get_user_from_openid(openid):
    user=session.query(Users).filter(Users.openid==openid).first()
    return user

    

def add_new_goods(picture,description,name,price,goods_id,num,kind1,kind2,admin):
    new_goods=Goods(picture=picture,description=description,name=name,price=price,goods_id=goods_id,num=num,kind1=kind1,kind2=kind2)
    a=get_user_from_openid(admin)
    new_goods.admin.append(a)
    session.add(new_goods)
    session.commit()

add_new_goods(lingshi1.get('picture'),lingshi1.get('description'),lingshi1.get('name'),lingshi1.get('price'),lingshi1.get('goods_id'),lingshi1.get('num'),lingshi1.get('kind1'),lingshi1.get('kind2'),lingshi1.get('admin'))
add_new_goods(lingshi2.get('picture'),lingshi2.get('description'),lingshi2.get('name'),lingshi2.get('price'),lingshi2.get('goods_id'),lingshi2.get('num'),lingshi2.get('kind1'),lingshi2.get('kind2'),lingshi2.get('admin'))
add_new_goods(lingshi3.get('picture'),lingshi3.get('description'),lingshi3.get('name'),lingshi3.get('price'),lingshi3.get('goods_id'),lingshi3.get('num'),lingshi3.get('kind1'),lingshi3.get('kind2'),lingshi3.get('admin'))
add_new_goods(chajiu1.get('picture'),chajiu1.get('description'),chajiu1.get('name'),chajiu1.get('price'),chajiu1.get('goods_id'),chajiu1.get('num'),chajiu1.get('kind1'),chajiu1.get('kind2'),chajiu1.get('admin'))
add_new_goods(chajiu2.get('picture'),chajiu2.get('description'),chajiu2.get('name'),chajiu2.get('price'),chajiu2.get('goods_id'),chajiu2.get('num'),chajiu2.get('kind1'),chajiu2.get('kind2'),chajiu2.get('admin'))
add_new_goods(chajiu3.get('picture'),chajiu3.get('description'),chajiu3.get('name'),chajiu3.get('price'),chajiu3.get('goods_id'),chajiu3.get('num'),chajiu3.get('kind1'),chajiu3.get('kind2'),chajiu3.get('admin'))
add_new_goods(tiaoliaohongbei1.get('picture'),tiaoliaohongbei1.get('description'),tiaoliaohongbei1.get('name'),tiaoliaohongbei1.get('price'),tiaoliaohongbei1.get('goods_id'),tiaoliaohongbei1.get('num'),tiaoliaohongbei1.get('kind1'),tiaoliaohongbei1.get('kind2'),tiaoliaohongbei1.get('admin'))
add_new_goods(tiaoliaohongbei2.get('picture'),tiaoliaohongbei2.get('description'),tiaoliaohongbei2.get('name'),tiaoliaohongbei2.get('price'),tiaoliaohongbei2.get('goods_id'),tiaoliaohongbei2.get('num'),tiaoliaohongbei2.get('kind1'),tiaoliaohongbei2.get('kind2'),tiaoliaohongbei2.get('admin'))
add_new_goods(tiaoliaohongbei3.get('picture'),tiaoliaohongbei3.get('description'),tiaoliaohongbei3.get('name'),tiaoliaohongbei3.get('price'),tiaoliaohongbei3.get('goods_id'),tiaoliaohongbei3.get('num'),tiaoliaohongbei3.get('kind1'),tiaoliaohongbei3.get('kind2'),tiaoliaohongbei3.get('admin'))
add_new_goods(qunzhuang1.get('picture'),qunzhuang1.get('description'),qunzhuang1.get('name'),qunzhuang1.get('price'),qunzhuang1.get('goods_id'),qunzhuang1.get('num'),qunzhuang1.get('kind1'),qunzhuang1.get('kind2'),qunzhuang1.get('admin'))
add_new_goods(nvkuzhuang1.get('picture'),nvkuzhuang1.get('description'),nvkuzhuang1.get('name'),nvkuzhuang1.get('price'),nvkuzhuang1.get('goods_id'),nvkuzhuang1.get('num'),nvkuzhuang1.get('kind1'),nvkuzhuang1.get('kind2'),nvkuzhuang1.get('admin'))
add_new_goods(nvshangzhuang1.get('picture'),nvshangzhuang1.get('description'),nvshangzhuang1.get('name'),nvshangzhuang1.get('price'),nvshangzhuang1.get('goods_id'),nvshangzhuang1.get('num'),nvshangzhuang1.get('kind1'),nvshangzhuang1.get('kind2'),nvshangzhuang1.get('admin'))
add_new_goods(jiayongqingjie1.get('picture'),jiayongqingjie1.get('description'),jiayongqingjie1.get('name'),jiayongqingjie1.get('price'),jiayongqingjie1.get('goods_id'),jiayongqingjie1.get('num'),jiayongqingjie1.get('kind1'),jiayongqingjie1.get('kind2'),jiayongqingjie1.get('admin'))
add_new_goods(xiyuyongpin1.get('picture'),xiyuyongpin1.get('description'),xiyuyongpin1.get('name'),xiyuyongpin1.get('price'),xiyuyongpin1.get('goods_id'),xiyuyongpin1.get('num'),xiyuyongpin1.get('kind1'),xiyuyongpin1.get('kind2'),xiyuyongpin1.get('admin'))
add_new_goods(zhijin1.get('picture'),zhijin1.get('description'),zhijin1.get('name'),zhijin1.get('price'),zhijin1.get('goods_id'),zhijin1.get('num'),zhijin1.get('kind1'),zhijin1.get('kind2'),zhijin1.get('admin'))
add_new_goods(jiaju1.get('picture'),jiaju1.get('description'),jiaju1.get('name'),jiaju1.get('price'),jiaju1.get('goods_id'),jiaju1.get('num'),jiaju1.get('kind1'),jiaju1.get('kind2'),jiaju1.get('admin'))
add_new_goods(jiafang1.get('picture'),jiafang1.get('description'),jiafang1.get('name'),jiafang1.get('price'),jiafang1.get('goods_id'),jiafang1.get('num'),jiafang1.get('kind1'),jiafang1.get('kind2'),jiafang1.get('admin'))
add_new_goods(riyongpin1.get('picture'),riyongpin1.get('description'),riyongpin1.get('name'),riyongpin1.get('price'),riyongpin1.get('goods_id'),riyongpin1.get('num'),riyongpin1.get('kind1'),riyongpin1.get('kind2'),riyongpin1.get('admin'))
add_new_goods(gerenyongpin1.get('picture'),gerenyongpin1.get('description'),gerenyongpin1.get('name'),gerenyongpin1.get('price'),gerenyongpin1.get('goods_id'),gerenyongpin1.get('num'),gerenyongpin1.get('kind1'),gerenyongpin1.get('kind2'),gerenyongpin1.get('admin'))
add_new_goods(shouji1.get('picture'),shouji1.get('description'),shouji1.get('name'),shouji1.get('price'),shouji1.get('goods_id'),shouji1.get('num'),shouji1.get('kind1'),shouji1.get('kind2'),shouji1.get('admin'))
add_new_goods(wenju1.get('picture'),wenju1.get('description'),wenju1.get('name'),wenju1.get('price'),wenju1.get('goods_id'),wenju1.get('num'),wenju1.get('kind1'),wenju1.get('kind2'),wenju1.get('admin'))
add_new_goods(shoujipeijian1.get('picture'),shoujipeijian1.get('description'),shoujipeijian1.get('name'),shoujipeijian1.get('price'),shoujipeijian1.get('goods_id'),shoujipeijian1.get('num'),shoujipeijian1.get('kind1'),shoujipeijian1.get('kind2'),shoujipeijian1.get('admin'))
add_new_goods(diannaobijiben1.get('picture'),diannaobijiben1.get('description'),diannaobijiben1.get('name'),diannaobijiben1.get('price'),diannaobijiben1.get('goods_id'),diannaobijiben1.get('num'),diannaobijiben1.get('kind1'),diannaobijiben1.get('kind2'),diannaobijiben1.get('admin'))
add_new_goods(shangwubangong1.get('picture'),shangwubangong1.get('description'),shangwubangong1.get('name'),shangwubangong1.get('price'),shangwubangong1.get('goods_id'),shangwubangong1.get('num'),shangwubangong1.get('kind1'),shangwubangong1.get('kind2'),shangwubangong1.get('admin'))
add_new_goods(zhinengshebei1.get('picture'),zhinengshebei1.get('description'),zhinengshebei1.get('name'),zhinengshebei1.get('price'),zhinengshebei1.get('goods_id'),zhinengshebei1.get('num'),zhinengshebei1.get('kind1'),zhinengshebei1.get('kind2'),zhinengshebei1.get('admin'))
add_new_goods(sheyingshexiang1.get('picture'),sheyingshexiang1.get('description'),sheyingshexiang1.get('name'),sheyingshexiang1.get('price'),sheyingshexiang1.get('goods_id'),sheyingshexiang1.get('num'),sheyingshexiang1.get('kind1'),sheyingshexiang1.get('kind2'),sheyingshexiang1.get('admin'))
add_new_goods(nanxie1.get('picture'),nanxie1.get('description'),nanxie1.get('name'),nanxie1.get('price'),nanxie1.get('goods_id'),nanxie1.get('num'),nanxie1.get('kind1'),nanxie1.get('kind2'),nanxie1.get('admin'))
add_new_goods(nvxie1.get('picture'),nvxie1.get('description'),nvxie1.get('name'),nvxie1.get('price'),nvxie1.get('goods_id'),nvxie1.get('num'),nvxie1.get('kind1'),nvxie1.get('kind2'),nvxie1.get('admin'))
add_new_goods(yundongfuzhuang1.get('picture'),yundongfuzhuang1.get('description'),yundongfuzhuang1.get('name'),yundongfuzhuang1.get('price'),yundongfuzhuang1.get('goods_id'),yundongfuzhuang1.get('num'),yundongfuzhuang1.get('kind1'),yundongfuzhuang1.get('kind2'),yundongfuzhuang1.get('admin'))
add_new_goods(yundongjianshen1.get('picture'),yundongjianshen1.get('description'),yundongjianshen1.get('name'),yundongjianshen1.get('price'),yundongjianshen1.get('goods_id'),yundongjianshen1.get('num'),yundongjianshen1.get('kind1'),yundongjianshen1.get('kind2'),yundongjianshen1.get('admin'))
add_new_goods(huwai1.get('picture'),huwai1.get('description'),huwai1.get('name'),huwai1.get('price'),huwai1.get('goods_id'),huwai1.get('num'),huwai1.get('kind1'),huwai1.get('kind2'),huwai1.get('admin'))
add_new_goods(caizhuang1.get('picture'),caizhuang1.get('description'),caizhuang1.get('name'),caizhuang1.get('price'),caizhuang1.get('goods_id'),caizhuang1.get('num'),caizhuang1.get('kind1'),caizhuang1.get('kind2'),caizhuang1.get('admin'))
add_new_goods(huli1.get('picture'),huli1.get('description'),huli1.get('name'),huli1.get('price'),huli1.get('goods_id'),huli1.get('num'),huli1.get('kind1'),huli1.get('kind2'),huli1.get('admin'))
add_new_goods(qingjiemeirong1.get('picture'),qingjiemeirong1.get('description'),qingjiemeirong1.get('name'),qingjiemeirong1.get('price'),qingjiemeirong1.get('goods_id'),qingjiemeirong1.get('num'),qingjiemeirong1.get('kind1'),qingjiemeirong1.get('kind2'),qingjiemeirong1.get('admin'))
add_new_goods(nanshangzhuang1.get('picture'),nanshangzhuang1.get('description'),nanshangzhuang1.get('name'),nanshangzhuang1.get('price'),nanshangzhuang1.get('goods_id'),nanshangzhuang1.get('num'),nanshangzhuang1.get('kind1'),nanshangzhuang1.get('kind2'),nanshangzhuang1.get('admin'))
add_new_goods(nankuzhuang1.get('picture'),nankuzhuang1.get('description'),nankuzhuang1.get('name'),nankuzhuang1.get('price'),nankuzhuang1.get('goods_id'),nankuzhuang1.get('num'),nankuzhuang1.get('kind1'),nankuzhuang1.get('kind2'),nankuzhuang1.get('admin'))
add_new_goods(zhubaoshipin1.get('picture'),zhubaoshipin1.get('description'),zhubaoshipin1.get('name'),zhubaoshipin1.get('price'),zhubaoshipin1.get('goods_id'),zhubaoshipin1.get('num'),zhubaoshipin1.get('kind1'),zhubaoshipin1.get('kind2'),zhubaoshipin1.get('admin'))
add_new_goods(shoubiaojundao1.get('picture'),shoubiaojundao1.get('description'),shoubiaojundao1.get('name'),shoubiaojundao1.get('price'),shoubiaojundao1.get('goods_id'),shoubiaojundao1.get('num'),shoubiaojundao1.get('kind1'),shoubiaojundao1.get('kind2'),shoubiaojundao1.get('admin'))
add_new_goods(yanjing1.get('picture'),yanjing1.get('description'),yanjing1.get('name'),yanjing1.get('price'),yanjing1.get('goods_id'),yanjing1.get('num'),yanjing1.get('kind1'),yanjing1.get('kind2'),yanjing1.get('admin'))
# add_new_goods(yanjing1.get('picture'),yanjing1.get('description'),yanjing1.get('name'),yanjing1.get('price'),yanjing1.get('goods_id'),yanjing1.get('num'),yanjing1.get('kind1'),yanjing1.get('kind2'),yanjing1.jxzjjrgswsyanjing1


def search_by_kind(kind1,kind2,word):    
    goods=session.query(Goods).filter(Goods.kind2==kind2).all()
    if word==None:
        print(goods)
        return goods
    name_list=[]
    for good in goods:
        name_list.append(good.description)
    
    res_name_list=fuzzyMatch(word,name_list)
    res=[]
    # print(res_name_list)
    for name in res_name_list:
        for i in range(0,len(name_list)):
            if goods[i].description==name:
                res.append(goods[i])

    print(res)
    return res

# search_by_kind(1,'眼镜',None)
# search_by_kind(1,'手表军刀',None)
# search_by_kind(1,'珠宝饰品',None)
# search_by_kind(1,'男裤装',None)


def getMyGoods(openid):
    user=get_user_from_openid(openid)
    return user.goods_sold


def deleteBuyCar(openid,goods_id):
    user=get_user_from_openid(openid)
    good_del=None
    for good in user.buy_car:
        if good.get('goods_id')==goods_id:
            good_del=good
    old_buy_car=user.buy_car
    old_buy_car.remove(good_del)
    session.query(Users).filter(Users.openid==openid).update({'buy_car':old_buy_car})
    session.commit()


def get_openid_from_session_key(session_key):
    openid=mc.get(session_key)
    return openid

def getBuyCar(openid):
    user=get_user_from_openid(openid)
    buy_car=user.buy_car
    return buy_car


def changeChecked(openid,goods_id,checked):
    user=get_user_from_openid(openid)
    old_buy_car=user.buy_car
    # print(bool(user.buy_car[0].get('checked')))
    for i in range(0,len(old_buy_car)):
        if old_buy_car[i].get('goods_id')==goods_id:
            old_buy_car[i]['checked']=checked
            # print(old_buy_car[i]['checked'])
            session.query(Users).filter(Users.openid==openid).update({'buy_car':old_buy_car})
            session.commit()
            return 0
    

def fname(filename):
	a=filename.split('.')
	if a[-1]!='jpg':
		filename=''
		i=0
		for i in range(0,len(a)-1):
			filename=filename+a[i]+'.'
			print(filename)
			i=i+1
	filename=filename+'jpg'
	return filename

def user_exist(openid):
    users=session.query(Users).filter(Users.openid==openid).all()
    res=[]
    for user in users:
        res.append(user.openid)
    if len(res) == 0:
        return False
    else:
        return True

def goods_exist(goods_id):
    goodss=session.query(Goods).filter(Goods.goods_id==goods_id).all()
    res=[]
    for goods in goodss:
        res.append(goods.goods_id)  
    if len(res)==0:
        return False
    else:
        return True

def deleteGoods(goods_id):
    goods=session.query(Goods).filter(Goods.goods_id==goods_id).first()
    session.delete(goods)

def randomRecommend():
    goods=session.query(Goods).limit(5).all()

    print(goods)
    return goods

def goodsRecommend(openid):
    user=get_user_from_openid(openid)
    custom=Custom()
    custom.matrix=user.like_matrix
    result=custom.static_reconmend()
    goods1=session.query(Goods).filter(Goods.kind2==result[0]).order_by(func.rand()).first()
    goods2=session.query(Goods).filter(Goods.kind2==result[1]).order_by(func.rand()).first()
    goods3=session.query(Goods).filter(Goods.kind2==result[2]).order_by(func.rand()).first()
    goods4=session.query(Goods).filter(Goods.kind2==result[3]).order_by(func.rand()).first()
    goods5=session.query(Goods).filter(Goods.kind2==result[4]).order_by(func.rand()).first()
    goods6=session.query(Goods).filter(Goods.kind2==result[5]).order_by(func.rand()).first()
    goods7=session.query(Goods).filter(Goods.kind2==result[6]).order_by(func.rand()).first()
    goods8=session.query(Goods).filter(Goods.kind2==result[7]).order_by(func.rand()).first()
    goods9=session.query(Goods).filter(Goods.kind2==result[8]).order_by(func.rand()).first()
    goods10=session.query(Goods).filter(Goods.kind2==result[9]).order_by(func.rand()).first()
    # goods3=session.query(Goods).filter(Goods.kind2==result[2]).first()
    goods_res=[goods1,goods2,goods3,goods4,goods5,goods6,goods7,goods8,goods9,goods10]
    res=[]
    for good in goods_res:
        if good is not None :
            if good not in res:
                res.append(good)
    return res

def chooseKind2(openid,searchName,choiceName,operation):
    user=get_user_from_openid(openid)
    custom=Custom()
    custom.matrix=user.like_matrix
    print(openid,searchName,choiceName,operation)
    custom.feedBack(searchName,choiceName,operation)
    session.query(Users).filter(Users.openid==openid).update({'like_matrix':custom.matrix})
    session.commit()


def goods_search_recommend(searchName,openid):
    user=get_user_from_openid(openid)
    custom=Custom()
    custom.matrix=user.like_matrix
    result=custom.recommend(searchName)
    goods1=session.query(Goods).filter(Goods.kind2==result[0]).first()
    goods2=session.query(Goods).filter(Goods.kind2==result[1]).first()
    goods3=session.query(Goods).filter(Goods.kind2==result[2]).first()
    goods4=session.query(Goods).filter(Goods.kind2==result[3]).first()
    goods5=session.query(Goods).filter(Goods.kind2==result[4]).first()
    goods6=session.query(Goods).filter(Goods.kind2==result[5]).first()
    goods7=session.query(Goods).filter(Goods.kind2==result[6]).first()
    goods8=session.query(Goods).filter(Goods.kind2==result[7]).first()
    goods9=session.query(Goods).filter(Goods.kind2==result[8]).first()
    goods10=session.query(Goods).filter(Goods.kind2==result[9]).first()
    # goods3=session.query(Goods).filter(Goods.kind2==result[2]).first()
    goods_res=[goods1,goods2,goods3,goods4,goods5,goods6,goods7,goods8,goods9,goods10]
    res=[]
    for good in goods_res:
        if good is not None :
            if good not in res:
                res.append(good)
    return res
# def changeInfo(goods_id,change,info):
#     goods=session.query(Goods).filter(Goods.goods_id==goods_id).first()
#     if change=='picture':
#         goods.picture=info
#         #print('1')
#         return True
#     if change=='name':
#         goods.name='sad'
#         session.commit()
#         #print('1')
#         return True
#     if change=='price':
#         goods.price=info
#         return True
#     if change=='description':
#         goods.description=info
#         return True
#     if change=='num':
#         goods.num=info
#         return True
#     if change=='tag':
#         goods.tag=info
#         return True
#     return 0

# newTest=Test(data={
#     'hgb':'son',
#     'lcy':'father'
# })

# session.add(newTest)
# session.commit()

# data=session.query(Test).all()
# print(data[0].data)

def buyGoods(goods_id,num,openid):
    goods=session.query(Goods).filter(Goods.goods_id==goods_id).first()
    if goods.num<num:
        return 0 
    else :
        goods.num=goods.num-num
        new_history={
            'goods_id':goods_id,
            'kind1':goods.kind1,
            'kind2':goods.kind2,
            'num':num,
            'picture':goods.picture,
            'description':goods.description,
            'price':goods.price
        }
        user=session.query(Users).filter(Users.openid==openid).first()
        old_history=user.buy_history
        old_buy_car=user.buy_car
        print('goods id is',goods_id)
        bought_goods=None
        for i in range(0,len(old_buy_car)):
            if old_buy_car[i].get('goods_id')==goods_id:
                bought_goods=old_buy_car[i]
        old_buy_car.remove(bought_goods)
        custom=Custom()
        custom.matrix=user.like_matrix
        custom.feedBack(bought_goods.get('kind2'),bought_goods.get('kind2'),'buy')
        print(bought_goods)
        print(0)
        print(old_buy_car)
        old_history.append(new_history)
        session.query(Users).filter(Users.openid==openid).update({'buy_history':old_history})
        session.commit()
        session.query(Users).filter(Users.openid==openid).update({'buy_car':old_buy_car})
        session.commit()

def getBuyHistory(openid):
    user=session.query(Users).filter(Users.openid==openid).filter().first()
    return user.buy_history

def check_admin(openid,goods_id):
    goods=session.query(Goods).filter(Goods.goods_id==goods_id).first()
    if goods.admin==openid:
        return True
    else:
        return False

def changeInfo(picture,description,name,price,goods_id,num,kind1,kind2,admin):
    # goods_change=session.query('Goods').filter(Goods.goods_id==goods_id).first()
    # new_goods=Goods(picture=picture,description=description,name=name,price=price,goods_id=goods_id,num=num,kind1=kind1,kind2=kind2)
    # goods_change.picture=picture
    # goods_change.description=description
    # goods_change.name=name
    # goods_change.price=price
    # goods_change.goods_id=goods_id
    # goods_change.num=num
    # goods_change.kind1=kind1
    # goods_change.kind2=kind2
    # a=get_user_from_openid(admin)
    # new_goods.admin.append(a)
    session.query(Goods).filter(Goods.goods_id==goods_id).update({'picture':picture})
    session.commit()
    session.query(Goods).filter(Goods.goods_id==goods_id).update({'name':name})
    session.commit()
    session.query(Goods).filter(Goods.goods_id==goods_id).update({'description':description})
    session.commit()
    session.query(Goods).filter(Goods.goods_id==goods_id).update({'price':price})
    session.commit()
    session.query(Goods).filter(Goods.goods_id==goods_id).update({'num':num})
    session.commit()
    session.query(Goods).filter(Goods.goods_id==goods_id).update({'kind1':kind1})
    session.commit()
    session.query(Goods).filter(Goods.goods_id==goods_id).update({'kind2':kind2})
    session.commit()


# add_user('openid')
# add_new_goods('picture','description','name',33,'goods_id',3,['tag1','tag2'],'openid')
# user=session.query(Users).filter(Users.openid=='openid').first()
# print(getBuyHistory('openid'))
# buyGoods('goods_id',1,'openid')
# user=session.query(Users).filter(Users.openid=='openid').first()
# print(getBuyHistory('openid'))
# buyGoods('goods_id',1,'openid')
# print(getBuyHistory('openid'))
# goods1=getGoodsInfo('goods_id')
# print(goods1.name)
# changeInfo('goods_id','name','asd')
# goods1=getGoodsInfo('goods_id')
# print(goods1.name)
# print(getBuyHistory('openid'))
# goods=session.query(Goods).filter(Goods.goods_id=='goods_id').first()
# print(goods.num)
# buyGoods('goods_id',1,'openid')
# goods=session.query(Goods).filter(Goods.goods_id=='goods_id').first()
# user=session.query(Users).filter(Users.openid=='openid').first()
# old_history=user.buy_history
# print(old_history)
# old_history.append({'asd':'das'})
# print(old_history)
# user.buy_history.append({'asd':'dsa'})
# print(user.buy_history)
# session.commit()
# print(goods.num)
# user=session.query(Users).filter(Users.openid=='openid').first()
# print(user.buy_history)

# user=session.query(Users).filter(Users.openid=='openid').first()
# print(user.buy_history)
# old_history=user.buy_history
# old_history.append('test')
# session.query(Users).filter(Users.openid=='openid').update({'buy_history':old_history})
# session.commit()
# user=session.query(Users).filter(Users.openid=='openid').first()
# print(user.buy_history)

# a=['qwe']
# a.append('ewq')
# print(a)
