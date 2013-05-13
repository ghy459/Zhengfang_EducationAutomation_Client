'''
Created on 2013-5-11

@author: ghy459

@my blog: http://hack0nair.me
'''



from urllib import request
from urllib import parse
from http import cookiejar,cookies
from bs4 import BeautifulSoup

import re,sys,time,os,subprocess
import info

from login import Login

INFO = info.INFO

class Student(object):
	"""docstring for Student"""
	def __init__(self, stuid, pwd) :
		super(Student, self).__init__()
		global INFO
		INFO['id'] = stuid
		INFO['pwd'] = pwd
		self._LOGIN = Login(stuid,pwd)
		self._LOGIN_TAG = self._LOGIN.get_login_tag()
		self.is_login()

		self._HEADERS = self._LOGIN._HEADERS
		self._OPENER = self._LOGIN._OPENER
		self._CJ = self._LOGIN._CJ

		self._VIEWSTATE = ""
		self._POST_DATA = {
							"hidLanguage":"",
							"ddlXN":"2011-2012",
							"ddlXQ":"2",
							"ddl_kcxz":"",
							"__VIEWSTATE":""
						}

		self.make_dir()
		self.get_SessionID()
		self.get_viewstate()


	def is_login(self) :

		if self._LOGIN_TAG == True :
			print ("登录成功！正在获取相关参数...")
		else :
			print ("登录失败！请检查学号和密码是否正确！")
			exit(1)


	def make_dir(self) :
		
		global INFO

		if os.path.exists(INFO['id']) :
			pass
		else :
			os.makedirs(INFO['id'])
		os.chdir(INFO['id'])
		return 


	def trans_to_gbk(self,name) :

		return parse.quote(name.encode('gbk'))


	def get_SessionID(self) :
		
		global INFO

		url = 'http://'+INFO['host_ea']+'/default_zzjk.aspx'

		self._HEADERS['Referer'] = 'http://portal.uestc.edu.cn/index.portal'
		self._HEADERS['Host'] = INFO['host_ea']

		req = request.Request(url,None,self._HEADERS,None,False,method='GET')
		
		#simple_cookie = 'LAST_PORTAL_PAGE=p346'

		'''
		c = cookies.SimpleCookie()
		c['LAST_PORTAL_PAGE'] = 'p346'
		c['LAST_PORTAL_PAGE']['path'] = '/'
		c['LAST_PORTAL_PAGE']['domain'] = '.uestc.edu.cn'
		'''
		
		#self._CJ.set_cookie(c)

		#pre_url = 'http://'+INFO['host_ea']+'/xs_main_zzjk.aspx'

		
		
		#pre_url = 'http://'+INFO['host_ea']+'/xscjcx.aspx?xh='+INFO['id']+'&xm=&gnmkdm=N121605'
		#pre_url1= 'http://ea.uestc.edu.cn//default_zzjk.aspx'
		#self.ban_refresh()
		#req = request.Request(pre_url1,None,self._HEADERS,None,False,method='GET')
		#resp = self._OPENER.open(req).read().decode('gb18030')
		#self.ban_refresh()

		
		resp = self._OPENER.open(req).read().decode('gb18030')

		#print (resp)
		#print (self._CJ)
		

	def get_viewstate(self) :
		
		global INFO

		url = 'http://'+INFO['host_ea']+'/xscjcx.aspx?xh='+INFO['id']+'&xm=&gnmkdm=N121605'
		self._HEADERS['Referer'] = 'http://'+INFO['host_ea']+'/xs_main_zzjk1.aspx'

		#req = request.Request(url,None,self._HEADERS,None,False,method='GET')
		req = request.Request(url,None,self._HEADERS,None,False,method='GET')

		resp = self._OPENER.open(req).read().decode('gb18030')

		s = r'<input[^>]*name=\"__VIEWSTATE\"[^>]*value=\"([^"]*)\"[^>]*>'
		self._VIEWSTATE = re.findall(s,resp)[0]


	def score_statistics(self) :

		global INFO

		filename = "成绩统计.txt"

		print ("正在查询\"成绩统计\"...")

		url = 'http://'+INFO['host_ea']+'/xscjcx.aspx?xh='+INFO['id']+'&xm=&gnmkdm=N121605'
		self._HEADERS['Referer'] = 'http://'+INFO['host_ea']+'/xscjcx.aspx'

		#self._POST_DATA['Button1'] = self.trans_to_gbk("成绩统计")
		self._POST_DATA.update(Button1=self.trans_to_gbk("成绩统计"))
		self._POST_DATA['__VIEWSTATE'] = self._VIEWSTATE

		postdata = parse.urlencode(self._POST_DATA)
		postdata = postdata.encode('gb2312')
		req = request.Request(url,postdata,self._HEADERS)
		resp = self._OPENER.open(req)
		msg = resp.read().decode('gb18030')

		soup = BeautifulSoup(msg,from_encoding='gb18030')

		b = soup.find_all('table',"formlist")[0]

		xh= (str((b.find_all(id='lbl_xh')[0].string)).split('：'))
		xm = (str((b.find_all(id='lbl_xm')[0].string)).split('：'))
		xy = (str((b.find_all(id='lbl_xy')[0].string)).split('：'))
		zy = (str((b.find_all(id='lbl_zy')[0].string)).split('：'))
		zymc = (str((b.find_all(id='lbl_zymc')[0].string)).split('：'))
		xzb = (str((b.find_all(id='lbl_xzb')[0].string)).split('：'))

		f = open(filename,'w')
		sys.stdout = f

		print ("------------------------------------------------------------------")

		print ("| "+xh[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xh[1].ljust(22),sep='',end='| ',file=sys.stdout,flush=True)
		print (xm[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xm[1].ljust(12),sep='',end='|\n',file=sys.stdout,flush=True)
		print ("------------------------------------------------------------------")
		print ("| "+xy[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xy[1].ljust(12),sep='',end='| ',file=sys.stdout,flush=True)
		print (zy[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (zymc[0].ljust(11),sep='',end='|\n',file=sys.stdout,flush=True)

		print ("------------------------------------------------------------------")

		print ()


		b = soup.find_all('table',"datelist")[0].find_all('td')
		count = 0
		print ("-----------------------------------------------------------------------------------------")
		for a in b :
			if count % 5 == 0 :
				if len(a.string) > 4 :
					print ("| "+a.string.ljust(11),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print ("| "+a.string.ljust(9),sep='',end='\t\t| ',file=sys.stdout,flush=True)
			if count % 5 == 1 :
				print (a.string.ljust(6),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 5 == 2 :
				print (a.string.ljust(6),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 5 == 3 :
				print (a.string.ljust(6),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 5 == 4 :
				print (a.string.ljust(6),sep='',end='\t|\n',file=sys.stdout,flush=True)
				print ("-----------------------------------------------------------------------------------------")
			count += 1

		print ()

		print ("-----------------------------------------------------------------------------------------")
		print ("| "+re.findall(r'bold;\">([^"]*)<br',(str(soup.find_all(id='xftj')[0])))[0].ljust(48),sep='',end='\t\t|\n',file=sys.stdout,flush=True)
		print ("-----------------------------------------------------------------------------------------")

		sys.stdout = sys.__stdout__
		f.close()
		f = open(filename,'rb+')
		con = f.read().replace(b"\n",b"\r\n")
		f.close()
		f = open(filename,'wb')
		f.write(con)
		f.close()

		print ('查询成功，文件保存路径：/'+INFO['id']+'/'+filename)
		if sys.platform == 'linux' :
			subprocess.Popen(['xdg-open', filename])
		elif sys.platform == 'win32' :
			os.startfile(filename)


	def best_score(self) :

		global INFO

		filename = "课程最高成绩.txt"

		print ("正在查询\"课程最高成绩\"...")

		url = 'http://'+INFO['host_ea']+'/xscjcx.aspx?xh='+INFO['id']+'&xm=&gnmkdm=N121605'
		self._HEADERS['Referer'] = 'http://'+INFO['host_ea']+'/xscjcx.aspx'

		#self._POST_DATA['Button1'] = self.trans_to_gbk("课程最高成绩")
		self._POST_DATA.update(btn_zg=self.trans_to_gbk("课程最高成绩"))
		self._POST_DATA['__VIEWSTATE'] = self._VIEWSTATE

		postdata = parse.urlencode(self._POST_DATA)
		postdata = postdata.encode('gb2312')
		req = request.Request(url,postdata,self._HEADERS)
		resp = self._OPENER.open(req)
		msg = resp.read().decode('gb18030')

		#print (msg)
		
		soup = BeautifulSoup(msg,from_encoding='gb18030')
		
		b = soup.find_all('table',"formlist")[0]

		xh= (str((b.find_all(id='lbl_xh')[0].string)).split('：'))
		xm = (str((b.find_all(id='lbl_xm')[0].string)).split('：'))
		xy = (str((b.find_all(id='lbl_xy')[0].string)).split('：'))
		zy = (str((b.find_all(id='lbl_zy')[0].string)).split('：'))
		zymc = (str((b.find_all(id='lbl_zymc')[0].string)).split('：'))
		xzb = (str((b.find_all(id='lbl_xzb')[0].string)).split('：'))
		
		f = open(filename,'w')
		sys.stdout = f

		print ("------------------------------------------------------------------")

		print ("| "+xh[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xh[1].ljust(22),sep='',end='| ',file=sys.stdout,flush=True)
		print (xm[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xm[1].ljust(12),sep='',end='|\n',file=sys.stdout,flush=True)
		print ("------------------------------------------------------------------")
		print ("| "+xy[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xy[1].ljust(12),sep='',end='| ',file=sys.stdout,flush=True)
		print (zy[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (zymc[0].ljust(11),sep='',end='|\n',file=sys.stdout,flush=True)

		print ("------------------------------------------------------------------")

		print ()


		b = soup.find_all('table',"datelist")[0].find_all('td')
		count = 0
		print ("-------------------------------------------------------------------------------------------------------------------------")
		for a in b :
			if count % 6 == 0 :
				if len(a.string) > 4 :
					print ("| "+a.string.ljust(8),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print ("| "+a.string.ljust(6),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 6 == 1 :
				if len(a.string) > 9 :
					print (a.string.ljust(24),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(28),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 6 == 2 :
				print (a.string.ljust(10),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 6 == 3 :
				print (a.string.ljust(3),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 6 == 4 :
				if len(a.string) > 4 :
					print (a.string.ljust(5),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(10),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 6 == 5 :
				print (a.string.ljust(6),sep='',end='\t|\n',file=sys.stdout,flush=True)
				print ("-------------------------------------------------------------------------------------------------------------------------")
			count += 1

		sys.stdout = sys.__stdout__
		f.close()
		f = open(filename,'rb+')
		con = f.read().replace(b"\n",b"\r\n")
		f.close()
		f = open(filename,'wb')
		f.write(con)
		f.close()

		print ('查询成功，文件保存路径：/'+INFO['id']+'/'+filename)
		if sys.platform == 'linux' :
			subprocess.Popen(['xdg-open', filename])
		elif sys.platform == 'win32' :
			os.startfile(filename)


	def failed_score(self) :

		global INFO

		filename = "未通过成绩.txt"

		print ("正在查询\"未通过成绩\"...")

		url = 'http://'+INFO['host_ea']+'/xscjcx.aspx?xh='+INFO['id']+'&xm=&gnmkdm=N121605'
		self._HEADERS['Referer'] = 'http://'+INFO['host_ea']+'/xscjcx.aspx'

		#self._POST_DATA['Button1'] = self.trans_to_gbk("课程最高成绩")
		self._POST_DATA.update(Button2=self.trans_to_gbk("未通过成绩"))
		self._POST_DATA['__VIEWSTATE'] = self._VIEWSTATE

		postdata = parse.urlencode(self._POST_DATA)
		postdata = postdata.encode('gb2312')
		req = request.Request(url,postdata,self._HEADERS)
		resp = self._OPENER.open(req)
		msg = resp.read().decode('gb18030')

		#print (msg)
		
		soup = BeautifulSoup(msg,from_encoding='gb18030')
		
		b = soup.find_all('table',"formlist")[0]

		xh= (str((b.find_all(id='lbl_xh')[0].string)).split('：'))
		xm = (str((b.find_all(id='lbl_xm')[0].string)).split('：'))
		xy = (str((b.find_all(id='lbl_xy')[0].string)).split('：'))
		zy = (str((b.find_all(id='lbl_zy')[0].string)).split('：'))
		zymc = (str((b.find_all(id='lbl_zymc')[0].string)).split('：'))
		xzb = (str((b.find_all(id='lbl_xzb')[0].string)).split('：'))
		
		f = open(filename,'w')
		sys.stdout = f

		print ("------------------------------------------------------------------")

		print ("| "+xh[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xh[1].ljust(22),sep='',end='| ',file=sys.stdout,flush=True)
		print (xm[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xm[1].ljust(12),sep='',end='|\n',file=sys.stdout,flush=True)
		print ("------------------------------------------------------------------")
		print ("| "+xy[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xy[1].ljust(12),sep='',end='| ',file=sys.stdout,flush=True)
		print (zy[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (zymc[0].ljust(11),sep='',end='|\n',file=sys.stdout,flush=True)

		print ("------------------------------------------------------------------")

		print ()


		b = soup.find_all('table',"datelist")[0].find_all('td')
		count = 0
		print ("-------------------------------------------------------------------------------------------------------------------------")
		for a in b :
			if count % 6 == 0 :
				if len(a.string) > 4 :
					print ("| "+a.string.ljust(8),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print ("| "+a.string.ljust(6),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 6 == 1 :
				if len(a.string) > 9 :
					print (a.string.ljust(24),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(28),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 6 == 2 :
				print (a.string.ljust(10),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 6 == 3 :
				print (a.string.ljust(3),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 6 == 4 :
				if len(a.string) > 4 :
					print (a.string.ljust(5),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(10),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 6 == 5 :
				print (a.string.ljust(6),sep='',end='\t|\n',file=sys.stdout,flush=True)
				print ("-------------------------------------------------------------------------------------------------------------------------")
			count += 1

		sys.stdout = sys.__stdout__
		f.close()
		f = open(filename,'rb+')
		con = f.read().replace(b"\n",b"\r\n")
		f.close()
		f = open(filename,'wb')
		f.write(con)
		f.close()

		print ('查询成功，文件保存路径：/'+INFO['id']+'/'+filename)
		if sys.platform == 'linux' :
			subprocess.Popen(['xdg-open', filename])
		elif sys.platform == 'win32' :
			os.startfile(filename)


	def all_score(self) :

		global INFO

		filename = "历年成绩.txt"

		print ("正在查询\"历年成绩\"...")

		url = 'http://'+INFO['host_ea']+'/xscjcx.aspx?xh='+INFO['id']+'&xm=&gnmkdm=N121605'
		self._HEADERS['Referer'] = 'http://'+INFO['host_ea']+'/xscjcx.aspx'

		#self._POST_DATA['Button1'] = self.trans_to_gbk("课程最高成绩")
		self._POST_DATA.update(btn_zcj=self.trans_to_gbk("历年成绩"))
		self._POST_DATA['__VIEWSTATE'] = self._VIEWSTATE

		postdata = parse.urlencode(self._POST_DATA)
		postdata = postdata.encode('gb2312')
		req = request.Request(url,postdata,self._HEADERS)
		resp = self._OPENER.open(req)
		msg = resp.read().decode('gb18030')

		
		soup = BeautifulSoup(msg,from_encoding='gb18030')
		
		b = soup.find_all('table',"formlist")[0]

		xh= (str((b.find_all(id='lbl_xh')[0].string)).split('：'))
		xm = (str((b.find_all(id='lbl_xm')[0].string)).split('：'))
		xy = (str((b.find_all(id='lbl_xy')[0].string)).split('：'))
		zy = (str((b.find_all(id='lbl_zy')[0].string)).split('：'))
		zymc = (str((b.find_all(id='lbl_zymc')[0].string)).split('：'))
		xzb = (str((b.find_all(id='lbl_xzb')[0].string)).split('：'))
		
		f = open(filename,'w',encoding='utf-8')
		sys.stdout = f

		print ("------------------------------------------------------------------")

		print ("| "+xh[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xh[1].ljust(22),sep='',end='| ',file=sys.stdout,flush=True)
		print (xm[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xm[1].ljust(12),sep='',end='|\n',file=sys.stdout,flush=True)
		print ("------------------------------------------------------------------")
		print ("| "+xy[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xy[1].ljust(12),sep='',end='| ',file=sys.stdout,flush=True)
		print (zy[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (zymc[0].ljust(11),sep='',end='|\n',file=sys.stdout,flush=True)

		print ("------------------------------------------------------------------")

		print ()


		b = soup.find_all('table',"datelist")[0].find_all('td')
		count = 0
		print ("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
		for a in b :
			if count % 16 == 0 :
				print ("| "+a.string.ljust(9),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 1 :
				if len(a.string) > 1 :
					print (a.string.ljust(2),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 3 :
				if len(a.string) > 9 :
					print (a.string.ljust(24),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(28),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 4 :
				print (a.string.ljust(10),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 6 :
				print (a.string.ljust(3),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 7 :
				if len(a.string) > 1 :
					print (a.string.ljust(2),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 8 :
				if a.string in ('通过','良好','优秀','及格','不及格') :
					print (a.string.ljust(2),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(3),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 9 :
				if len(a.string) > 1 :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(8),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 10 :
				if len(a.string) > 1 :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(8),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 12 :
				if len(a.string) > 1 :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(8),sep='',end='\t| ',file=sys.stdout,flush=True)
				print ("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
				
			count += 1

		sys.stdout = sys.__stdout__
		f.close()
		f = open(filename,'rb+')
		con = f.read().replace(b"\n",b"\r\n")
		f.close()
		f = open(filename,'wb')
		f.write(con)
		f.close()

		print ('查询成功，文件保存路径：/'+INFO['id']+'/'+filename)
		if sys.platform == 'linux' :
			subprocess.Popen(['xdg-open', filename])
		elif sys.platform == 'win32' :
			os.startfile(filename)


	def term_score(self,year,term) :

		global INFO

		filename = year+"学年第"+term+"学期成绩.txt"

		print ("正在查询\""+year+"学年第"+term+"学期成绩.txt"+"\"...")

		url = 'http://'+INFO['host_ea']+'/xscjcx.aspx?xh='+INFO['id']+'&xm=&gnmkdm=N121605'
		self._HEADERS['Referer'] = 'http://'+INFO['host_ea']+'/xscjcx.aspx'

		self._POST_DATA['ddlXN'] = year
		self._POST_DATA['ddlXQ'] = term
		self._POST_DATA.update(btn_xq=self.trans_to_gbk("学期成绩"))
		self._POST_DATA['__VIEWSTATE'] = self._VIEWSTATE

		postdata = parse.urlencode(self._POST_DATA)
		postdata = postdata.encode('gb2312')
		req = request.Request(url,postdata,self._HEADERS)
		resp = self._OPENER.open(req)
		msg = resp.read().decode('gb18030')

		soup = BeautifulSoup(msg,from_encoding='gb18030')
		
		b = soup.find_all('table',"formlist")[0]

		xh= (str((b.find_all(id='lbl_xh')[0].string)).split('：'))
		xm = (str((b.find_all(id='lbl_xm')[0].string)).split('：'))
		xy = (str((b.find_all(id='lbl_xy')[0].string)).split('：'))
		zy = (str((b.find_all(id='lbl_zy')[0].string)).split('：'))
		zymc = (str((b.find_all(id='lbl_zymc')[0].string)).split('：'))
		xzb = (str((b.find_all(id='lbl_xzb')[0].string)).split('：'))
		
		f = open(filename,'w')
		sys.stdout = f

		print ("------------------------------------------------------------------")

		print ("| "+xh[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xh[1].ljust(22),sep='',end='| ',file=sys.stdout,flush=True)
		print (xm[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xm[1].ljust(12),sep='',end='|\n',file=sys.stdout,flush=True)
		print ("------------------------------------------------------------------")
		print ("| "+xy[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xy[1].ljust(12),sep='',end='| ',file=sys.stdout,flush=True)
		print (zy[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (zymc[0].ljust(11),sep='',end='|\n',file=sys.stdout,flush=True)

		print ("------------------------------------------------------------------")

		print ()


		b = soup.find_all('table',"datelist")[0].find_all('td')
		count = 0
		print ("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
		for a in b :
			if count % 16 == 0 :
				print ("| "+a.string.ljust(9),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 1 :
				if len(a.string) > 1 :
					print (a.string.ljust(2),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 3 :
				if len(a.string) > 9 :
					print (a.string.ljust(24),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(28),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 4 :
				print (a.string.ljust(10),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 6 :
				print (a.string.ljust(3),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 7 :
				if len(a.string) > 1 :
					print (a.string.ljust(2),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 8 :
				if a.string in ('通过','良好','优秀','及格','不及格') :
					print (a.string.ljust(2),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(3),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 9 :
				if len(a.string) > 1 :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(8),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 10 :
				if len(a.string) > 1 :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(8),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 12 :
				if len(a.string) > 1 :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(8),sep='',end='\t| ',file=sys.stdout,flush=True)
				print ("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
				
			count += 1

		sys.stdout = sys.__stdout__
		f.close()
		f = open(filename,'rb+')
		con = f.read().replace(b"\n",b"\r\n")
		f.close()
		f = open(filename,'wb')
		f.write(con)
		f.close()

		print ('查询成功，文件保存路径：/'+INFO['id']+'/'+filename)
		if sys.platform == 'linux' :
			subprocess.Popen(['xdg-open', filename])
		elif sys.platform == 'win32' :
			os.startfile(filename)
		

	def year_score(self,year) :

		global INFO

		filename = year+"学年成绩.txt"

		print ("正在查询\""+year+"学年成绩.txt"+"\"...")

		url = 'http://'+INFO['host_ea']+'/xscjcx.aspx?xh='+INFO['id']+'&xm=&gnmkdm=N121605'
		self._HEADERS['Referer'] = 'http://'+INFO['host_ea']+'/xscjcx.aspx'

		self._POST_DATA['ddlXN'] = year
		#self._POST_DATA['ddlXQ'] = term
		self._POST_DATA.update(btn_xn=self.trans_to_gbk("学年成绩"))
		self._POST_DATA['__VIEWSTATE'] = self._VIEWSTATE

		postdata = parse.urlencode(self._POST_DATA)
		postdata = postdata.encode('gb2312')
		req = request.Request(url,postdata,self._HEADERS)
		resp = self._OPENER.open(req)
		msg = resp.read().decode('gb18030')

		soup = BeautifulSoup(msg,from_encoding='gb18030')
		
		b = soup.find_all('table',"formlist")[0]

		xh= (str((b.find_all(id='lbl_xh')[0].string)).split('：'))
		xm = (str((b.find_all(id='lbl_xm')[0].string)).split('：'))
		xy = (str((b.find_all(id='lbl_xy')[0].string)).split('：'))
		zy = (str((b.find_all(id='lbl_zy')[0].string)).split('：'))
		zymc = (str((b.find_all(id='lbl_zymc')[0].string)).split('：'))
		xzb = (str((b.find_all(id='lbl_xzb')[0].string)).split('：'))
		
		f = open(filename,'w')
		sys.stdout = f

		print ("------------------------------------------------------------------")

		print ("| "+xh[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xh[1].ljust(22),sep='',end='| ',file=sys.stdout,flush=True)
		print (xm[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xm[1].ljust(12),sep='',end='|\n',file=sys.stdout,flush=True)
		print ("------------------------------------------------------------------")
		print ("| "+xy[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (xy[1].ljust(12),sep='',end='| ',file=sys.stdout,flush=True)
		print (zy[0].ljust(8),sep='',end='| ',file=sys.stdout,flush=True)
		print (zymc[0].ljust(11),sep='',end='|\n',file=sys.stdout,flush=True)

		print ("------------------------------------------------------------------")

		print ()


		b = soup.find_all('table',"datelist")[0].find_all('td')
		count = 0
		print ("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
		for a in b :
			if count % 16 == 0 :
				print ("| "+a.string.ljust(9),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 1 :
				if len(a.string) > 1 :
					print (a.string.ljust(2),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 3 :
				if len(a.string) > 9 :
					print (a.string.ljust(24),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(28),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 4 :
				print (a.string.ljust(10),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 6 :
				print (a.string.ljust(3),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 7 :
				if len(a.string) > 1 :
					print (a.string.ljust(2),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 8 :
				if a.string in ('通过','良好','优秀','及格','不及格') :
					print (a.string.ljust(2),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(3),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 9 :
				if len(a.string) > 1 :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(8),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 10 :
				if len(a.string) > 1 :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(8),sep='',end='\t| ',file=sys.stdout,flush=True)
			if count % 16 == 12 :
				if len(a.string) > 1 :
					print (a.string.ljust(4),sep='',end='\t| ',file=sys.stdout,flush=True)
				else :
					print (a.string.ljust(8),sep='',end='\t| ',file=sys.stdout,flush=True)
				print ("-----------------------------------------------------------------------------------------------------------------------------------------------------------------")
				
			count += 1

		sys.stdout = sys.__stdout__
		f.close()
		f = open(filename,'rb+')
		con = f.read().replace(b"\n",b"\r\n")
		f.close()
		f = open(filename,'wb')
		f.write(con)
		f.close()

		print ('查询成功，文件保存路径：/'+INFO['id']+'/'+filename)
		if sys.platform == 'linux' :
			subprocess.Popen(['xdg-open', filename])
		elif sys.platform == 'win32' :
			os.startfile(filename)