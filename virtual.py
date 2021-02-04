import pyttsx3
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
def similarity_index_history(data):
    X =data
    str2=" "
    Y=['show previous history', 'past history']
    for ele in Y:
      str2 += ele
    print(str2)
    Y_list = word_tokenize(str2)
    print(Y_list)
    X_list = word_tokenize(X)    

    sw = stopwords.words('english')
    l1 =[];l2 =[]

# remove stop words from the string
    X_set = {w for w in X_list if not w in sw}
    Y_set = {w for w in Y_list if not w in sw}
    print(X_set)
    print(Y_set)

# form a set containing keywords of both strings
    rvector = X_set.intersection(Y_set)

    #rvector.add("give")
    rvector.add("display")

    #rvector = X_set.intersection(Y_set)
    print("vectorr=", rvector)

#rvector = X_set.union(Y_set)
    if len(rvector)== 0:
      index_val = 0.0
      return index_val
    else:
      for w in rvector:
        if w in X_set: l1.append(1) # create a vector
        else: l1.append(0)
        if w in Y_set: l2.append(1)
        else: l2.append(0)
        c = 0
        print(l1)
        print(l2)
   # cosine formula
      for i in range(len(rvector)):
                  c+= l1[i]*l2[i]
      cosine = c / float((sum(l1)*sum(l2))**0.5)
      print("similarity: ", cosine)
      return cosine

similarity_index_history("i would like to get history of past 2 month")