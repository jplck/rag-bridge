namespace Company.Function {
    public interface IChunker {
        IReadOnlyCollection<string>? Chunk(string content, int sizeOfChunk = 1000);
    }
}