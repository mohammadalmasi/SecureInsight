import chardet
import shutil
from pygments import lex
from pygments.lexers import get_lexer_by_name
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from threading import Lock
from tqdm import tqdm

class Tokenizer:
    def __init__(self, lexer, input_paths, chunk_size, progress_callback=None, status_callback=None):
        self.lexer = lexer
        self.input_paths = input_paths
        self.output_path = ""
        self.chunk_index_path = ""
        self.chunk_size = chunk_size * 1024 * 1024
        self.lock = Lock()
        self.items = {}  # Dictionary to store tokenized chunks with their indices
        self.next_index = 0  # Track the next index for consecutive writing
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.tqdm_lock = Lock()  # Lock for tqdm updates
        self.total_chunks = 0  # Total number of chunks to be processed
        
    def generate_output_path(self, suffix):
        last_file_path = self.input_paths[-1]
        directory, filename = os.path.split(last_file_path)
        name, ext = os.path.splitext(filename)
        new_filename = f"{name}{suffix}{ext}"
        output_path = os.path.join(directory, new_filename)
        return output_path

    def merge_files(self, output_path):
        with open(output_path, 'wb') as outfile:
            for file_path in self.input_paths:
                with open(file_path, 'rb') as infile:
                    shutil.copyfileobj(infile, outfile)

    def detect_encoding(self, input_path):
        with open(input_path, 'rb') as f:
            sample = f.read(10000)
        result = chardet.detect(sample)
        return result['encoding']

    def process_chunk(self, input_path, encoding, start, end, chunk_index):
        with open(input_path, 'r', encoding=encoding, errors='ignore') as f:
            f.seek(start)
            code_chunk = f.read(end - start)

        lexer = get_lexer_by_name(self.lexer)
        tokens = lex(code_chunk, lexer)
        token_list = [token_value for token_type, token_value in tokens]

        with self.lock:
            self.items[chunk_index] = token_list
            while self.next_index in self.items:
                self.write_to_output(self.next_index, self.items.pop(self.next_index))
                self.next_index += 1

    def write_to_output(self, chunk_index, token_list):
        if self.progress_callback:
            self.progress_callback((chunk_index + 1) / self.total_chunks * 100)
                
        with open(self.output_path, 'a', encoding='utf-8') as out_file:
            out_file.write(' '.join(token_list) + '\n')
        
        with open(self.chunk_index_path, 'a', encoding='utf-8') as out_file:
            out_file.write(str(chunk_index) + '\n')

    def tokenize_file(self, input_path):
        encoding = self.detect_encoding(input_path)
        file_size = os.path.getsize(input_path)
        self.total_chunks = (file_size + self.chunk_size - 1) // self.chunk_size

        if not self.progress_callback:
            self.pbar = tqdm(total=self.total_chunks, desc=f"Processing {os.path.basename(input_path)}", unit="chunk")

        with ThreadPoolExecutor() as executor:
            futures = []
            for i in range(self.total_chunks):
                start = i * self.chunk_size
                end = min(start + self.chunk_size, file_size)
                future = executor.submit(self.process_chunk, input_path, encoding, start, end, i)
                futures.append(future)

            for future in as_completed(futures):
                future.result()

        if not self.progress_callback:
            self.pbar.close()

    def tokenize(self):
        self.output_path = self.generate_output_path(f"_{self.lexer}_final_tokenize")
        self.chunk_index_path = self.generate_output_path(f"_{self.lexer}_chunk_index")
        merge_output_path = self.generate_output_path("_merge")
        
        if self.status_callback:
            self.status_callback("Starting to merge files...")
        self.merge_files(merge_output_path)
        
        try:
            if self.status_callback:
                self.status_callback("Starting to tokenize...")
            self.tokenize_file(merge_output_path)
            if self.status_callback:
                self.status_callback("Finish.")
            return True
        except Exception as e:
            if self.status_callback:
                self.status_callback(f"An error occurred while processing the file {merge_output_path}: {e}")
            return False

if __name__ == "__main__":
    language = "csharp"
    chunk_size = 1  # 1MB
    
    input_paths = [
        r"C:\00\almasi\A.txt",
        r"C:\00\almasi\B.txt",
    ]
    
    def progress_callback(progress):
        print(f"Progress: {progress:.2f}%")

    def status_callback(status):
        print(f"status: {str(status)}")

    tokenizer = Tokenizer(language, input_paths, chunk_size, progress_callback, status_callback)
    result = tokenizer.tokenize()
