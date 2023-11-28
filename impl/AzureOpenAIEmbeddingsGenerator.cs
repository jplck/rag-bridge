using System.Collections.ObjectModel;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.AI.Embeddings;

namespace Company.Function {

    public class AzureOpenAIEmbeddingsGenerator : IEmbeddings {

        private ITextEmbeddingGeneration _embeddingGenerator;

        private IKernel _kernel;

        public AzureOpenAIEmbeddingsGenerator(IKernel kernel) {
            _kernel = kernel;
            _embeddingGenerator = _kernel.GetService<ITextEmbeddingGeneration>();
        }

        public async Task<IList<ReadOnlyMemory<float>>> GetEmbeddingAsync(IReadOnlyCollection<string> chunks)
        {
            var results = await _embeddingGenerator.GenerateEmbeddingsAsync(chunks.ToList());
            return results;
        }
    }

}