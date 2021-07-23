from threading import Thread
import os
import common
import spider
import shotcut
import cutter
import generator
import editor
import time

global_ths=[]

# 装载已存在的视频文件，分析后加入素材库
def load(bvid):
    print("load",bvid)
    filename = "/root/mediahub/%s.mp4" % bvid
    if os.path.isfile(filename) == False:
        print("INVALID INPUT FILE.")
        return

    if len(common.query(common.readConfig("dbname"), "select * from state_board where bvid='%s' and `desc`='%s'"%(bvid,"media")))==0:
        spider.importMedia(bvid,filename)
        common.query(common.readConfig("dbname"), "insert ignore into state_board (bvid,`desc`) values ('%s','%s')" % (bvid,"media"))
    
    if len(common.query(common.readConfig("dbname"), "select * from state_board where bvid='%s' and `desc`='%s'"%(bvid,"info")))==0:
        spider.downloadInfo(bvid)
        common.query(common.readConfig("dbname"), "insert ignore into state_board (bvid,`desc`) values ('%s','%s')" % (bvid,"info"))

    if len(common.query(common.readConfig("dbname"), "select * from state_board where bvid='%s' and `desc`='%s'"%(bvid,"cut")))==0:
        cutter.solve(bvid, 0)
        common.query(common.readConfig("dbname"), "insert ignore into state_board (bvid,`desc`) values ('%s','%s')" % (bvid,"cut"))

# 从网络拉取视频文件，分析后加入素材库
def pull(bvid):
    print("pull",bvid)
    if len(common.query(common.readConfig("dbname"), "select * from state_board where bvid='%s' and `desc`='%s'"%(bvid,"media")))==0:
        spider.downloadMedia(bvid)
        common.query(common.readConfig("dbname"), "insert ignore into state_board (bvid,`desc`) values ('%s','%s')" % (bvid,"media"))

    if len(common.query(common.readConfig("dbname"), "select * from state_board where bvid='%s' and `desc`='%s'"%(bvid,"info")))==0:
        spider.downloadInfo(bvid)
        common.query(common.readConfig("dbname"), "insert ignore into state_board (bvid,`desc`) values ('%s','%s')" % (bvid,"info"))

    if len(common.query(common.readConfig("dbname"), "select * from state_board where bvid='%s' and `desc`='%s'"%(bvid,"cut")))==0:
        cutter.solve(bvid, 0)
        common.query(common.readConfig("dbname"), "insert ignore into state_board (bvid,`desc`) values ('%s','%s')" % (bvid,"cut"))


def downloadTemplate(template_bvid):
    if len(common.query(common.readConfig("dbname"),  """ select * from in_source where bvid='%s'; """%template_bvid ))>0:
        print("Template is already in source. No need to download. ",template_bvid)
        return
    if len(common.query(common.readConfig("dbname"), "select * from state_board where bvid='%s' and `desc`='%s'"%(template_bvid,"media")))==0:
        spider.downloadMedia(template_bvid)
        common.query(common.readConfig("dbname"), "insert ignore into state_board (bvid,`desc`) values ('%s','%s')" % (template_bvid,"media"))

# 生成剪辑描述表
def generate(src_type, clip_type):
    print("generate",src_type,clip_type)
    template_list=common.query(common.readConfig("dbname"), "select bvid from in_templates where src_type=%d and clip_type=%d;"%(src_type, clip_type))
    handles=[]
    def _solve_one(template_bvid):
        if len(common.query(common.readConfig("dbname"), "select * from state_board where bvid='%s' and `desc`='%s'"%(template_bvid,"media")))==0:
            spider.downloadMedia(template_bvid)
            common.query(common.readConfig("dbname"), "insert ignore into state_board (bvid,`desc`) values ('%s','%s')" % (template_bvid,"media"))
        if len(common.query(common.readConfig("dbname"), "select * from state_gen where bvid='%s' and src_type=%d and clip_type=%d"%(template_bvid,src_type,clip_type)))==0:
            ovid = generator.generate(template_bvid, src_type, clip_type)
            common.query(common.readConfig("dbname"), "insert ignore into state_gen (ovid,`desc`,bvid,src_type,clip_type) values ('%s','%s','%s',%d,%d)" %(ovid,"ok",template_bvid,src_type,clip_type))
    for i in template_list:
        template_bvid=i[0]
        th = Thread(target=_solve_one,args=(template_bvid,))
        th.start()
        handles.append(th)
    for i in handles:
        i.join()

# 根据剪辑描述表剪辑视频
def edit():
    print("edit")
    outvideo_list=common.query(common.readConfig("dbname"), "select distinct ovid from out_editdesc;")
    for i in outvideo_list:
        ovid=i[0]
        if len(common.query(common.readConfig("dbname"), "select * from state_out where ovid='%s' and `desc`='%s'"%(ovid,"ok")))==0:
            edit_desc = common.query(common.readConfig("dbname"), "select * from out_editdesc where ovid='%s';"%ovid, isDict=True)
            output_filename="../data/edited/%s.mp4"%ovid
            editor.edit(edit_desc,output_filename+".temp.mp4")
            template_bvid=common.query(common.readConfig("dbname"), "select bvid from out_template where ovid='%s'"%ovid)[0][0]
            os.system("ffmpeg -i "+output_filename+".temp.mp4"+" -i ../data/media/%s.hd.mp4 -c copy -map 0:0 -map 1:1 -y %s %s" % (template_bvid,output_filename,common.readConfig("ffmpeg_quiet")))
            common.query(common.readConfig("dbname"), "insert ignore into state_out (ovid,`desc`) values ('%s','%s')" % (ovid,"ok"))

# 将视频和相关信息推送到发布池
def publish(ovid):
    print("to be continue")

# sql_res = common.query("banime", "select distinct bvid from Vinfo")
# for i in sql_res[:1]:
#     load(i[0])

def main():
    common.query(common.readConfig("dbname"), "truncate table state_board")
    common.query(common.readConfig("dbname"), "truncate table state_gen")
    common.query(common.readConfig("dbname"), "truncate table state_out")
    common.query(common.readConfig("dbname"), "truncate table out_editdesc")
    common.query(common.readConfig("dbname"), "truncate table out_template")
    common.query(common.readConfig("dbname"), "truncate table extraction")
    source_list=common.query(common.readConfig("dbname"), "select distinct bvid from in_source;")
    template_list=common.query(common.readConfig("dbname"), "select distinct bvid from in_templates;")
    time_begin=time.time()
    # 并行拉取
    handles=[]
    for i in source_list:
        bvid=i[0]
        th = Thread(target=pull,args=(bvid,))
        th.start()
        handles.append(th)

    for i in template_list:
        bvid=i[0]
        th = Thread(target=downloadTemplate,args=(bvid,))
        th.start()
        handles.append(th)
    for i in handles:
        i.join()
    time_pull=time.time()-time_begin
    # 生成阶段
    generate(0,0)
    time_gen=time.time()-time_pull-time_begin
    # 输出阶段
    edit()
    time_out=time.time()-time_gen-time_pull-time_begin
    print("各阶段用时：",time_pull,time_gen,time_out)
    common.query(common.readConfig("dbname_backend"),""" truncate table state_exec; """)
    
# def main_test():
#     print("hahaha")
#     common.query(common.readConfig("dbname_backend"),""" truncate table state_exec; """)

def execute():
    th=Thread(target=main)
    th.start()
    global_ths.append(th)

if __name__=="__main__":
    main()