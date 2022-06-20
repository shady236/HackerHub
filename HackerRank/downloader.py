import os
from time import sleep
import json
from HackerRank import authentication as hacherRankAuth
from HackerRank.domains import getDomainSlug


def saveChallenge(session, challengeSlug, challengeName, parentDirPath):

    # trim spaces in end & start of challenge name
    challengeName = challengeName.strip()
    
    # remove \/:*?"<>| from the challenge name
    notValidChars = '\\/:*?"<>|'
    challengeValidName = '' + challengeName     # start with a copy of the original name
    for char in notValidChars:
        challengeValidName = challengeValidName.replace(char, '')  # remove all invalid characters
    

    challengeDirPath = os.path.join(parentDirPath, challengeValidName)

    # if directory already exists & is not empty, skip
    if (os.path.exists(challengeDirPath)) and (len(os.listdir(challengeDirPath)) > 0):
        return
    
    # get submitions page
    submissionUrl = f'https://www.hackerrank.com/rest/contests/master/challenges/{challengeSlug}/submissions/?'
    params = {
        'offset': 0,
        'limit': 0,			# don't get any submissions now, get only thier count
    }
    page = session.get(submissionUrl, params=params)

    # get count of solved challenges
    submittedCnt = json.loads(page.text)['total']

    # get first accepted submission
    submissionNum = 0
    params['limit'] = 1     # get only one submission at a time
    while (submissionNum < submittedCnt):
        params['offset'] = submissionNum

        page = session.get(submissionUrl, params=params)
        jsonData = json.loads(page.text)
        if jsonData['models'][0]['status'] == 'Accepted':
            break

        submissionNum += 1

    # get this submission's page
    submissionId = jsonData['models'][0]['id']
    submissionUrl = f'https://www.hackerrank.com/rest/contests/master/challenges/{challengeSlug}/submissions/{submissionId}'
    page = session.get(submissionUrl)
    
    jsonData = {
        'model': '',
    }
    try:
        jsonData = json.loads(page.text)
    except:
        return
        
    while (type(jsonData['model']) is not dict):
        sleep(1)       # wait for the website to process the requests
        page = session.get(submissionUrl)
        jsonData = json.loads(page.text)

    # get the submission source code
    sourceCode = jsonData['model']['code']

    language = jsonData['model']['language'].lower()
    languageExtension = {
        'c': '.c',
        'cpp': '.cpp',
        'c_cpp': '.cpp',
        'cpp11': '.cpp',
        'cpp14': '.cpp',
        'cpp17': '.cpp',
        'c++': '.cpp',
        'csharp': '.cs',
        'c#': '.cs',
        'erlang': '.erl',
        'go': '.go',
        'haskell': '.hs',
        'java': '.java',
        'java8': '.java',
        'java11': '.java',
        'jave15': '.java',
        'javascript': '.js',
        'julia': '.jl',
        'kotlin': '.kt',
        'lua': '.lua',
        'ocaml': '.ml',
        'objectivec': '.m',
        'pascal': '.pas',
        'perl': '.pl',
        'php': '.php',
        'pypy': '.py',
        'pypy3': '.py',
        'python': '.py',
        'python2': '.py',
        'python3': '.py',
        'r': '.r',
        'ruby': '.rb',
        'scala': '.scala',
        'shell': '.sh',
        'swift': '.swift',
        'tcl': '.tcl',
        'text': '.txt',
        'typescript': '.ts',
        'visualbasic': '.vb',
    }

    try:
        # if this challenge has no directory, create it
        if not os.path.exists(challengeDirPath):
            os.makedirs(challengeDirPath)

        # save the submission code
        fileName = challengeValidName.strip() + languageExtension[language].strip()
        filePath = os.path.join(challengeDirPath, fileName)
        f = open(filePath, 'w')
        f.write(sourceCode)
        f.close()
    except Exception as e:
        print(e)



progress = 0

def downloadDomainChallenges(session, userName, password, domainName, saveDirPath):
    
    global progress
    
    domainDirPath = os.path.join(saveDirPath, domainName)
    if not os.path.exists(domainDirPath):
        os.makedirs(domainDirPath)
    
    if hacherRankAuth.login(session, userName, password) is False:
        print('Login failed')
        return

    # get domain slug
    domainSlug = getDomainSlug(session, domainName)

    # get the page with the solved domain challenges
    domainUrl = f'https://www.hackerrank.com/rest/contests/master/tracks/{domainSlug}/challenges?filters%5Bstatus%5D%5B%5D=solved'
    downloadParams = {
        'offset': 0,
        'limit': 0,			# don't get any challenges
        'filters%5Bstatus%5D%5B%5D': 'solved',
        'track_login': 'true'
    }
    page = session.get(domainUrl, params=downloadParams)

    # get count of solved challenges in this domain
    solvedCnt = json.loads(page.text)['total']

    # get all solved challenges one by one
    challengeNum = 0              # start from the first challenge
    downloadParams['limit'] = 1   # get only one challenge at a time
    while (challengeNum < solvedCnt):
        downloadParams['offset'] = challengeNum

        # get next solved challenge name & slug
        page = session.get(domainUrl, params=downloadParams)
        jsonData = json.loads(page.text)
        while (type(jsonData['models']) is not list):
            sleep(1)       # wait for the website to process the requests
            page = session.get(domainUrl, params=downloadParams)
            jsonData = json.loads(page.content)
        
        
        challengeSlug = jsonData['models'][0]['slug']
        challengeName = jsonData['models'][0]['name']

        saveChallenge(session, challengeSlug, challengeName, domainDirPath)

        challengeNum += 1
        
        progress = (challengeNum  * 100) // solvedCnt
    
    progress = 100



def getProgress():
    global progress
    return progress