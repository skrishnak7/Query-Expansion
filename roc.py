from __future__ import division
import re
import sys
import math
import json
import operator
from nltk.stem.porter import*
from operator import add
from collections import Counter

def encode(text):
	return text.encode('utf-8')

def getWordTF(word,doc):
	count=0
	for i in doc:
		if i==word:
			count=count+1

	return count

def getmaxtf(doc):
	terms=[]
	z=[]
	maxtf=0
	for term in doc:
		terms.append(term)
	z=Counter(terms)
	sorted_key = reversed(sorted(z.items(),key = operator.itemgetter(1)))
	for i,j in sorted_key:
		maxtf=j
		break

	return maxtf

def getdocFreq(word,documents):
	count=0
	for doc in documents:
		if word in doc:
			count+=1
	return count
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

def weight1(term,document,documents):
     tf= getWordTF(term,document)
     maxtf = getmaxtf(document)
     if term in document:
     	w1= (0.4+0.6*math.log(tf+0.5)/math.log(maxtf+1.0))
     else:
        w1=0	
     return w1

def weight11(term,document,documents):
     tf= getWordTF(term,document)
     maxtf = getmaxtf(document)
     cs=10
     df=getdocFreq(term,documents)
     if term in document:
     	w1= (0.4+0.6*math.log(  tf+0.5)/math.log(maxtf+1.0))*(math.log(cs/df)/math.log(cs))  
     else:
        w1=0

     return w1


alpha = 1
beta = 0.8
#gamma = 0

def getVector(doc,documents,terms):
	dummy=[]
	for term in terms:
		if term in doc:
			w1=weight11(term,doc,documents)
			dummy.append(w1)
		else:
			dummy.append(0)
	return dummy 		

def getVector1(doc,documents,terms):
	dummy=[]
	for term in terms:
		if term in doc:
			w1=weight1(term,doc,documents)
			dummy.append(w1)
		else:
			dummy.append(0)
	return dummy

def rocchio(query,documents,terms):
	
	docvecs=[]
	for doc in documents:
		c=getVector(doc,documents,terms)
		docvecs.append(c)

	docsum = [sum(x) for x in zip(*docvecs)]
	docsum = [x/len(documents) for x in docsum]
	docsum = [x*beta for x in docsum]

	qv = getVector1(query,documents,terms)
	qv = [x*alpha for x in qv]

	qm = map(add,qv,docsum)
	return qm
   
docs=[]



with open('1.json') as data_file:    
    data = json.load(data_file)

#pprint(data)

for doc in data:
	#print "content:",encode(doc["content"])
	docs.append(encode(doc["content"]))

p = PorterStemmer()
stopwords = getStopWords('stopwords')
commonwords = getStopWords('common_words')

docs1=[]
terms=[]
for doc in docs:
	doc = re.sub(r'[^\sa-zA-Z]','',doc)
	doc = doc.split()
	doc = [term.lower() for term in doc]
	#doc = [p.stem(term) for term in doc]
	doc = [x for x in doc if x not in stopwords]
	doc = [x for x in doc if x not in commonwords]
	docs1.append(doc)	

for doc in docs1:
	for term in doc:
		terms.append(term)	 

z= Counter(terms)
z1 = sorted(z.items(),key=operator.itemgetter(0))

vocab=[]
for i,j in z1:
	vocab.append(i)


for doc in docs1:
	l=getVector(doc,docs1,terms)
	#print len(l),l

#print len(terms)

query = "classic cars"
q1=query.split()

qvec=getVector1(query,docs1,vocab)

#print "qvec",qvec

#print len(rocchio(q1,docs1,vocab))
#print (rocchio(q1,docs1,vocab))

l= rocchio(q1,docs1,vocab)

dic = {}
i=0
for term in vocab:
	dic[term]=l[i]
	i=i+1

#print dic	

f=sorted(dic.items(),key=operator.itemgetter(1),reverse=True)

#print f
#print dic
#print len(dic)

#print z1[art]

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

print f[d][0],f[d+1][0]
#print query
print query + " " + f[d][0]