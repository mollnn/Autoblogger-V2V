# 后端

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import common
import spider
import pipeline 
import jieba
from threading import Thread
from common import sqlQuery

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

CORS(app, resources=r'/*')

app_thread_handles=[]

#######################################################################
# 萃取机控制 API

### 参数说明
# bvid：你懂的
# template 的 bvid：用作模板的 bvid，实际上已经被泛化，但总归是一个字符串
# tag: 每个 XV 和 OV 以及 Template 会唯一对应一个 tag，表示它的类型
# 源素材在表 in_src 中，生成描述（模板）在表 in_gen 中

# 添加 bvid 作为素材
@app.route('/api/source/insert/<bvid>/')
def api_source_insert(bvid):
    common.query(common.readConfig("dbname_backend"),""" insert into in_src (bvid) values ("%s"); """%bvid)
    return "ok"

# 添加 bvid with tag 作为模板
@app.route('/api/template/insert/<bvid>/<int:tag>/')
def api_template_insert(bvid, tag):
    common.query(common.readConfig("dbname_backend"),""" insert into in_gen (description, tag) values ("%s", %d); """%(bvid,tag))
    return "ok"

# 去 B 站搜索 kw，将结果 bvid 添加为素材
@app.route('/api/source/searchinsert/<kw>/')
def api_source_insert_x(kw):
    res=spider.getSearchResult(kw)
    for i in range(min(len(res),20)):
        if i%2==1: continue
        bvid=res[i]
        common.query(common.readConfig("dbname_backend"),""" insert into in_src (bvid) values ("%s"); """%(bvid))
    return "ok"

# 去 B 站搜索 kw，将结果 bvid with tag 添加为模板
@app.route('/api/template/searchinsert/<kw>/<int:tag>/')
def api_template_insert_x(kw, tag):
    res=spider.getSearchResult(kw)
    for i in range(min(len(res),10)):
        if i%2==1: continue
        bvid=res[i]
        common.query(common.readConfig("dbname_backend"),""" insert into in_gen (description, tag) values ("%s", %d); """%(bvid,tag))
    return "ok"

# 删除素材
@app.route('/api/source/delete/<bvid>/')
def api_source_delete(bvid):
    common.query(common.readConfig("dbname_backend"),""" delete from in_src where bvid="%s"; """%(bvid))
    return "ok"

# 删除模板
@app.route('/api/template/delete/<bvid>/<int:tag>/')
def api_template_delete(bvid, tag):
    common.query(common.readConfig("dbname_backend"),""" delete from in_gen where bvid="%s" and tag=%d; """%(bvid,tag))
    return "ok"

# 清空素材
@app.route('/api/source/clear/')
def api_source_clear():
    common.query(common.readConfig("dbname_backend"),""" truncate table in_src; """)
    return "ok"

# 清空模板
@app.route('/api/template/clear/')
def api_template_clear():
    common.query(common.readConfig("dbname_backend"),""" truncate table in_gen """)
    return "ok"

# 查询素材
@app.route('/api/source/query/')
def api_source_query():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select * from in_src; """))

# 查询模板
@app.route('/api/template/query/')
def api_template_query():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select * from in_gen; """))

# 进度监控：媒体载入段
@app.route('/api/status/load/')
def api_status_source():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select id, max(p) as prog from status where ext=0 and id like 'BV%' group by id; """))

# 进度监控：片段提取段
@app.route('/api/status/extract/')
def api_status_templates():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select id, max(p) as prog from status where ext=1 and id not like 'OV%' group by id; """))

# 进度监控：成片生成段
@app.route('/api/status/generate/')
def api_status_output():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select id, max(p) as prog from status where ext=0 and id like 'OV%' group by id; """))

# 执行任务（自带互斥）
@app.route('/api/exec/')
def api_exec():
    if len(common.query(common.readConfig("dbname_backend"),""" select * from status_mutex; """))>0:
        return "fail"
    common.query(common.readConfig("dbname_backend"),"""insert into status_mutex (s) values ("s")""")

    def A():
        print("new exec start")
        pipeline.execute()
        common.query(common.readConfig("dbname_backend"),"""truncate table status_mutex""")

    th = Thread(target=A)
    th.start()
    app_thread_handles.append(th)
    return "ok"

# 查看成片列表
@app.route('/api/ov/list/')
def api_ov_list():
    return jsonify(sqlQuery("select * from out_info "))

# 下载生成的媒体
@app.route('/api/ov/video/<name>/')
def api_video(name):
    return common.getBinaryFile("../data/edited/%s.mp4" % name)

# 下载生成的封面
@app.route('/api/ov/poster/<name>/')
def api_poster(name):
    return common.getBinaryFile("../data/poster/%s.jpg" % name)

######################################################################
# 视频终端 API

# @app.route('/list/<int:src_type>/<int:tag>/')
# def api_list(src_type, tag):
#     sql_result = common.query(common.readConfig("dbname_backend"), "select id, bvid from extraction where src_type=%d and tag=%d order by rand();" % (
#         src_type, tag), isDict=True)
#     return jsonify(sql_result)


# @app.route('/video/<name>/')
# def api_video(name):
#     return common.getBinaryFile("../data/output/%s.mp4" % name)


# @app.route('/poster/<name>/')
# def api_poster(name):
#     return common.getBinaryFile("../data/poster/%s.jpg" % name)


# @app.route('/assets/<name>/')
# def api_assets(name):
#     return common.getBinaryFile("assets/%s" % name)


# @app.route('/vinfo/<xvid>/')
# def api_vinfo(xvid):
#     return jsonify(common.query(common.readConfig("dbname_backend"), """select * from Vinfo where bvid in (select bvid from extraction where id = '{xvid}');""".format(xvid=xvid), isDict=True))


# @app.route('/xv/danmu/<xvid>/')
# def api_vtdanmu(xvid):
#     return jsonify(common.query(common.readConfig("dbname_backend"), """select text from (select text,abs(floattime-tm) as dt from Danmu,(select frame_begin/24 as tm from extraction 
#         where id = '{xvid}') as T1 where cid in (select cid from Vinfo where bvid in 
#         (select bvid from extraction where id = '{xvid}')) order by dt limit 20) as T2;""".format(xvid=xvid), isDict=False))


# def wordFreqCount(txt):
#     words = jieba.lcut(txt)
#     counts = {}
#     for word in words:
#         if len(word) == 1:
#             continue
#         else:
#             counts[word] = counts.get(word, 0) + 1
#     items = list(counts.items())
#     items.sort(key=lambda x: x[1], reverse=True)
#     return items

# @app.route('/xv/wordcloud/<xvid>/')
# def api_vtwordcloud(xvid):
#     sqlres= common.query(common.readConfig("dbname_backend"), """select text from (select text,abs(floattime-tm) as dt from Danmu,(select frame_begin/24 as tm from extraction 
#         where id = '{xvid}') as T1 where cid in (select cid from Vinfo where bvid in 
#         (select bvid from extraction where id = '{xvid}')) order by dt limit 200) as T2;""".format(xvid=xvid), isDict=False)
#     lst = []
#     cnt=100
#     for i in sqlres:
#         lst += [i[0]]
#     str = ' '.join(lst)
#     wf = wordFreqCount(str)
#     ans = []
#     for i in wf:
#         ans += [{"name":i[0], "value":i[1]}]
#         cnt -= 1
#         if cnt == 0:
#             break
#     return jsonify(ans)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
