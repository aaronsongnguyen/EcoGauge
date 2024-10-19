import json
import random
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import f1_score

class Sentiment:
    NEGATIVE = "Negative"
    POSITIVE = "Positive"
    NEUTRAL = "Neutral"

class Review:
    def __init__(self, text, score):
        self.text = text
        self.score = score
        self.sentiment = self.get_sentiment()

    def get_sentiment(self):
        if self.score <= 2:
            return Sentiment.NEGATIVE
        elif self.score == 3:
            return Sentiment.NEUTRAL
        else:
            return Sentiment.POSITIVE

class ReviewContainer:
    def __init__(self, reviews):
        self.reviews = reviews

    def get_text(self):
        return [x.text for x in self.reviews]

    def get_sentiment(self):
        return [x.sentiment for x in self.reviews]


    def evenly_distribute(self):
        negative = list(filter(lambda x: x.sentiment == Sentiment.NEGATIVE, self.reviews))
        positive = list(filter(lambda x: x.sentiment == Sentiment.POSITIVE, self.reviews))

        positive_shrunk = positive[:len(negative)]
        self.reviews = negative + positive_shrunk
        random.shuffle(self.reviews)


file_name = '/Users/kylehan/Downloads/Books_small_10000.json'

reviews = []

with open(file_name) as f:
    for line in f:
        review = json.loads(line)
        
        reviews.append(Review(review['reviewText'], review['overall'])) #creates a list with Review objects with text and score attributes



training, testing = train_test_split(reviews, test_size=0.33, random_state=42)
train_container = ReviewContainer(training)
test_container = ReviewContainer(testing)


train_container.evenly_distribute()
training_x = train_container.get_text()
training_y = train_container.get_sentiment()

test_container.evenly_distribute()
testing_x = test_container.get_text()
testing_y = test_container.get_sentiment()

training_y.count(Sentiment.POSITIVE)
training_y.count(Sentiment.NEGATIVE)



#vectorizes training and testing text data into numerical format
vectorizer = TfidfVectorizer()
training_x_vectors = vectorizer.fit_transform(training_x)
testing_x_vectors = vectorizer.transform(testing_x)





#scikit learn svm model
clf_svm = svm.SVC(kernel='linear')
clf_svm.fit(training_x_vectors, training_y)
clf_svm.predict(testing_x_vectors[0])

#scikit decision tree model
clf_dec = DecisionTreeClassifier()
clf_dec.fit(training_x_vectors, training_y)
clf_dec.predict(testing_x_vectors[0])

#scitkit gaussian naive bayes model
clf_gnb = GaussianNB()
training_x_vectors_dense = training_x_vectors.toarray()
testing_x_vectors_dense = testing_x_vectors.toarray()
clf_gnb.fit(training_x_vectors_dense, training_y)
clf_gnb.predict(testing_x_vectors_dense[0].reshape(1, -1))

#scikit logistic regression model
clf_log = LogisticRegression()
clf_log.fit(training_x_vectors, training_y)
clf_log.predict(testing_x_vectors[0])


#prints the accuracy of each model
print(f'This is the initial svm model accuracy: {clf_svm.score(testing_x_vectors, testing_y)}')
print(f'This is the inital dec model accuracy: {clf_dec.score(testing_x_vectors, testing_y)}')
print(f'This is the initial gnb model accuracy: {clf_gnb.score(testing_x_vectors_dense, testing_y)}')
print(f'This is the initial log model accuracy: {clf_log.score(testing_x_vectors, testing_y)}')




f1_score(testing_y, clf_svm.predict(testing_x_vectors), average=None, labels=[Sentiment.POSITIVE, Sentiment.NEGATIVE])


test_set = ['the customer service was not that great given the fact that they served me raw chicken', "wow this restaurant is really favorable", "horrible waste of time"]
new_test = vectorizer.transform(test_set)
print('\n')
print(test_set)
print(f'This is the prediction results for the sample test set: {clf_svm.predict(new_test)}')



#parameter tuning to increase model accuracy
parameters = {'kernel': ('linear', 'rbf'), 'C': (1, 4, 8, 16, 32)}
svc = svm.SVC()
clf = GridSearchCV(svc, parameters, cv=5)
clf.fit(training_x_vectors, training_y)
print('\n')
print(f'This is the svm accuracy post parameter tuning: {clf.score(testing_x_vectors, testing_y)}')
