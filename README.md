Step 1. Corpus
Choosing Between Git CLI and ‘pydriller’:
The decision to use direct Git CLI commands in the provided script likely prioritizes real-time progress reporting and control over operations, crucial for maintaining client engagement and understanding of ongoing tasks. This approach allows the script to dynamically update progress based on actual operations performed, enhancing transparency and user experience during lengthy operations such as repository traversal and commit processing.

Execution Flow
1. Initialization: Sets up the repository path, language, and callback function.
2. Counting Commits: Counts all commits across branches.
3. Fetching Commit Hashes: Asynchronously fetches commit hashes for all branches.
4. Processing Commits:
•	Process Commits Loop:
1.	Fetch and Process: Asynchronously processes each commit to extract source code files.
2.	Mark Commit as Processed: Commits are marked as processed in batches.
3.	Progress Update: Calls progress_callback to update the progress based on the number of commits processed.
4.	Output: Writes the processed source code to an output file (repo_name.txt).


Step 2. Tokenazation
Tokenization in C# typically involves breaking down a piece of text, often source code, into individual tokens that represent the smallest units of meaningful syntax, such as keywords, identifiers, literals, and punctuation. Roslyn, the .NET compiler platform, provides robust support for tokenization and syntax analysis. Here's how we tokenized C# code using Roslyn:

Step 3. Word2VecModel

Step 4. LSTMModel

Step 5. MLPModel

Step 6. CNNModel

Step 7. Demonstrate

Step 8. Metrics

Step 9. Analysis

