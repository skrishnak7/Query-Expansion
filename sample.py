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

def take(n, iterable):
    return list(islice(iterable, n))

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

def getITF(doc,documents):
	len1=0
	for doc1 in documents:
		len1 = len1 + len(doc1)

	itf= math.log(len1/len(doc))	 
	return itf 

def getfreq(term,doc):
	count = 0
	for i in doc:
		if (i == term) :
			count = count+1
	return count 		


def getmaxfreq(u,documents):
	freqlist=[]
	for doc in documents:
		c=getfreq(u,doc)
		freqlist.append(c)
	#print freqlist,"#####"
	return max(freqlist)	


def getweightvector(u,documents):
	vec=[]
	maxfreq= getmaxfreq(u,documents)
	sumweights=0
	for doc in documents:
		wij = (0.5 + 0.5*(getfreq(u,doc))/ maxfreq*getITF(doc,documents)) 
		w= wij*wij
		sumweights = sumweights + w
	
	for doc in documents:
		wij = (0.5 + 0.5*(getfreq(u,doc))/ maxfreq*getITF(doc,documents))
		#print wij
		weight = wij / math.sqrt(sumweights)
		vec.append(weight)

	return vec	


def getQueryWeight(query):
	#q1=query.split()
	w=1/math.sqrt(len(q1))
	return w

#def getqueryvector(q1,docs1):
#	qweight=[]
#	qw=getQueryWeight(query)
#	for word in q1:
#		c= getweightvector(word,docs1)
#		qweight.append(c)
#
#	q2 = [sum(x)  for x in zip(*qweight)]
#	q2 = [x*qw for x in q2]	
#	return q2 

def CUV(u,v,documents):
	a = getweightvector(u,documents)
	b = getweightvector(v,documents)
	ab= [x*y for x,y in zip(a,b)]
	ab1 = sum(ab)
	return ab1

def sim(q,v,documents,terms):
	qw=getQueryWeight(q)
	l=0
	for term in terms:
		if term in q:
			l=l+qw*CUV(term,v,documents)
	return l		

docs=[]
'''
doc1 = "The girl is studying in Paris while her brother lives in London. She likes a lot of girlish, artistic Parisian things"
doc2 = "The big museums in London are mostly free to the public, unlike those in Paris. This is why the girl goes to visits her brother often. There are more art lovers in Paris than in London, all youngsters."
doc3 = "Girls like to visit Paris since they are young, whereas boys do not want to hear about Paris at all. London, with the tennis and soccer attractions, is more interesting to them. Boys like sports more."
doc4 = "London is a bigger city than Paris, and they both have metro lines. Lots of people take the metro to go to work or to visit museums in their spare time. More people ride the metro in Paris than in London."
doc5 = "London has a terrific theater scene, unlike Paris. In Paris people have interest in the movies. But they appreciate all sorts of art. Both cities have a great music scene, that often attracts young boys and girls."

docs.append(doc1)
docs.append(doc2)
docs.append(doc3)
docs.append(doc4)
docs.append(doc5)
'''
D1 = "The Mustang, built in Flat Rock, Mich., is still a novelty in Europe, where it went on sale for the first time two years ago."
D2 = "Food allergies have been on the rise in recent years and are currently estimated to affect up to eight percent of children worldwide."
D3 = "Adobe has released an emergency update to its Flash Player after security researchers discovered a bug that allows attackers to take over and then crash users' machines."
D4 = "The worst attack on Adobe software came in 2013, when hackers managed to access personal data for nearly 3 million customers."
D5 = "The Mustang is relatively expensive in Italy compared to the United States. There are few cars available in Italy that offer the Mustang's performance capabilities at a similar price."
D6 = "Adobe said it appeared that the flaw was being actively exploited on systems running Windows with Flash Player. In a statement, Adobe called the flaw a critical vulnerability and urged users to update as soon as possible."
D7 = "Active avoidance of food allergens in baby's diets did not protect them from developing food allergies"
D8 = "Flash Player is widely used for watching video animations and other multimedia"

#docs.append(D1)
#docs.append(D2)
#docs.append(D3)
#docs.append(D4)
#docs.append(D5)
docs.append(D6)
#docs.append(D7)
docs.append(D8)

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

query = "video security"
q1=query.split()


finalsim={}
for term in terms:
	l=sim(q1,term,docs1,terms)
	print term,l
	finalsim[term]=l


f= sorted(finalsim.items(),key=operator.itemgetter(1),reverse=True)
print f

for i,j in f:
	d=0
	expandedterm=""
	if i in q1:
		#print i,j,"#There#"
		continue
	else:
		#print i,"NOtT"
		expandedterm=expandedterm+i
		d=d+1
		break

,  
print query
print query + " " + f[d-1][0]+ " "+f[d][0]	
l="video"
j="security"
print getweightvector(l,docs1)
print getweightvector(j,docs1)