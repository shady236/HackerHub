from bs4 import BeautifulSoup


# get all available domain names at HackerRank 
def getDomainNames(session):
	
	# not a robot header
	session.headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33'
	}
	
	dashBoardUrl = 'https://www.hackerrank.com/dashboard'
	
	try:
		page = session.get(dashBoardUrl)
		
		soup = BeautifulSoup(page.content, 'html5lib')
		domainsList = soup.find('ul', class_='topics-list').find_all('li')
		
		domains = []
		for domain in domainsList:
			domains.append(domain.find('div', class_='topic-name').text)
		return domains
	
	except:
		return []


# get domain slug from domain name
def getDomainSlug(session, domainName):
	
	# not a robot header
	session.headers = {
		'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36 Edg/102.0.1245.33'
	}
	
	dashBoardUrl = 'https://www.hackerrank.com/dashboard'
	
	try:
		page = session.get(dashBoardUrl)
		
		soup = BeautifulSoup(page.content, 'html5lib')
		domainsList = soup.find('ul', class_='topics-list').find_all('li')
		
		# print(domainList)
		
		for domain in domainsList:
			if domain.find('div', class_='topic-name').text == domainName:
				return domain.find('a', class_='topic-link').get('data-cd-topic-slug')
	except:
		return ""


