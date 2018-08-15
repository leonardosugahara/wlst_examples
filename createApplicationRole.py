import sys
import StringIO
import re
from java.io import FileInputStream

username = "weblogic"
password = "weblogic1"
adminUrl = "t3://localhost:8001"
domainName = "mydomain"
realmName = "myrealm"
dictionaryAppRoles = {}

def connectDomain():
	try:
		connect(username, password, adminUrl)
		print '|-----------Successfully connected to the domain.'
		serverConfig()
	except:
		print '|-----------The domain is unreacheable. Please try again'
		exit()

##########################################################
#
# Example content properties
#approle.name.group.0=MyApplicationRole.GROUP01
#approle.name.group.0=MyApplicationRole.GROUP02
#approle.name.group.1=OtherApplicationRole.GROUP2
#
#approle.total=2
#
########################################################
def createAppRolesAndGroups():
	try:
		propInputStream = FileInputStream("createAppRoles.properties")
		#inputStreamReader = InputStreamReader(propInputStream,"UTF8")		
		configProps = Properties()
		configProps.load(inputStreamReader)		

		appRoleTotal = configProps.get("approle.total")
		i=0

		while (i < int(appRoleTotal)) :
			
			roleName, groupName = configProps.get("approle.name.group."+ str(i)).split('.')
			
			print '|-----------Role Name: ' + roleName + ' Group Name: ' + groupName
			createGroup(groupName)
			createApplicationRole(roleName)
			grantApplicationRole(roleName,groupName)
			print '|-----------'
			i = i + 1

		
	except:
		print 'ERROR'
		print sys.exc_info()[0] 
		print sys.exc_info()[1]
		exit()

def grantApplicationRole(roleName,groupName):
	try:
		if roleName in dictionaryAppRoles:
			if groupName in dictionaryAppRoles[roleName]:
				print "|-----------Group " + groupName + " already granted to " + roleName
			else:
				grantAppRole("soa-infra",roleName,"weblogic.security.principal.WLSGroupImpl",groupName)
				dictionaryAppRoles[roleName].append(groupName)
				print "|-----------Granted " + groupName + " to application role " + roleName
		else:
			grantAppRole("soa-infra",roleName,"weblogic.security.principal.WLSGroupImpl",groupName)
			dictionaryAppRoles[roleName].append(groupName)
			print "|-----------Granted " + groupName + " to application role " + roleName
	except:
		print "|-----------Error grant Application Role"
		print sys.exc_info()[0] 
		print sys.exc_info()[1]
		exit()

def createGroup(groupName):
	try:

		if myrealmDefaultAuthenticator.groupExists(groupName):
			print "|-----------Group " + groupName + " exists"
		else:
			myrealmDefaultAuthenticator.createGroup(groupName , groupName)
			print "|-----------Group " + groupName + " created"
	except:
		print '|-----------Problem check group'
		print sys.exc_info()[0] 
		print sys.exc_info()[1]
		exit()

def createApplicationRole(roleName):
	try:

		if roleName in dictionaryAppRoles:
			print "|-----------Application Role " + roleName + " exists"
		else:
			createAppRole("soa-infra",roleName)
			dictionaryAppRoles[roleName] = []	
			print "|-----------AppRole " + roleName + " created"
		
	except:
		print '|-----------Problem Check Application Role'
		print sys.exc_info()[0] 
		print sys.exc_info()[1]
		exit()

def loadAppRoles():
	try:
		oldstdout = sys.stdout
		sys.stdout = output = StringIO.StringIO()
		
		listAppRoles("soa-infra")
		sys.stdout = oldstdout
		result = output.getvalue()
		output.close()
		
		principalNames = re.findall("Principal Name \: \w+", result)
		for principalName in principalNames:
			appRoleName = principalName.split(": ")[1]
			dictionaryAppRoles[appRoleName] = []
			loadMembersAppRoles(appRoleName)
	except:
		print '|-----------Problem load exists Application Roles'
		print sys.exc_info()[0] 
		print sys.exc_info()[1]
		exit()

def loadMembersAppRoles(roleName):
	try:
		oldstdout = sys.stdout
		sys.stdout = output = StringIO.StringIO()
		
		listAppRoleMembers("soa-infra",roleName)
		sys.stdout = oldstdout
		result = output.getvalue()
		output.close()
		
		principalNames = re.findall("Principal Name \: \w+", result)
		for principalName in principalNames:
			groupName = principalName.split(": ")[1]
			dictionaryAppRoles[roleName].append(groupName)
	except:
		print '|-----------Problem load exists Members Application Roles'
		print sys.exc_info()[0] 
		print sys.exc_info()[1]
		exit()

def loadMyrealmDefaultAuthenticator():
	try:
		global myrealmDefaultAuthenticator
		myrealmDefaultAuthenticator= cmo.getSecurityConfiguration().getDefaultRealm().lookupAuthenticationProvider("DefaultAuthenticator")
	except:
		print "|-----------Error load DefaultAuthenticator"
		print sys.exc_info()[0] 
		print sys.exc_info()[1]
		exit()


connectDomain()
loadAppRoles()
loadMyrealmDefaultAuthenticator()
createAppRolesAndGroups()
disconnect()
exit()
