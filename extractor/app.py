from flask import Flask, jsonify, render_template
from flask_cors import CORS
import common
import spider
# import pipeline 

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

CORS(app, resources=r'/*')


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
        bvid=res[i]
        common.query(common.readConfig("dbname_backend"),""" insert into in_source (bvid, src_type) values ("%s",%d); """%(bvid,src_type))
    return "ok"


@app.route('/api/template/searchinsert/<kw>/<int:src_type>/<int:clip_type>/')
def api_template_insert_x(kw, src_type, clip_type):
    res=spider.getSearchResult(kw)
    for i in range(min(len(res),5)):
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
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select in_templates.bvid, cast(round(count(*)*100) as signed) as progress from state_board inner join in_templates on state_board.bvid=in_templates.bvid group by in_templates.bvid; """))

@app.route('/api/status/output/')
def api_status_output():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select distinct TT.ovid, src_type, clip_type,progress  from (select ovid, cast(count(*)*50 as signed) as progress from (select ovid from state_gen union all select ovid from state_out) as T group by ovid) as TT inner join state_gen; """))

@app.route('/api/exec/')
def api_exec():
    # if len(common.query(common.readConfig("dbname_backend"),""" select * from state_exec; """))>0:
    #     return "fail"
    # pipeline.execute()
    return "ok"


if __name__ == '__main__':
    app.run(host="172.26.55.117", port=5000, debug=True)
