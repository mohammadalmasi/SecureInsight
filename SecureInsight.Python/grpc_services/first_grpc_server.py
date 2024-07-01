import sys
import os
from typing import Callable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from concurrent import futures
import grpc
from grpc import StatusCode
import PythonCorpusService_pb2
import PythonCorpusService_pb2_grpc
import PythonTokenizerService_pb2
import PythonTokenizerService_pb2_grpc
from corpus import Corpus
from tokenizer import Tokenizer
        
class PythonCorpusService(PythonCorpusService_pb2_grpc.PythonCorpusServiceServicer):
    def Start(self, request, context):
        try:
            responses = []

            def progress_callback(progress):
                try:
                    if isinstance(progress, (list, tuple)):
                        for p in progress:
                            responses.append(PythonCorpusService_pb2.StartResponse(progress=p))
                    else:
                        responses.append(PythonCorpusService_pb2.StartResponse(progress=progress))
                except Exception as e:
                    # context.set_details(f"Error in progress_callback: {str(e)}")
                    # context.set_code(grpc.StatusCode.INTERNAL)
                    return

            def status_callback(status):
                try:
                    # Ensure status is a string
                    if not isinstance(status, str):
                        status = str(status)
                    print(f"status_callback called with status of type {type(status)} and value {status}")
                    
                    responses.append(PythonCorpusService_pb2.StartResponse(status=status))
                except Exception as e:
                    # context.set_details(f"Error in status_callback: {str(e)}")
                    # context.set_code(grpc.StatusCode.INTERNAL)
                    return

            corpus = Corpus(
                request.language,
                request.remote_url,
                request.path,
                progress_callback,
                status_callback,
            )
            result = corpus.collect()

            responses.append(PythonCorpusService_pb2.StartResponse(result=result))

            for response in responses:
                yield response

        except Exception as e:
            # context.set_details(f'Error occurred: {str(e)}')
            # context.set_code(grpc.StatusCode.INTERNAL)
            return
        

class PythonTokenizerService(PythonTokenizerService_pb2_grpc.PythonTokenizerServiceServicer):
    def Start(self, request, context):
        try:
            responses = []
            seen_statuses = set()  # Track seen statuses to avoid duplicates

            def progress_callback(progress):
                try:
                    if isinstance(progress, (list, tuple)):
                        for p in progress:
                            responses.append(PythonCorpusService_pb2.StartResponse(progress=p))
                    else:
                        responses.append(PythonCorpusService_pb2.StartResponse(progress=progress))
                except Exception as e:
                    context.set_details(f"Error in progress_callback: {str(e)}")
                    context.set_code(grpc.StatusCode.INTERNAL)
                    return

            def status_callback(status):
                try:
                    # Ensure status is a string
                    if not isinstance(status, str):
                        status = str(status)
                    print(f"status_callback called with status of type {type(status)} and value {status}")
                    
                    # Check for duplicate status
                    if status not in seen_statuses:
                        seen_statuses.add(status)
                        responses.append(PythonCorpusService_pb2.StartResponse(status=status))
                        print(f"Added new status: {status}")
                    else:
                        print(f"Ignored duplicate status: {status}")
                except Exception as e:
                    context.set_details(f"Error in status_callback: {str(e)}")
                    context.set_code(grpc.StatusCode.INTERNAL)
                    return

            print("Starting tokenizer")
            tokenizer = Tokenizer(
                request.language, 
                request.input_paths, 
                request.chunk_size, 
                progress_callback,
                status_callback,
            )
            result = tokenizer.tokenize()
            print(f"Tokenization result: {result}")

            responses.append(PythonCorpusService_pb2.StartResponse(result=result))
            print(f"Final result added to responses: {result}")

            for response in responses:
                print(f"Yielding response: {response}")
                yield response

        except Exception as e:
            context.set_details(f'Error occurred: {str(e)}')
            context.set_code(grpc.StatusCode.INTERNAL)
            print(f"Exception in Start method: {str(e)}")
            return





# class PythonTokenizerService(PythonTokenizerService_pb2_grpc.PythonTokenizerServiceServicer):
#     def Start(self, request, context):
#         try:
#             responses = []

#             def progress_callback(progress):
#                 try:
#                     if isinstance(progress, (list, tuple)):
#                         for p in progress:
#                             responses.append(PythonCorpusService_pb2.StartResponse(progress=p))
#                     else:
#                         responses.append(PythonCorpusService_pb2.StartResponse(progress=progress))
#                 except Exception as e:
#                     context.set_details(f"Error in progress_callback: {str(e)}")
#                     context.set_code(grpc.StatusCode.INTERNAL)
#                     return

#             def status_callback(status):
#                 try:
#                     # Ensure status is a string
#                     if not isinstance(status, str):
#                         status = str(status)
#                     print(f"status_callback called with status of type {type(status)} and value {status}")
                    
#                     responses.append(PythonCorpusService_pb2.StartResponse(status=status))
#                 except Exception as e:
#                     context.set_details(f"Error in status_callback: {str(e)}")
#                     context.set_code(grpc.StatusCode.INTERNAL)
#                     return

#             tokenizer = Tokenizer(
#                 request.language, 
#                 request.input_paths, 
#                 request.chunk_size, 
#                 progress_callback,
#                 status_callback,
#                 )
#             result = tokenizer.tokenize()

#             responses.append(PythonCorpusService_pb2.StartResponse(result=result))

#             for response in responses:
#                 yield response

#         except Exception as e:
#             context.set_details(f'Error occurred: {str(e)}')
#             context.set_code(grpc.StatusCode.INTERNAL)
#             return

def serve():
    # Create a gRPC server with a thread pool of 10 worker threads
    MAX_MESSAGE_SIZE = 100 * 1024 * 1024  # 100 MB
    options = [('grpc.max_receive_message_length', MAX_MESSAGE_SIZE)]
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=options)
    
    # Register the services with the server
    PythonCorpusService_pb2_grpc.add_PythonCorpusServiceServicer_to_server(PythonCorpusService(), server)
    PythonTokenizerService_pb2_grpc.add_PythonTokenizerServiceServicer_to_server(PythonTokenizerService(), server)

    # Specify the server to listen on port 50051
    server.add_insecure_port('[::]:50051')
    
    # Start the server
    server.start()
    print("Server started on port 50051")
    
    # Keep the server running and wait for termination signal
    server.wait_for_termination()

if __name__ == '__main__':
    serve()# Start the gRPC server

