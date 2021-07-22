from flask import Flask, jsonify, render_template
from flask_cors import CORS
import common

app = Flask(__name__)

app.config['JSON_AS_ASCII'] = False
app.config['JSONIFY_MIMETYPE'] = "application/json;charset=utf-8"

CORS(app, resources=r'/*')


@app.route('/post/source/<s>/')
def api_post_source(s):
    print("source",s)

@app.route('/post/template/<s>/')
def api_post_template(s):
    print("template",s)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
