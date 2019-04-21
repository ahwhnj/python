# -*- coding: utf-8 -*-

import datetime,json
from util.DateTimeEncoder import DateTimeEncoder


class test(object):
    def dump(self):
        now = datetime.datetime.now()  #获取当前时间
        day = datetime.date.today()    #获取当天日期
        print type(day)

        #造一个dict
        data ={
                    "a":"b",
                    "c":[
                        "d","f"
                    ],
                    "g":[
                        {"a":now},
                        {"a":day}
                    ]
                }
        #将字典转化成 json输出.
        # print json.dumps(data,ensure_ascii=False,indent=4,cls=DateTimeEncoder)
        # print json.dumps(now,cls=DateTimeEncoder)
        # print json.dumps(day,cls=DateTimeEncoder)
        # return json.dumps(data,ensure_ascii=False,indent=4,cls=DateTimeEncoder)
        return json.dumps(data,cls=DateTimeEncoder)

if __name__ =='__main__':
    test().dump()