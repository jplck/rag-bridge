namespace Company.Function {
    public interface IVectorStore {
        Task AddDocumentAsync<T>(string indexName, IReadOnlyCollection<T> documents);
        void CreateIndex<T>(string indexName);
    }
}