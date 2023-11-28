using Azure.Search.Documents.Indexes;
using Newtonsoft.Json;

namespace Company.Function {
    public class GenericDataObject
    {
        [SimpleField(IsKey = true, IsFilterable = true, IsSortable = true)]
        public required string Id { get; set; }

        [SearchableField(IsFilterable = true, IsSortable = true)]
        public required string Name { get; set; }

        [SearchableField(AnalyzerName = "en.microsoft")]
        public required string Description { get; set; }

        [VectorSearchField(VectorSearchDimensions = 1536, VectorSearchProfileName  = "vector-config")]
        [JsonIgnore]
        public IReadOnlyList<float>? DescriptionVector { get; set; }
    }
}