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

@app.route('/api/source/insert/<bvid>/<int:src_type>/')
def api_source_insert(bvid, src_type):
    common.query(common.readConfig("dbname_backend"),""" insert into in_source (bvid, src_type) values ("%s",%d); """%(bvid,src_type))
    return "ok"

@app.route('/api/template/insert/<bvid>/<int:src_type>/<int:clip_type>/')
def api_template_insert(bvid, src_type, clip_type):
    common.query(common.readConfig("dbname_backend"),""" insert into in_templates (bvid, src_type, clip_type) values ("%s",%d, %d); """%(bvid,src_type,clip_type))
    return "ok"


@app.route('/api/source/searchinsert/<kw>/<int:src_type>/')
def api_source_insert_x(kw, src_type):
    res=spider.getSearchResult(kw)
    for i in range(min(len(res),20)):
        if i%2==1: continue
        bvid=res[i]
        common.query(common.readConfig("dbname_backend"),""" insert into in_source (bvid, src_type) values ("%s",%d); """%(bvid,src_type))
    return "ok"


@app.route('/api/template/searchinsert/<kw>/<int:src_type>/<int:clip_type>/')
def api_template_insert_x(kw, src_type, clip_type):
    res=spider.getSearchResult(kw)
    for i in range(min(len(res),10)):
        if i%2==1: continue
        bvid=res[i]
        common.query(common.readConfig("dbname_backend"),""" insert into in_templates (bvid, src_type, clip_type) values ("%s",%d, %d); """%(bvid,src_type,clip_type))
    return "ok"


@app.route('/api/source/delete/<bvid>/<int:src_type>/')
def apt_source_delete(bvid, src_type):
    common.query(common.readConfig("dbname_backend"),""" delete from in_source where bvid="%s" and src_type=%d; """%(bvid,src_type))
    return "ok"

@app.route('/api/template/delete/<bvid>/<int:src_type>/<int:clip_type>/')
def api_template_delete(bvid, src_type, clip_type):
    common.query(common.readConfig("dbname_backend"),""" delete from in_templates where bvid="%s" and src_type=%d and clip_type=%d; """%(bvid,src_type,clip_type))
    return "ok"


@app.route('/api/source/query/')
def api_source_query():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select * from in_source; """))

@app.route('/api/template/query/')
def api_template_query():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select * from in_templates; """))



@app.route('/api/status/source/')
def api_status_source():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select in_source.bvid, cast(round(count(*)*33.34) as signed) as progress from state_board inner join in_source on state_board.bvid=in_source.bvid group by in_source.bvid; """))

@app.route('/api/status/templates/')
def api_status_templates():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select in_templates.bvid, cast(round(count(distinct in_templates.bvid)*100) as signed) as progress from state_board inner join in_templates on state_board.bvid=in_templates.bvid group by in_templates.bvid; """))

@app.route('/api/status/output/')
def api_status_output():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select distinct TT.ovid, src_type, clip_type,progress  from (select ovid, cast(count(*)*50 as signed) as progress from (select ovid from state_gen union all select ovid from state_out) as T group by ovid) as TT inner join state_gen; """))

@app.route('/api/exec/')
def api_exec():
    if len(common.query(common.readConfig("dbname_backend"),""" select * from state_exec; """))>0:
        return "fail"
    common.query(common.readConfig("dbname_backend"),"""insert into state_exec (s) values ("s")""")
    pipeline.execute()
    return "ok"


######################################################################
# 视频终端 API

@app.route('/list/<int:src_type>/<int:clip_type>/')
def api_list(src_type, clip_type):
    sql_result = common.query(common.readConfig("dbname_backend"), "select id, bvid from extraction where src_type=%d and clip_type=%d order by rand();" % (
        src_type, clip_type), isDict=True)
    return jsonify(sql_result)


@app.route('/video/<name>/')
def api_video(name):
    return common.getBinaryFile("../data/output/%s.mp4" % name)


@app.route('/poster/<name>/')
def api_poster(name):
    return common.getBinaryFile("../data/poster/%s.jpg" % name)


@app.route('/assets/<name>/')
def api_assets(name):
    return common.getBinaryFile("assets/%s" % name)


@app.route('/vinfo/<xvid>/')
def api_vinfo(xvid):
    return jsonify(common.query(common.readConfig("dbname_backend"), """select * from Vinfo where bvid in (select bvid from extraction where id = '{xvid}');""".format(xvid=xvid), isDict=True))


@app.route('/xv/danmu/<xvid>/')
def api_vtdanmu(xvid):
    return jsonify(common.query(common.readConfig("dbname_backend"), """select text from (select text,abs(floattime-tm) as dt from Danmu,(select frame_begin/24 as tm from extraction 
        where id = '{xvid}') as T1 where cid in (select cid from Vinfo where bvid in 
        (select bvid from extraction where id = '{xvid}')) order by dt limit 20) as T2;""".format(xvid=xvid), isDict=False))


def wordFreqCount(txt):
    words = jieba.lcut(txt)
    counts = {}
    for word in words:
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word, 0) + 1
    items = list(counts.items())
    items.sort(key=lambda x: x[1], reverse=True)
    return items

@app.route('/xv/wordcloud/<xvid>/')
def api_vtwordcloud(xvid):
    sqlres= common.query(common.readConfig("dbname_backend"), """select text from (select text,abs(floattime-tm) as dt from Danmu,(select frame_begin/24 as tm from extraction 
        where id = '{xvid}') as T1 where cid in (select cid from Vinfo where bvid in 
        (select bvid from extraction where id = '{xvid}')) order by dt limit 200) as T2;""".format(xvid=xvid), isDict=False)
    lst = []
    cnt=100
    for i in sqlres:
        lst += [i[0]]
    str = ' '.join(lst)
    wf = wordFreqCount(str)
    ans = []
    for i in wf:
        ans += [{"name":i[0], "value":i[1]}]
        cnt -= 1
        if cnt == 0:
            break
    return jsonify(ans)


if __name__ == '__main__':
    app.run(host="172.26.55.117", port=5000, debug=True)
