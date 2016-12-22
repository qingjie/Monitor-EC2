#!/usr/bin/python
import os
import string
import sys
import time
import datetime
import boto.ec2.cloudwatch

cw = boto.ec2.cloudwatch.connect_to_region('us-east-1')
InstanceId=os.popen('wget -q -O - http://169.254.169.254/latest/meta-data/instance-id')
Instance_Id=InstanceId.read()
InstanceId.close()

def fileIsExist(fileName):
    dir='/usr/local/utils'
    os.chdir(dir)
    file_name = os.path.exists(fileName)
    '''
    #print fileName
    if file_name:
        print '%s %s %s' % ('File',fileName,'is exist.')
    else:
        print '%s %s %s' % ('File',fileName,'is not exist.')
    '''


def fileLineCount(fileName):
    count = -1
    for count, line in enumerate(open(fileName, 'rU')):
        pass
    count += 1
    #print '%s %s %s %s %s' % ('File',fileName,'has',count,'line.')
    return count

def putData(fileName):
	fileIsExist(fileName)
	line_count =  fileLineCount(fileName)
    	namespaceStr = "CustomMetric"
        strMetricName = '%s%s%s' % (Instance_Id,'_',fileName)
    	cw.put_metric_data(namespace=namespaceStr, name=strMetricName, value=line_count, unit='Count')

if __name__ == '__main__':
	putData('cacheUpdater.log')
	putData('cleaner.log')
	putData('creativeUpdater.log')
	putData('pixelUpdater.log')
	putData('sender.log')
