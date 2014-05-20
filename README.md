tt-rss-naive-bayes
==================
After spending hours each day for finding the most interesting articles in my TinyTinyRSS (ttrss) instance, I started investigating, how to reduce the amount of news articles i have to read each day.
In the ttrss forum was mentioned to do this by applying a bayes filter.
This approach handles new rss items as ham/spam and scores them accordingly. 


In this first version of the application, all starred and published items are handled as ham, already read items as spam.
The data for training will be extracted based on a bag-of-words approach:
	1.) the content of an article is being extracted
	2.) the content gets stripped of all html tags (and optional stopwords)
	3.) all words are added to the global bag-of-words
	4.) the word-bag collects all words and their word-counts for ham and spam
	5.) the intersection of all words of an article with the bag-of-words forms the features of an article
	

Based on this trainingdata the filter tries to calculate a score for new items.

The next version also will approach the problem by classifying with a k-nearest-neighbor algorithm.
