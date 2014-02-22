from string import punctuation, digits
import numpy as np
import matplotlib.pyplot as plt

def extract_words(input_string):
    """
      Returns a list of lowercase words in a strong.
      Punctuation and digits are separated out into their own words.
    """
    for c in punctuation + digits:
        input_string = input_string.replace(c, ' ' + c + ' ')

    return input_string.lower().split()

def extract_dictionary(file):
    """
      Given a text file, returns a dictionary of unique words.
      Each line is passed into extract_words, and a list on unique
      words is maintained. 
    """
    dict = []
    
    f = open(file, 'r')
    for line in f:
        flist = extract_words(line)
        
        for word in flist:
            if(word not in dict):
                dict.append(word)

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
            flist = extract_words(line)
            for word in flist:
                if(word in dict):
                    feature_matrix[pos, dict.index(word)] = 1
            pos = pos + 1
            
    f.close()
    
    return feature_matrix

def averager(feature_matrix, labels):
    """
      Implements a very simple classifier that averages the feature vectors multiplied by the labels.
      Inputs are an (m, n) matrix (m data points and n features) and a length m label vector. 
      Returns a length-n theta vector (theta_0 is 0). 
    """
    (nsamples, nfeatures) = feature_matrix.shape
    theta_vector = np.zeros([nfeatures])
    theta_0 = 0

    for i in xrange(0, nsamples):
        label = labels[i]
        sample_vector = feature_matrix[i, :]
        theta_vector = theta_vector + label*sample_vector
        theta_0 +=label
    
    #print theta_0, "is theta_0"
    theta_vector = np.append(theta_vector, theta_0)
    return theta_vector

def read_vector_file(fname):
    """
      Reads and returns a vector from a file. 
    """
    return np.genfromtxt(fname)

def perceptron_classify(feature_matrix, theta_0, theta_vector):
    """
      Classifies a set of data points given a weight vector and offset.
      Inputs are an (m, n) matrix of input vectors (m data points and n features),
      a real number offset, and a length n parameter vector.
      Returns a length m label vector. 
    """
    (nsamples, nfeatures) = feature_matrix.shape
    label_output = np.zeros([nsamples])
    
    print nsamples
    
    for i in xrange(0, nsamples):   
        sample_features = feature_matrix[i, :]
        perceptron_output = theta_0 + np.dot(theta_vector, sample_features)

        if(perceptron_output > 0):
            label_output[i] = 1
        else:
            label_output[i] = -1

    return label_output
    
def perceptron(feature_matrix, labels):
    (nsamples, nfeatures) = feature_matrix.shape
    theta = np.zeros([nfeatures])
    theta_0 = 0
    solved = False
    while not solved:
        flag = True
        for i in xrange(0, nsamples):
            label = labels[i]
            sample_features = feature_matrix[i,:]
            if (np.dot(theta, sample_features) + theta_0)*label <= 0 :
                theta = theta + label*sample_features
                theta_0 = theta_0 + label
                flag = False
        if flag:
            solved = True
    #print theta_0, "is the new theta0"
    theta = np.append(theta, [theta_0])
    return theta
    
def passive_agressive(feature_matrix, labels):
    (nsamples, nfeatures) = feature_matrix.shape
    theta = np.zeros([nfeatures])
    solved = False
    while not solved :
        old_theta = theta
        count = 0
        for i in xrange(0, nsamples):
            label = labels[i]
            sample_features = feature_matrix[i,:]
            loss = 0
            if np.dot(theta, sample_features) * label <=1:
                loss = 1- np.dot(theta, sample_features) * label
                count = 0
            eta = loss/((np.linalg.norm(sample_features))**2)
            theta = theta + sample_features*eta*label
            count+=1
        if np.array_equal(theta, old_theta) or count == nsamples:
            solved = True  
    return theta          
    
    
def cross_validation_perceptron(feature_matrix, labels):
    (nsamples, nfeatures) = feature_matrix.shape
    count = 0
    for i in xrange(0, nsamples):
        label = labels[i]
        labels1 = np.delete(labels, i)
        sample_feature = feature_matrix[i, :]
        feature_matrix1 = np.delete(feature_matrix, i,0)
        
        theta = perceptron(feature_matrix1, labels1)
        theta_0 = theta[len(theta)-1]
        theta = np.delete(theta, len(theta)-1)
        
        output = 1 if (np.dot(theta, np.transpose(sample_feature))+theta_0)>0 else -1
        if output == label:
            count+=1
    return count

def cross_validation_passive_agressive(feature_matrix, labels):
    (nsamples, nfeatures) = feature_matrix.shape
    count = 0
    for i in xrange(0, 5):
        label = labels[i]
        labels1 = np.delete(labels, i)
        sample_feature = feature_matrix[i, :]
        feature_matrix1 = np.delete(feature_matrix, i,0)
        
        theta = passive_agressive(feature_matrix1, labels1)
        
        output = 1 if np.dot(theta, np.transpose(sample_feature))>0 else -1
        #print output
        if output == label:
            count+=1
    return count

def write_label_answer(vec, outfile):
    """
      Outputs your label vector the a given file.
      The vector must be of shape (70, ) or (70, 1),
      i.e., 70 rows, or 70 rows and 1 column.
    """
    
    if(vec.shape[0] != 70):
        print("Error - output vector should have 70 rows.")
        print("Aborting write.")
        return

    for v in vec:
        if((v != -1.0) and (v != 1.0)):
            print("Invalid value in input vector.")
            print("Aborting write.")
            return
        
    np.savetxt(outfile, vec)
        

def plot_2d_examples(feature_matrix, labels, theta_0, theta):
    """
      Uses Matplotlib to plot a set of labeled instances, and
      a decision boundary line.
      Inputs: an (m, 2) feature_matrix (m data points each with
      2 features), a length-m label vector, and hyper-plane
      parameters theta_0 and length-2 vector theta. 
    """
    
    cols = []
    xs = []
    ys = []
    
    for i in xrange(0, len(labels)):
        if(labels[i] == 1):
            cols.append('b')
        else:
            cols.append('r')
        xs.append(feature_matrix[i][0])
        ys.append(feature_matrix[i][1])

    plt.scatter(xs, ys, s=40, c=cols)

    [xmin, xmax, ymin, ymax] = plt.axis()

    linex = []
    liney = []
    for x in np.linspace(xmin, xmax):
        linex.append(x)
        if(theta[1] != 0.0):
            y = (-theta_0 - theta[0]*x) / (theta[1])
            liney.append(y)
        else:
            liney.append(0)
    
    plt.plot(linex, liney, 'k-')

    plt.show()
