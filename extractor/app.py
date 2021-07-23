from flask import Flask, jsonify, render_template
from flask_cors import CORS
import common

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

CORS(app, resources=r'/*')


@app.route('/api/source/insert/<bvid>/<int:src_type>/')
def api_source_insert(bvid, src_type):
    common.query(common.readConfig("dbname_backend"),""" insert into in_source (bvid, src_type) values ("%s",%d); """%(bvid,src_type))
    return "ok"

@app.route('/api/template/insert/<bvid>/<int:src_type>/<int:clip_type>')
def api_template_insert(bvid, src_type, clip_type):
    common.query(common.readConfig("dbname_backend"),""" insert into in_templates (bvid, src_type, clip_type) values ("%s",%d, %d); """%(bvid,src_type,clip_type))
    return "ok"


@app.route('/api/source/delete/<bvid>/<int:src_type>/')
def apt_source_delete(bvid, src_type):
    common.query(common.readConfig("dbname_backend"),""" delete from in_source where bvid="%s" and src_type=%d; """%(bvid,src_type))
    return "ok"

@app.route('/api/template/delete/<bvid>/<int:src_type>/<int:clip_type>')
def api_template_delete(bvid, src_type, clip_type):
    common.query(common.readConfig("dbname_backend"),""" delete from in_templates where bvid="%s" and src_type=%d and clip_type=%d; """%(bvid,src_type,clip_type))
    return "ok"


@app.route('/api/source/query/')
def api_source_query():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select * from in_source; """))

@app.route('/api/template/query/')
def api_template_query():
    return jsonify(common.query(common.readConfig("dbname_backend"),""" select * from in_templates; """))




if __name__ == '__main__':
    app.run(host="172.26.55.117", port=5000, debug=True)
