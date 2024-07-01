import sys
import os
# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from concurrent import futures
import grpc
# import PythonCorpusService_pb2
# import PythonCorpusService_pb2_grpc
# import PythonTokenizerService_pb2
# import PythonTokenizerService_pb2_grpc
import PythonMakeWord2VecModelService_pb2
import PythonMakeWord2VecModelService_pb2_grpc
import PythonMakeLSTMModelService_pb2
import PythonMakeLSTMModelService_pb2_grpc
import PythonMakeMLPModelService_pb2
import PythonMakeMLPModelService_pb2_grpc
import PythonMakeCNNModelService_pb2
import PythonMakeCNNModelService_pb2_grpc
import PythonDemonstrateService_pb2
import PythonDemonstrateService_pb2_grpc
import PythonLSTMMetricsAnalysisService_pb2
import PythonLSTMMetricsAnalysisService_pb2_grpc
import PythonMLPMetricsAnalysisService_pb2
import PythonMLPMetricsAnalysisService_pb2_grpc
import PythonCNNMetricsAnalysisService_pb2
import PythonCNNMetricsAnalysisService_pb2_grpc
from database import get_session
# from corpus import Corpus
# from tokenizer import Tokenizer
from make_word2vec_model import Word2VecModel
from make_lstm_model import MakeLSTMModel
from make_mlp_model import MakeMLPModel
from make_cnn_model import MakeCNNModel
from demonstrate import Demonstrate
from lstm_metrics_analysis import LSTMMetricsAnalysis
from mlp_metrics_analysis import MLPMetricsAnalysis
from cnn_metrics_analysis import CNNMetricsAnalysis
from csharp_make_word2vec_model import CsharpWord2VecModel


# class PythonCorpusService(PythonCorpusService_pb2_grpc.PythonCorpusServiceServicer):
#     def Start(self, request, context):
#         # List to store responses
#         responses = []

#         # Callback function to handle progress updates
#         def progress_callback(progress):
#             # Ensure progress is iterable
#             if isinstance(progress, (list, tuple)):
#                 for p in progress:
#                     responses.append(PythonCorpusService_pb2.StartResponse(progress=p))
#             else:
#                 # Handle the case where progress is not iterable
#                 responses.append(PythonCorpusService_pb2.StartResponse(progress=progress))
        
#         try:
#             # Initialize the source code collector with the progress callback
#             corpus = Corpus(request.language, request.remote_url, request.path, progress_callback)
#             result = corpus.collect()

#             # Collect final response with the collected source codes
#             responses.append(PythonCorpusService_pb2.StartResponse(result=result))

#         except Exception as e:
#             # Handle and log the exception, if any
#             context.set_details(f'Error occurred: {str(e)}')
#             context.set_code(grpc.StatusCode.INTERNAL)
#             return

#         # Yield all stored responses
#         for response in responses:
#             yield response

# class PythonTokenizerService(PythonTokenizerService_pb2_grpc.PythonTokenizerServiceServicer):
#     def Start(self, request, context):
#         # List to store responses
#         responses = []

#         # Callback function to handle progress updates
#         def progress_callback(progress):
#             # Ensure progress is iterable
#             if isinstance(progress, (list, tuple)):
#                 for p in progress:
#                     responses.append(PythonTokenizerService_pb2.StartResponse(progress=p))
#             else:
#                 # Handle the case where progress is not iterable
#                 responses.append(PythonTokenizerService_pb2.StartResponse(progress=progress))
        
#         try:
#             # Initialize the source code tokenizer with the progress callback
#              tokenizer = Tokenizer(request.language, request.input_paths, request.chunk_size, progress_callback)
#              result = tokenizer.tokenize()

#              # Collect final response with the collected source codes
#              responses.append(PythonTokenizerService_pb2.StartResponse(result=result))

#         except Exception as e:
#             # Handle and log the exception, if any
#             context.set_details(f'Error occurred: {str(e)}')
#             context.set_code(grpc.StatusCode.INTERNAL)
#             return

#         # Yield all stored responses
#         for response in responses:
#             yield response

class PythonMakeWord2VecModelService(PythonMakeWord2VecModelService_pb2_grpc.PythonMakeWord2VecModelServiceServicer):
    def Start(self, request, context):
        # List to store responses
        responses = []

        # Callback function to handle progress updates
        def progress_callback(progress):
            # Ensure progress is iterable
            if isinstance(progress, (list, tuple)):
                for p in progress:
                    responses.append(PythonMakeWord2VecModelService_pb2.StartResponse(progress=p))
            else:
                # Handle the case where progress is not iterable
                responses.append(PythonMakeWord2VecModelService_pb2.StartResponse(progress=progress))
        
        try:
            if(request.tokenize_lanquage==1):
                # Initialize the source code collector with the progress callback
                word2VecModel = Word2VecModel(request.tokenized_data_path, request.model_path, request.vector_size,
                                          request.iterations, request.min_count, request.workers)
                result = word2VecModel.train_model()

                # Collect final response with the collected source codes
                responses.append(PythonMakeWord2VecModelService_pb2.StartResponse(result=result))
                
            else:
                # Initialize the source code collector with the progress callback
                word2VecModel = CsharpWord2VecModel(request.tokenized_data_path, request.model_path, request.vector_size,
                                          request.iterations, request.min_count, request.workers)
                result = word2VecModel.train_model()

                # Collect final response with the collected source codes
                responses.append(PythonMakeWord2VecModelService_pb2.StartResponse(result=result))    
                

        except Exception as e:
            # Handle and log the exception, if any
            context.set_details(f'Error occurred: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return

        # Yield all stored responses
        for response in responses:
            yield response

class PythonMakeLSTMModelService(PythonMakeLSTMModelService_pb2_grpc.PythonMakeLSTMModelServiceServicer):
    def Start(self, request, context):
        # List to store responses
        responses = []

        # Callback function to handle progress updates
        def progress_callback(progress):
            # Ensure progress is iterable
            if isinstance(progress, (list, tuple)):
                for p in progress:
                    responses.append(PythonMakeLSTMModelService_pb2.StartResponse(progress=p))
            else:
                # Handle the case where progress is not iterable
                responses.append(PythonMakeLSTMModelService_pb2.StartResponse(progress=progress))
        
        try:
            # Initialize the source code collector with the progress callback
            lstmModel = MakeLSTMModel(request.modes, request.samples_path, request.save_model_path, 
                                      request.dropout, request.neurons, request.epochs, request.batch_size, 
                                      request.vector_size, request.iteration, request.min_count)
            result = lstmModel.train_model()

            # Collect final response with the collected source codes
            responses.append(PythonMakeLSTMModelService_pb2.StartResponse(result=result))

        except Exception as e:
            # Handle and log the exception, if any
            context.set_details(f'Error occurred: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return

        # Yield all stored responses
        for response in responses:
            yield response

class PythonMakeMLPModelService(PythonMakeMLPModelService_pb2_grpc.PythonMakeMLPModelServiceServicer):
    def Start(self, request, context):
        # List to store responses
        responses = []

        # Callback function to handle progress updates
        def progress_callback(progress):
            # Ensure progress is iterable
            if isinstance(progress, (list, tuple)):
                for p in progress:
                    responses.append(PythonMakeMLPModelService_pb2.StartResponse(progress=p))
            else:
                # Handle the case where progress is not iterable
                responses.append(PythonMakeMLPModelService_pb2.StartResponse(progress=progress))
        
        try:
            # Initialize the source code collector with the progress callback
            mlpModel = MakeMLPModel(request.modes, request.save_model_path, 
                                    request.epochs, request.batch_size)
            result = mlpModel.train_model()

            # Collect final response with the collected source codes
            responses.append(PythonMakeMLPModelService_pb2.StartResponse(result=result))

        except Exception as e:
            # Handle and log the exception, if any
            context.set_details(f'Error occurred: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return

        # Yield all stored responses
        for response in responses:
            yield response
        
class PythonMakeCNNModelService(PythonMakeCNNModelService_pb2_grpc.PythonMakeCNNModelServiceServicer):
    def Start(self, request, context):
        # List to store responses
        responses = []

        # Callback function to handle progress updates
        def progress_callback(progress):
            # Ensure progress is iterable
            if isinstance(progress, (list, tuple)):
                for p in progress:
                    responses.append(PythonMakeCNNModelService_pb2.StartResponse(progress=p))
            else:
                # Handle the case where progress is not iterable
                responses.append(PythonMakeCNNModelService_pb2.StartResponse(progress=progress))
        
        try:
            # Initialize the source code collector with the progress callback
            cnnModel = MakeCNNModel(request.modes, request.save_model_path, request.epochs, request.batch_size)
            result = cnnModel.train_model()

            # Collect final response with the collected source codes
            responses.append(PythonMakeCNNModelService_pb2.StartResponse(result=result))

        except Exception as e:
            # Handle and log the exception, if any
            context.set_details(f'Error occurred: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return

        # Yield all stored responses
        for response in responses:
            yield response           
        
class PythonDemonstrateService(PythonDemonstrateService_pb2_grpc.PythonDemonstrateServiceServicer):
    def Start(self, request, context):
        # List to store responses
        responses = []

        # Callback function to handle progress updates
        def progress_callback(progress):
            # Ensure progress is iterable
            if isinstance(progress, (list, tuple)):
                for p in progress:
                    responses.append(PythonDemonstrateService_pb2.StartResponse(progress=p))
            else:
                # Handle the case where progress is not iterable
                responses.append(PythonDemonstrateService_pb2.StartResponse(progress=progress))
        
        try:
            # Initialize the source code collector with the progress callback
            demonstrate = Demonstrate(request.modes, request.samples_path, request.save_model_path, request.vector_size, 
                                      request.iteration, request.min_count, request.save_blocks_visual_path, 
                                      request.number_of_example)
            
            result = demonstrate.getblocksVisual()

            # Collect final response with the collected source codes
            responses.append(PythonDemonstrateService_pb2.StartResponse(result=result))

        except Exception as e:
            # Handle and log the exception, if any
            context.set_details(f'Error occurred: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return

        # Yield all stored responses
        for response in responses:
            yield response
            
class PythonLSTMMetricsAnalysisService(PythonLSTMMetricsAnalysisService_pb2_grpc.PythonLSTMMetricsAnalysisServiceServicer):
    def Start(self, request, context):
        # List to store responses
        responses = []
        
        # Callback function to handle progress updates
        def progress_callback(progress):
            # Ensure progress is iterable
            if isinstance(progress, (list, tuple)):
                for p in progress:
                    responses.append(PythonLSTMMetricsAnalysisService_pb2.StartResponse(progress=p))
            else:
                # Handle the case where progress is not iterable
                responses.append(PythonLSTMMetricsAnalysisService_pb2.StartResponse(progress=progress))
        
        try:
            DATABASE_URL = f'sqlite:///{request.save_model_path}\SecureInsight.db'
            db_session = get_session(DATABASE_URL)

            # Initialize the source code collector with the progress callback
            lSTMMetricsAnalysis = LSTMMetricsAnalysis(request.modes, request.save_model_path, db_session)
            result = lSTMMetricsAnalysis.metrics_analysis()
            print(result)

            # Collect final response with the collected source codes
            responses.append(PythonLSTMMetricsAnalysisService_pb2.StartResponse(result=result))

        except Exception as e:
            # Handle and log the exception, if any
            context.set_details(f'Error occurred: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return

        # Yield all stored responses
        for response in responses:
            yield response 
            
class PythonMLPMetricsAnalysisService(PythonMLPMetricsAnalysisService_pb2_grpc.PythonMLPMetricsAnalysisServiceServicer):
    def Start(self, request, context):
        # List to store responses
        responses = []
        
        # Callback function to handle progress updates
        def progress_callback(progress):
            # Ensure progress is iterable
            if isinstance(progress, (list, tuple)):
                for p in progress:
                    responses.append(PythonMLPMetricsAnalysisService_pb2.StartResponse(progress=p))
            else:
                # Handle the case where progress is not iterable
                responses.append(PythonMLPMetricsAnalysisService_pb2.StartResponse(progress=progress))
        
        try:
            DATABASE_URL = f'sqlite:///{request.save_model_path}\SecureInsight.db'
            db_session = get_session(DATABASE_URL)

            # Initialize the source code collector with the progress callback
            mLPMetricsAnalysis = MLPMetricsAnalysis(request.modes, request.save_model_path, db_session)
            result = mLPMetricsAnalysis.metrics_analysis()

            # Collect final response with the collected source codes
            responses.append(PythonMLPMetricsAnalysisService_pb2.StartResponse(result=result))

        except Exception as e:
            # Handle and log the exception, if any
            context.set_details(f'Error occurred: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return

        # Yield all stored responses
        for response in responses:
            yield response 
            
class PythonCNNMetricsAnalysisService(PythonCNNMetricsAnalysisService_pb2_grpc.PythonCNNMetricsAnalysisServiceServicer):
    def Start(self, request, context):
        # List to store responses
        responses = []
        
        # Callback function to handle progress updates
        def progress_callback(progress):
            # Ensure progress is iterable
            if isinstance(progress, (list, tuple)):
                for p in progress:
                    responses.append(PythonCNNMetricsAnalysisService_pb2.StartResponse(progress=p))
            else:
                # Handle the case where progress is not iterable
                responses.append(PythonCNNMetricsAnalysisService_pb2.StartResponse(progress=progress))
        
        try:
            DATABASE_URL = f'sqlite:///{request.save_model_path}\SecureInsight.db'
            db_session = get_session(DATABASE_URL)

            # Initialize the source code collector with the progress callback
            cNNMetricsAnalysis = CNNMetricsAnalysis(request.modes, request.save_model_path, db_session)
            result = cNNMetricsAnalysis.metrics_analysis()

            # Collect final response with the collected source codes
            responses.append(PythonCNNMetricsAnalysisService_pb2.StartResponse(result=result))

        except Exception as e:
            # Handle and log the exception, if any
            context.set_details(f'Error occurred: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            return

        # Yield all stored responses
        for response in responses:
            yield response 



def serve():
    # Create a gRPC server with a thread pool of 10 worker threads
    MAX_MESSAGE_SIZE = 100 * 1024 * 1024  # 100 MB
    options = [('grpc.max_receive_message_length', MAX_MESSAGE_SIZE)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
    
    # Register the services with the server
    # PythonCorpusService_pb2_grpc.add_PythonCorpusServiceServicer_to_server(PythonCorpusService(), server)
    # PythonTokenizerService_pb2_grpc.add_PythonTokenizerServiceServicer_to_server(PythonTokenizerService(), server)
    PythonMakeWord2VecModelService_pb2_grpc.add_PythonMakeWord2VecModelServiceServicer_to_server(PythonMakeWord2VecModelService(), server)
    PythonMakeLSTMModelService_pb2_grpc.add_PythonMakeLSTMModelServiceServicer_to_server(PythonMakeLSTMModelService(), server)
    PythonMakeMLPModelService_pb2_grpc.add_PythonMakeMLPModelServiceServicer_to_server(PythonMakeMLPModelService(), server)
    PythonMakeCNNModelService_pb2_grpc.add_PythonMakeCNNModelServiceServicer_to_server(PythonMakeCNNModelService(), server)
    PythonDemonstrateService_pb2_grpc.add_PythonDemonstrateServiceServicer_to_server(PythonDemonstrateService(), server)
    PythonLSTMMetricsAnalysisService_pb2_grpc.add_PythonLSTMMetricsAnalysisServiceServicer_to_server(PythonLSTMMetricsAnalysisService(), server)
    PythonMLPMetricsAnalysisService_pb2_grpc.add_PythonMLPMetricsAnalysisServiceServicer_to_server(PythonMLPMetricsAnalysisService(), server)
    PythonCNNMetricsAnalysisService_pb2_grpc.add_PythonCNNMetricsAnalysisServiceServicer_to_server(PythonCNNMetricsAnalysisService(), server)


    # Specify the server to listen on port 50052
    server.add_insecure_port('[::]:50052')
    
    # Start the server
    server.start()
    print("Server started on port 50052")
    
    # Keep the server running and wait for termination signal
    server.wait_for_termination()

if __name__ == '__main__':
    serve()# Start the gRPC server

