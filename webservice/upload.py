import requests
import os
import re
import json
import base64
import sys
import time
url1 = 'https://member.bilibili.com/preupload?name={}&size={}&r=upos&profile=ugcupos%2Fbup&ssl=0&version=2.8.12&build=2081200&upcdn=qn&probe_version=20200810'
url2 = 'https://upos-sz-upcdnqn.bilivideo.com/ugcboss/{}?uploads&output=json'
url3 = 'https://upos-sz-upcdnqn.bilivideo.com/ugcboss/{}?partNumber={}&uploadId={}&chunk={}&chunks={}&size={}&start={}&end={}&total={}'
url4 = 'https://upos-sz-upcdnqn.bilivideo.com/ugcboss/{}?output=json&name={}&profile=ugcupos%2Fbup&uploadId={}&biz_id={}'
url5 = 'https://member.bilibili.com/x/vu/web/cover/up'
url6 = 'https://member.bilibili.com/x/vu/web/add?csrf={}'

class upload:
    #请求头
    header = {
        # 'cookie':"_uuid=FE18E94F-CAB1-69C0-753C-245A94DB063C04672infoc; buvid3=5D8ED97F-100C-4AAE-951D-9720D91F29EC143079infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(k|RYJYllJY0J'uY|ukYlm||; buivd_fp=5D8ED97F-100C-4AAE-951D-9720D91F29EC143079infoc; buvid_fp_plain=5D8ED97F-100C-4AAE-951D-9720D91F29EC143079infoc; buvid_fp=5D8ED97F-100C-4AAE-951D-9720D91F29EC143079infoc; fingerprint3=7cdce1880b09344ee0d74616931713d7; fingerprint_s=193f3299bcb4e2c36d107cd3a0b51a14; CURRENT_QUALITY=112; bp_video_offset_471644009=542730492934997055; bp_t_offset_471644009=542734418540372470; LIVE_BUVID=AUTO4616264373573122; fingerprint=8ad433d08805dd3661276580326c9208; SESSDATA=4b205deb,1642470292,f6610*71; bili_jct=7e4d9ba2897d7ed66e90e6ffd63f18ba; DedeUserID=327074361; DedeUserID__ckMd5=b5989e33de2a6abb; sid=6xct9ybc; bsource=search_baidu; _dfcaptcha=52c37e0e20fb82c0451705500419ae0c; PVID=2"
       
         'cookie':"",
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
        
    }
    #上传视频的格式
    data = {
        'copyright': 1,
        'cover': '',
        'desc': '',
        'desc_format_id': 32,
        'dynamic': '',
        'interactive': 0,
        'mission_id': 0,
        'no_reprint': 1,
        'subtitle': {
            'open': 0,
            'lan': ""
        },
        'tag': '',
        'tid': 0,
        'title': '',
        'up_close_danmu': False,
        'up_close_reply': False,
        'videos': [
            {
                'filename': '', 
                'title': '', 
                'desc': '', 
                'cid': ''
            }
        ]
    }
    
    def __init__(self,bili_jct="eb42bd2a4760256000effcc6b355ecdb",cookie='SESSDATA=23009bef%2C1634952897%2Cabdaba71',videoconfig="./videoconfig.json") -> None:
        self.bili_jct=bili_jct
        self.videoconfig=videoconfig
        self.header['cookie']=cookie
        # self.setconfig(self.videoconfig)
        
    def setconfig(self,videoconfig) -> None:
        # try:
        #     self.header['cookie'] = self.config['cookie']
        #     if len(re.findall(r'bili_jct=(\S+?);',self.config['cookie'])):
        #         self.bili_jct = re.findall(r'bili_jct=(\S+?);',self.config['cookie'])[0]
        #     else:
        #         self.bili_jct = re.findall(r'bili_jct=(\S+?)$',self.config['cookie'])[0]
        # except Exception:
        #     print('cookie error')
        #     sys.exit()
        
        try:
            with open(videoconfig,'r',encoding='utf8')as fp:
                self.vconfig = json.load(fp)
        except Exception:
            yield "视频配置地址错误"
        try:
            #必选参数
            self.video_path = self.vconfig['video_path']
            self.cover_path = self.vconfig['cover_path']
            self.config=self.vconfig['config']
            self.data['desc'] = self.config['desc']
            self.data['tag'] = self.config['tag']
            self.data['tid'] = self.config['tid']
            self.data['title'] = self.config['title']
            #可选参数
            if 'copyright' in self.config:
                self.data['copyright'] = self.config['copyright']
            if 'dynamic' in self.config:
                self.data['dynamic'] = self.config['dynamic']
            if 'no_reprint' in self.config:
                self.data['no_reprint'] = self.config['no_reprint']
            if 'subtitle' in self.config:
                self.data['subtitle'] = self.config['subtitle']
            if 'up_close_danmu' in self.config:
                self.data['up_close_danmu'] = self.config['up_close_danmu']
            if 'up_close_reply' in self.config:
                self.data['up_close_reply'] = self.config['up_close_reply']
        except Exception:
            yield "视频配置出错"
            sys.exit()
    def picture_upload(self) -> None:
        try:
            with open(self.cover_path,'rb+') as file:
                yield '正在上传封面'
                # print(self.cover_path)
                code = b'data:image/jpeg;base64,'+base64.b64encode(file.read())
                # yield self.bili_jct
                # yield self.header
                
                content=requests.post(url5,data={'cover': code,'csrf': self.bili_jct},headers=self.header).text
                # yield (content)
                js = json.loads(content)
                self.data['cover'] = js['data']['url'].split(':')[1]
                yield '封面上传完毕'
        except Exception:
            yield '封面路径无效'
            sys.exit()
    def video_upload(self) -> None:
        try:
            yield '正在上传视频'
            header = self.header
            video_path = self.video_path
            video_name = video_path.split('\\')[-1]
            size = os.path.getsize(video_path)
            c=0
            while c<10:
                # yield(video_name,size)
                # yield(header)
                # yield(requests.get(url1.format(video_name,size),headers=header).content)
                js1 = json.loads(requests.get(url1.format(video_name,size),headers=header).content.decode("utf-8"))
                header['X-Upos-Auth'] = js1['auth']
                upos_uri = js1['upos_uri'].split('/')[-1]
                biz_id = js1['biz_id']
                # yield(biz_id)
                if requests.post(url2.format(upos_uri),headers=header).status_code ==200:
                    content=requests.post(url2.format(upos_uri),headers=header).content.decode("utf-8")
                    break
                c+=1
                time.sleep(3)
                yield "视频投稿重连第%s次"% c
            #问题：有大约0.5的概率返回的状态为403.
               
            js2 = json.loads(content)
            upload_id = js2['upload_id']
            with open(video_path,'rb+') as file:
                requests.put(url3.format(upos_uri,1,upload_id,0,1,size,0,size,size),headers=header,data=file.read()).content.decode("utf-8")
            js3 = requests.post(url4.format(upos_uri,video_name,upload_id,biz_id),headers=header).text
            if 'OK' in js3:
                yield '视频上传完毕' 
            self.data['videos'][0]['filename'] = upos_uri.split('.')[0]
            self.data['videos'][0]['cid'] = biz_id
            self.data['videos'][0]['title'] = video_name.split('.')[0]
        except IOError:
            yield '视频路径无效'
        except KeyError:
            yield '视频配置出错'
    def upload(self) :
        for x in self.setconfig(self.videoconfig):
            yield x
        for x in  self.picture_upload():
            yield x
        for x in  self.video_upload():
            yield x
        js = json.loads(requests.post(url6.format(self.bili_jct),headers=self.header,data=json.dumps(self.data).encode('utf-8')).text)
        # yield js
        
        if js['code'] != 0:
            yield js['message']
        else:
            yield '投稿成功'
    
if __name__=="__main__":
    ul = upload()
    for x in ul.upload():
        print(x)
