import paramiko




username = "t1"
ip = "192.168.7."
host = [str(ip)+str(i) for i in range(30,60)]
# host = [ip]
password = "uni1"
try:
	for i in host:
		print ("Trying for ",i)
		#print (local_loc , remote)
		try:
			ssh_client = paramiko.SSHClient()
			ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh_client.connect(hostname=i,username=username,password=password)
			ssh_client.invoke_shell()
			
			ssh_client.exec_command("poweroff")#To only poweroff all systems comment all the upcoming lines . 
			
			ssh_client.exec_command ("(cd /home/t1/Documents && touch get-pip.py && touch requirements.txt )")
			ssh_client.exec_command (" wget --no-check-certificate  https://bootstrap.pypa.io/get-pip.py ") 
			ssh_client.exec_command (" python2.7 -m install get-pip.py  ")
			
			local_loc = os.popen("pwd").read()
			ftp_client = ssh_client.open_sftp()
			local_loc = "/home/jafer/lab_freak/get-pip.py"
			remote = "/home/t1/Documents/get-pip.py"
			
		
			ftp_client.put(local_loc,remote)
			local = "/home/jafer/lab_freak/requirements.txt"
			remote = "/home/t1/Documents/requirements.txt"
			ftp_client.put(local,remote)
			
			ftp_client.close()
			ssh_client.exec_command("python /home/t1/Documents/get-pip.py --user")
			ssh_client.exec_command("python2.7 -m pip install  --user  -r /home/t1/Documents/requirements.txt")
			
			ssh_client.exec_command("python2.7 -m pip install  --user  scipy")
			ssh_client.exec_command("python2.7 -m pip install  --user   sklearn")
		except:
			pass



except Exception as e:
	print (e)
	pass
