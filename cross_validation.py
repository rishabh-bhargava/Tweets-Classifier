import project1_code as p1

dictionary = p1.extract_dictionary('train-tweet.txt')
labels = p1.read_vector_file('train-answer.txt')
feature_matrix = p1.extract_feature_vectors('train-tweet.txt', dictionary)
#print feature_matrix.shape

#test = p1.cross_validation_perceptron(feature_matrix, labels)
#print test
#returned 519

test = p1.cross_validation_passive_agressive(feature_matrix, labels)
print test