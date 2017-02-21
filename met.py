from __future__ import division
import re
import sys
import operator
import math
import json
from pprint import pprint
from nltk.stem.porter import*
from collections import Counter
from itertools import islice

#Function to encode the retrieved json content 
def encode(text):
	return text.encode('utf-8')

#Take out the first two elements of the dictionary 
def take(n, iterable):
    return list(islice(iterable, n))

#Retrive stopwords from the file named stopwords 
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


def dist(u,v,doc):
	countu=0
	countv=0
	count=0
	for term in doc:
		if term == u:
			countu=count
		if term == v:
			countv=count
		count=count+1
	return countu-countv	

#Correlation factor for Association Clustering 
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


#Correlation factor for Metric Clustering
def MCorrelationFactor(u,v,documents):
	cuv=0
	for doc in documents:
		if ((u in doc) and (v in doc)) :
			r=abs(dist(u,v,doc))
		else:
			r=0
		if(r!=0):	
		 cuv=cuv+(1/r)

	return cuv	




#Metric Cluster for word U in the relevant documents obtained
def metric(u,documents,z):
	s={}
	for i,j in z.items():
		suv=MCorrelationFactor(u,i,documents)
		s[i]=suv

	slist= reversed(sorted(s.items(),key=operator.itemgetter(1)))
	top2= take(20,slist)
	return top2	

				
docs=[]


D1 = "The Mustang, built in Flat Rock, Mich., is still a novelty in Europe, where it went on sale for the first time two years ago."
D2 = "Food allergies have been on the rise in recent years and are currently estimated to affect up to eight percent of children worldwide."
D3 = "Adobe has released an emergency update to its Flash Player after security researchers discovered a bug that allows attackers to take over and then crash users' machines."
D4 = "The worst attack on Adobe software came in 2013, when hackers managed to access personal data for nearly 3 million customers."
D5 = "The Mustang is relatively expensive in Italy compared to the United States. There are few cars available in Italy that offer the Mustang's performance capabilities at a similar price."
D6 = "Adobe appear flaw active exploit system run Window Flash Player statement Adobe flaw critical vulnerability urg user update soon possible"
D7 = "Active avoidance of food allergens in baby's diets did not protect them from developing food allergies"
D8 = "Flash Player wide use watch video animation multimedia."

#docs.append(D1)
#docs.append(D2)
#docs.append(D3)
#docs.append(D4)
#docs.append(D5)
docs.append(D6)
#docs.append(D7)
docs.append(D8)


#with open('1.json') as data_file:    
 #   data = json.load(data_file)

#pprint(data)

#for doc in data:
	#print "content:",encode(doc["content"])
#	docs.append(encode(doc["content"]))


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


for doc in docs1:
	print doc
	for term in doc:
		if (term in stopwords) or (term in commonwords):
			continue
		else:	 
			terms.append(term)	 

z= Counter(terms)
k=1

z1 = sorted(z.items(),key=operator.itemgetter(0))
#for i,j in z1:
#	print i
for i, j in z1:
	print k,i,j
	k=k+1

 
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

for row in mat1:
	print len(row),row

query="video security"
q1=query.split()
#q1=[p.stem(term) for term in q1]

for q in q1:
	l=metric(q,docs1,z)
	#print q,len(l),l
	print l[0][0]
