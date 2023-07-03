# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request,session,Response
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from statsmodels.tsa.arima_model import ARIMA
import yfinance as yf
import utils
import nltk

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin':
			error = 'Invalid Credentials. Please try again.'
		else:
			return redirect(url_for('home'))

	return render_template('login.html', error=error)

@app.route('/home', methods=['GET', 'POST'])
def home():
	return render_template('home.html')

@app.route('/info', methods=['GET', 'POST'])
def info():
	return render_template('info.html')

@app.route('/input', methods=['GET', 'POST'])
def input():
	if request.method == 'POST':
		
		stock = request.form['stock']
		sdate = request.form['sdate']
		edate = request.form['edate']

		data = yf.download(stock,sdate,edate)
		stockPrice = data['Adj Close']
		print(stockPrice)
		stockPrice.to_csv('historic_data.csv')
		data['Adj Close'].plot()
		plt.savefig('static/images/stockprice.jpg')

		df = stockPrice
		currentPrice = df[len(df)-1]
		model = ARIMA(df, order=(1, 1, 1))
		model_fit = model.fit(disp=False)
		yhat = model_fit.predict(len(df), len(df), typ='levels')
		predictedPrice = yhat.tolist()
		print(type(yhat))

		#data = yf.download(stock,edate,edate)
		#stockPrice = (data['Adj Close']).tolist()
		stockPrice = stockPrice[-1]

		return render_template('input.html',stock=stock,sdate=sdate,edate=edate,pprice=predictedPrice,cprice=stockPrice)

	return render_template('input.html')

@app.route('/testing',methods=['GET', 'POST'])
def testing(): 
	if request.method == 'POST':
		stock_name = request.form['stock']
		screen_name = request.form['name']
		#print(username)
		count = 300	

		tweets = utils.cleanTweets(utils.getTweets('rachana_ranade',stock_name, count))
		print(tweets)		
		utils.export("data/" + "person1.txt", tweets, "w")

	
		tweets = utils.cleanTweets(utils.getTweets("PRSundar64", stock_name,count))
		#print(tweets)		
		utils.export("data/"+"person2.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets("PranjalKamra", stock_name,count))
		utils.export("data/"+"person3.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets("CNBC_Awaaz", stock_name,count))
		utils.export("data/"+"person4.txt", tweets, "w")

		with open(os.path.join('data/'+'person1.txt'),encoding="utf8") as fp:
			Tweets1 = fp.readlines()

		with open(os.path.join('data/'+'person2.txt'),encoding="utf8") as fp:
			Tweets2 = fp.readlines()

		with open(os.path.join('data/'+'person3.txt'),encoding="utf8") as fp:
			Tweets3 = fp.readlines()						

		with open(os.path.join('data/'+'person4.txt'),encoding="utf8") as fp:
			Tweets4 = fp.readlines()

		TotalTweets = Tweets1 + Tweets2 + Tweets3 + Tweets4

		utils.export("data/"+"person.txt", TotalTweets, "w")
	
		'''	
		with open('Person.txt','w') as fp:
			fp.write(TotalTweets)			
		'''
		data = utils.getTrainData()
		tot = 0		
		pos = 0	
		neg = 0	
		def get_words_in_tweets(tweets):	
			all_words = []
			for (words, sentiment) in tweets:
	  			all_words.extend(words)
			return all_words

		def get_word_features(wordlist):		
		
			wordlist = nltk.FreqDist(wordlist)
			word_features = wordlist.keys()
			return word_features

		word_features = get_word_features(get_words_in_tweets(data))
		#print(word_features)				
		


		def extract_features(document):		
			document_words = set(document)
			features = {}
			for word in word_features:
				#features[word.decode("utf8")] = (word in document_words)
				features[word] = (word in document_words)
			print(features)
			return features

		allsetlength = len(data)
		print(allsetlength)		
		#training_set = nltk.classify.apply_features(extract_features, data[:allsetlength/10*8])		
		training_set = nltk.classify.apply_features(extract_features, data[:88])
		#test_set = data[allsetlength/10*8:]		
		test_set = data[88:]		
		classifier = nltk.NaiveBayesClassifier.train(training_set)			
		
		def classify(tweet):
			return(classifier.classify(extract_features(tweet.split())))
			
				
			
		f = open("data/person.txt", "r",encoding="utf8")	
			
		#print(tot,neg,pos)
		for tweet in f:
			tot = tot + 1
			result = classify(tweet)
			if(result == 'pos'):
				pos = pos + 1		
			elif(result == 'neg'):				
				neg = neg + 1
			senti = (neg/(tot/2))*100    #divided by two because of blank lines in person.txt

			if(senti > 35):
				"""
				message = client.messages \
				.create(
					 body="Join Earth's mightiest heroes. Like Kevin Bacon.",
					 from_='+15017122661',
					 to='+15558675310'
				 )
				print(message.sid)
				"""
				print('SMS Sent')              
				
		if(tot>0):
			pos1 = pos - (tot/2)					
			tot1 = tot/2
			diff = (pos1 - neg)/tot1
			print(pos1,neg,tot1,diff)
		else:
			diff = 0 			    
		#pred = float(currentPrice) + (float(currentPrice)*diff)
		if(diff>0.5):
			pred = "Stock Will Increase"
		else:
			pred = "Stock Will Decrease"			    			    
			
		return render_template('testing.html',tot=int(tot/2),pos=int(pos-(tot/2)),neg=neg,senti=pred,stock=stock_name,per=diff*100,name=screen_name)			    
	return render_template('testing.html')

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=True, threaded=True)