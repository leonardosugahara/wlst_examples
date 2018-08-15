import subprocess
import os

###################################################################
#
# SET YOUR ENVIRONMENTS, ALIAS AND .crt FILE
#
################################################################### 
MIDDLEWARE_HOME = "/app/oracle/Middleware_12.2.1.2"
JAVA_HOME = "/app/jdk/jdk1.8.0_131"
CERT_FILE="/app/mycert.crt"
CERT_ALIAS = "mycertalias"
###################################################################

###################################################################
#
# IF PRODUCTS 11G
# WLS_SERVER_LIB = "/wlserver_10.3/server/lib"
#
###################################################################
WLS_SERVER_LIB = "/wlserver/server/lib"

my_env = os.environ.copy()
my_env['JAVA_HOME'] = JAVA_HOME
my_env['PATH'] = my_env['JAVA_HOME'] + "/bin:" + my_env['PATH']

os.chdir(MIDDLEWARE_HOME+WLS_SERVER_LIB)

listKeytoolCommand = ["keytool","-list","-v","-keystore","DemoTrust.jks","-storepass","DemoTrustKeyStorePassPhrase"]

keytoolListProcess = subprocess.Popen(listKeytoolCommand, stdout=subprocess.PIPE, env=my_env)
grepProcess = subprocess.Popen(["grep","-i","alias"],stdin=keytoolListProcess.stdout , stdout=subprocess.PIPE, env=my_env)
stdout, stderr = grepProcess.communicate()

for line in stdout.split('\n'):
	if line.find(":") > -1 :
		alias = line.split(": ")[1]
		#print alias
		if alias == CERT_ALIAS:
			print CERT_ALIAS + " already exists"
			exit()
	 
importKeytoolCommand = ["keytool","-import","-v","-noprompt","-trustcacerts","-alias", CERT_ALIAS,"-file", CERT_FILE, "-keystore", 
"DemoTrust.jks","-storepass", "DemoTrustKeyStorePassPhrase"]

importProcess = subprocess.Popen(importKeytoolCommand,stdout=subprocess.PIPE, env=my_env)
stdout, stderr = importProcess.communicate()

print stdout