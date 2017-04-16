# -*- coding: utf-8 -*-
import urllib
import urllib2
import lxml.html
import cookielib
import xlrd
LOGIN_URL="http://my.haust.edu.cn/cas/login?service=http://210.43.0.37:8080/xgxt/home/xgsyPage.action"

LOGIN_USERNAME='######'
LOGIN_PASSWD='######'
def get_info():
	data =xlrd.open_workbook("./ID.xlsx")
	table=data.sheets()[0]
	ncols=table.ncols
	IDs=table.col_values(0)
	names=table.col_values(1)
	IDs.extend(names)
	info=IDs[:]
	return info
def parse_from(html):
	tree=lxml.html.fromstring(html)
	data={}
	for e in tree.cssselect('form input'):
		if e.get('name'):
			data[e.get('name')]=e.get('value')
	return data

def get_img():
	i=0
	cj=cookielib.CookieJar()
	opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	html=opener.open(LOGIN_URL).read()
	data=parse_from(html)
	# print data
	data['username']=LOGIN_USERNAME
	data['password']=LOGIN_PASSWD
	encoded_data=urllib.urlencode(data)
	request=urllib2.Request(LOGIN_URL,encoded_data)
	response=opener.open(request)
	info=get_info()
	for i in range(0,330):
		ID=info[i]
		name=info[i+331]
		print ID
		print name
		IMG_URL="http://me.haust.edu.cn:9900/sys/yx/stu.do?method=getZPT&xh=%s"%ID
		response1=opener.open(IMG_URL)
		data=response1.read()
		with open('./img/%s.%s.jpg'%(ID,name),"w+") as f:
			f.write(data)
if __name__ == '__main__':
	get_img()
	print "Have Deen!"
	# get_ID()
