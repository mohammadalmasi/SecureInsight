import os
import sys
import pickle
import numpy as np
from colorama import Fore, Style
from tensorflow.keras.models import load_model
from highlighted_excepthook import ExceptionSetup
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from database import get_session, CNNmetrics

class CNNMetricsAnalysis: 
   def __init__(self, modes, save_model_path, db_session):
       self.modes = modes
       self.save_model_path = save_model_path
       self.db = db_session

   def reshape_dataset(self, data_list, target_shape=(64, 64, 3)):
       if not isinstance(data_list, (list, tuple, np.ndarray)):
            raise ValueError("Expected data_list to be a list, tuple, or numpy array.")
       
       reshaped_list = []
       
       for sublist in data_list:
           # Flatten the data
           flat_data = [item for sublist1 in sublist for item in sublist1]
           
           # Calculate the required number of elements
           required_elements = np.prod(target_shape)
           
           # Pad or truncate the data
           if len(flat_data) < required_elements:
               flat_data.extend([0] * (required_elements - len(flat_data)))
           else:
               flat_data = flat_data[:required_elements]
           
           # Reshape the data
           reshaped_data = np.array(flat_data).reshape(target_shape)
           reshaped_list.append(reshaped_data)
       
       return np.array(reshaped_list)
       
   def metrics_analysis(self):
        results = []
        
        for mode in self.modes:
            # Get the vulnerability from the command line argument
            if len(sys.argv) > 1:
                mode = sys.argv[1]
        
            # Load the model from the file
            model = load_model(f'{self.save_model_path}/cnn_model_{mode}.keras')  
              
            with open(os.path.join(self.save_model_path, f'{mode}_dataset_finaltest_X'), 'rb') as fp:
                FinaltestX = pickle.load(fp)
            with open(os.path.join(self.save_model_path, f'{mode}_dataset_finaltest_Y'), 'rb') as fp:
                FinaltestY = pickle.load(fp)
        
            # Prepare the data for the LSTM model
            X_finaltest = np.array(FinaltestX, dtype=object)
            y_finaltest =  np.array(FinaltestY)
            
            # In the original collection of data, the 0 and 1 were used the other way round, so now they are switched so 
            # that "1" means vulnerable and "0" means clean.
            for i in range(len(y_finaltest)):
                y_finaltest[i] = 1 if y_finaltest[i] == 0 else 0
            
            print(f"{Style.BRIGHT}{Fore.YELLOW}Samples in the final test set: {Style.RESET_ALL}{Style.BRIGHT}{len(X_finaltest)}")
            
            csum = sum(y_finaltest)
            percentage_vulnerable = int((csum / len(X_finaltest)) * 10000) / 100
            print(f"{Style.BRIGHT}{Fore.YELLOW}Percentage of vulnerable samples: {Style.RESET_ALL}{Style.BRIGHT}{percentage_vulnerable}%")
            
            print(f"{Style.BRIGHT}{Fore.YELLOW}Absolute amount of vulnerable samples in test set: {Style.RESET_ALL}{Style.BRIGHT}{str(csum)}%\n")

            X_finaltest = self.reshape_dataset(X_finaltest)
            
            yhat_prob = model.predict(X_finaltest)
            yhat_classes = (yhat_prob > 0.5).astype(int)  # Convert probabilities to binary class labels (assuming a threshold of 0.5)
            y_finaltest = y_finaltest.astype(int)  # Ensure y_finaltest is also binary  
        
            accuracy = accuracy_score(y_finaltest, yhat_classes)
            precision = precision_score(y_finaltest, yhat_classes)
            recall = recall_score(y_finaltest, yhat_classes)
            F1Score = f1_score(y_finaltest, yhat_classes)
              
            metrics = {
                'mode': mode,
                'accuracy': accuracy,
                'precision': precision,
                'recall': recall,
                'f1_score': F1Score
            }

            results.append(metrics)
            
            print(f"{Style.BRIGHT}{Fore.YELLOW}Classification metrics for: {Style.RESET_ALL}{Style.BRIGHT}{Fore.GREEN}{mode}")
            print(f"{Fore.GREEN}Accuracy: {Style.RESET_ALL}{Style.BRIGHT}{accuracy}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Precision: {Style.RESET_ALL}{Style.BRIGHT}{precision}{Style.RESET_ALL}")
            print(f"{Fore.RED}Recall: {Style.RESET_ALL}{Style.BRIGHT}{recall}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}F1 score: {Style.RESET_ALL}{Style.BRIGHT}{F1Score}{Style.RESET_ALL}")
            print(f"{Style.BRIGHT}------------------------------------------------------")
            
            cnn_metrics = CNNmetrics(
                mode=mode,
                accuracy=accuracy,
                precision=precision,
                recall=recall,
                f1_score=F1Score
            )
            self.db.add(cnn_metrics)
            self.db.commit()

        self.db.close()
        return results
    

# Example usage
if __name__ == "__main__":
    # Create an instance of the setup class
    ExceptionSetup().setup_exception_hook()
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    modes = ['xss', 'remote_code_execution', 'command_injection', 'path_disclosure', 'xsrf', 'sql', 'open_redirect']
    save_model_path = r'C:\00\model'
    
    DATABASE_URL = f'sqlite:///{save_model_path}\SecureInsight.db'
    db_session = get_session(DATABASE_URL)
    
    cnnMetricsAnalysis = CNNMetricsAnalysis(modes, save_model_path, db_session)
    result = cnnMetricsAnalysis.metrics_analysis()

    print(result)  # This will print the list of metrics dictionaries
