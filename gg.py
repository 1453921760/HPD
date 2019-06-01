x = "我是你爹"
import re 

data = ["我是你爹","你是我儿子","我是你爷爷的爹","叫我爸爸","叫我爷爷","李晨阳是gb"]
            #将数据库的所有商品的名字给出来,类型为list


def fuzzyMatch(name,data):

    zset = [x for x in name]
    eset = {}
    for x in zset:
        for y in data:
            tmp = re.match(r".*%s.*"%(x),y)
            if tmp != None:
                if tmp.group(0) in eset.keys() :
                    eset[tmp.group(0)] = eset[tmp.group(0)] + 1
                else :
                    eset[tmp.group(0)] = 0
    r = [i+2 for i in range(len(name)-2)]
    for i in r :
        for j in range(len(name)):
            x1 = name[j:j+i]
            if len(x1)== i:
                for y in data:
                    tmp = re.match(r".*%s.*"%(x1),y)
                    if tmp != None:
                        if tmp.group(0) in eset.keys() :
                            eset[tmp.group(0)] = eset[tmp.group(0)] + 1
                







    return list(dict(sorted(eset.items(),key=lambda x:x[1],reverse = True)))



print(fuzzyMatch("我是你爹",data))