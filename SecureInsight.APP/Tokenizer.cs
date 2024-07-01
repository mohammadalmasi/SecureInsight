using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;

namespace SecureInsight.APP
{
    public class Tokenizer : ITokenizer
    {
        public bool Tokenize(string[] InputPaths, int ChunkSize, IFileMerger fileMerger)
        {
            try
            {
                // Step 1: Generate merged output file path
                string mergePath = fileMerger.GenerateOutputPath(InputPaths, "_merge");

                // Step 2: Merge input files into the mergePath
                fileMerger.MergeFiles(InputPaths, mergePath);

                // Step 3: Read merge file in chunks and process
                using (StreamReader reader = new StreamReader(mergePath))
                {
                    string line;
                    int linesRead = 0;
                    string codeChunk = "";

                    while ((line = reader.ReadLine()) != null)
                    {
                        // Accumulate lines to form a chunk
                        codeChunk += line + Environment.NewLine;
                        linesRead++;

                        // Check if chunk size reached, or end of file
                        if (linesRead >= ChunkSize || reader.EndOfStream)
                        {
                            // Parse chunk into syntax tree
                            SyntaxTree tree = CSharpSyntaxTree.ParseText(codeChunk);

                            // Process the syntax tree to extract tokens
                            SyntaxNode root = tree.GetRoot();

                            // Step 4: Write tokens to Text file
                            string directory = Path.GetDirectoryName(mergePath);
                            string outputPath = Path.Combine(directory, "csharp_tokenization_results.txt");

                            using (StreamWriter writer = new StreamWriter(outputPath, append: true))
                            {
                                foreach (var token in root.DescendantTokens())
                                {
                                    // Write the token text to the file
                                    writer.WriteLine(token.Text);
                                }
                            }

                            // Reset chunk variables
                            codeChunk = "";
                            linesRead = 0;
                        }
                    }
                }

                return true;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"An error occurred: {ex.Message}");
                return false;
            }
        }

    }

    public interface IFileMerger
    {
        string GenerateOutputPath(string[] inputPaths, string suffix);
        void MergeFiles(string[] sourceFiles, string destinationFile);
    }

    public class FileMerger : IFileMerger
    {
        public string GenerateOutputPath(string[] inputPaths, string suffix)
        {
            // Get the last file path
            string lastFilePath = inputPaths[inputPaths.Length - 1];

            // Extract directory and file name
            string directory = Path.GetDirectoryName(lastFilePath);
            string filename = Path.GetFileName(lastFilePath);

            // Extract name and extension
            string name = Path.GetFileNameWithoutExtension(filename);
            string extension = Path.GetExtension(filename);

            // Create new file name with suffix
            string newFilename = $"{name}{suffix}{extension}";

            // Construct full output path
            string outputPath = Path.Combine(directory, newFilename);

            return outputPath;
        }

        public void MergeFiles(string[] sourceFiles, string destinationFile)
        {
            // Create a FileStream for the destination file
            using (var destinationStream = new FileStream(destinationFile, FileMode.Create))
            {
                foreach (var sourceFile in sourceFiles)
                {
                    // Open each source file using FileStream
                    using (var sourceStream = new FileStream(sourceFile, FileMode.Open, FileAccess.Read))
                    {
                        // Use Stream.CopyTo to copy from sourceStream to destinationStream
                        sourceStream.CopyTo(destinationStream);
                    }
                }
            }
        }
    }
}
