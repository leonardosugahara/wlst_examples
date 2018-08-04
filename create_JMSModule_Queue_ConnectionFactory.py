PATH_JMS_SYSTEM_RESOURCES="/JMSSystemResources/"

def connectDomain():
	try:
		connect(username, password, adminUrl)
		print '|-----------Successfully connected to the domain'
	except:
		print '|-----------The domain is unreacheable. Please try again'
		exit()

def createJMSModule():
	try:
		cd('/')
		jmsModuleMBean = getMBean(PATH_JMS_SYSTEM_RESOURCES+jmsModuleToCreate)
		global jmsModuleCreated
		if jmsModuleMBean is None:
			
			jmsModuleCreated = create(jmsModuleToCreate, "JMSSystemResource")
			print "|-----------Created JMS Module"

			cd(PATH_JMS_SYSTEM_RESOURCES+jmsModuleToCreate)
			set('Targets',jarray.array([ObjectName('com.bea:Name='+targetServer+',Type='+typeServer)], ObjectName)) 
			print "|-----------JMS Module" + jmsModuleToCreate + "target " + targetServer
		else:
			jmsModuleCreated=jmsModuleMBean
			print "|-----------JMS Module "+ jmsModuleToCreate +" already exists"
	except:
		print "Error try create JMS Module"
		print sys.exc_info()[0] 
		print sys.exc_info()[1]
		stopEdit('y')
		exit()

def createJMSSubdeployment():
	try:
		print "|-----------Creating SubDeployment"
		jmsSubDeploymentMBean=getMBean(PATH_JMS_SYSTEM_RESOURCES+jmsModuleToCreate+"/SubDeployments/"+subdeploymentName)
		
		if jmsSubDeploymentMBean is None:
			jmsSubDeploymentMBean=jmsModuleCreated.createSubDeployment(subdeploymentName)

			print "|-----------SubDeployment " + subdeploymentName +" created"

			cd('/SystemResources/'+jmsModuleToCreate+'/SubDeployments/'+subdeploymentName)
			set('Targets',jarray.array([ObjectName('com.bea:Name='+jmsServerName+',Type=JMSServer')], ObjectName))

			print "|-----------SubDeployment " + subdeploymentName +" targeted"
		else:
			print "|-----------SubDeployment " + subdeploymentName +" already exists"
		
	except:
		print "Error try create JMSSubdeployment"
		print sys.exc_info()[0] 
		print sys.exc_info()[1]
		stopEdit('y')
		exit()

def createJMSConnectionFactory(connectionFactoryName,connectionFactoryJNDI):
	try:
		print "|-----------Creating Connection Factory " + connectionFactoryName
		if jmsResourceMBean.lookupConnectionFactory(connectionFactoryName) is None:
			newConnectionFactory = jmsResourceMBean.createConnectionFactory(connectionFactoryName)
			newConnectionFactory.setJNDIName(connectionFactoryJNDI)
			newConnectionFactory.setSubDeploymentName(subdeploymentName)
			newConnectionFactory.transactionParams.setXAConnectionFactoryEnabled(true)
			print "|-----------Created Connection Factory " + connectionFactoryName
		else:
			print "|-----------Connection Factory " + connectionFactoryName + " already exists"
	except:
		print "Error try create JMS Connection Factory"
		print sys.exc_info()[0] 
		print sys.exc_info()[1]
		stopEdit('y')
		exit()

def createJMSQueue(queueName,queueJNDI):
	try:
		print "|-----------Creating Queue " + queueName 
		
		if jmsResourceMBean.lookupQueue(queueName) is None:
			newQueue = jmsResourceMBean.createQueue(queueName)
			newQueue.setJNDIName(queueJNDI)
			newQueue.setSubDeploymentName(subdeploymentName)
			print "|-----------Created Queue " + queueName 
		else: 
			print "|-----------JMS Queue " + queueName + " already exists"
	except:
		print "Error try create JMS Queue"
		print sys.exc_info()[0] 
		print sys.exc_info()[1]
		stopEdit('y')
		#cancelEdit()
		exit()

def defJMSResourcesMBean():
	global jmsResourceMBean
	jmsResourceMBean = getMBean(PATH_JMS_SYSTEM_RESOURCES+jmsModuleToCreate+'/JMSResource/'+jmsModuleToCreate)

###################################################################
#
# Example content connectionFactoryAndQueue.txt
#
# applicationConnectionFactory.queueName
# applicationConnectionFactory.queueName_error
# application2ConnectionFactory.queueName
#
###################################################################
def createConnectionFactoriesAndQueues():
	file = open("connectionFactoryAndQueue.txt", "r") 
	for line in file:

		if line.find(".") > -1:
			connectionFactoryName = line[0:line.find(".")]
			connectionFactoryJNDI = connectionFactoryName
			queueName = line[line.find(".")+1:]
			queueName = queueName.replace("\n","")
			queueJNDI = queueName

			print "|-----------"
			createJMSConnectionFactory(connectionFactoryName,connectionFactoryJNDI)
			print "|-----------"
			createJMSQueue(queueName,queueJNDI)

	file.close() 

#############################################
#
# Variables
#
#############################################

username = "weblogic"
password = "weblogic1"
adminUrl = "t3://localhost:7001"
domainName = "mydomain"
targetServer = "osb_server1"
typeServer = "Server"
jmsServerName = "myJMSServer"
jmsModuleToCreate="myModule"
subdeploymentName="mySubdeployment"

#############################################
#
# Create Module, ConnectionFactory and Queue
#
#############################################
connectDomain();
edit()
startEdit()
createJMSModule()
createJMSSubdeployment()
defJMSResourcesMBean()
createConnectionFactoriesAndQueues()
activate()
dumpStack()
exit()