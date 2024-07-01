# import os
# import pickle
# import warnings
# import numpy as np
# import tensorflow as tf
# import logging
# from colorama import Fore, Style
# from highlighted_excepthook import ExceptionSetup
# from sklearn.exceptions import ConvergenceWarning
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

# # Define a callback to log training progress
# class LoggingCallback(tf.keras.callbacks.Callback):
#     def on_epoch_end(self, epoch, logs=None):
#         logging.info(f'Epoch {epoch + 1}: {logs}')
        
#     def on_batch_end(self, batch, logs=None):
#         logging.info(f'Batch {batch + 1}: {logs}')

# class MakeCNNModel:
#     def __init__(self, modes, save_model_path, epochs, batch_size, callbacks=None):
#         self.modes = modes
#         self.save_model_path = save_model_path
#         self.epochs = epochs
#         self.batch_size = batch_size
#         self.callbacks = callbacks if callbacks else []

#     def load_dataset(self, mode, dataset_type):
#         file_path = os.path.join(self.save_model_path, f'{mode}_dataset_{dataset_type}')
#         with open(file_path, 'rb') as fp:
#             return pickle.load(fp)

#     def reshape_dataset(self, data_list, target_shape=(64, 64, 3)):
#         reshaped_list = []

#         for sublist in data_list:
#             flat_data = [item for sublist1 in sublist for item in sublist1]
#             required_elements = np.prod(target_shape)
#             if len(flat_data) < required_elements:
#                 flat_data.extend([0] * (required_elements - len(flat_data)))
#             else:
#                 flat_data = flat_data[:required_elements]
#             reshaped_data = np.array(flat_data).reshape(target_shape)
#             reshaped_list.append(reshaped_data)

#         return np.array(reshaped_list)

#     def train_model(self):
#         for mode in self.modes:
#             print(f"+++++++++++++++++++++++++++++ {Fore.GREEN}{Style.BRIGHT}{mode}{Style.RESET_ALL} +++++++++++++++++++++++++++++")

#             TrainX = self.load_dataset(f'{mode}', 'train_X')
#             TrainY = self.load_dataset(f'{mode}', 'train_Y')
#             ValidateX = self.load_dataset(f'{mode}', 'validate_X')
#             ValidateY = self.load_dataset(f'{mode}', 'validate_Y')

#             X_train = self.reshape_dataset(TrainX)
#             X_validate = self.reshape_dataset(ValidateX)
#             y_train = np.array(TrainY)
#             y_test = np.array(ValidateY)

#             model = Sequential()
#             model.add(Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
#             model.add(MaxPooling2D(pool_size=(2, 2)))
#             model.add(Conv2D(64, (3, 3), activation='relu'))
#             model.add(MaxPooling2D(pool_size=(2, 2)))
#             model.add(Conv2D(128, (3, 3), activation='relu'))
#             model.add(MaxPooling2D(pool_size=(2, 2)))
#             model.add(Flatten())
#             model.add(Dense(128, activation='relu'))
#             model.add(Dropout(0.5))
#             model.add(Dense(1, activation='sigmoid'))

#             model.compile(optimizer='adam', 
#                           loss='binary_crossentropy',
#                           metrics=['accuracy'])

#             history = model.fit(
#                 X_train, y_train,
#                 epochs=self.epochs,
#                 batch_size=self.batch_size,
#                 validation_data=(X_validate, y_test),
#                 callbacks=self.callbacks
#             )

#             print(f"{Fore.YELLOW}\nSaving CNN model {Style.BRIGHT}{mode}.{Style.RESET_ALL}")
#             fname = os.path.join(self.save_model_path, f'cnn_model_{mode}.keras')
#             model.save(fname)

#         return True



# # Example usage
# if __name__ == "__main__":
#     # Create an instance of the setup class
#     ExceptionSetup().setup_exception_hook()
#     os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#     # Suppress ConvergenceWarning
#     warnings.filterwarnings("ignore", category=ConvergenceWarning)
    
#     # Set up logging to file
#     logging.basicConfig(filename='training.log', level=logging.INFO, format='%(message)s')

#     modes = ['xss', 'remote_code_execution', 'command_injection', 'path_disclosure', 'xsrf', 'sql', 'open_redirect']
#     save_model_path = r'C:\00\c#'
#     epochs = 1
#     batch_size = 1

#     # Initialize the model with an optional LoggingCallback
#     makeCNNModel = MakeCNNModel(modes, save_model_path, epochs, batch_size, callback=LoggingCallback())
#     result = makeCNNModel.train_model()



import os
import pickle
import warnings
import numpy as np
import tensorflow as tf
import logging
from colorama import Fore, Style
from highlighted_excepthook import ExceptionSetup
from sklearn.exceptions import ConvergenceWarning
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout


class MakeCNNModel:
    def __init__(self, modes, save_model_path, epochs, batch_size):
        self.modes = modes
        self.save_model_path = save_model_path
        self.epochs = epochs
        self.batch_size = batch_size

    def load_dataset(self, mode, dataset_type):
        file_path = os.path.join(self.save_model_path, f'{mode}_dataset_{dataset_type}')
        with open(file_path, 'rb') as fp:
            return pickle.load(fp)

    def reshape_dataset(self, data_list, target_shape=(64, 64, 3)):
        reshaped_list = []

        for sublist in data_list:
            flat_data = [item for sublist1 in sublist for item in sublist1]
            required_elements = np.prod(target_shape)
            if len(flat_data) < required_elements:
                flat_data.extend([0] * (required_elements - len(flat_data)))
            else:
                flat_data = flat_data[:required_elements]
            reshaped_data = np.array(flat_data).reshape(target_shape)
            reshaped_list.append(reshaped_data)

        return np.array(reshaped_list)

    def train_model(self):
        for mode in self.modes:
            print(f"+++++++++++++++++++++++++++++ {Fore.GREEN}{Style.BRIGHT}{mode}{Style.RESET_ALL} +++++++++++++++++++++++++++++")

            TrainX = self.load_dataset(f'{mode}', 'train_X')
            TrainY = self.load_dataset(f'{mode}', 'train_Y')
            ValidateX = self.load_dataset(f'{mode}', 'validate_X')
            ValidateY = self.load_dataset(f'{mode}', 'validate_Y')

            X_train = self.reshape_dataset(TrainX)
            X_validate = self.reshape_dataset(ValidateX)
            y_train = np.array(TrainY)
            y_test = np.array(ValidateY)

            model = Sequential()
            model.add(Conv2D(32, (3, 3), input_shape=(64, 64, 3), activation='relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Conv2D(64, (3, 3), activation='relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Conv2D(128, (3, 3), activation='relu'))
            model.add(MaxPooling2D(pool_size=(2, 2)))
            model.add(Flatten())
            model.add(Dense(128, activation='relu'))
            model.add(Dropout(0.5))
            model.add(Dense(1, activation='sigmoid'))

            model.compile(optimizer='adam', 
                          loss='binary_crossentropy',
                          metrics=['accuracy'])

            history = model.fit(
                X_train, y_train,
                epochs=self.epochs,
                batch_size=self.batch_size,
                validation_data=(X_validate, y_test)
            )

            print(f"{Fore.YELLOW}\nSaving CNN model {Style.BRIGHT}{mode}.{Style.RESET_ALL}")
            fname = os.path.join(self.save_model_path, f'cnn_model_{mode}.keras')
            model.save(fname)

        return True



# Example usage
if __name__ == "__main__":
    # Create an instance of the setup class
    ExceptionSetup().setup_exception_hook()
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    # Suppress ConvergenceWarning
    warnings.filterwarnings("ignore", category=ConvergenceWarning)
    
    # Set up logging to file
    logging.basicConfig(filename='training.log', level=logging.INFO, format='%(message)s')

    # modes = ['xss', 'remote_code_execution', 'command_injection', 'path_disclosure', 'xsrf', 'sql', 'open_redirect']
    modes = [ 'open_redirect','sql']
    save_model_path = r'C:\00\c#'
    epochs = 1
    batch_size = 1

    # Initialize the model with an optional LoggingCallback
    makeCNNModel = MakeCNNModel(modes, save_model_path, epochs, batch_size)
    result = makeCNNModel.train_model()
