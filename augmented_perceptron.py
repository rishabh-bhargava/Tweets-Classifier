import numpy as np
import project1_code as p1
import math

def extract_dictionary(file):
    """
      Given a text file, returns a dictionary of unique words.
      Each line is passed into extract_words, and a list on unique
      words is maintained. 
    """
    dict = []
    
    f = open(file, 'r')
    for line in f:
        flist = p1.extract_words(line)
        
        for word in flist:
            is_new_word = True
            for entry in dict:
            	if word == entry[0]:
            		entry[1]+=1
            		is_new_word = False
            if is_new_word:
            	dict.append([word, 1])

    f.close()

    return dict

def extract_feature_vectors(file, dict): 
    """
      Returns a bag-of-words representation of a text file, given a dictionary.
      The returned matrix is of shape (m, n), where the text file has m non-blank
      lines, and the dictionary has n entries. 
    """
    f = open(file, 'r') 
    num_lines = 0

    for line in f:
    	if(line.strip()):
        	num_lines = num_lines + 1

    f.close()

    feature_matrix = np.zeros([num_lines, len(dict)])

    f = open(file, 'r')
    pos = 0
    
    for line in f:
    	if(line.strip()):
    		flist = p1.extract_words(line)
    		for word in flist: 
    			for entry in dict:
    				if word == entry[0]:
    					feature_matrix[pos, dict.index(entry)] = math.floor(math.log(1+entry[1]))
    		pos = pos + 1
            
    f.close()
    
    return feature_matrix

dictionary = extract_dictionary('train-tweet.txt')
labels = p1.read_vector_file('train-answer.txt')
feature_matrix = extract_feature_vectors('train-tweet.txt', dictionary)

theta = p1.perceptron(feature_matrix, labels)
theta_0 = theta[len(theta)-1]
theta = np.delete(theta, len(theta)-1)
label_output = p1.perceptron_classify(feature_matrix, theta_0, theta)

correct = 0
for i in xrange(0, len(label_output)):
    if(label_output[i] == labels[i]):
        correct = correct + 1

percentage_correct = 100.0 * correct / len(label_output)
print("Augmented perceptron gets " + str(percentage_correct) + "% correct (" + str(correct) + " out of " + str(len(label_output)) + ").")

test = p1.cross_validation_perceptron(feature_matrix, labels)
print test

#returned 508