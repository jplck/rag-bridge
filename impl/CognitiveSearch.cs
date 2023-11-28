
using Microsoft.Extensions.Configuration;
using Azure.Search.Documents;
using Azure.Identity;
using Azure.Search.Documents.Indexes;
using Azure.Search.Documents.Indexes.Models;
using Azure.Search.Documents.Models;
using Extensions;

//https://github.com/Azure-Samples/azure-search-dotnet-samples/blob/main/quickstart-semantic-search/SemanticSearchQuickstart/Program.cs

namespace Company.Function
{
    public class CognitiveSearch : IVectorStore
    {
        IConfiguration _configuration;

        SearchIndexClient _searchIndexClient;

        string _searchEndpoint;

        public CognitiveSearch(IConfiguration configuration)
        {
            _configuration = configuration;

            _searchEndpoint = _configuration.TryGet("COGNITIVE_SEARCH_ENDPOINT");

            _searchIndexClient = new SearchIndexClient(
                new Uri(_searchEndpoint),
                new DefaultAzureCredential()
            );
        }

        public void CreateIndex<T>(string indexName)
        {
            var vectorAlgoName = "hnsw";

            var index = _searchIndexClient.TryGetIndex(indexName);
            if (index is null) {
                var fieldBuilder = new FieldBuilder();
                var searchFields = fieldBuilder.Build(typeof(T));

                SearchIndex searchIndex = new(indexName, searchFields) {
                    SemanticSearch = new() {
                        Configurations = {
                            new SemanticConfiguration(
                                _configuration.TryGet("SEMANTIC_CONFIG_NAME"),
                                new() {
                                    ContentFields = {
                                        new SemanticField("Content")
                                    },
                                }
                            )
                        }
                    },
                    VectorSearch = new() {
                        Profiles = {
                            new VectorSearchProfile(
                                _configuration.TryGet("VECTOR_CONFIG_NAME"),
                                vectorAlgoName
                            )
                        },
                        Algorithms = {
                            new HnswAlgorithmConfiguration(vectorAlgoName)
                        }
                    }
                };

                _searchIndexClient.CreateOrUpdateIndex(searchIndex);
            }
            
        }

        public async Task AddDocumentAsync<T>(string indexName, IReadOnlyCollection<T> documents)
        {
            IndexDocumentsBatch<T> batch = IndexDocumentsBatch.Create<T>();

            foreach (var document in documents)
            {
                var item = new IndexDocumentsAction<T>(IndexActionType.Upload, document);
                batch.Actions.Add(item);
            }

            try
            {
                var searchClient = new SearchClient(
                    new Uri(_searchEndpoint),
                    indexName,
                    new DefaultAzureCredential()
                );

                await searchClient.IndexDocumentsAsync(batch);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                throw new Exception("Failed to index documents.");
            }
        }
    }
}