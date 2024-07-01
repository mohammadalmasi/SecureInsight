import os
from highlighted_excepthook import ExceptionSetup
import myutils
import sys
import json
from keras.models import load_model
from gensim.models import Word2Vec
from colorama import Fore, Style

class Demonstrate:
   def __init__(self, modes, samples_path, save_model_path, vector_size,
                iteration, min_count, save_blocks_visual_path, number_of_example):
       self.modes = modes
       self.samples_path = samples_path
       self.save_model_path = save_model_path
       self.vector_size = vector_size
       self.iteration = iteration
       self.min_count = min_count
       self.save_blocks_visual_path = save_blocks_visual_path
       self.number_of_example = number_of_example

  
   def getblocksVisual(self):
        for mode in self.modes:
            threshold = []
            threshold1 = [0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1]
            threshold2 = [0.9999,0.999,0.99,0.9,0.5,0.1,0.01,0.001,0.0001]
            
            nr = "2"
            fine = ""
            
            if (len(sys.argv) > 1):
              mode = sys.argv[1]
              if len(sys.argv) > 2:
                nr = sys.argv[2]
                if len(sys.argv) > 3:
                  fine = sys.argv[3]
                  
            if fine == "fine":
              threshold = threshold2
            else:
              threshold = threshold1
            
            # #get word2vec model
            w2vmodel = f"{self.save_model_path}\\word2vec_{self.vector_size}_{self.iteration}_{self.min_count}.model"
            
            w2v_model = Word2Vec.load(w2vmodel)

            step = 5
            fulllength = 10

            if (len(sys.argv) > 1):
              mode = sys.argv[1]
              if len(sys.argv) > 2:
                nr = sys.argv[2]
                if len(sys.argv) > 3:
                  fine = sys.argv[3]
            
            path = f'{self.save_model_path}\\lstm_model_'+mode+'.keras'
            model = load_model(path,custom_objects={'f1_loss': myutils.f1_loss, 'f1':myutils.f1})
            
            with open(f'{self.samples_path}\\plain_' + mode+'.txt', 'r') as infile:
              data = json.load(infile)
              
            print(f"{Style.BRIGHT}{Fore.GREEN}Finished loading. {Style.RESET_ALL}")
              
            identifying = myutils.getIdentifiers(mode,nr)
            info = myutils.getFromDataset(identifying,data)
            sourcefull = info[0]



#             sourcefull='''
#             using System;
# using System.Data.SqlClient;

# static class Program
# {
#     static void Main()
#     {
#         const string connectionString =
#             "Data Source=(local);Initial Catalog=Northwind;"
#             + "Integrated Security=true";

#         // Provide the query string with a parameter placeholder.
#         const string queryString =
#             "SELECT ProductID, UnitPrice, ProductName from dbo.products "
#                 + "WHERE UnitPrice > @pricePoint "
#                 + "ORDER BY UnitPrice DESC;";

#         // Specify the parameter value.
#         const int paramValue = 5;

#         // Create and open the connection in a using block. This
#         // ensures that all resources will be closed and disposed
#         // when the code exits.
#         using (SqlConnection connection =
#             new(connectionString))
#         {
#             // Create the Command and Parameter objects.
#             SqlCommand command = new(queryString, connection);
#             command.Parameters.AddWithValue("@pricePoint", paramValue);

#             // Open the connection in a try/catch block.
#             // Create and execute the DataReader, writing the result
#             // set to the console window.
#             try
#             {
#                 connection.Open();
#                 SqlDataReader reader = command.ExecuteReader();
#                 while (reader.Read())
#                 {
#                     Console.WriteLine("\t{0}\t{1}\t{2}",
#                         reader[0], reader[1], reader[2]);
#                 }
#                 reader.Close();
#             }
#             catch (Exception ex)
#             {
#                 Console.WriteLine(ex.Message);
#             }
#             Console.ReadLine();
#         }
#     }
#             '''

            sourcefull='''
        // Provide the query string with a parameter placeholder.
        const string queryString =
            "SELECT ProductID, UnitPrice, ProductName from dbo.products "
                + "WHERE UnitPrice > @pricePoint "
                + "ORDER BY UnitPrice DESC;";

            // Open the connection in a try/catch block.
            // Create and execute the DataReader, writing the result
            // set to the console window.
 
        }
    }
            '''
            
            
            commentareas = myutils.findComments(sourcefull)
            myutils.getblocksVisual(mode,sourcefull, [], commentareas, fulllength, step, nr, w2v_model, 
                                    model,threshold,"",self.save_blocks_visual_path, self.number_of_example)
            
        return True
                                
# Example usage
if __name__ == "__main__":
    # Create an instance of the setup class
    ExceptionSetup().setup_exception_hook()
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    
    #modes = ['xss', 'remote_code_execution', 'command_injection', 'path_disclosure', 'xsrf', 'sql', 'open_redirect']
    modes = ['sql']
    
    samples_path = r'C:\00\samples_path'
    save_model_path = r'C:\00\c#'
    
    vector_size = 1 
    iteration = 1 
    min_count = 1
    
    save_blocks_visual_path = r'C:\00\c#\img'
    
    number_of_example = 1


    demonstrate = Demonstrate(modes, samples_path, save_model_path, vector_size, 
                              iteration, min_count, save_blocks_visual_path, number_of_example)
    result = demonstrate.getblocksVisual()