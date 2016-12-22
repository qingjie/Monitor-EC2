#!/usr/bin/python
import boto
import sys
import os

aws_access_id=""
aws_secret_key=""
c = boto.connect_cloudwatch(aws_access_id, aws_secret_key)
fileName="/usr/share/jetty/logs/activeLog.log"
namespaceStr = "CustomMetric"
InstanceId=os.popen('wget -q -O - http://169.254.169.254/latest/meta-data/instance-id')
Instance_Id=InstanceId.read()
InstanceId.close()

def linecount(fileName):
    count = -1
    for count, line in enumerate(open(fileName, 'rU')):
        pass
    count += 1
    return count

def createAlarm():
    #str_alarm_name = 'ALARM_ErrorActiveLog'
    str_alarm_name='%s%s%s'%('ALARM_',Instance_Id,'_/usr/share/jetty/logs/activeLog.log')
    alarms = c.describe_alarms(alarm_name_prefix=str_alarm_name)
    if alarms:
        print 'The activeLog.log has alarm.'
    else:
        print 'This activeLog.log does not have alarm.'
        print '*************** start to create alarm *******************'
        #line_count = linecount(fileName)
        strMetricName = '%s%s' % (Instance_Id,'_activeLog.log')
        alarm_ErrorLine = boto.ec2.cloudwatch.MetricAlarm(name=str_alarm_name, metric=strMetricName, namespace="CustomMetric", statistic="Maximum", evaluation_periods =1,comparison=">=", threshold=200, period=300, description="Error lines in Log are greater than 200.",alarm_actions = "arn:aws:sns:us-east-1:739963839279:Anonymous_Dev")
        c.create_alarm(alarm_ErrorLine)
        print '************************ done ***************************'

if __name__ == '__main__':
    createAlarm()
