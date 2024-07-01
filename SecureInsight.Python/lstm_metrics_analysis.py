import os
import sys
import pickle
import myutils
import numpy as np
from colorama import Fore, Style
from keras.models import load_model
from keras.preprocessing import sequence
from highlighted_excepthook import ExceptionSetup
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from database import get_session, LSTMmetrics

class LSTMMetricsAnalysis: 
    def __init__(self, modes, save_model_path, db_session):
        self.modes = modes
        self.save_model_path = save_model_path
        self.db = db_session

    def metrics_analysis(self):
        results = []

        for mode in self.modes:
            if len(sys.argv) > 1:
                mode = sys.argv[1]

            model = load_model(f'{self.save_model_path}/lstm_model_{mode}.keras', custom_objects={'f1_loss': myutils.f1_loss, 'f1': myutils.f1})

            with open(os.path.join(self.save_model_path, f'{mode}_dataset_finaltest_X'), 'rb') as fp:
                FinaltestX = pickle.load(fp)
            with open(os.path.join(self.save_model_path, f'{mode}_dataset_finaltest_Y'), 'rb') as fp:
                FinaltestY = pickle.load(fp)

            X_finaltest = np.array(FinaltestX, dtype=object)
            y_finaltest = np.array(FinaltestY)

            for i in range(len(y_finaltest)):
                y_finaltest[i] = 1 if y_finaltest[i] == 0 else 0

            print(f"{Style.BRIGHT}{Fore.YELLOW}Samples in the final test set: {Style.RESET_ALL}{Style.BRIGHT}{len(X_finaltest)}")

            csum = sum(y_finaltest)
            percentage_vulnerable = int((csum / len(X_finaltest)) * 10000) / 100
            print(f"{Style.BRIGHT}{Fore.YELLOW}Percentage of vulnerable samples: {Style.RESET_ALL}{Style.BRIGHT}{percentage_vulnerable}%")
            print(f"{Style.BRIGHT}{Fore.YELLOW}Absolute amount of vulnerable samples in test set: {Style.RESET_ALL}{Style.BRIGHT}{str(csum)}%\n")

            max_length = 10
            X_finaltest = sequence.pad_sequences(X_finaltest, maxlen=max_length)

            yhat_classes = np.around(model.predict(X_finaltest, verbose=0))
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

            lstm_metrics = LSTMmetrics(
                mode=mode,
                accuracy=accuracy,
                precision=precision,
                recall=recall,
                f1_score=F1Score
            )
            self.db.add(lstm_metrics)
            self.db.commit()

        self.db.close()
        return results
    

# Example usage
if __name__ == "__main__":
    ExceptionSetup().setup_exception_hook()
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    #modes = ['xss', 'remote_code_execution', 'command_injection', 'path_disclosure', 'xsrf', 'sql', 'open_redirect']
    modes = ['xss','remote_code_execution']
    save_model_path = r'C:\00\model'
    
    DATABASE_URL = f'sqlite:///{save_model_path}\SecureInsight.db'
    db_session = get_session(DATABASE_URL)

    lstmMetricsAnalysis = LSTMMetricsAnalysis(modes, save_model_path, db_session)
    result = lstmMetricsAnalysis.metrics_analysis()

    print(result)  # This will print the list of metrics dictionaries
