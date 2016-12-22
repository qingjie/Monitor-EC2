#!/usr/bin/python
import boto.ses
import time

class alarm_email_sender:

	def __init__(self):
        	aws_access_id=""
        	aws_secret_key=""
        	self.cw = boto.connect_cloudwatch(aws_access_id, aws_secret_key)
        	self.cr = boto.ses.connect_to_region('us-east-1',aws_access_key_id=aws_access_id, aws_secret_access_key=aws_secret_key)
	
	
	def checkAlarm(self):
	        temp_value = "ALARM"
        	alarms=self.cw.describe_alarms(state_value=temp_value)
       		strBody=""
        	for item in alarms:
        		strBody += '%s %s' % (item.name,'has alarm.\n')
		return strBody

	def sendEmail(self):
        	title =  '%s %s' % ('Alarm reminder at',time.ctime())
        	body = self.checkAlarm()
        	#conn.verify_email_address('qingjie@aerifymedia.com')
        	self.cr.send_email('qingjie@aerifymedia.com',title,body,['qingjie@aerifymedia.com'])
    		

aes = alarm_email_sender()
aes.sendEmail()