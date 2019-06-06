from flask import Flask,request,jsonify,send_from_directory,send_file
import requests
from mem import *
from models import*
from md5 import *
import json
from time_stamp import *
from x import *


app=Flask(__name__)

methods=['POST','GET']

appid='wx266cdbdce2e62a92'
secret='28bdc3dc03849b27f03c3b1c28d083ab'

@app.route('/index')
def index():
    return 'this is index page'

@app.route('/delete_buy_car')
def delete_buy_car():
    session=request.args.get('session')
    goods_id=request.args.get('goods_id')
    openid=get_openid_from_session_key(session)
    deleteBuyCar(openid,goods_id)
    current_buy_car=getBuyCar(openid)
    return jsonify({
        'flag':'success',
        'current_buy_car':current_buy_car
    })

@app.route('/add_buy_car',methods=methods)
def add_buy_car():
    session=request.args.get('session')
    goods_id=request.args.get('goods_id')
    num=request.args.get('num')
    checked=request.args.get('checked')
    openid=get_openid_from_session_key(session)
    addBuyCar(openid,goods_id,num,checked)
    current_buy_car=getBuyCar(openid)
    return jsonify({
        'flag':'success',
        'current_buy_car':current_buy_car
    })

@app.route('/change_checked')
def change_checked():
    checked=request.args.get('checked')
    session=request.args.get('session')
    openid=get_openid_from_session_key(session)
    goods_id=request.args.get('goods_id')
    changeChecked(openid,goods_id,checked)
    current_buy_car=getBuyCar(openid)
    return jsonify({
        'flag':'success',
        'current_buy_car':current_buy_car
    })

@app.route('/get_file/<filename>')
def get_file(filename):
    filename='pictures/'+filename
    return send_file(filename)

@app.route('/get_buy_car',methods=methods)
def get_buy_car():
    session=request.args.get('session')
    openid=get_openid_from_session_key(session)
    buy_car=getBuyCar(openid)
    return jsonify({
        'buy_car':buy_car
    })

@app.route('/first_login',methods=methods) #登录小程序储存用户信息
def first_login():
    jscode=request.args.get('code')
    print(jscode)
    url='https://api.weixin.qq.com/sns/jscode2session'
    params={
        'appid':appid,
        'secret':secret,
        'js_code':jscode,
        'grant_type':'authorization_code'
    }
    print('before_request')
    res=requests.get(url,params=params)
    print('after')
    data=json.loads(res.text)

    openid=data.get('openid')
    session=md5_encode(str(openid)+str(make_time_stamp()))
    print('session',session)
    store_session(session,openid,3600)
    if not user_exist(openid):
        add_user(openid)
    return jsonify({
            'flag':'success',
            'session':session
        })
    
@app.route('/get_my_goods')
def get_my_goods():
    session=request.args.get('session')
    openid=get_openid_from_session_key(session)
    goods=getMyGoods(openid)
    my_goods=[]
    for good in goods:
        my_good={
            'price':good.price,
            'name':good.name,
            'description':good.description,
            'picture':good.picture,
            'goods_id':good.goods_id,
            'num':good.num,
            'kind1':good.kind1,
            'kind2':good.kind2
        }
        my_goods.append(my_good)
    return jsonify({
        'flag':'success',
        'my_goods':my_goods
    })
 
@app.route('/recommend')
def goods_recommend():
    session=request.args.get('session')
    if session == 'null':
        res=[]
        goods=randomRecommend()
        for good in goods:
            data={
            'price':good.price,
            'name':good.name,
            'description':good.description,
            'picture':good.picture,
            'goods_id':good.goods_id,
            'kind2':good.kind2
            }
            res.append(data)
        return jsonify({
            'data':res
        })
    openid=get_openid_from_session_key(session)
    if openid is None:
        res=[]
        goods=randomRecommend()
        for good in goods:
            data={
            'price':good.price,
            'name':good.name,
            'description':good.description,
            'picture':good.picture,
            'goods_id':good.goods_id,
            'kind2':good.kind2
            }
            res.append(data)
        return jsonify({
            'data':res
        })
        
    result=goodsRecommend(openid)
    res=[]
    for good in result:
        data={
            'price':good.price,
            'name':good.name,
            'description':good.description,
            'picture':good.picture,
            'goods_id':good.goods_id,
            'kind2':good.kind2
        }
        res.append(data)
    return jsonify({
        'data':res
    })
    

@app.route('/add_goods',methods=methods)  #商品上架
def add_goods():
    session=request.form.get('session')
    openid=get_openid_from_session_key(session)
    name=request.form.get('name')
    kind1=request.form.get('kind1')
    change_flag=request.form.get('change_flag')
    old_goods_id=request.form.get('goods_id')
    if kind1=='shipin':
        kind1='食品'
    if kind1=='nvzhuang':
        kind1='女装'
    if kind1=='xihu':
        kind1='洗护'
    if kind1=='baihuo':
        kind1='百货'
    if kind1=='shuma':
        kind1='数码'
    if kind1=='xiexue':
        kind1='鞋靴'
    if kind1=='yundong':
        kind1='运动'
    if kind1=='meizhuang':
        kind1='美妆'
    if kind1=='nanzhuang':
        kind1='男装'
    if kind1=='zhuangshi':
        kind1='装饰'
    kind2=request.form.get('kind2')
    picture=request.files['picture']
    goods_id=md5_encode(openid+str(make_time_stamp()))
    fname='pictures/'+goods_id+'.jpg'
    picture.save(fname)
    num=request.form.get('num')
    price=request.form.get('price')
    description=request.form.get('description')    
    filename=goods_id+'.jpg'
    if int(change_flag)!=0:
        changeInfo(filename,description,name,price,old_goods_id,num,kind1,kind2,openid) 
    else:
        add_new_goods(filename,description,name,price,goods_id,num,kind1,kind2,openid)
    return jsonify({ 
        'flag':'success'
    })

@app.route('/delete_goods',methods=methods) #商品下架
def delete_goods():
    session=request.form.get('session')
    openid=get_openid_from_session_key(session)
    goods_id=request.form.get('goods_id')
    if not goods_exist(goods_id):
        return jsonify({
            'flag':'goods_not_exist'
        })
    deleteGoods(goods_id)
    return jsonify({
        'flag':'success'
    })

@app.route('/buy',methods=methods) #商品购买
def buy():
    session=request.args.get('session')
    openid=get_openid_from_session_key(session)
    goods_buy=request.args.get('data')
    goods_buy=json.loads(goods_buy)
    print('025')
    print(goods_buy)
    a=len(goods_buy)
    for i in range(0,a):
        num=int(goods_buy[i].get('num'))
        goods_id=goods_buy[i].get('goods_id')
        buyGoods(goods_id,num,openid)
    current_buy_car=getBuyCar(openid)
    return jsonify({
        'flag':'success',
        'current_buy_car':current_buy_car
    })

@app.route('/get_buy_history',methods=methods)#获取购买历史记录
def get_buy_history():
    session=request.args.get('session')
    openid=get_openid_from_session_key(session)
    buy_history=getBuyHistory(openid)
    return jsonify({
        'flag':'success',
        'data':buy_history
    })

# @app.route('/change_info',methods=methods)#修改商品信息
# def change_info():
#     session=request.args.get('session')
#     openid=get_openid_from_session_key(session)
#     goods_id=request.args.get('goods_id')
#     if not check_admin(openid,goods_id):
#         return jsonify({
#             'flag':'not_admin'
#         })
#     change=request.form.get('change')
#     info=request.form.get('info')
#     if changeInfo(goods_id,change,info):
#         return jsonify({
#             'flag':'success'
#         })
#     else:
#         return jsonify({
#             'flag':'error'
#         })

@app.route('/get_goods_info',methods=methods)
def get_goods_info():
    goods_id=request.form.get('goods_id')
    if not goods_exist(goods_id):
        return jsonify({
            'flag':'goods_not_exist'
        })
    goods=getGoodsInfo(goods_id)
    return jsonify({
        'picture':goods.picture,
        'description':goods.description,
        'name':goods.name,
        'price':goods.price,
        'goods_id':goods_id,
        'num':goods.num,
        'tag':goods.tag,
        'admin':goods.admin
    })
    
@app.route('/choose_kind2')
def choose_kind2():
    session=request.args.get('session')
    openid=get_openid_from_session_key(session)
    searchName=request.args.get('searchName')
    choiceName=request.args.get('choose_kind')
    operation=request.args.get('operation')
    print(choiceName,'searchName')
    chooseKind2(openid,searchName,choiceName,operation)
    return jsonify({
        'flag':'success' 
    })

@app.route('/search_goods_by_kind',methods=methods)
def search_goods_by_kind():
    session=request.args.get('session')
    openid=get_openid_from_session_key(session)
    kind1=request.args.get('kind1')
    kind2=request.args.get('kind2')
    word=request.args.get('word')
    goods=search_by_kind(kind1,kind2,word)
    data=[]
    i=0
    for good in goods:
        data.append({
            'id':i+1,
            'price':good.price,
            'name':good.name,
            'description':good.description,
            'picture':good.picture,
            'goods_id':good.goods_id,
            'kind2':good.kind2
        })
    data_rec=goods_search_recommend(kind2,openid)
    for good in data_rec:
        data.append({
            'id':i+1,
            'price':good.price,
            'name':good.name,
            'description':good.description,
            'picture':good.picture,
            'goods_id':good.goods_id,
            'kind2':good.kind2
        })
    if kind1!=None and kind2!= None :
        return jsonify({
            'data':data
        })
    return 'success'

if __name__=='__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)    

