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
# url = 'https://d11.baidupcs.com/file/e64b1bed490d0c18eee00d48e2f5bb75?bkt=p3-0000c68e399db2a725c2e796fd08920c7da7&xcode=2aa47080c970b60beca704ff4ea6a188dacd30019c2e03ec6c16d630bd1a21e34b6fb1541247b96253831634a5b507f39a7e3ac4ae9d7ad8&fid=923560557-250528-403301876027105&time=1555862391&sign=FDTAXGERLQBHSKf-DCb740ccc5511e5e8fedcff06b081203-diurtTCB3s%2F8vtEvTV1Sz1ctR%2Fc%3D&to=d11&size=6095963&sta_dx=6095963&sta_cs=177&sta_ft=zip&sta_ct=5&sta_mt=3&fm2=MH%2CQingdao%2CAnywhere%2C%2Canhui%2Cct&ctime=1552445867&mtime=1555254421&resv0=cdnback&resv1=0&vuk=923560557&iv=0&htype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=0000c68e399db2a725c2e796fd08920c7da7&sl=76480590&expires=8h&rt=pr&r=143886941&mlogid=2574400854690343722&vbdid=2402823470&fin=00013822-RTLWlanU_MacOS10.9_MacOS10.14_Driver_1830.20.b35_1827.4.b33_UI_5.0.8.b5.zip&fn=00013822-RTLWlanU_MacOS10.9_MacOS10.14_Driver_1830.20.b35_1827.4.b33_UI_5.0.8.b5.zip&rtype=1&dp-logid=2574400854690343722&dp-callid=0.1.1&hps=1&tsl=80&csl=80&csign=5sr%2BtGIKAb5SQRN%2Buev5Rk5Msq4%3D&so=0&ut=6&uter=4&serv=0&uc=3242004348&ti=54c943154d862903c3b9f3eefebae6cbeea93ea789eaaaf6&by=themis'
url = 'https://nbcache00.baidupcs.com/file/a132aa40d8acf6c03e325eddc11cc61b?bkt=p3-1400a132aa40d8acf6c03e325eddc11cc61b161267e7000000d4a8fc&xcode=b5924b2995ee864e11555051eaa64299793ec9386b9b71e89b3e0dd587d2c11bb90cc3b40aff088753831634a5b507f39a7e3ac4ae9d7ad8&fid=923560557-250528-750570472797308&time=1555862658&sign=FDTAXGERLQBHSKf-DCb740ccc5511e5e8fedcff06b081203-bwJ4xhwmuudNjHeLMncpHjLNOPk%3D&to=h5&size=13936892&sta_dx=13936892&sta_cs=59&sta_ft=zip&sta_ct=7&sta_mt=7&fm2=MH%2CYangquan%2CAnywhere%2C%2Canhui%2Cct&ctime=1430843226&mtime=1505233078&resv0=cdnback&resv1=0&vuk=923560557&iv=0&htype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=1400a132aa40d8acf6c03e325eddc11cc61b161267e7000000d4a8fc&sl=76480590&expires=8h&rt=pr&r=401418071&mlogid=2574472536096508347&vbdid=2402823470&fin=burpsuite_pro_v1.6.17withloader.zip&fn=burpsuite_pro_v1.6.17withloader.zip&rtype=1&dp-logid=2574472536096508347&dp-callid=0.1.1&hps=1&tsl=80&csl=80&csign=5sr%2BtGIKAb5SQRN%2Buev5Rk5Msq4%3D&so=0&ut=6&uter=4&serv=0&uc=3242004348&ti=34c17094e7d5a0c904329f75e2466ca6da556809893a659b&by=themis'
down_file_name = 'Your file name'
# 如果该变量不填就会下载到运行程序的目录下
address = '/Users/niujie/Downloads/'  # 记得最后要加斜杠

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