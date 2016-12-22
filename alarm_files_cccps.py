#!/usr/bin/python
import boto
import sys
import os

aws_access_id=""
aws_secret_key=""
c = boto.connect_cloudwatch(aws_access_id, aws_secret_key)
InstanceId=os.popen('wget -q -O - http://169.254.169.254/latest/meta-data/instance-id')
Instance_Id=InstanceId.read()
InstanceId.close()

def fileIsExist(fileName):
    dir='/usr/local/utils'
    os.chdir(dir)
    file_name = os.path.exists(fileName)
    #print fileName
    #if file_name:
       # print '%s %s %s' % ('File',fileName,'is exist.')
    #else:
       # print '%s %s %s' % ('File',fileName,'is not exist.')

def fileLineCount(fileName):
    count = -1
    for count, line in enumerate(open(fileName, 'rU')):
        pass
    count += 1
    #print '%s %s %s %s %s' % ('File',fileName,'has',count,'line.')
    return count


def createAlarm(fileName):
    fileIsExist(fileName)
    line_count =  fileLineCount(fileName)
    namespaceStr = "CustomMetric"
    str_alarm_name = '%s%s%s%s%s'%('ALARM_',Instance_Id,'_/usr/local/utils/',fileName,'_files_cccps')
    alarms = c.describe_alarms(alarm_name_prefix=str_alarm_name)
    if alarms:
        print '%s %s %s' % ('File',str_alarm_name,'has alarm.')
    else:
        print '%s %s %s' % ('File',str_alarm_name,'does not have alarm.')
        print '*************** start to create alarm *******************'
        #line_count = linecount(fileName)
        #strname= '%s%s' % (fileName,'_files_cccps')
        strMetricName = '%s%s%s' % (Instance_Id,'_',fileName)
        alarm_Line = boto.ec2.cloudwatch.MetricAlarm(name=str_alarm_name, metric=strMetricName, namespace=namespaceStr, statistic="Maximum", evaluation_periods =1,comparison=">=", threshold=50, period=300, description="File content is more than 50 lines.",alarm_actions = "arn:aws:sns:us-east-1:739963839279:Anonymous_Dev")
	c.create_alarm(alarm_Line)
        print '************************ done ***************************'

if __name__ == '__main__':
	createAlarm('cacheUpdater.log')
	createAlarm('cleaner.log')
	createAlarm('creativeUpdater.log')
	createAlarm('sender.log')
	createAlarm('pixelUpdater.log')
