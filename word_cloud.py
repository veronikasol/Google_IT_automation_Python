"""This assignment is from the final project of the first course "Crash course on Python"
The task was to write the script that would take a text file and create a word cloud of it using wordcloud module
"""

import wordcloud

uninteresting = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", 
                 "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", 
                 "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", 
                 "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", 
                 "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", 
                 "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", 
                 "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", 
                 "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", 
                 "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", 
                 "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", 
                 "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", 
                 "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", 
                 "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", 
                 "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", 
                 "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", 
                 "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", 
                 "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", 
                 "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", 
                 "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own",
                 "part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", 
                 "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", 
                 "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", 
                 "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", 
                 "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", 
                 "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", 
                 "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", 
                 "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", 
                 "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", 
                 "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", 
                 "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", 
                 "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", 
                 "the"]

punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
filename = input('Please, enter text file name from current dirrectory to make a word cloud from\n')

def create_word_cloud(text_file, stop_words):
	"""Take text file and list of stop words that will not be counted.
	Create a dictionary with words and word frequencies.
	Then pass this dictionary to the generate_from_frequencies function of the WordCloud class.
	And create (passed_filename).jpg file with words cloud."""
	
	def word_clear(line, stop_words):
		"""Util function to clean line of words from punctuation and stop words"""
		words = line.split()
		clean_words=[]
		for word in words:
			word = word.lower().strip(punctuations)
			if word not in stop_words and len(word)>2:
				clean_words.append(word)
		return clean_words
	# Creating dictionary of words with their frequencies
	frequencies = {}
	with open(text_file, 'r') as f:
		for line in f:
			n_line = word_clear(line, uninteresting)
			for word in n_line:
				frequencies[word] = frequencies.get(word,0) + 1

	#Passing created dictionary to wordcloud module to create a picture of the most used words
	cloud = wordcloud.WordCloud()
	cloud.generate_from_frequencies(frequencies)
	
	#Generating new image of word cloud
	cloud_filename = text_file.split('.')[0]
	cloud.to_file("{}.jpg".format(cloud_filename))
	print('You have created new file with word cloud. File name is {}.jpg'.format(cloud_filename))


if __name__ == "__main__":
	if not filename:
		print('You did not enter any file name')
	else:
		try:
			create_word_cloud(filename, uninteresting)
		except FileNotFoundError:
			print("There's no such file")
		except UnicodeDecodeError:
			print("File format doesn't allow to count words and to create a cloud of it")
		except:
			print('Something went wrong')