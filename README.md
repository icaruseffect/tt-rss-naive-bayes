tt-rss-naive-bayes
==================
After spending hours each day for finding the most interesting articles in my TinyTinyRSS (tt-rss) instance, I started investigating, how to reduce the amount of news articles i have to read each day.
In the ttrss forum was mentioned to do this by applying a bayes filter.
This approach handles new rss items as ham/spam and scores them accordingly. 


Before explaining further details: Starred items still need to be implemented. Help is welcome.

In this first version of the application, all starred and published items are handled as ham, already read items as spam.
The data for training will be extracted based on a bag-of-words approach:

	1.) the content of an article is being extracted
	
	2.) the content gets stripped of all html tags (and optional stopwords)
	
	3.) all words are added to the global bag-of-words 
	
	4.) the word-bag collects all words and their word-counts for ham and spam 
	
	5.) the intersection of all words of an article with the bag-of-words forms the features of an article 

Based on this trainingdata the filter tries to calculate a score for new items. 

The next version also will approach the problem by classifying with a k-nearest-neighbor algorithm and evaluating 

backend
-------
Processing the data is handled by 3 parts of the backend:

1.) database_manager

-handles the connection to the mysql-server wich holds the tt-rss database.

-It creates an layer between the database and the article_manager to reduce the amount of code.

2.) article_manager

	-handles articles. In the first version handles following tasks:
	-fetches all articles
	-extracts all words 
	-determines individual article features 
	-feeds the filter (*)
	-hands results back to the database manager 
	-drops old articles in a user defined time-span, to keep the filter adapted to current interests. 

3.) filter_manager

	-handles the filters being applied to determine a score (later also individual labels):
	-handling of training-sets
	-creating, saving, loading training-sets 
	-updating training-sets for continious learning/ enhancement of the filter 
	-classification of new articles 
	-provides statistics 
	-comparison of different training sets 
	-precision of ham/spam 
