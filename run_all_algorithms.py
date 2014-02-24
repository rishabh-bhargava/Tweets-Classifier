import numpy as np
import project1_code as p1

dictionary = p1.extract_dictionary('train-tweet.txt')
labels = p1.read_vector_file('train-answer.txt')
feature_matrix = p1.extract_feature_vectors('train-tweet.txt', dictionary)
feature_matrix_real = p1.extract_feature_vectors('sample_from_tweepy.txt', dictionary)


average_without_offset_theta = p1.averager(feature_matrix, labels)
theta_0 = average_without_offset_theta[len(average_without_offset_theta)-1]
average_without_offset_theta = np.delete(average_without_offset_theta, len(average_without_offset_theta)-1)

label_output = p1.perceptron_classify(feature_matrix, 0, average_without_offset_theta)

correct = 0
for i in xrange(0, len(label_output)):
    if(label_output[i] == labels[i]):
        correct = correct + 1

percentage_correct = 100.0 * correct / len(label_output)
print("Averager without offset gets " + str(percentage_correct) + "% correct (" + str(correct) + " out of " + str(len(label_output)) + ").")


average_theta = p1.averager(feature_matrix, labels)
theta_0 = average_theta[len(average_theta)-1]
average_theta = np.delete(average_theta, len(average_theta)-1)

label_output = p1.perceptron_classify(feature_matrix, theta_0, average_theta)

correct = 0
for i in xrange(0, len(label_output)):
    if(label_output[i] == labels[i]):
        correct = correct + 1

percentage_correct = 100.0 * correct / len(label_output)
print("Averager gets " + str(percentage_correct) + "% correct (" + str(correct) + " out of " + str(len(label_output)) + ").")


perceptron_theta = p1.perceptron(feature_matrix, labels)
theta_0 = perceptron_theta[len(perceptron_theta)-1]
perceptron_theta = np.delete(perceptron_theta, len(perceptron_theta)-1)

label_output = p1.perceptron_classify(feature_matrix, theta_0, perceptron_theta)
real_label_output = p1.perceptron_classify(feature_matrix_real, theta_0,perceptron_theta)
p1.write_label_answer(real_label_output,"sample_from_tweepy_answer.txt")
correct = 0
for i in xrange(0, len(label_output)):
    if(label_output[i] == labels[i]):
        correct = correct + 1

percentage_correct = 100.0 * correct / len(label_output)
print("Perceptron gets " + str(percentage_correct) + "% correct (" + str(correct) + " out of " + str(len(label_output)) + ").")



passive_agressive_theta = p1.passive_agressive(feature_matrix, labels)

label_output = p1.perceptron_classify(feature_matrix, 0, passive_agressive_theta)

correct = 0
for i in xrange(0, len(label_output)):
    if(label_output[i] == labels[i]):
        correct = correct + 1

percentage_correct = 100.0 * correct / len(label_output)
print("Passive Agressive gets " + str(percentage_correct) + "% correct (" + str(correct) + " out of " + str(len(label_output)) + ").")

