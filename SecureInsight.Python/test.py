# import re
# import numpy as np
# from gensim.models import Word2Vec
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Embedding, LSTM, Dense

# # Tokenization function
# def tokenize_code(code):
#     tokens = re.findall(r"\w+|[^\s\w]", code)
#     return tokens

# # Sample C# code with potential vulnerabilities
# csharp_code = """
# using System;
# using System.Web;

# namespace VulnerableApp
# {
#     class Program
#     {
#         static void Main(string[] args)
#         {
#             string userInput = HttpContext.Current.Request.QueryString["input"];
#             Response.Write("<script>alert('" + userInput + "');</script>");
            
#             string command = "ping " + userInput;
#             System.Diagnostics.Process.Start("cmd.exe", command);
#         }
#     }
# }
# """

# # Tokenize the code
# tokens = tokenize_code(csharp_code)

# # Train Word2Vec model
# model = Word2Vec([tokens], vector_size=100, window=5, min_count=1, workers=4)
# word_vectors = model.wv

# # Prepare sequences for LSTM
# def prepare_sequences(tokens, word_vectors, seq_length):
#     sequences = []
#     for i in range(len(tokens) - seq_length):
#         seq = tokens[i:i+seq_length]
#         sequences.append([word_vectors[token] for token in seq if token in word_vectors])
#     return sequences

# seq_length = 10
# sequences = prepare_sequences(tokens, word_vectors, seq_length)
# X = np.array(sequences)

# # Dummy labels for demonstration purposes
# # 0: non-vulnerable, 1: XSS, 2: Remote Code Execution
# y = np.array([0] * (len(X) - 2) + [1, 2])

# # Define the LSTM model
# model = Sequential([
#     LSTM(128, input_shape=(seq_length, 100)),
#     Dense(3, activation='softmax')
# ])
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# # Train the model
# model.fit(X, y, epochs=10)

# # Detect vulnerabilities
# def detect_vulnerabilities(tokens, model, word_vectors, seq_length):
#     sequences = prepare_sequences(tokens, word_vectors, seq_length)
#     X = np.array(sequences)
#     predictions = model.predict(X)
#     vulnerability_types = np.argmax(predictions, axis=1)
#     return predictions, vulnerability_types

# predictions, vulnerability_types = detect_vulnerabilities(tokens, model, word_vectors, seq_length)

# # Debugging prints
# print("Predictions:", predictions)
# print("Vulnerability Types:", vulnerability_types)

# # Generate report
# def generate_report(vulnerability_types, code):
#     lines = code.split('\n')
#     report = "Vulnerability Detection Report\n\n"
#     report += "Potential vulnerabilities found at the following lines:\n"
#     vulnerability_names = ['None', 'XSS', 'Remote Code Execution']
#     for i, v_type in enumerate(vulnerability_types):
#         if v_type != 0:
#             report += f"Line {i + 1}: {lines[i]}\n"
#             report += f"Reason: {vulnerability_names[v_type]} vulnerability detected.\n\n"
#     return report

# report = generate_report(vulnerability_types, csharp_code)
# print(report)





# import re
# import numpy as np
# from gensim.models import Word2Vec
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Embedding, LSTM, Dense

# # Tokenization function
# def tokenize_code(code):
#     tokens = re.findall(r"\w+|[^\s\w]", code)
#     return tokens

# # Sample C# code with potential vulnerabilities
# csharp_code = """
# using System;
# using System.Web;

# namespace VulnerableApp
# {
#     class Program
#     {
#         static void Main(string[] args)
#         {
#             string userInput = HttpContext.Current.Request.QueryString["input"];
#             Response.Write("<script>alert('" + userInput + "');</script>");
            
#             string command = "ping " + userInput;
#             System.Diagnostics.Process.Start("cmd.exe", command);
#         }
#     }
# }
# """




# input_file = r'C:\00\test\corpus_part4.txt'  
# with open(input_file, 'r', encoding='utf-8') as file:
#     # Read the entire content of the file
#     content = file.read()

# # Tokenize the code
# tokens = tokenize_code(content)

# # Train Word2Vec model
# model = Word2Vec([tokens], vector_size=100, window=5, min_count=1, workers=4)
# word_vectors = model.wv

# # Prepare sequences for LSTM
# def prepare_sequences(tokens, word_vectors, seq_length):
#     sequences = []
#     for i in range(len(tokens) - seq_length):
#         seq = tokens[i:i+seq_length]
#         sequences.append([word_vectors[token] for token in seq if token in word_vectors])
#     return sequences

# seq_length = 10
# sequences = prepare_sequences(tokens, word_vectors, seq_length)
# X = np.array(sequences)

# # Dummy labels for demonstration purposes
# # 0: non-vulnerable, 1: XSS, 2: Remote Code Execution
# y = np.array([0] * (len(X) - 2) + [1, 2])

# # Define the LSTM model
# model = Sequential([
#     LSTM(128, input_shape=(seq_length, 100)),
#     Dense(3, activation='softmax')
# ])
# model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# # Train the model
# model.fit(X, y, epochs=10)

# # Detect vulnerabilities
# def detect_vulnerabilities(tokens, model, word_vectors, seq_length):
#     sequences = prepare_sequences(tokens, word_vectors, seq_length)
#     X = np.array(sequences)
#     predictions = model.predict(X)
#     vulnerability_types = np.argmax(predictions, axis=1)
#     return vulnerability_types

# vulnerability_types = detect_vulnerabilities(tokens, model, word_vectors, seq_length)

# # Generate report
# def generate_report(vulnerability_types, code):
#     lines = code.split('\n')
#     report = "Vulnerability Detection Report\n\n"
#     report += "Potential vulnerabilities found at the following lines:\n"
#     vulnerability_names = ['None', 'XSS', 'Remote Code Execution']
#     for i, v_type in enumerate(vulnerability_types):
#         if v_type != 0:
#             report += f"Line {i + 1}: {lines[i]}\n"
#             report += f"Reason: {vulnerability_names[v_type]} vulnerability detected.\n\n"
#     return report

# report = generate_report(vulnerability_types, csharp_code)
# print(report)





