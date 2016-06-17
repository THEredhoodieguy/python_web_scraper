import urllib.request, re

def get_links(link, domain, domain_type):
	"""Returns a list of links present on a page
	excludes links that are not apart of the main domain"""

	links = list()

	handle = urllib.request.urlopen(link)
	html = handle.read()

	#regex to find '<a href=" " and capture the contents'
	expr = re.compile(r'(?is)<a.*?href=.*?"(\S*?)".*?>', re.IGNORECASE | re.DOTALL)
	
	f = expr.findall(str(html))

	if f:
		links = f

	for i in range(0,len(links)):
		if(domain_type not in links[i]):
			links[i] = domain + links[i]


	return links


def generate_sitemap(starter_page, domain, domain_type):
	"""Take a starter page and a domain name to create a sitemap.
	The domain prevents the function from trying to create a map 
	of the entire internet"""

	#Dictionary to hold links that we have visited
	webpages = {}

	#List to hold pages we want to visit
	pages_to_visit = list()
	pages_to_visit.append(starter_page)
	pages_visited = list()


	while(len(pages_to_visit) > 0):
		#While there are pages left to visit, keep parsing pages
		
		#Get a page to visit and denote that it has been visited
		current_page = pages_to_visit[0]
		pages_visited.append(current_page)

		links = get_links(current_page, domain, domain_type)

		#populate the sitemap
		webpages[current_page] = links

		for link in links:
			if((domain in link) and (link not in pages_visited)):
				pages_to_visit.append(link)

		pages_to_visit.pop(0)

	return webpages