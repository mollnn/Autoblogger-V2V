import common
import os
import ffmpeg
from common import conf
from common import sqlQuery

# 剪辑描述符 edit_desc is a list of dict{'xvid'=?, 'start'=?, 'duration'=?}


def generateByConcatAll(description, tag):
    # 此函数返回一个剪辑描述符
    # 自行从数据表 extraction 中读取素材
    src_clips = sqlQuery("select id, fe-fb as len from extraction")
    return [{"xvid":src_clip[0],"start":0,"duration":src_clip[1]/24} for src_clip in src_clips]

def generateByVideoTemplate(template_bvid, tag):
    # 此函数返回一个剪辑描述符
    # 自行从数据表 extraction 中读取素材
    return []

def edit(edit_desc, output_filename):
    # 根据剪辑描述符剪辑视频
    # 先把每个片段切成 .ts
    ts_list=[]
    for i in edit_desc:
        tsid=common.generateTempid()
        ts_list.append(tsid)
        os.system("ffmpeg -i {fin} -ss {ts} -t {tt} -b:v 20000k {fout} {fg}".format(
            fin="../data/output/%s.hd.mp4"%i["xvid"],
            ts=i["start"],
            tt=i["duration"],
            fout="../tmp/%s.ts"%tsid,
            fg=conf("ffmpeg_default")
        ))
    # 将一堆 .ts 合并并重新编码
    os.system(""" ffmpeg -i "concat:{fin}" {fconf} {fout} {fg}""".format(
        fin="|".join(["../tmp/%s.ts"%tsid for tsid in ts_list]),
        fconf="-vcodec libx264 -acodec aac -b:v 1000k",
        fout=output_filename,
        fg=conf("ffmpeg_default")
    ))

def writeEditDesc(ovid, edit_desc):
    id=0
    for i in edit_desc:
        sqlQuery("insert into editdesc (ovid,id,xvid,tb,te) values ('%s',%d,'%s',%f,%f)"%(
            ovid, id, i["xvid"], i["start"],i["duration"]
        ))
        id+=1

def main(description, tag):
    # description: 生成方法描述
    # tag: 素材标记号
    # 按照 description 的方法（可能是视频模板，可能是音乐），利用所有带 tag 的素材生成视频
    ovid=common.generateOvid()
    if description=="ConcatAll":
        edit_desc = generateByConcatAll(description, tag)
    elif len(description)>2 and description[0:2]=="BV":
        # 按视频模板剪辑
        edit_desc = generateByVideoTemplate(description, tag)
    # 根据剪辑描述符剪辑视频
    edit(edit_desc, "../data/edited/%s.mp4"%ovid)
    # 将剪辑描述符写入数据库
    writeEditDesc(ovid, edit_desc)