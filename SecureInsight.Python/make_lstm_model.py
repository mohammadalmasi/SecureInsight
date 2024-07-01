import os
import sys
import json
import numpy
import random
import pickle
import myutils
import warnings
from datetime import datetime
from colorama import Fore, Style
from keras.models import Sequential
from sklearn.utils import class_weight
from keras.preprocessing import sequence
from keras.layers import LSTM, Dense
from gensim.models import Word2Vec
from highlighted_excepthook import ExceptionSetup

class MakeLSTMModel:
    def __init__(self, modes, samples_path, save_model_path, dropout, neurons, epochs, batch_size, vector_size, iteration, min_count):
        self.modes = modes
        self.samples_path = samples_path
        self.save_model_path = save_model_path
        self.dropout = dropout
        self.neurons = neurons
        self.epochs = epochs
        self.batch_size = batch_size
        self.vector_size = vector_size
        self.iteration = iteration
        self.min_count = min_count
        self.w2v_model, self.word_vectors = self.LoadModel()

    def LoadModel(self):
        #get word2vec model
        w2vmodel = f"{self.save_model_path}\\word2vec_{self.vector_size}_{self.iteration}_{self.min_count}.model"
        #load word2vec model
        if not (os.path.isfile(w2vmodel)):
          print(f"{Style.BRIGHT}{Fore.YELLOW}WORD2VEC model is still being created...")
          sys.exit()
          
        w2v_model = Word2Vec.load(w2vmodel)
        word_vectors = w2v_model.wv
        return w2v_model , word_vectors
    
    def train_model(self):
        for mode in self.modes:
            #default mode / type of vulnerability
            print(f"+++++++++++++++++++++++++++++ {Fore.GREEN}{Style.BRIGHT}{mode}{Style.RESET_ALL} +++++++++++++++++++++++++++++")
            
            #get the vulnerability from the command line argument
            if (len(sys.argv) > 1):
              mode = sys.argv[1]
            
            progress = 0
            count = 0
            
            ### paramters for the filtering and creation of samples
            restriction = [20000,5,6,10] #which samples to filter out
            step = 5 #step lenght n in the description
            fulllength = 10 #context length m in the description
            
            #load data
            with open(f'{self.samples_path}/plain_' + mode +'.txt', 'r') as infile:
              data = json.load(infile)

            allblocks = []
            
            for r in data:
              progress = progress + 1
              
              for c in data[r]:
                
                if "files" in data[r][c]:                      
                #  if len(data[r][c]["files"]) > restriction[3]:
                    #too many files
                #    continue
                  
                  for f in data[r][c]["files"]:
                    
              #      if len(data[r][c]["files"][f]["changes"]) >= restriction[2]:
                      #too many changes in a single file
               #       continue
                    
                    if not "source" in data[r][c]["files"][f]:
                      #no sourcecode
                      continue
                    
                    if "source" in data[r][c]["files"][f]:
                      sourcecode = data[r][c]["files"][f]["source"]                          
                 #     if len(sourcecode) > restriction[0]:
                        #sourcecode is too long
                 #       continue
                      
                      allbadparts = []
                      
                      for change in data[r][c]["files"][f]["changes"]:
                        
                            #get the modified or removed parts from each change that happened in the commit                  
                            badparts = change["badparts"]
                            count = count + len(badparts)
                            
                       #     if len(badparts) > restriction[1]:
                              #too many modifications in one change
                       #       break
                            
                            for bad in badparts:
                              #check if they can be found within the file
                              pos = myutils.findposition(bad,sourcecode)
                              if not -1 in pos:
                                  allbadparts.append(bad)
                                  
                         #   if (len(allbadparts) > restriction[2]):
                              #too many bad positions in the file
                         #     break
                                  
                      if(len(allbadparts) > 0):
                     #   if len(allbadparts) < restriction[2]:
                          #find the positions of all modified parts
                          positions = myutils.findpositions(allbadparts,sourcecode)
            
                          #get the file split up in samples
                          blocks = myutils.getblocks(sourcecode, positions, step, fulllength)
                          
                          for b in blocks:
                              #each is a tuple of code and label
                              allblocks.append(b)
            
            keys = []
            
            #randomize the sample and split into train, validate and final test set
            for i in range(len(allblocks)):
              keys.append(i)
            random.shuffle(keys)
            
            cutoff = round(0.7 * len(keys)) #     70% for the training set
            cutoff2 = round(0.85 * len(keys)) #   15% for the validation set and 15% for the final test set
            
            keystrain = keys[:cutoff]
            keystest = keys[cutoff:cutoff2]
            keysfinaltest = keys[cutoff2:]
            
            print(f"{Style.BRIGHT}{Fore.YELLOW}cutoff: {str(cutoff)}")
            print(f"{Style.BRIGHT}{Fore.YELLOW}cutoff2: {str(cutoff2)}")

            
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_keystrain'), 'wb') as fp:
              pickle.dump(keystrain, fp)
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_keystest'), 'wb') as fp:
              pickle.dump(keystest, fp)
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_keysfinaltest') , 'wb') as fp:
              pickle.dump(keysfinaltest, fp)
            
            TrainX = []
            TrainY = []
            ValidateX = []
            ValidateY = []
            FinaltestX = []
            FinaltestY = []
            
            print(f"{Fore.YELLOW}Creating {Style.BRIGHT}{mode} {Style.RESET_ALL}{Fore.YELLOW} training dataset...")
            for k in keystrain:
              block = allblocks[k]    
              code = block[0]
              token = myutils.getTokens(code) #get all single tokens from the snippet of code
              vectorlist = []
              for t in token: #convert all tokens into their word2vec vector representation
                if t in self.word_vectors.key_to_index and t != " ":
                  vector = self.w2v_model.wv[t]
                  vectorlist.append(vector.tolist()) 
              TrainX.append(vectorlist) #append the list of vectors to the X (independent variable)
              TrainY.append(block[1]) #append the label to the Y (dependent variable)
            
            print(f"{Fore.YELLOW}Creating {Style.BRIGHT}{mode} {Style.RESET_ALL}{Fore.YELLOW} validation dataset...")
            for k in keystest:
              block = allblocks[k]
              code = block[0]
              token = myutils.getTokens(code) #get all single tokens from the snippet of code
              vectorlist = []
              for t in token: #convert all tokens into their word2vec vector representation
                if t in self.word_vectors.key_to_index and t != " ":
                  vector = self.w2v_model.wv[t]
                  vectorlist.append(vector.tolist()) 
              ValidateX.append(vectorlist) #append the list of vectors to the X (independent variable)
              ValidateY.append(block[1]) #append the label to the Y (dependent variable)
            
            print(f"{Fore.YELLOW}Creating {Style.BRIGHT}{mode} {Style.RESET_ALL}{Fore.YELLOW} finaltest dataset...{Style.RESET_ALL}")
            for k in keysfinaltest:
              block = allblocks[k]  
              code = block[0]
              token = myutils.getTokens(code) #get all single tokens from the snippet of code
              vectorlist = []
              for t in token: #convert all tokens into their word2vec vector representation
                if t in self.word_vectors.key_to_index and t != " ":
                  vector = self.w2v_model.wv[t]
                  vectorlist.append(vector.tolist()) 
              FinaltestX.append(vectorlist) #append the list of vectors to the X (independent variable)
              FinaltestY.append(block[1]) #append the label to the Y (dependent variable)
            
            print(f"{Fore.YELLOW}\nTrain length: {Style.BRIGHT}{str(len(TrainX))}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Test length: {Style.BRIGHT}{str(len(ValidateX))}{Style.RESET_ALL}") 
            print(f"{Fore.YELLOW}Finaltesting length: {Style.BRIGHT}{str(len(FinaltestX))}{Style.RESET_ALL}")
            
            # saving samples
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_train_X'), 'wb') as fp:
             pickle.dump(TrainX, fp)
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_train_Y'), 'wb') as fp:
             pickle.dump(TrainY, fp)
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_validate_X'), 'wb') as fp:
             pickle.dump(ValidateX, fp)
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_validate_Y'), 'wb') as fp:
             pickle.dump(ValidateY, fp)
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_finaltest_X'), 'wb') as fp:
              pickle.dump(FinaltestX, fp)
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_finaltest_Y'), 'wb') as fp:
              pickle.dump(FinaltestY, fp)
              

            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_train_X'), 'rb') as fp:
                TrainX = pickle.load(fp)
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_train_Y'), 'rb') as fp:
                TrainY = pickle.load(fp)
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_validate_X'), 'rb') as fp:
                ValidateX = pickle.load(fp)
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_validate_Y'), 'rb') as fp:
                ValidateY = pickle.load(fp)
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_finaltest_X'), 'rb') as fp:
                FinaltestX = pickle.load(fp)
            with open(os.path.join(self.save_model_path+"\\", f'{mode}_dataset_finaltest_Y'), 'rb') as fp:
                FinaltestY = pickle.load(fp)
            
            #Prepare the data for the LSTM model
            X_train =  numpy.array(TrainX, dtype=object)
            y_train =  numpy.array(TrainY)
            X_test =  numpy.array(ValidateX, dtype=object)
            y_test =  numpy.array(ValidateY)
            X_finaltest =  numpy.array(FinaltestX, dtype=object)
            y_finaltest =  numpy.array(FinaltestY)
            
            #in the original collection of data, the 0 and 1 were used the other way round, so now they are switched so that "1" means vulnerable and "0" means clean.
            
            for i in range(len(y_train)):
              if y_train[i] == 0:
                y_train[i] = 1
              else:
                y_train[i] = 0
                
            for i in range(len(y_test)):
              if y_test[i] == 0:
                y_test[i] = 1
              else:
                y_test[i] = 0
                
            for i in range(len(y_finaltest)):
              if y_finaltest[i] == 0:
                y_finaltest[i] = 1
              else:
                y_finaltest[i] = 0
            
            print(f"{Fore.YELLOW}Samples in the training set: {Style.BRIGHT}{str(len(X_train))}{Style.RESET_ALL}")      
            print(f"{Fore.YELLOW}Samples in the validation set: {Style.BRIGHT}{str(len(X_test))}{Style.RESET_ALL}") 
            print(f"{Fore.YELLOW}Samples in the final test set: {Style.BRIGHT}{str(len(X_finaltest))}{Style.RESET_ALL}")
              
            csum = 0
            for a in y_train:
              csum = csum+a
            print(f"{Fore.YELLOW}\nPercentage of vulnerable samples: {Style.BRIGHT}{str(int((csum / len(X_train)) * 10000)/100)}{Style.RESET_ALL}")
              
            testvul = 0
            for y in y_test:
              if y == 1:
                testvul = testvul+1
            print(f"{Fore.YELLOW}Absolute amount of vulnerable samples in test set: {Style.BRIGHT}{str(testvul)}{Style.RESET_ALL}")
            
            max_length = 10
              
            #hyperparameters for the LSTM model
            dropout = self.dropout
            neurons = self.neurons
            optimizer = "adam"
            epochs = self.epochs
            batch_size = self.batch_size

            print(f"{Fore.YELLOW}Dropout: {Style.BRIGHT}{str(dropout)}{Style.RESET_ALL}, {Fore.YELLOW}Neurons: {Style.BRIGHT}{str(neurons)}{Style.RESET_ALL}, {Fore.YELLOW}Optimizer: {Style.BRIGHT}{optimizer}{Style.RESET_ALL}, {Fore.YELLOW}Epochs: {Style.BRIGHT}{str(epochs)}{Style.RESET_ALL}, {Fore.YELLOW}Batch Size: {Style.BRIGHT}{str(batch_size)}{Style.RESET_ALL}, {Fore.YELLOW}Max length: {Style.BRIGHT}{str(max_length)}{Style.RESET_ALL}")
            
            #padding sequences on the same length
            X_train = sequence.pad_sequences(X_train, maxlen=max_length)
            X_test = sequence.pad_sequences(X_test, maxlen=max_length)
            X_finaltest = sequence.pad_sequences(X_finaltest, maxlen=max_length)
            
            #creating the model  
            model = Sequential()
            model.add(LSTM(neurons, dropout = dropout, recurrent_dropout = dropout))
            model.add(Dense(1, activation='sigmoid'))
            
            # Compile the model
            model.compile(loss=myutils.f1_loss, optimizer='adam', metrics=[myutils.f1])
            
            #account with class_weights for the class-imbalanced nature of the underlying data
            class_weights = class_weight.compute_class_weight(class_weight='balanced', classes=numpy.unique(y_train), y=y_train)
            class_weights = dict(enumerate(class_weights))
            
            X_train = X_train.astype(numpy.float32)
            y_train = y_train.astype(numpy.float32)
            
            # Train the model
            history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, class_weight=class_weights)
            
            print(f"{Fore.YELLOW}\nSaving LSTM model {Style.BRIGHT}{mode}.{Style.RESET_ALL}")
            fname = f"{self.save_model_path}\\lstm_model_{mode}.keras"
            model.save(fname)
            
        return True
            
      

# Example usage
if __name__ == "__main__":
    # Create an instance of the setup class
    ExceptionSetup().setup_exception_hook()
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    # Suppress the specific warning about HDF5 format
    warnings.filterwarnings("ignore", message=".*saving your model as an HDF5 file via `model.save()`.*")

    modes = ['xss', 'remote_code_execution', 'command_injection', 'path_disclosure', 'xsrf', 'sql', 'open_redirect']
    
    samples_path = r'C:\00\samples_path'
    save_model_path = r'C:\00\c#'

    dropout = 0.2
    neurons = 100
    epochs = 1
    batch_size = 10
    
    vector_size = 10
    min_count = 10
    iteration = 10
    
    makeLSTMModel = MakeLSTMModel(modes, samples_path, save_model_path, dropout, neurons, epochs, 
                                  batch_size, vector_size, iteration, min_count)
    result = makeLSTMModel.train_model()

