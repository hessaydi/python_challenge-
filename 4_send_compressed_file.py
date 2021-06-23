# First we have to install pysmb module in our envirnment:pip3 install pysmb

from smb.SMBConnection import SMBConnection

def send(compressed_file_path=""):
	host="xxx.xxx.xxx.xxx"  #ip or domain name
	username="xxxxxx"
	password="xxxxxx"
	conn = SMBConnection(username,password, "", "", use_ntlm_v2 = True) # configure out connection session
	result = conn.connect(host, 445) # connexion to the server

	print("login successful")


	## Upload file to the server
	localFile=open(file_path,"rb") # Open local files, note that if a binary file, such as zip package, need to add the parameter b, that is binary mode, the default mode is t, that is, text text mode.
	Storage_path = "" # here we put path to the local where we want to store out file into
	conn.storeFile("Shared folder name","",localFile)  # Smb upload files to the server, the default 30-second timeout, you can modify: timeout = xx. Storage path is a relative path of the shared folder.

	localFile.close() # we close the session
	print('the file has been submited successfully')

if __name__ == '__main__':
	# the path to the file that we want the send to Windows share
	compressed_file_path = input('put path into your compressed  backup file: ')
	send(compressed_file_path)

