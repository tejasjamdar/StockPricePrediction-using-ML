# import the necessary packages
from flask import Flask, render_template, redirect, url_for, request,session,Response
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import utils
from statsmodels.tsa.arima_model import ARIMA
import yfinance as yf 
import nltk

login_status = 0

app = Flask(__name__)

app.secret_key = '1234'
app.config["CACHE_TYPE"] = "null"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/', methods=['GET', 'POST'])
def login():
	global login_status
	error = None
	if request.method == 'POST':
		if request.form['username'] != 'admin' or request.form['password'] != 'admin@123':
			error = 'Invalid Credentials. Please try again.'
		else:
			login_status = 1
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
	global login_status
	if login_status == 0:
		return redirect(url_for('login'))
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
	global login_status
	if login_status == 0:
		return redirect(url_for('login')) 
	if request.method == 'POST':
		stock_name = request.form['stock']
		#print(username)
		count = 300	

		tweets = utils.cleanTweets(utils.getTweets('rachana_ranade',stock_name,count))	
		print(tweets)
		utils.export("data/" + "person1.txt", tweets, "w")	

		tweets = utils.cleanTweets(utils.getTweets("PRSundar64", stock_name,count))
		#print(tweets)		
		utils.export("data/"+"person2.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets("PranjalKamra", stock_name,count))
		utils.export("data/"+"person3.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets("CNBC_Awaaz", stock_name,count))
		utils.export("data/"+"person4.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets('TCS',stock_name,count))		
		utils.export("data/" + "person5.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets('Infosys',stock_name,count))		
		utils.export("data/" + "person6.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets('TataSteelLtd',stock_name,count))		
		utils.export("data/" + "person7.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets('NSE_NIFTY',stock_name,count))		
		utils.export("data/" + "person8.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets('smcglobal',stock_name,count))		
		utils.export("data/" + "person9.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets('RNTata2000',stock_name,count))		
		utils.export("data/" + "person10.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets('Pratik_raje96',stock_name,count))		
		utils.export("data/" + "person11.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets('SENSEX_BSE',stock_name,count))		
		utils.export("data/" + "person12.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets('AnilSinghvi_',stock_name,count))		
		utils.export("data/" + "person13.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets('sanjiv_bhasin',stock_name,count))		
		utils.export("data/" + "person14.txt", tweets, "w")

		tweets = utils.cleanTweets(utils.getTweets('RelianceDigital',stock_name,count))		
		utils.export("data/" + "person15.txt", tweets, "w")


		with open(os.path.join('data/'+'person1.txt'),encoding="utf8") as fp:
			Tweets1 = fp.readlines()

		with open(os.path.join('data/'+'person2.txt'),encoding="utf8") as fp:
			Tweets2 = fp.readlines()

		with open(os.path.join('data/'+'person3.txt'),encoding="utf8") as fp:
			Tweets3 = fp.readlines()						

		with open(os.path.join('data/'+'person4.txt'),encoding="utf8") as fp:
			Tweets4 = fp.readlines()

		with open(os.path.join('data/'+'person5.txt'),encoding="utf8") as fp:
			Tweets5 = fp.readlines()

		with open(os.path.join('data/'+'person6.txt'),encoding="utf8") as fp:
			Tweets6= fp.readlines()

		with open(os.path.join('data/'+'person7.txt'),encoding="utf8") as fp:
			Tweets7= fp.readlines()

		with open(os.path.join('data/'+'person8.txt'),encoding="utf8") as fp:
			Tweets8= fp.readlines()

		with open(os.path.join('data/'+'person9.txt'),encoding="utf8") as fp:
			Tweets9= fp.readlines()

		with open(os.path.join('data/'+'person10.txt'),encoding="utf8") as fp:
			Tweets10= fp.readlines()

		with open(os.path.join('data/'+'person11.txt'),encoding="utf8") as fp:
			Tweets11= fp.readlines()

		with open(os.path.join('data/'+'person12.txt'),encoding="utf8") as fp:
			Tweets12= fp.readlines()

		with open(os.path.join('data/'+'person13.txt'),encoding="utf8") as fp:
			Tweets13= fp.readlines()

		with open(os.path.join('data/'+'person14.txt'),encoding="utf8") as fp:
			Tweets14= fp.readlines()

		with open(os.path.join('data/'+'person15.txt'),encoding="utf8") as fp:
			Tweets15= fp.readlines()


		TotalTweets = Tweets1 + Tweets2 + Tweets3 + Tweets4 + Tweets5 + Tweets6 + Tweets7 + Tweets8 + Tweets9 + Tweets10 + Tweets11 + Tweets12 + Tweets13 + Tweets14 + Tweets15


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
					 from_='+12524944507',
					 to='+919860933917'
				 )
				print(message.sid)
				"""
				
				print('SMS Sent')              
				
		if(tot>0):
			pos1 = pos - (tot/2)					
			tot1 = tot/2
			diff = (pos1)/tot1
			print(pos1,neg,tot1,diff)	
		else:
			diff = 0 			    
		#pred = float(currentPrice) + (float(currentPrice)*diff)
		if(diff>0.5):
			pred = "Stock Will Increase"
		else:
			pred = "Stock Will Decrease"			    			    
			
		return render_template('testing.html',tot=int(tot/2),pos=int(pos-(tot/2)),neg=neg,senti=pred,stock=stock_name,per=diff*100)			    
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