from bottle import route, run, request
import requests
import time
from bs4 import BeautifulSoup
import json

@route('/')
def index():
	 output='<b>Hello</b>'
	 return output
@route('/form', method='POST')
def form():
	import requests
	from bs4 import BeautifulSoup
	from treelib import Tree
	import re

	def extract_n_from_page(url, count):
	    assert count>0
	    page = requests.get(url)
	    print('Requested', url)
	    soup = BeautifulSoup(page.text, 'html.parser')
	    for tag in soup.select('table'):
	        tag.decompose()
	    page_data = soup.find(id="bodyContent", class_="mw-body-content")

	    links = []
	    for url in page_data.find_all('p'):
	        var = url.find('a')
	        if var != None:
	            a = var.get('href')
	            pattern = r'/wiki/\w+$'
	            match = re.match(pattern, a)
	            if match:
	                link = 'https://en.wikipedia.org' + a
	                if link in links:
	                	continue
	                links.append(link)
	    return(links[:count])

	def extract(node, num_links, depth):
	    if depth == 0: return
	    links = extract_n_from_page(node.tag, num_links)
	    for child_url in links:
	        child_node = tree.create_node(child_url, parent=node)
	        extract(child_node, num_links, depth-1)


	website=request.forms.get('website')
	no_links = request.forms.get('no_links')
	no_links=int(no_links)
	depth = request.forms.get('depth')
	depth=int(depth)
	tree = Tree()
	root = tree.create_node(website)
	extract(root, no_links, depth)
	tree.show(line_type="ascii-em")
	print(tree.to_json())
	with open('data.json', 'w') as outfile:
		json.dump(tree.to_dict(),outfile)
	return tree.to_json()
@route('/form1', method='POST')
def form1():
	website=request.forms.get('website')
	no_links=request.forms.get('no_links')
	no_links=int(no_links)
	depth=request.forms.get('depth')
	depth=int(depth)
	start_time = time.clock()
	l=[]
	dic={}
	s=2
	e=1
	t=0
	k=1
	f=1
	def extract(web,count):
		page = requests.get(web)
		soup = BeautifulSoup(page.text, 'html.parser')
		for tag in soup.select('table'):
			tag.decompose()
		page_data = soup.find(id="bodyContent", class_="mw-body-content")
		for url in page_data.find_all('p'):
			var=url.find('a')
			if var != None:
				a = var.get('href')

				if a != None and a[0] != '#' and a != 'None' and a[0:2] != '//' and a != '#mw-head' and a != '#p-search' and a[-1] != ')' and a[-4] != '.' and a[0] !='(':
					if a[0:3] != 'www' and a[0:4] != 'http':
						links = 'https://en.wikipedia.org' + a
						if links in l:
							continue
						l.append(links)
						count=count-1
						if count<1:
							break
		return(len(l))


	def dictionary(i,var1):
		dic[i] = l[var1:]
		return()

	def crawl(x,y,z,w):
		for num in range(x,y):
			time.sleep(0.1)
			extract(l[num],no_links)
		dictionary(z,w)
		return(len(l))
	dic[0]=website
	q=extract(website,no_links)
	dictionary(1,0)
	while(depth>1):
		depth=depth-1
		r=0
		for num in range(0,k-1):
			r=((len(dic[num+1])+r))*t
			print("value of r",r)
		k=k+1
		crawl(r,len(l),s,len(l))
		t=1
		s=s+1
		e=e+1
	f=0
	print(l)
	print(len(l))
	for k,v in dic.items():
		print ("level : ," ,k)
		print ("Links : ",v)
		print ("-----------------")
	def search(myDict, lookup):
		for key, value in myDict.items():
			for v in value:
				if lookup in v:
					print("I Found it")
					return key
	m=search(dic,'https://en.wikipedia.org/wiki/Latin')
	print("value of m",m)
	f=dic[m].index('https://en.wikipedia.org/wiki/Latin')
	print('Value of f ',f)
	def tracking(index):
		counting=-1
		for num in range(0,1000):
			counting=counting+1
			if index in range(0+no_links*num,no_links+no_links*num):
				break
		return (counting)


	while(m>1):
		m=m-1
		f=tracking(f)
		print('tracked location',f)
		print("path",dic[m][f])
	print (time.clock() - start_time, "seconds")
	var=dic
	return var
run(host='localhost', port=8080, debug='True',reloader='True')
