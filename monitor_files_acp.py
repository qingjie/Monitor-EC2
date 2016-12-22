#!/usr/bin/python
import os
import string
import sys
import time
import datetime
import boto.ec2.cloudwatch

class files_acp:
	def __init__(self):
		self.cw = boto.ec2.cloudwatch.connect_to_region('us-east-1')
		InstanceId=os.popen('wget -q -O - http://169.254.169.254/latest/meta-data/instance-id')
		self.Instance_Id=InstanceId.read()
		InstanceId.close()
		self.namespaceStr = "CustomMetric"
	
	#if file is exist, tempValue is 1, else tempValue is 0.
	def fileIsExist(self,fileName):
		dir='/usr/share/jetty/pixellogs'
		os.chdir(dir)
		bln = os.path.exists(fileName)
		if bln:
			tempValue = 1 
        		#print '%s %s %s' % ('File',fileName,'is exist.')
    		else:
			tempValue = 0
        		#print '%s %s %s' % ('File',fileName,'is not exist.')
		return tempValue

	def fileLineCount(self,fileName):
    		count = -1
    		for count, line in enumerate(open(fileName, 'rU')):
        		pass
    		count += 1
    		#print '%s %s %s %s %s' % ('File',fileName,'has',count,'line.')
    		return count

	def putDataForExist(self,fileName):
		temp =  self.fileIsExist(fileName)
		strMetricName = '%s%s%s' % (self.Instance_Id,'_line_',fileName)
		self.cw.put_metric_data(namespace=self.namespaceStr, name=strMetricName, value=temp, unit='Count')

		'''
        	line_count =  self.fileLineCount(fileName)
        	print line_count
        	namespaceStr = "CustomMetric"
        	strMetricName = '%s%s%s' % (self.Instance_Id,'_',fileName)
        	#cw.put_metric_data(namespace=namespaceStr, name=strMetricName, value=line_count, unit='Count')
			
		now = datetime.datetime.now()
		m = now.minute
		temp = '%s' % (m)
		lastDigit = temp[-1]
		if (lastDigit == 5):
			fileIsExist(fileName)
			line_count =  fileLineCount(fileName)
   	 		print line_count
			namespaceStr = "CustomMetric"
    			cw.put_metric_data(namespace=namespaceStr, name=fileName, value=line_count, unit='Count')
		print 'It is time to check.'
		'''

	def putDataForLine(self,fileName):
		temp1 =  self.fileIsExist(fileName)
		if (temp1 == 1):
			line_count =  self.fileLineCount(fileName)
			strMetricName1 = '%s%s%s' % (self.Instance_Id,'_line_',fileName)
			self.cw.put_metric_data(namespace=self.namespaceStr, name=strMetricName1, value=line_count, unit='Count')
		else:
			pass

	def putData(self,name1,name2,name3):
		self.putDataForExist(name1)
		self.putDataForExist(name2)
		self.putDataForExist(name3)
		self.putDataForLine(name1)
		self.putDataForLine(name2)
		self.putDataForLine(name3)
		


facp = files_acp()
name1 = 'requestAdserver.log'
name2 = 'requestClick.log'
name3 = 'requestPixel.log'
facp.putData(name1,name2,name3)