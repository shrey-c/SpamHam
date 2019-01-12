import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import string
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


messages = [line.rstrip() for line in open('smsspamcollection/SMSSpamCollection')]
print(len(messages))

for message_no, message in enumerate(messages[:10]):
    print(message_no, message)
    print('\n')

messages = pd.read_csv('smsspamcollection/SMSSpamCollection', sep='\t',
                           names=["label", "message"])
messages.head()
messages.describe()
messages.groupby('label').describe()
messages['length'] = messages['message'].apply(len)
messages.head()

messages['length'].plot(bins=50, kind='hist')
messages.length.describe()
messages[messages['length'] == 910]['message'].iloc[0]
messages.hist(column='length', by='label', bins=50,figsize=(12,4))


mess = 'Sample message! Notice: it has punctuation.'

# Check characters to see if they are in punctuation
nopunc = [char for char in mess if char not in string.punctuation]

# Join the characters again to form the string.
nopunc = ''.join(nopunc)


stopwords.words('english')[0:10] # Show some stop words
nopunc.split()
# Now just remove any stopwords
clean_mess = [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]


def text_process(mess):
    """
    Takes in a string of text, then performs the following:
    1. Remove all punctuation
    2. Remove all stopwords
    3. Returns a list of the cleaned text
    """
    # Check characters to see if they are in punctuation
    nopunc = [char for char in mess if char not in string.punctuation]

    # Join the characters again to form the string.
    nopunc = ''.join(nopunc)

    # Now just remove any stopwords
    return [word for word in nopunc.split() if word.lower() not in stopwords.words('english')]

messages.head()
# Check to make sure its working
messages['message'].head(5).apply(text_process)
# Show original dataframe
messages.head()

# Might take awhile...
bow_transformer = CountVectorizer(analyzer=text_process).fit(messages['message'])

# Print total number of vocab words
print(len(bow_transformer.vocabulary_))

message4 = messages['message'][3]
print(message4)

bow4 = bow_transformer.transform([message4])
print(bow4)
print(bow4.shape)

print(bow_transformer.get_feature_names()[4073])
print(bow_transformer.get_feature_names()[9570])
messages_bow = bow_transformer.transform(messages['message'])
print('Shape of Sparse Matrix: ', messages_bow.shape)
print('Amount of Non-Zero occurences: ', messages_bow.nnz)
sparsity = (100.0 * messages_bow.nnz / (messages_bow.shape[0] * messages_bow.shape[1]))
print('sparsity: {}'.format(round(sparsity)))

tfidf_transformer = TfidfTransformer().fit(messages_bow)
tfidf4 = tfidf_transformer.transform(bow4)
print(tfidf4)

print(tfidf_transformer.idf_[bow_transformer.vocabulary_['u']])
print(tfidf_transformer.idf_[bow_transformer.vocabulary_['university']])

messages_tfidf = tfidf_transformer.transform(messages_bow)
print(messages_tfidf.shape)

spam_detect_model = MultinomialNB().fit(messages_tfidf, messages['label'])

print('predicted:', spam_detect_model.predict(tfidf4)[0])
print('expected:', messages.label[3])
all_predictions = spam_detect_model.predict(messages_tfidf)
print(all_predictions)

print (classification_report(messages['label'], all_predictions))
