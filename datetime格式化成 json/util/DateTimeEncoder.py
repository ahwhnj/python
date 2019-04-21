# -*- coding: utf-8 -*-

import datetime,json
import re
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    now = datetime.datetime.now()
    print DateTimeEncoder().default(obj=now)
