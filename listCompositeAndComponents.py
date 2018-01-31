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

 		

def selectComponentsByComposite():
	try:
		for soaConfigProperty in listSOAObjects:

			compositeObject = ObjectName(soaConfigProperty)

			if compositeObject.getKeyProperty('SCAComposite') in mapComposite:
				mapComposite[compositeObject.getKeyProperty('SCAComposite')].append(compositeObject)
	except:
		print "problem select components: " + sys.exc_info()[0] + " " + sys.exc_info()[1]
		exit() 
 		
def showCompositeAndComponents():

	try:
		for compositeNameMap in mapComposite:
	 		print compositeNameMap
	 		listItens = mapComposite[compositeNameMap]
	 		for item in listItens:
	 			if item.getKeyProperty('name') in "WSBinding":
	 				if item.getKeyProperty('SCAComposite.SCAReference'):
	 					print "|----" + item.getKeyProperty('SCAComposite.SCAReference')
	 				else:
	 					print "|----" + item.getKeyProperty('SCAComposite.SCAService')
	 			else:
	 				print "|----" + item.getKeyProperty('name')
	 				compProperties = mbs.getAttribute(item, 'Properties')
	 				for prop in compProperties:
	 					print "     |------------" + prop.get('name') 							
	except:
		print "problem show composites: " + sys.exc_info()[0] + " " + sys.exc_info()[1] 
 		exit()


connectDomain();
listOracleSoaConfig();
selectComposite();
selectComponentsByComposite();
showCompositeAndComponents();
disconnect();
exit();
