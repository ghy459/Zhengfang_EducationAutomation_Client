#!/usr/bin/python  
# -*- coding: utf-8 -*- 

'''
Created on 2013-5-11

@author: ghy459

@my blog: http://hack0nair.me

'''

from urllib import request
from urllib import parse
from http import cookiejar,cookies,client

import info
import re
import socket

INFO = info.INFO


def my_host(host) :
	
	if INFO['io'] == 'in' :
		if host == 'portal.uestc.edu.cn' :
			return '222.197.164.72'
		else :
			return '222.197.164.82'
	else :
		if host == 'portal.uestc.edu.cn' :
			return '125.71.228.241'
		else :
			return '125.71.228.243'

class MyHTTPConnection(client.HTTPConnection):

	def connect(self):
		self.sock = socket.create_connection((my_host(self.host),self.port),self.timeout)


class MyHTTPHandler(request.HTTPHandler):
	
	def http_open(self,req):
		return self.do_open(MyHTTPConnection,req)


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
	def __init__(self,stuid,pwd,io):
		super(Login, self).__init__()
		global INFO
		INFO['id'] = stuid
		INFO['pwd'] = pwd
		INFO['io'] = io
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
						"Accept-Encoding": "gzip, deflate",
						"Referer":"http://portal.uestc.edu.cn/index.portal",
						"Host":"portal.uestc.edu.cn",
						"Content-Type": "application/x-www-form-urlencoded",
						'User-agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
						"Connection": "Keep-Alive",
						"Cache-Control": "no-cache",
						}

		self._CJ = cookiejar.CookieJar()
		self._OPENER = request.build_opener(request.HTTPCookieProcessor(self._CJ),SimpleCookieHandler(),MyHTTPHandler())
		request.install_opener(self._OPENER)
		self._LOGIN_TAG = False
		self._URL = 'http://'+INFO['host_portal']+'/userPasswordValidate.portal'
		try:
			self.login()
		except:
			print ("当前网络不稳定，请稍后再试！")
			exit(1)


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