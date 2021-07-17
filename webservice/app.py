from flask import Flask, jsonify, render_template
from flask_cors import CORS
import osapi
import msql

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

CORS(app, resources=r'/*')


@app.route('/')
def api_index():
    return render_template("index.html")

@app.route('/list/<int:src_type>/<int:clip_type>/')
def api_list(src_type, clip_type):
    sql_result = msql.query("biliextract","select id, bvid from extraction where src_type=%d and clip_type=%d;"%(src_type,clip_type), isDict=True)
    return jsonify(sql_result)


@app.route('/video/<name>/')
def api_video(name):
    return osapi.getBinaryFile("../data/output/%s.mp4" % name)

@app.route('/poster/<name>/')
def api_poster(name):
    return osapi.getBinaryFile("../data/poster/%s.mp4" % name)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)