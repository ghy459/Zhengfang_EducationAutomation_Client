from urllib import request
from urllib import parse
from http import cookiejar,cookies

import info
import re

INFO = info.INFO

class SimpleCookieHandler(request.BaseHandler):
    def http_request(self, req):
        simple_cookie = 'LAST_PORTAL_PAGE=p346'
        if not req.has_header('Cookie'):
            req.add_unredirected_header('Cookie', simple_cookie)
        else:
            cookie = req.get_header('Cookie')
            req.add_unredirected_header('Cookie', simple_cookie + '; ' + cookie)
        return req


class Login(object):
	"""docstring for Login"""
	def __init__(self,stuid,pwd):
		super(Login, self).__init__()
		global INFO
		INFO['id'] = stuid
		INFO['pwd'] = pwd
		self._LOGIN_DATA = {
							"Login.Token1":INFO['id'],
							"Login.Token2":INFO['pwd'],
							"goto":"http://portal.uestc.edu.cn/loginSuccess.portal",
							"gotoOnFail":"http://portal.uestc.edu.cn/loginFailure.portal"
							}
		self._HEADERS = {
						"Accept": "Accept:text/html,application/xhtml+xml,image/gif,image/x-xbitmap,image/jpeg,image/pjpeg,application/x-shockwave-flash,application/xml;q=0.9,*/*;q=0.8",
						"Accept-Charset":"GBK,utf-8;q=0.7,*;q=0.3",
						"Accept-Language": "zh-CN,zh;q=0.8",
						"Referer":"http://portal.uestc.edu.cn/index.portal",
						"Host":INFO['host_portal'],
						"Content-Type": "application/x-www-form-urlencoded",
						'User-agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
						"Connection": "Keep-Alive",
						"Cache-Control": "no-cache",
						}

		self._CJ = cookiejar.CookieJar()
		self._OPENER = request.build_opener(request.HTTPCookieProcessor(self._CJ),SimpleCookieHandler())
		request.install_opener(self._OPENER)
		self._LOGIN_TAG = False
		self._URL = 'http://'+INFO['host_portal']+'/userPasswordValidate.portal'
		self.login()
		

	def ban_refresh(self) :

		print ("等待\'5秒防刷\'!")
		time.sleep(6)

	def get_viewstate(self,url) :
		
		resp = self._OPENER.open(url).read().decode('gb2312')
		s = r'<input[^>]*name=\"__VIEWSTATE\"[^>]*value=\"([^"]*)\"[^>]*>'
		t = re.findall(s,resp)[0]
		self._LOGIN_DATA.update(__VIEWSTATE=t)
		

	def login(self) :

		url = self._URL
		postdata = parse.urlencode(self._LOGIN_DATA)
		postdata = postdata.encode('gb2312')
		req = request.Request(url,postdata,self._HEADERS)
		resp = self._OPENER.open(req)
		msg = resp.read().decode('utf-8')
		if msg.find("Success") != -1 :
			self._LOGIN_TAG = True
			#resp.info()['Set-cookie']
		else :
			self._LOGIN_TAG = False
		


	def get_login_tag(self) :

		return self._LOGIN_TAG