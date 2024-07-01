import os
import sys
import pickle
import numpy as np
from colorama import Fore, Style
from keras.preprocessing import sequence
from highlighted_excepthook import ExceptionSetup
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from database import get_session, MLPmetrics

class MLPMetricsAnalysis: 
   def __init__(self, modes, save_model_path, db_session):
       self.modes = modes
       self.save_model_path = save_model_path
       self.db = db_session

   def metrics_analysis(self):
      results = []

      for mode in self.modes:
        #get the vulnerability from the command line argument
        if (len(sys.argv) > 1):
          mode = sys.argv[1]
        
        # Load the model from the file
        with open(f'{self.save_model_path}\\mlp_model_{mode}', 'rb') as fp:
            model = pickle.load(fp)
        
        with open(os.path.join(self.save_model_path, f'{mode}_dataset_finaltest_X'), 'rb') as fp:
          FinaltestX = pickle.load(fp)
        with open(os.path.join(self.save_model_path, f'{mode}_dataset_finaltest_Y'), 'rb') as fp:
          FinaltestY = pickle.load(fp)
        
        #Prepare the data for the LSTM model
        X_finaltest =  np.array(FinaltestX, dtype=object)
        y_finaltest =  np.array(FinaltestY)
        
        #in the original collection of data, the 0 and 1 were used the other way round, so now they are switched so 
        #that "1" means vulnerable and "0" means clean.
        for i in range(len(y_finaltest)):
          if y_finaltest[i] == 0:
            y_finaltest[i] = 1
          else:
            y_finaltest[i] = 0
        
        print(f"{Style.BRIGHT}{Fore.YELLOW}Samples in the final test set: {Style.RESET_ALL}{Style.BRIGHT}{len(X_finaltest)}")
        
        csum = 0
        for y in y_finaltest:  
          csum = csum + y
        
        percentage_vulnerable = int((csum / len(X_finaltest)) * 10000) / 100
        print(f"{Style.BRIGHT}{Fore.YELLOW}Percentage of vulnerable samples: {Style.RESET_ALL}{Style.BRIGHT}{percentage_vulnerable}%")
        
        print(f"{Style.BRIGHT}{Fore.YELLOW}Absolute amount of vulnerable samples in test set: {Style.RESET_ALL}{Style.BRIGHT}{str(csum)}%\n")
        
        #padding sequences on the same length
        max_length = 10   
        X_finaltest = sequence.pad_sequences(X_finaltest, maxlen=max_length)
        X_finaltest = X_finaltest.reshape(X_finaltest.shape[0], -1)
        
        yhat_classes = model.predict(X_finaltest)
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

        mlp_metrics = MLPmetrics(
            mode=mode,
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=F1Score
        )
        self.db.add(mlp_metrics)
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
    
    mlpMetricsAnalysis = MLPMetricsAnalysis(modes, save_model_path, db_session)
    result = mlpMetricsAnalysis.metrics_analysis()

    print(result)  # This will print the list of metrics dictionaries
