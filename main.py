#!/usr/bin/python  
# -*- coding: utf-8 -*-  

'''
Created on 2013-5-11

@author: ghy459

@my blog: http://hack0nair.me
'''

from optparse import OptionParser
from student import Student
import os,info

INFO = info.INFO


def usage() :
	
	global INFO

	usage = "%prog [options] [ -o -i ] [ -d ] " 
	parser = OptionParser(usage,version="教务系统快速查询客户端 v1.2")
	parser.add_option("-o",action="store_true", dest="o",help="校外访问")
	parser.add_option("-i",action="store_true", dest="i",help="校内访问")
	parser.add_option("-d",action="store_true", dest="d",help="清理查询痕迹")

	(options, args) = parser.parse_args()

	if options.o == True :
		INFO['io'] = "out"
	if options.i == True :
		INFO['io'] = "in"
	if options.d == True :
		INFO['del'] = True


def del_file() :

	filelist = os.listdir(os.getcwd())
	path = os.path.dirname(os.getcwd())
	try:
		for f in filelist :
			os.remove(f)
		os.chdir(path)
		os.rmdir(INFO['id'])
	except:
		print ("文件删除出错！")
		exit(1)


if __name__ == '__main__':

	print ("\n欢迎使用教务系统快速查询客户端，程序正在启动中...")
	usage()
	print ()
	if INFO['id'] == "" :
		INFO['id'] = input("请输入学号:")
	if INFO['pwd'] == "" :
		INFO['pwd'] = input("请输入密码:")
	print ()
	stu = Student(INFO['id'],INFO['pwd'],INFO['io'])

	while (1) :

		print ()
		print ("---------------功能命令---------------")
		print ("    1        查询XX学年XX学期成绩")
		print ("    2        查询XX学年成绩")
		print ("    3        查询历年成绩")
		print ("    4        查询课程最高成绩")
		print ("    5        查询未通过成绩")
		print ("    6        查询成绩统计")
		print ("    7        退出程序")
		print ("--------------------------------------")
		print ()
		op = input("请输入命令:")

		try:
			if op == '1' :
				year = input("请输入学年（格式： 2012-2013 ）：")
				term = input("请输入学期（格式： 1 ）：")
				stu.term_score(year,term)
			if op == '2' :
				year = input("请输入学年（格式： 2012-2013 ）：")
				stu.year_score(year)
			if op == '3' :
				stu.all_score()
			if op == '4' :
				stu.best_score()
			if op == '5' :
				stu.failed_score()
			if op == '6' :
				stu.score_statistics()
			if op == '7' :
				if INFO['del'] == True :
					del_file()
				print ("程序正常退出！")
				exit(0)
		except:
			print ("当前网络不稳定，请重试！")
			continue