# 后端

from flask import Flask, jsonify, render_template
from flask_cors import CORS
import common
import spider
import pipeline 
import jieba

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

CORS(app, resources=r'/*')

#######################################################################
# 萃取机控制 API

@app.route('/api/source/insert/<x>/')
def api_source_insert(x):
    common.query(common.readConfig("dbname_backend"),""" insert into in_src (bvid) values ("%s"); """%(x))
    return "ok"

@app.route('/api/template/insert/<x>/<int:y>/')
def api_template_insert(x, y):
    common.query(common.readConfig("dbname_backend"),""" insert into in_gen (description, tag) values ("%s",%d, %d); """%(x,y))
    return "ok"


@app.route('/api/source/searchinsert/<kw>/')
def api_source_insert_x(kw):
    res=spider.getSearchResult(kw)
    for i in range(min(len(res),20)):
        if i%2==1: continue
        bvid=res[i]
        common.query(common.readConfig("dbname_backend"),""" insert into in_src (bvid) values ("%s",%d); """%(bvid))
    return "ok"


@app.route('/api/template/searchinsert/<kw>/<int:tag>/')
def api_template_insert_x(kw, tag):
    res=spider.getSearchResult(kw)
    for i in range(min(len(res),10)):
        if i%2==1: continue
        bvid=res[i]
        common.query(common.readConfig("dbname_backend"),""" insert into in_gen (bvid, tag) values ("%s",%d, %d); """%(bvid,tag))
    return "ok"


@app.route('/api/source/delete/<bvid>/')
def apt_source_delete(bvid):
    common.query(common.readConfig("dbname_backend"),""" delete from in_src where bvid="%s"; """%(bvid))
    return "ok"

@app.route('/api/template/delete/<bvid>/<int:tag>/')
def api_template_delete(bvid, tag):
    common.query(common.readConfig("dbname_backend"),""" delete from in_gen where bvid="%s" and tag=%d; """%(bvid,tag))
    return "ok"


@app.route('/api/source/query/')
def api_source_query():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select * from in_src; """))

@app.route('/api/template/query/')
def api_template_query():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select * from in_gen; """))



@app.route('/api/status/source/')
def api_status_source():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select id, max(p) as prog from status where ext=0 and id like 'BV%' group by id; """))

@app.route('/api/status/templates/')
def api_status_templates():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select id, max(p) as prog from status where ext=1 and id not like 'OV%' group by id; """))

@app.route('/api/status/output/')
def api_status_output():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select id, max(p) as prog from status where ext=0 and id like 'OV%' group by id; """))

@app.route('/api/exec/')
def api_exec():
    if len(common.query(common.readConfig("dbname_backend"),""" select * from state_exec; """))>0:
        return "fail"
    common.query(common.readConfig("dbname_backend"),"""insert into state_exec (s) values ("s")""")
    pipeline.execute()
    return "ok"


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
    app.run(host="172.26.55.118", port=5000, debug=True)
