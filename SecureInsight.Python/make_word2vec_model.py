import logging
from gensim.models import Word2Vec

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Word2VecModel:
    def __init__(self, tokenized_data_path, model_path, vector_size, iterations, min_count, workers=None):
        """
        Initializes the Word2VecModel with the given parameters.
        
        Parameters:
        - tokenized_data_path: Path to the tokenized data file.
        - model_path: Path to save the trained models.
        - vector_size: List of vector sizes to try.
        - iterations: List of iteration counts (epochs) to try.
        - min_count: List of minimum count thresholds to try.
        - workers: Number of worker threads to use. Defaults to 4 if not provided.
        """
        self.tokenized_data_path = tokenized_data_path
        self.model_path = model_path
        self.vector_size = vector_size
        self.iterations = iterations
        self.min_count = min_count
        self.workers = workers if workers is not None else 4

    def load_tokenized_data(self):
        """
        Loads the tokenized data from the file specified in tokenized_data_path.
        
        Returns:
        - A list of token lists, where each inner list represents a sentence.
        """
        try:
            with open(self.tokenized_data_path, 'r', encoding='utf-8') as file:
                token_lists = [line.strip().split() for line in file]
            return token_lists
        except FileNotFoundError:
            logging.error(f"File not found: {self.tokenized_data_path}")
            return []
        except Exception as e:
            logging.error(f"An error occurred while loading tokenized data: {e}")
            return []

    def train_model(self):
        """
        Trains Word2Vec models using the loaded tokenized data and saves them with different parameters.
        """
        all_tokens = self.load_tokenized_data()
        if not all_tokens:
            logging.error("No tokenized data available for training.")
            return

        # Try different parameter combinations
        for vector_size in self.vector_size:
            for iteration in self.iterations:
                for min_count in self.min_count:
                    try:
                        # Train the Word2Vec model with the current parameters
                        model = Word2Vec(sentences=all_tokens, vector_size=vector_size, epochs=iteration, min_count=min_count, workers=self.workers)
                        
                        # Get the vocabulary size
                        vocabulary = len(model.wv.key_to_index)
                        logging.info(f"Trained model with vector_size={vector_size}, iteration={iteration}, min_count={min_count}, vocabulary size={vocabulary}")
                        
                        # Construct the file name to save the model
                        fname = f"{self.model_path}\\word2vec_{vector_size}_{iteration}_{min_count}.model"
                        
                        # Save the model to disk
                        model.save(fname)
                        logging.info(f"Model saved to {fname}")
                    except Exception as e:
                        logging.error(f"An error occurred during model training: {e}")
        
        return True

if __name__ == "__main__":
    # Paths to the tokenized data and the directory to save the models
    tokenized_data_path = r"C:\00\last\tokenization_results_part2.txt"
    model_path = r"C:\00\last"
    
    # Define the parameters for the Word2Vec model
    vector_size = [10]
    iterations = [10] 
    min_count = [10]  
    workers = 4  
    
    # Create an instance of Word2VecModel and train the models
    word2VecModel = Word2VecModel(tokenized_data_path, model_path, vector_size, iterations, min_count, workers)
    result = word2VecModel.train_model()
    