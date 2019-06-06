import memcache

mc=memcache.Client(['127.0.0.1:11211'],debug=True)

# mc.set('username','zhiliao',time=120)
# mc.set('age',12,time=120)

# mc.set_multi({
#     'title':'钢铁是怎样炼成的',
#     'content':'xxx',
#     'page':'123'
# })

def check(key):
    res=mc.get(key)
    if res is not None:
        return (True)
    else:
        return (False)


def store_session(session,openid,time):
    mc.set(session,openid,time=time)



# mc.set('asd','dsa')
# print(mc.get('asd'))