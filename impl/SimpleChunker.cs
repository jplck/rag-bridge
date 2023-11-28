
using Microsoft.SemanticKernel.Text;

namespace Company.Function {
    public class SimpleChunker : IChunker
    {
        public IReadOnlyCollection<string>? Chunk(string content, int sizeOfChunk = 1000)
        {
            var chunks = TextChunker.SplitPlainTextLines(content, sizeOfChunk);
            return chunks;
        }
    }
}