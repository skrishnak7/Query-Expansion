# Query-Expansion


As association cluster is based on the co-occurrence of stems (or terms) inside
documents. The idea is that stems which co-occur frequently inside documents
have a synonymity association. 

Association clusters are based on the frequency of co-occurrence of pairs of
terms in documents and do not take into account where the terms occur in
a document.
Since two terms which occur in the same sentence seem more
correlated than two terms which occur far apart in a document, it
might be worthwhile to factor in the distance between two terms in the
computation of their correlation factor. Metric clusters are based on this
idea.

One additional form of deriving a synonymity relationship between
two local stems (or terms) su
and sv
is by comparing the sets Su
(n)
and Sv
(n).
 The idea is that two stems with similar neighborhoods have some
synonymity relationship.
 In this case we say that the relationship is indirect or induced by the
neighborhood.
 One way of quantifying such neighborhood relationships is to
arrange all correlation values su,I in a vector , to arrange all
correlation values sv,I in another vector , and to compare these
vectors through a scalar measure.
 For instance, the cosine of the angle between the two vectors is
a popular scalar similarity measure. 


local.py ->Query expansion using Scalar clustering 
roc.py -> Query expansion using Rocchio Algorithm
sample.py ->Query expansion using Association Clustering
met.py -> Query expansion using Metric Clustering  


