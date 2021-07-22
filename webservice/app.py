from flask import Flask, jsonify, render_template
from flask_cors import CORS
import osapi
import msql
import jieba

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

CORS(app, resources=r'/*')


@app.route('/')
def api_index():
    return render_template("index.html")


@app.route('/list/<int:src_type>/<int:clip_type>/')
def api_list(src_type, clip_type):
    sql_result = msql.query("biliextract", "select id, bvid from extraction where src_type=%d and clip_type=%d order by rand();" % (
        src_type, clip_type), isDict=True)
    return jsonify(sql_result)


@app.route('/video/<name>/')
def api_video(name):
    return osapi.getBinaryFile("../data/output/%s.mp4" % name)


@app.route('/poster/<name>/')
def api_poster(name):
    return osapi.getBinaryFile("../data/poster/%s.jpg" % name)


@app.route('/assets/<name>/')
def api_assets(name):
    return osapi.getBinaryFile("assets/%s" % name)


@app.route('/vinfo/<xvid>/')
def api_vinfo(xvid):
    return jsonify(msql.query("biliextract", """select * from Vinfo where bvid in (select bvid from extraction where id = '{xvid}');""".format(xvid=xvid), isDict=True))


@app.route('/xv/danmu/<xvid>/')
def api_vtdanmu(xvid):
    return jsonify(msql.query("biliextract", """select text from (select text,abs(floattime-tm) as dt from Danmu,(select frame_begin/24 as tm from extraction 
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
    sqlres= msql.query("biliextract", """select text from (select text,abs(floattime-tm) as dt from Danmu,(select frame_begin/24 as tm from extraction 
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
    app.run(host="0.0.0.0", port=5001, debug=True)
