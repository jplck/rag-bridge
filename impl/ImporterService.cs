using Microsoft.Extensions.Hosting;

namespace Company.Function {
    public class ImporterService
    {
        private readonly List<IImporter> _importers;

        public ImporterService(List<IImporter> importers)
        {
            _importers = importers;
        }

        public async Task RunAsync()
        {
            foreach (var importer in _importers)
            {
                await importer.ImportAsync();
            }
        }
    }
}