#!/usr/bin/python
import boto
import sys
import os

class CMSD:
	
	def __init__(self):
		aws_access_id=""
		aws_secret_key=""
		self.c = boto.connect_cloudwatch(aws_access_id, aws_secret_key)
		#state_value = "OK"
		#alarms = c.describe_alarms(state_value=state_value)
		#Instance_Id=sys.argv[1]
		#Instance_Id="i-9aecaee0"
		InstanceId=os.popen('wget -q -O - http://169.254.169.254/latest/meta-data/instance-id')
		self.Instance_Id=InstanceId.read()
		InstanceId.close()


	def createAlarm(self,name):
		ALARM_NAME = '%s%s%s%s' % ('ALARM_',self.Instance_Id,'_',name)
		alarms = self.c.describe_alarms(alarm_name_prefix=ALARM_NAME)
		if alarms:
			print '%s has alarm.' % ALARM_NAME
		else:
			if(name == 'CPU'):
				tempMetric = 'CPUUtilization'
				tempNameSpace = 'AWS/EC2'
				tempPeriod = 300
				tempEvaluation_periods = 2
				tempDimensions = {"InstanceId":self.Instance_Id}
			elif(name == 'MEM'):
				tempMetric = 'MemoryUtilization'
				tempNameSpace = 'System/Linux'
				tempPeriod = 300
				tempEvaluation_periods = 2
				tempDimensions = {"InstanceId":self.Instance_Id}
			elif(name == 'SWAP'):
				tempMetric = 'SwapUtilization'
				tempNameSpace = 'System/Linux'
				tempPeriod = 300
				tempEvaluation_periods = 2
				tempDimensions = {"InstanceId":self.Instance_Id}
			elif(name == 'DISK'):
				tempMetric = 'DiskSpaceUtilization'
				tempNameSpace = 'System/Linux'
				tempPeriod = 60
				tempEvaluation_periods = 1
				tempDimensions = {"InstanceId":self.Instance_Id,"MountPath":"/","Filesystem":"/dev/xvda1"}
			else:
				pass

			tempDescription = '%s %s %s' %  ('Alarm when',name,'exceeds 80%')
			print '%s does not have alarm.' % ALARM_NAME
                        print '************************ start **************************'
                        print '--------   start to create %s   ---------' % ALARM_NAME
			alarm = boto.ec2.cloudwatch.MetricAlarm(name=ALARM_NAME, metric=tempMetric, namespace=tempNameSpace, statistic="Average", comparison=">=", threshold=80, period=tempPeriod, evaluation_periods=tempEvaluation_periods, unit="Percent", description=tempDescription, dimensions=tempDimensions, alarm_actions = "arn:aws:sns:us-east-1:739963839279:Anonymous_Dev") 
			self.c.create_alarm(alarm)
     			print '---------    %s created      ------------' % ALARM_NAME
			print '************************ done ***************************'

cmsd = CMSD()
cmsd.createAlarm('CPU')
cmsd.createAlarm('MEM')
cmsd.createAlarm('SWAP')
cmsd.createAlarm('DISK')
