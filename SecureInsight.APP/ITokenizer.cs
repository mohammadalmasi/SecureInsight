namespace SecureInsight.APP
{
    public interface ITokenizer
    {
        bool Tokenize(string[] InputPaths, int ChunkSize, IFileMerger fileMerger);
    }
}
