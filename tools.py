#-*- coding: utf8 -*-

from xlwt import Workbook
import re, json
import time
from time import gmtime, strftime
import sys, os
from flask import Flask,url_for,render_template, request, send_from_directory

app = Flask(__name__)
# debug=True 時，每當程式一修改， flask 會
# 自動重新載入 app
app.debug = True ##啟動debug mode

# 避免重新轉址造成誤 
app.url_map.strict_slashes = False

@app.route('/tools/<path:filename>')
def catch_all(path):
	return 'You want path: %s' % filename

@app.route("/tools/")
def Index(name=None):
	return render_template('index.html',time=time.time())

wordtable_info=[
	[u"中國時報",u"data/中國時報詞頻.json",u"data/中國時報詞頻序位.json"],
	[u"口語語料",u"data/口語語料詞頻.json",u"data/口語語料詞頻序位.json"],
	[u"國語日報",u"data/國語日報詞頻.json",u"data/國語日報詞頻序位.json"],
	[u"平衡語料庫",u"data/平衡語料庫詞頻.json",u"data/平衡語料庫詞頻序位.json"],
	[u"聯合報",u"data/聯合報詞頻.json",u"data/聯合報詞頻序位.json"],
	[u"遠流語料",u"data/遠流語料詞頻.json",u"data/遠流語料詞頻序位.json"],
	[u"教材語料",u"data/教材語料詞頻.json",u"data/教材語料詞頻序位.json"],
]

wordtableL=[]
for idx,info in enumerate(wordtable_info):
	freqT=json.load(open(info[1]))
	orderT=json.load(open(info[2]))
	N=sum(freqT.values())
	wordtableL.append({'name':info[0],'freq':freqT,'order':orderT,'N':N})

@app.route("/tools/wordlist/",methods=['GET','POST'])
def WordList():
	if request.method=='POST':
		filename="wordlist_%s.xls"%(strftime("%Y%m%d%H%M%S",gmtime()))
		wbw = Workbook()
		shw = wbw.add_sheet(u'詞表統計')
		shw.write(0,0,u"序號")
		shw.write(0,1,u"詞彙")
		for idx,info in enumerate(wordtable_info):
			offset=2+idx*4
			shw.write(0,offset+0,u"%s序位"%(info[0]))
			shw.write(0,offset+1,u"%s詞頻"%(info[0]))
			shw.write(0,offset+2,u"%s累計詞頻"%(info[0]))
			shw.write(0,offset+3,u"%s覆蓋率"%(info[0]))

		output={}
		output['filename']="/tools/download/%s"%filename
		#print "DEBUG1:%s"%(json.dumps(request.json))
		wordlist=request.json.get('wordlist',[])
		accL=[0]*len(wordtableL)
		accT={}
		for idx,w in enumerate(wordlist,0):
			shw.write(1+idx,0,idx+1)
			shw.write(1+idx,1,w)
			wL=[]
			if '/' in w:
				wL=w.split('/')
			else:
				wL=[w]
			for jdx,wordtable in enumerate(wordtableL):
				offset=2+jdx*4
				order=999999
				for x in wL:
					x=re.sub(u'[0-9~]+',u'',x)
					if wordtable['order'].get(x,order) < order:
						order=wordtable['order'].get(x,order)
				if order>=999999:
					shw.write(1+idx,offset+0,'N/A')
				else:
					shw.write(1+idx,offset+0,order)
				freq=0
				accFreq=0
				for x in wL:
					x=re.sub(u'[0-9~]+',u'',x)
					freq+=wordtable['freq'].get(x,0)
					if not x in accT:
						accFreq+=wordtable['freq'].get(x,0)
				shw.write(1+idx,offset+1,freq)

				accL[jdx]+=accFreq
				shw.write(1+idx,offset+2,accL[jdx])
				shw.write(1+idx,offset+3,float(accL[jdx])/wordtable['N'])
			for x in wL:
				x=re.sub(u'[0-9~]+',u'',x)
				if not x in accT:
					accT[x]=1

		wbw.save("download/%s"%(filename))
		#L=[('Hello',0.5),('World',0.5)]
		#print json.dumps(output, ensure_ascii=False).encode("UTF-8")
		return json.dumps(output, ensure_ascii=False).encode("UTF-8")


# css, pic, js 檔
@app.route('/tools/pic/<path:filename>')
def send_pic(filename):	
	return send_from_directory('./static/pic/', filename)

@app.route('/tools/css/<path:filename>')
def send_css(filename):
	return send_from_directory('./static/css/', filename)

@app.route('/tools/js/<path:filename>')
def send_js(filename):
	return send_from_directory('./static/js/', filename)

@app.route('/tools/fonts/<path:filename>')
def send_fonts(filename):
	return send_from_directory('./static/fonts/', filename)

@app.route('/tools/download/<path:filename>')
def send_download(filename):
	return send_from_directory('./download/', filename)


if __name__ == "__main__":
	app.run(host = "0.0.0.0",port=6869)
   
