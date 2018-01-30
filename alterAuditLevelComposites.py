import sys
import os
from java.lang import System

username = "weblogic"
password = "weblogic1"
adminUrl = "t3://localhost:7005"
mapComposite = {}

def connectDomain():
    try:
        connect(username, password, adminUrl)
        print 'Successfully connected to the domain\n'
    except:
        print 'The domain is unreacheable. Please try again\n'
        exit()

def listOracleSoaConfig():

	try:
		custom()
 		cd('oracle.soa.config')
 		redirect('/dev/null','false')
 		global listSOAObjects
 		listSOAObjects = ls(returnMap='true')
 		redirect('/dev/null','true')
 		return
 	except:
 		print "problem list soa config: " + sys.exc_info()[0] + " " + sys.exc_info()[1]
 		exit() 

def selectComposite():

	try:

 		for soaConfigProperty in listSOAObjects:

 			compositeObject = ObjectName(soaConfigProperty)

 			if compositeObject.getKeyProperty('j2eeType') == 'SCAComposite':

				if compositeObject.getKeyProperty('name') in mapComposite:
					mapComposite[compositeObject.getKeyProperty('name')].append(compositeObject)
				else:
					mapComposite[compositeObject.getKeyProperty('name')] = [compositeObject]
	except:
		print "problem select composites: " + sys.exc_info()[0] + " " + sys.exc_info()[1]
		exit()

def alterAuditLevelAllComposites():
	try:
		auditParams = ['auditLevel','Inherit']
 		sign = ['java.lang.String','java.lang.String']
		
		for compositeNameMap in mapComposite:
	 		print "alter composite audit level for " + compositeNameMap
	 		listItens = mapComposite[compositeNameMap]
	 		for item in listItens:
	 			mbs.invoke(item,'setProperty',auditParams,sign)
	except:
		print "problem alter audit level composites: " + sys.exc_info()[0] + " " + sys.exc_info()[1]
		exit()

def showCompositeAndComponents():

	try:
		for compositeNameMap in mapComposite:
	 		print compositeNameMap
	 		listItens = mapComposite[compositeNameMap]
	 		for item in listItens:
	 			print "|----" + item.getKeyProperty('name')
	 			compProperties = mbs.getAttribute(item, 'Properties')
	 			for prop in compProperties:
	 				print "     |------------" + prop.get('name') + " value: " + prop.get('value')  							
	except:
		print "problem show composites: " + sys.exc_info()[0] + " " + sys.exc_info()[1] 
 		exit()
 							
	
connectDomain();
listOracleSoaConfig();
selectComposite();
showCompositeAndComponents();
alterAuditLevelAllComposites();
showCompositeAndComponents();
disconnect();
exit();