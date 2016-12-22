#!/usr/bin/python
import boto.ec2.cloudwatch
import os

cw = boto.ec2.cloudwatch.connect_to_region('us-east-1')
InstanceId=os.popen('wget -q -O - http://169.254.169.254/latest/meta-data/instance-id')
Instance_Id=InstanceId.read()
InstanceId.close()


def fileLength(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
	#print i
    return i + 1
strMetricName = '%s%s' % (Instance_Id,'_activeLog.log')
activeLog_ErrorLine = fileLength("/usr/share/jetty/logs/activeLog.log")
cw.put_metric_data(namespace="CustomMetric", name=strMetricName, value=activeLog_ErrorLine, unit='Count')
