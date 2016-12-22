#!/usr/bin/python
import boto
import sys
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import boto.ec2.cloudwatch
from vo_hadoop_file import VO
import datetime 
import time 


class CheckS3:
	
	def __init__(self,conn,ca):
        	aws_access_id=""
        	aws_secret_key=""
        	conn = S3Connection(aws_access_id, aws_secret_key)
            	self.conn = conn
            	ca = boto.connect_cloudwatch(aws_access_id, aws_secret_key)
            	self.ca = ca

    	def getListOfFileSize(self,bucket_name):
		self.list=['click_count_day','country_creative_day','creative_camp_day','creative_camp_hourly','creative_url_camp_day','dma_creative_day','dma_pixel_day','event_count_day','event_count_day','event_count_increment','pvc','impression_count_day','revenue_count_day','url_camp_day','url_domain_day','watched_video_count_day','xch_line_creative_click_count_day','xch_line_creative_impression_count_day','xch_line_creative_revenue_count_day','xch_line_creative_watched_video_count_day']
		self.listVO = []
		listDir = []
		strds = '%s%s' % ('ds=',datetime.date.today().strftime('%Y-%m-%d'))
		for item in self.list:
			if ((item == 'creative_camp_day') or (item == 'event_count_increment')):
				for num in range(0,24):
					temp = '%s/%s/%s/%s%s/' % ('output',item,strds,'id=',num)
					listDir.append(temp)
			else:
				temp = '%s/%s/%s/' % ('output',item,strds)
				listDir.append(temp)


		bucket = self.conn.get_bucket(bucket_name)	
		for tempDir in listDir:
			rs = bucket.list(tempDir)
			for key in rs:
				strKeyName = key.name
                                strKeySize = key.size
				#if('id=' in strKeyName):
					#print '%s %s' % ( key.name,key.last_modified)

				if(strKeySize >= 0 and strKeySize <= 20):
                                	vo = VO(strKeyName,strKeySize)
                                        self.listVO.append(vo)
                                else:
                                	pass
		return self.listVO
		



	def createSizeAlarm(self,_list,bucket_name):
		#print '~~~~~%s' % (len(_list))
		namespaceStr = "CustomMetric"
		for temp in _list:
			alarm_name = '%s%s%s%s' % ('ALARM_S3_',bucket_name,'_',temp.getName())
        		#print alarm_name
			alarmNameExist = self.ca.describe_alarms(alarm_name_prefix=alarm_name)
        		if alarmNameExist:
            			print '%s %s' % (alarm_name,'has alarm.')
        		else:
           			print '%s %s' % (alarm_name,'does not have alarm.')
            			print '*************** start to create alarm *******************'
            			alarm = boto.ec2.cloudwatch.MetricAlarm(name=alarm_name, metric=temp.getName(), namespace=namespaceStr, statistic="Maximum", evaluation_periods =1,comparison="<=", threshold=20, period=60, description="File size is less than 20 bytes",alarm_actions = "arn:aws:sns:us-east-1:739963839279:Dev2")
            			self.ca.create_alarm(alarm)
            			print '************************ done ***************************'



cs3 = CheckS3('conn','ca')
bucket_name='hadoop.anonymous.com'
#print 'start %s' % time.ctime()
tempList = cs3.getListOfFileSize(bucket_name)
cs3.createSizeAlarm(tempList,bucket_name)
#print 'end   %s' % time.ctime()
