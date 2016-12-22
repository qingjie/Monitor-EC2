#!/usr/bin/python
import boto
import sys
import os

class alarm_files_acp:
	
	def __init__(self):
		aws_access_id=""
		aws_secret_key=""
		self.cw = boto.connect_cloudwatch(aws_access_id, aws_secret_key)
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


	def createAlarmForExist(self,fileName):
    		temp = self.fileIsExist(fileName)
		str_alarm_name = '%s%s%s%s%s' % ('ALARM_',self.Instance_Id,'_line_/usr/share/jetty/pixellogs/',fileName,'_files_acp')
		alarms = self.cw.describe_alarms(alarm_name_prefix=str_alarm_name)	
		if alarms:
		        print '%s %s %s' % ('File',str_alarm_name,'has alarm.')
   		else:
        		print '%s %s %s' % ('File',str_alarm_name,'does not have alarm.')
        		print '*************** start to create alarm *******************'
			strMetricName = '%s%s%s' % (self.Instance_Id,'_line_',fileName)
        		alarm_file = boto.ec2.cloudwatch.MetricAlarm(name=str_alarm_name, metric=strMetricName, namespace=self.namespaceStr, statistic="Maximum", evaluation_periods =1,comparison="<", threshold=1, period=300, description="File is not exist.",alarm_actions = "arn:aws:sns:us-east-1:739963839279:Anonymous_Dev")
        		self.cw.create_alarm(alarm_file)
        		print '************************ done ***************************'



	def createAlarmForLine(self,fileName):
    		temp1 = self.fileIsExist(fileName)
		if (temp1 == 1):
			line_count = self.fileLineCount(fileName)
			str_alarm_name1 = '%s%s%s%s%s' % ('ALARM_',self.Instance_Id,'_line_/usr/share/jetty/pixellogs/',fileName,'_files_acp')	
			alarms1 = self.cw.describe_alarms(alarm_name_prefix=str_alarm_name1)
			if alarms1:
        			print '%s %s' % (str_alarm_name1, ' has alarm.')
    			else:
        			print '%s %s' % (str_alarm_name1,' does not have alarm.')
        			print '*************** start to create alarm *******************'
        			strMetricName1 = '%s%s%s' % (self.Instance_Id,'_line_',fileName)
        			alarm_Line = boto.ec2.cloudwatch.MetricAlarm(name=str_alarm_name1, metric=strMetricName1, namespace=self.namespaceStr, statistic="Maximum", evaluation_periods =1,comparison="<", threshold=1, period=300, description="File content is less than 1 line.",alarm_actions = "arn:aws:sns:us-east-1:739963839279:Anonymous_Dev")
        			self.cw.create_alarm(alarm_Line)
        			print '************************ done ***************************'
		else:
			pass


	def createAlarm(self,name1,name2,name3):
		self.createAlarmForExist(name1)
		self.createAlarmForExist(name2)
		self.createAlarmForExist(name3)
		self.createAlarmForLine(name1)
		self.createAlarmForLine(name2)
		self.createAlarmForLine(name3)


afacp = alarm_files_acp()
name1 = 'requestAdserver.log'
name2 = 'requestClick.log'
name3 = 'requestPixel.log'
afacp.createAlarm(name1,name2,name3)
