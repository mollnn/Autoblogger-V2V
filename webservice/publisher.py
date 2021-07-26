from posix import times_result
import common
import spider
import os
from common import sqlQuery
import time
from threading import Thread
import time
import json
from bilibili import main
from common import conf

def run(ovid, title_prefix="AI混剪:第二轮测试,参数")->None:
    title='{pref}:{}'.format(title_prefix,int(time.time()))
    video_path='../data/edited/{}.mp4'.format(ovid)
    cover_path='../data/poster/{}.jpg'.format(ovid)
    config_path='videoconfig.json'
    vc={}
    with open(config_path,'r',encoding='utf8')as fp:
        vc = json.load(fp)
    vc['video_path']=video_path
    vc['cover_path']=cover_path
    vc['config']['title']=title
    vc['config']['desc']=ovid
    
    with open(config_path,'w',encoding='utf8')as fp:
        json.dump(vc,fp,ensure_ascii=False)
    
    main()


def publish(ovid):
    print("publish",ovid)
    run(ovid, title_prefix=conf("title_prefix"))
    print("pub finish")