import os
from bs4 import BeautifulSoup
from GitHub import authentication as gitHubAuth



progress = 0

def uploadDir(session, userName, password, dirPath):
    
    global progress
    
    if gitHubAuth.login(session, userName, password) is False:
        return 
    
    # get all repositorie names at github
    repositoriesUrl = f'https://github.com/{userName}?tab=repositories'
    repositoriesPage = session.get(repositoriesUrl)
    gitHubAuth.updateCookie(session, repositoriesPage)
    # sys.stdout.buffer.write(repositoriesPage.text.encode('utf-8'))
    
    soup = BeautifulSoup(repositoriesPage.text, 'html5lib')
    reposDiv = soup.find('div', {'id': 'user-repositories-list'})
    reposList = reposDiv.find_all('li')
    reposNames = []
    for repo in reposList:
        reposNames.append(repo.find('a').text)
    
    # check if repo exists with name HackerRank-Solutions
    repoExists = False
    for repo in reposNames:
        if repo.find('HackerRank-Solutions') != -1:
            repoExists = True
            break
    
    
    # if repo not excist, create it
    if not repoExists:
        createRepoUrl = f'https://github.com/new'
        createRepoPage = session.get(createRepoUrl)
        gitHubAuth.updateCookie(session, createRepoPage)
        
        soup = BeautifulSoup(createRepoPage.text, 'html5lib')
        form = soup.find('form', attrs={'action': '/repositories'})
        soup = BeautifulSoup(form.prettify(), 'html5lib')
        createRepoToken = soup.find('input', attrs={'name': 'authenticity_token'})['value']
        
        newRepoData = {
            'authenticity_token': createRepoToken,
            'owner': userName,
            'repository[name]': 'HackerRank-Solutions',
            'repository[visibility]': 'public',
            'repository[auto_init]': '0',
        }
        
        createRepoUrl = 'https://github.com/repositories'
        createRepoRes = session.post(createRepoUrl, data=newRepoData)
        gitHubAuth.updateCookie(session, createRepoRes)
        
    
    
    dirPath = dirPath.replace('\\', '/')
    domainName = os.path.basename(dirPath)
    
    subDirs = os.listdir(dirPath)
    totalUploads = len(subDirs)
    uploaded = 0
    
    for subDir in subDirs:
        subDirPath = os.path.join(dirPath, subDir)
        if os.path.isdir(subDirPath) == False:
            continue
        
        filesNames = os.listdir(subDirPath)
        if len(filesNames) == 0:
            continue
        
        fileName = filesNames[0]
        fileContent = open(os.path.join(subDirPath, fileName), 'r').read()
        
        
        uploadUrl = f'https://github.com/{userName}/HackerRank-Solutions/new/main'
        uploadPage = session.get(uploadUrl)
        gitHubAuth.updateCookie(session, uploadPage)
        
        soup = BeautifulSoup(uploadPage.text, 'html5lib')
        form = soup.find('form', attrs={'action': f'/{userName}/HackerRank-Solutions/create/main'})
        soup = BeautifulSoup(form.prettify(), 'html5lib')
        createToken = soup.find('input', attrs={'name': 'authenticity_token'})['value']
        
        commitList = soup.find_all('input', attrs={'name': 'commit'})
        commitValue = ''
        for commit in commitList:
            # if commit has value attribute, it is the commit button
            if commit.has_attr('value'):
                commitValue = commit['value']
                break
        
        
        newFolderData = {
            'authenticity_token': createToken,
            'filename': fileName,
            'new_filename': f'{domainName}/{subDir}/{fileName}',
            'content_changed': 'true',
            'value': fileContent,
            'message': 'Uploaded from HackerHub',
            'commit-choice': 'direct',
            'target_branch': 'main',
            'same_repo': 1,
            'commit': commitValue,
        }
        
        createUrl = f'https://github.com/{userName}/HackerRank-Solutions/create/main'
        createResponce = session.post(createUrl, data=newFolderData)
        gitHubAuth.updateCookie(session, createResponce)
        
        uploaded += 1
        progress = (uploaded * 100) // totalUploads
        
    
    progress = 100
    os._exit(status=0)



def getProgress():
    global progress
    return progress

