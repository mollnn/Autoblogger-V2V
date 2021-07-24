from threading import Thread
import os
import common
import spider
import shotcut
import cutter
import generator
import editor
import time

global_ths = []


def load(bvid):
    # 装载已存在的视频文件，分析后加入素材库
    filename = "/root/mediahub/%s.mp4" % bvid
    spider.importMedia(bvid, filename)
    spider.downloadInfo(bvid)
    cutter.solve(bvid, 0)


def pull(bvid):
    # 从网络拉取视频文件，分析后加入素材库
    spider.downloadMedia(bvid)
    spider.downloadInfo(bvid)
    cutter.solve(bvid, 0)


def downloadTemplate(template_bvid):
    # 从网络下载模板文件
    if len(common.query(common.readConfig("dbname"),  """ select * from in_source where bvid='%s'; """ % template_bvid)) > 0:
        print("Template is already in source. No need to download. ", template_bvid)
        return
    spider.downloadMedia(template_bvid)


def generate(src_type, clip_type):
    # 生成剪辑描述表
    template_list = common.query(common.readConfig("dbname"), "select bvid from in_templates where src_type=%d and clip_type=%d;" % (src_type, clip_type))
    handles = []
    for i in template_list:
        template_bvid = i[0]
        ovid = generator.generate(template_bvid, src_type, clip_type)


def edit():
    # 根据剪辑描述表剪辑视频
    outvideo_list = common.query(common.readConfig("dbname"), "select distinct ovid from out_editdesc;")
    for i in outvideo_list:
        ovid = i[0]
        editor.edit_by_ovid(ovid)


def publish(ovid):
    # 将视频和相关信息推送到发布池
    print("to be continue")


def main():
    common.query(common.readConfig("dbname"), "truncate table out_editdesc")
    common.query(common.readConfig("dbname"), "truncate table out_template")
    common.query(common.readConfig("dbname"), "truncate table extraction")

    time_begin = time.time()
    # 读取源素材列表和模板列表并拉取
    source_list = common.query(common.readConfig(
        "dbname"), "select distinct bvid from in_source;")
    template_list = common.query(common.readConfig(
        "dbname"), "select distinct bvid from in_templates;")
    for i in source_list:
        bvid = i[0]
        pull(bvid)
    for i in template_list:
        downloadTemplate(bvid)
    time_pull = time.time()-time_begin
    # 生成阶段
    generate(0, 0)
    time_gen = time.time()-time_pull-time_begin
    # 输出阶段
    edit()
    # 你可以在这里添加输出后操作，如生成介绍、上传发布等
    time_out = time.time()-time_gen-time_pull-time_begin
    print("各阶段用时：", time_pull, time_gen, time_out)

def execute():
    th = Thread(target=main)
    th.start()
    global_ths.append(th)


if __name__ == "__main__":
    main()
