# -*- coding: utf-8 -*-

import requests
import threading
from time import time
import json
import re


def downloadFile(URL, spos, epos, fp):
    try:
        header = {}
        header["Range"] = "bytes={}-{}".format(spos, epos)
        result = requests.get(URL, headers=header)
        fp.seek(spos)
        fp.write(result.content)
    except Exception:
        print(Exception)


def split_file(file_size):
    start_p = []
    end_p = []
    per_size = int(file_size / thread_num)
    int_size = per_size * thread_num  # 整除部分
    for i in range(0, int_size, per_size):
        start_p.append(i)
        end_p.append(i + per_size - 1)
    if int_size < file_size:  # size 不一定 n 等分，将不能等分余下的部分添加到最后一个 sub 里
        end_p[-1] = file_size
    return start_p, end_p


# 线程数量
thread_num = 30

# 需要填写的变量
 url = 'urlpagth'
down_file_name = 'Your file name'
# 如果该变量不填就会下载到运行程序的目录下
address = '/Users/root/Downloads/'  # 记得最后要加斜杠

file = open(address + down_file_name, 'wb')
res = requests.head(url)
# 若有单引号替换成双引号
json_data = re.sub('\'', '\"', str(res.headers))
head_dict = json.loads(json_data)
size = int(head_dict['Content-Length'])
start_pos, end_pos = split_file(size)

tmp = []
print('start download...')
t0 = time()
for i in range(0, thread_num):
    t = threading.Thread(
        target=downloadFile,
        args=(
            url,
            start_pos[i],
            end_pos[i],
            file))
    t.setDaemon(True)  # 主进程结束时，线程也随之结束
    t.start()
    tmp.append(t)
for i in tmp:
    i.join()

file.close()
t1 = time()
total_time = t1 - t0
speed = float(size) / (1000 * total_time)
print('total_time:%.2f s' % total_time)
print('speed:%.2f KB/s' % speed)
