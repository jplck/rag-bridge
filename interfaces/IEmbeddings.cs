namespace Company.Function {
    public interface IEmbeddings {
        Task<IList<ReadOnlyMemory<float>>> GetEmbeddingAsync(IReadOnlyCollection<string> chunks);
    }
}