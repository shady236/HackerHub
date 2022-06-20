import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import requests
import threading
from HackerRank import domains
from HackerRank import downloader 
from HackerRank import authentication as hackerRankAuth
from GitHub import authentication as gitHubAuth
from GitHub import uploader



def errorMsg(msgTitle, msgText):
	errorMsg = Toplevel()
	errorMsg.title(msgTitle)
	errorMsg.minsize(max(len(msgText) * 9, 300), 100)
	errorMsg.resizable(False, False)
	
	errorMsgLabel = Label(errorMsg, text='\n' + msgText, font=('Arial', 11))
	errorMsgLabel.pack()
	
	


# no internet connection
def noInternetConnection():
	errorMsg('No internet connection', 'Please check your internet connection')
	


# wrong user name or password
def authError(website):
	errorMsg('Authentication Error', f'Please check your {website} user name and password')




hackerRankUserName = ''
hackerRankPassword = ''
domain = {}
saveToDirectory = ''
gitHubUserName = ''
gitHubPassword = ''

def submitInfo():
	
	global hackerRankUserName, hackerRankPassword, domain, saveToDirectory, gitHubUserName, gitHubPassword
	global root, hackerRankUserNameEntry, hackerRankPasswordEntry, domainComboBox, saveToDirectoryEntry, gitHubUserNameEntry, gitHubPasswordEntry
	
	# get input info from user
	hackerRankUserName = hackerRankUserNameEntry.get()
	hackerRankPassword = hackerRankPasswordEntry.get()
	domain = domainComboBox.get()
	saveToDirectory = saveToDirectoryEntry.get()
	gitHubUserName = gitHubUserNameEntry.get()
	gitHubPassword = gitHubPasswordEntry.get()
	
	# check if all fields are filled
	if (hackerRankUserName == '') or (hackerRankPassword == '') or (domain == '') or (saveToDirectory == '') or (gitHubUserName == '') or (gitHubPassword == ''):
		errorMsg('Missing information', 'Please fill all fields')
		return
	
	# make sure the directory exists
	if not os.path.exists(saveToDirectory):
		errorMsg('Invalid directory', 'Please check the directory path')
		return
	
	# make sure the user name and password for HackerRank are correct
	if hackerRankAuth.login(requests.Session(), hackerRankUserName, hackerRankPassword) == False:
		authError('HackerRank')
		return
	
	# make sure the user name and password for GitHub are correct
	if gitHubAuth.login(requests.Session(), gitHubUserName, gitHubPassword) == False:
		authError('GitHub')
		return
	
	# now all info is correct, start downloading & uploading in new thread
	threading.Thread(target=downloadAndUpload).start()
	
	# update the progress bar each second
	threading.Timer(1, updateProgressBar).start()
	
	
	


def downloadAndUpload():
	session = requests.Session()
	downloader.downloadDomainChallenges(session, hackerRankUserName, hackerRankPassword, domain, saveToDirectory)
	uploader.uploadDir(session, gitHubUserName, gitHubPassword, os.path.join(saveToDirectory, domain))
	


def updateProgressBar():
	
	global root, progressBar, progressBarLabel
	
	downloadProgress = downloader.getProgress()
	uploadProgress = uploader.getProgress()
	
	if downloadProgress == 100 and uploadProgress == 100:
		# if root is not closed, close it
		if root.state() != 'withdrawn':
			root.destroy()
		return
	elif downloadProgress == 100:
		progressLabel.config(text='Uploading...')
		progressBar['value'] = uploadProgress
		progressBar.update()
	else:
		progressLabel.config(text='Downloading...')
		progressBar.config(value=downloadProgress)
		progressBar.update()
	
	threading.Timer(1, updateProgressBar).start()




def openBrowsingWindow():
	saveToDirectoryEntry.delete(0, END)
	saveToDirectoryEntry.insert(0, filedialog.askdirectory())


availableDomains = domains.getDomainNames(requests.Session())
entryWidth  = 40
smallFont = ('calibri', 8)
regularFont = ('calibri', 13, 'normal')
boldFont = ('calibri', 10, 'bold')
bigFont  = ('calibri', 20, 'bold')


root = Tk()
root.title('HackerHub')
root.minsize(500, 600)

# add margins to the window
frame = Frame(root)
frame.pack(fill = 'both', expand = True, padx = 10, pady = 10)




curRow = 0
# create a label & entry for HackerRank user name
Label(frame, text='HackerRank username', font=regularFont).grid(row=curRow, sticky=W)
curRow += 1
hackerRankUserNameEntry = Entry(frame, width=entryWidth, font=regularFont)
hackerRankUserNameEntry.grid(row=curRow, sticky=W)
curRow += 1


# insert some padding
Label(frame, text='', font=smallFont).grid(row=curRow)
curRow += 1


# create a label & entry for HackerRank password
Label(frame, text='HackerRank password', font=regularFont).grid(row=curRow, sticky=W)
curRow += 1
hackerRankPasswordEntry = Entry(frame, width=entryWidth, font=regularFont, show='*')
hackerRankPasswordEntry.grid(row=curRow, sticky=W)
curRow += 1


# insert some padding
Label(frame, text='', font=smallFont).grid(row=curRow)
curRow += 1


# create a label & combobox for domain selection
Label(frame, text='Domain', font=regularFont).grid(row=curRow, sticky=W)
curRow += 1
domainComboBox = ttk.Combobox(frame, values=list(availableDomains), width=entryWidth - 2, font=regularFont, state='readonly')
domainComboBox.grid(row=curRow, sticky=W)
curRow += 1
if availableDomains == []:
	noInternetConnection()
else:
	domainComboBox.current(0)


# insert some padding
Label(frame, text='', font=smallFont).grid(row=curRow)
curRow += 1



# create a label, entry & button for save to directory
Label(frame, text='Directory path', font=regularFont).grid(row=curRow, sticky=W)
curRow += 1
saveToDirectoryEntry = Entry(frame, width=entryWidth, font=regularFont)
saveToDirectoryEntry.grid(row=curRow, sticky=W)
saveToBrowseBtn = Button(frame, text='. . .', command=openBrowsingWindow, bg='grey80', font=boldFont)
saveToBrowseBtn.grid(row=curRow, column=1, sticky=W)
curRow += 1


# insert some padding
Label(frame, text='', font=smallFont).grid(row=curRow)
curRow += 1

# create a label & entry for gitHub user name
Label(frame, text='GitHub username', font=regularFont).grid(row=curRow, sticky=W)
curRow += 1
gitHubUserNameEntry = Entry(frame, width=entryWidth, font=regularFont)
gitHubUserNameEntry.grid(row=curRow, sticky=W)
curRow += 1


# insert some padding
Label(frame, text='', font=smallFont).grid(row=curRow)
curRow += 1


# create a label & entry for gitHub password
Label(frame, text='GitHub password', font=regularFont).grid(row=curRow, sticky=W)
curRow += 1
gitHubPasswordEntry = Entry(frame, width=entryWidth, font=regularFont, show='*')
gitHubPasswordEntry.grid(row=curRow, sticky=W)
curRow += 1


# insert big padding
Label(frame, text='', font=bigFont).grid(row=curRow)
curRow += 1



# create a button to submit the info and start downloading
submitBtn = Button(frame, text='Start Downloading', command=submitInfo, width=entryWidth//2, bg='green', fg='white', font=bigFont)
submitBtn.grid(row=curRow, sticky=S)
curRow += 1


# insert some padding
Label(frame, text='', font=smallFont).grid(row=curRow)
curRow += 1



# progress bar
progressLabel = Label(frame, text='', font=regularFont)
progressLabel.grid(row=curRow, sticky=W)
curRow += 1
progressBar = ttk.Progressbar(frame, orient=HORIZONTAL, length=entryWidth * 9, mode="determinate", maximum=100, value=0)
progressBar.grid(row=curRow)




root.mainloop()

# kill all threads
for thread in threading.enumerate():
	if thread is threading.current_thread():
		continue
	thread.join()
