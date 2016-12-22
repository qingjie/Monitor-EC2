#!/usr/bin/python

class VO:

	def __init__(self,temp1,temp2):
		self.Name = temp1
		self.Size = temp2
		
	def setName(self,name):
		self.Name = name

	def getName(self):
		return self.Name

	def setSize(self,size):
		self.Size = size

	def getSize(self):
		return self.Size
        
	name = property(getName,setName)
	size = property(getSize,setSize)

