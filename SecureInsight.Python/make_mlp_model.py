import os
import numpy
import pickle
import warnings
from colorama import Fore, Style
from keras.preprocessing import sequence
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from highlighted_excepthook import ExceptionSetup
from sklearn.exceptions import ConvergenceWarning
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

class MakeMLPModel:
    def __init__(self, modes, save_model_path, epochs, batch_size):
        self.modes = modes
        self.save_model_path = save_model_path
        self.epochs = epochs
        self.batch_size = batch_size
        
    def train_model(self):
        for mode in self.modes:
            print(f"+++++++++++++++++++++++++++++ {Fore.GREEN}{Style.BRIGHT}{mode}{Style.RESET_ALL} +++++++++++++++++++++++++++++")
            
            # Step 2: Load dataset
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
            
            #Prepare the data for the MLP model
            X_train =  numpy.array(TrainX, dtype=object)
            y_train =  numpy.array(TrainY)
            X_test =  numpy.array(ValidateX, dtype=object)
            y_test =  numpy.array(ValidateY)
            X_finaltest =  numpy.array(FinaltestX, dtype=object)
            y_finaltest =  numpy.array(FinaltestY)
            
            max_length = 10
            #padding sequences on the same length
            X_train = sequence.pad_sequences(X_train, maxlen=max_length)
            X_test = sequence.pad_sequences(X_test, maxlen=max_length)
            X_finaltest = sequence.pad_sequences(X_finaltest, maxlen=max_length)
            
            print(f"{Fore.YELLOW}Samples in the training set: {Style.BRIGHT}{str(len(X_train))}{Style.RESET_ALL}")      
            print(f"{Fore.YELLOW}Samples in the validation set: {Style.BRIGHT}{str(len(X_test))}{Style.RESET_ALL}") 
            print(f"{Fore.YELLOW}Samples in the final test set: {Style.BRIGHT}{str(len(X_finaltest))}{Style.RESET_ALL}")
 
            # Step 3: Standardize the features (important for neural networks)
            scaler = StandardScaler()
            # Apply StandardScaler to the reshaped data (Flatten the features)
            X_train = scaler.fit_transform(X_train.reshape(X_train.shape[0], -1))
            X_test = scaler.fit_transform(X_test.reshape(X_test.shape[0], -1))
            X_finaltest = scaler.fit_transform(X_finaltest.reshape(X_finaltest.shape[0], -1))

            # Step 4: Initialize the MLPClassifier
            mlp = MLPClassifier(hidden_layer_sizes=(100,), max_iter=self.epochs, alpha=0.0001, solver='adam', random_state=42, tol=0.0001)
            

            # Step 5: Apply SMOTE to balance the dataset
            smote = SMOTE(random_state=42)
            X_resampled, y_resampled = smote.fit_resample(X_train, y_train)

            # Step 6: Fit the model on the resampled data
            mlp.fit(X_resampled, y_resampled)
                
            # Save the model using pickle
            print(f"{Fore.YELLOW}\nSaving MLP model {Style.BRIGHT}{mode}.{Style.RESET_ALL}")
            with open(f'{self.save_model_path}/mlp_model_' + mode, 'wb') as fp:
             pickle.dump(mlp, fp)
             
        return True
             

# Example usage
if __name__ == "__main__":
    # Create an instance of the setup class
    ExceptionSetup().setup_exception_hook()
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    # Suppress ConvergenceWarning
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    
    modes = ['xss', 'remote_code_execution', 'command_injection', 'path_disclosure', 'xsrf', 'sql', 'open_redirect']
    
    save_model_path = r'C:\00\c#'

    epochs = 1
    batch_size = 32
    
    makeMLPModel = MakeMLPModel(modes, save_model_path, epochs, batch_size)
    result = makeMLPModel.train_model()
 