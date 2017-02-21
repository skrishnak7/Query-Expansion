from __future__ import division
import sys
import math
import operator
import json
from pprint import pprint
from nltk.stem.porter import*
from itertools import islice
from collections import Counter

def take(n, iterable):
    return list(islice(iterable, n))

def encode(text):
	return text.encode('utf-8')

def getStopWords(filename):
	stopwords = []
	fp= open(filename,'r')
	line = fp.readline()
	while line:
		word =line.strip()
		stopwords.append(word)
		line = fp.readline()

	fp.close()
	return stopwords


def CorrelationFactor(u,v,mat1,z):
	uindex=0
	vindex=0
	cuv=0
	count = 0
	for i,j in z.items():
		if i==u :
			uindex=count 

		if i==v :
			vindex = count

		count = count + 1		

	for row in mat1:
		cuv=cuv+row[uindex]*row[vindex]
        
	return cuv 	


def StemCLuster(u,mat1,z):
	s={}
	for i,j in z.items():
		suv = (CorrelationFactor(u,i,mat1,z) / ((CorrelationFactor(u,u,mat1,z)) + CorrelationFactor(i,i,mat1,z)+ CorrelationFactor(u,i,mat1,z))) 
		#print suv
		s[i]= suv

	sorteds= sorted(s.items(),key=operator.itemgetter(1),reverse=True)
	#firsttwoitems = take(3,sorteds)
	#print firsttwoitems
	return sorteds    

docs=[]


with open('1.json') as data_file:    
    data = json.load(data_file)

#pprint(data)

for doc in data:
	#print "content:",encode(doc["content"])
	docs.append(encode(doc["content"]))

#print len(data)


stopwords = getStopWords('stopwords')
commonwords = getStopWords('common_words')

p = PorterStemmer()

terms = [] 

docs1=[]
for doc in docs:
	doc = re.sub(r'[^\sa-zA-Z]', '', doc)
	doc = doc.split()
	doc = [term.lower() for term in doc]
	#doc = [p.stem(term) for term in doc]
	docs1.append(doc)

#for doc in docs1:
#	print doc

for doc in docs1:
	for term in doc:
		if (term in stopwords) or (term in commonwords):
			continue
		else:	 
			terms.append(term)	 

z= Counter(terms)
z1 = sorted(z.items(),key=operator.itemgetter(0))


mat1 = []

for doc in docs1:
	row = []
	y=Counter(doc)
	for term,count in z.items():
		if term in doc:
			c=y[term]
			row.append(c)
		else:
			row.append(0)
	mat1.append(row)			
    
#for row in mat1:
#	print row

query= "car rental"
q1=query.split()

f=StemCLuster(query,mat1,z)

for i,j in f:
	d=0
	expandedterm=""
	if i in q1:
		#print i,"#There#"
		continue
	else:
		#print i,"NOtT"

		expandedterm=expandedterm+i
		d=d+1
		break

print f
#print f[d][0],f[d+1][0]
#print query
print query + " " + f[d][0]
