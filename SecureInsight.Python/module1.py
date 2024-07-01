# from PIL import Image, ImageDraw, ImageFont
# import os
# import numpy
# import myutils
# from keras.preprocessing import sequence
# from gensim.models import Word2Vec
# from keras.models import load_model

# class SourceCodeImageGenerator:
#     def __init__(self, sourcecode, save_blocks_visual_path, save_model_path, 
#                  vector_size, iteration, min_count, mode='sql', name='almasi', img_width=1000, line_height=20):
#         self.sourcecode = sourcecode
#         self.save_blocks_visual_path = save_blocks_visual_path
#         self.save_model_path = save_model_path
#         self.vector_size = vector_size
#         self.iteration = iteration
#         self.min_count = min_count
#         self.mode = mode
#         self.name = name
#         self.img_width = img_width
#         self.line_height = line_height

#     def load_word2vec_model(self):
#             w2vmodel = f"{self.save_model_path}\\word2vec_{self.vector_size}_{self.iteration}_{self.min_count}.model"
            
#             w2v_model = Word2Vec.load(w2vmodel)
#             word_vectors = w2v_model.wv
#             return word_vectors

#     def Load_lstm_model(self):
#             path = f'{self.save_model_path}\\lstm_model_'+self.mode+'.keras'
#             lstm_model = load_model(path,custom_objects={'f1_loss': myutils.f1_loss, 'f1':myutils.f1}) 
#             return lstm_model
    
#     def predict(vectorlist,model): 
#         if (len(vectorlist) > 0):
#           one = []
#           one.append(vectorlist)
#           one = numpy.array(one)
#           max_length = 10
#           one = sequence.pad_sequences(one, maxlen=max_length)
#           yhat_probs = model.predict(one, verbose=0)
#           prediction = int(yhat_probs[0][0] * 100000)
#           prediction = 0.00001 * prediction 
#           return prediction
          
#         else:
#           return -1
            
#     def generate_image(self):
#         word_vectors = self.load_word2vec_model();
#         lstm_model = self.Load_lstm_model()

#         # Split the source code into lines
#         lines = self.sourcecode.splitlines()

#         # Calculate dimensions based on number of lines and font size
#         img_height = (len(lines) + 1) * self.line_height

#         # Create a blank image
#         img = Image.new('RGB', (self.img_width, img_height), color='white')
#         draw = ImageDraw.Draw(img)

#         # Use a monospace font for consistent line spacing
#         font = ImageFont.truetype("arial.ttf", 16)

#         # Draw each line of source code with appropriate color
#         y = 0
#         for line in lines:
#             # Check if the line is a comment
#             if '//' in line:
#                 draw.text((10, y), line, font=font, fill='grey')
#             else:
#                 tokens = line.split()
#                 if (len(tokens) > 1):
#                     vectorlist = []
#                     for token in tokens:
#                         if token in word_vectors.key_to_index and token != " ":
#                              vector = word_vectors.wv[token]
#                              vectorlist.append(vector.tolist())  
                             
#                     if len(vectorlist) > 0:
#                         p = self.predict(vectorlist,lstm_model)
#                         if p > 0.8:
#                              draw.text((10, y), line, font=font, fill='red')
#                         elif p > 0.5:
#                             draw.text((10, y), line, font=font, fill='yeloow')
#                         else:
#                             draw.text((10, y), line, font=font, fill='blue')
                             

#                 draw.text((10, y), line, font=font, fill='blue')

#             y += self.line_height

#         # Save the image
#         os.makedirs(self.save_blocks_visual_path, exist_ok=True)
#         filename = f'demo_{self.mode}_{self.name}.png'
#         img.save(os.path.join(self.save_blocks_visual_path, filename))
#         print(f"Image saved as {filename}.")
        

# # Example usage:
# if __name__ == "__main__":
#     sourcecode = '''
#     using System;
#     using System.Data.SqlClient;

#     static class Program
#     {
#         static void Main()
#         {
#             // Your C# code here
#             Console.WriteLine("Hello from C#");
#         }
#     }
#     '''

#     save_blocks_visual_path = r'C:\00\c#\img'
#     save_model_path = r'C:\00\c#'
    
#     vector_size = 1 
#     iteration = 1 
#     min_count = 1
    
#     modes = ['xss', 'remote_code_execution', 'command_injection', 'path_disclosure', 'xsrf', 'sql', 'open_redirect']
    
#     generator = SourceCodeImageGenerator(sourcecode, save_blocks_visual_path, save_model_path, vector_size, iteration, min_count)
#     generator.generate_image()







from PIL import Image, ImageDraw, ImageFont
import os
import numpy as np
import myutils
from keras.preprocessing import sequence
from gensim.models import Word2Vec
from keras.models import load_model

class Demonstrate:
    def __init__(self, sourcecode, save_blocks_visual_path, save_model_path, 
                 vector_size, iteration, min_count, modes, img_width=1000, line_height=20):
        self.sourcecode = sourcecode
        self.save_blocks_visual_path = save_blocks_visual_path
        self.save_model_path = save_model_path
        self.vector_size = vector_size
        self.iteration = iteration
        self.min_count = min_count
        self.modes = modes
        self.img_width = img_width
        self.line_height = line_height

    def load_word2vec_model(self):
        w2vmodel = f"{self.save_model_path}\\word2vec_{self.vector_size}_{self.iteration}_{self.min_count}.model"
        w2v_model = Word2Vec.load(w2vmodel)
        word_vectors = w2v_model.wv
        return word_vectors

    def load_lstm_model(self, mode):
        path = f'{self.save_model_path}\\lstm_model_{mode}.keras'
        lstm_model = load_model(path, custom_objects={'f1_loss': myutils.f1_loss, 'f1': myutils.f1}) 
        return lstm_model
    
    def predict(self, vectorlist, model): 
        if len(vectorlist) > 0:
            one = []
            one.append(vectorlist)
            one = np.array(one)
            max_length = 10
            one = sequence.pad_sequences(one, maxlen=max_length)
            yhat_probs = model.predict(one, verbose=0)
            prediction = int(yhat_probs[0][0] * 100000)
            prediction = 0.00001 * prediction 
            return prediction
        else:
            return -1
            
    def getblocksVisual(self):
        for mode in self.modes:
            word_vectors = self.load_word2vec_model()
            lstm_model = self.load_lstm_model(mode)

            # Split the source code into lines
            lines = self.sourcecode.splitlines()

            # Calculate dimensions based on number of lines and font size
            img_height = (len(lines) + 1) * self.line_height

            # Create a blank image
            img = Image.new('RGB', (self.img_width, img_height), color='white')
            draw = ImageDraw.Draw(img)

            # Use a monospace font for consistent line spacing
            font = ImageFont.truetype("arial.ttf", 16)

            # Draw each line of source code with appropriate color
            y = 0
            for line in lines:  
                # Check if the line is a comment
                if '//' in line:
                    draw.text((10, y), line, font=font, fill='grey')
                else:
                    tokens = line.split()
                    if len(tokens) > 1:
                        vectorlist = []
                        for token in tokens:
                            if token in word_vectors.key_to_index and token != " ":
                                vector = word_vectors[token]
                                vectorlist.append(vector.tolist())  
                                 
                        if len(vectorlist) > 0:
                            p = self.predict(vectorlist, lstm_model)
                            if p > 0.9:
                                draw.text((10, y), line, font=font, fill='red')
                            elif p > 0.5:
                                draw.text((10, y), line, font=font, fill='yellow')
                            else:
                                draw.text((10, y), line, font=font, fill='blue')
                        else:
                            draw.text((10, y), line, font=font, fill='blue')
                    else:
                        draw.text((10, y), line, font=font, fill='blue')

                y += self.line_height

            # Save the image
            os.makedirs(self.save_blocks_visual_path, exist_ok=True)
            filename = f'demo_{self.mode}.png'
            img.save(os.path.join(self.save_blocks_visual_path, filename))
            print(f"Image saved as {filename}.")
            
        return True

# Example usage:
if __name__ == "__main__":
    sourcecode = '''
    using System;
    using System.Data.SqlClient;

    static class Program
    {
        static void Main()
        {
            // Your C# code here
            Console.WriteLine("Hello from C#");
        }
    }
    '''

    save_blocks_visual_path = r'C:\00\c#\img'
    save_model_path = r'C:\00\last'
    
    vector_size = 100
    iteration = 5 
    min_count = 1
    
    modes = ['xss', 'remote_code_execution', 'command_injection', 'path_disclosure', 'xsrf', 'sql', 'open_redirect']
    
    generator = Demonstrate(sourcecode, save_blocks_visual_path, 
                                         save_model_path, vector_size, iteration, min_count, modes)
    result = generator.getblocksVisual()

    