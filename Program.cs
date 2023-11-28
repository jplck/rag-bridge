using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.DependencyInjection;
using Company.Function;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using Azure.Identity;
using Microsoft.Extensions.Configuration;

var configuration = new ConfigurationBuilder()
    .AddJsonFile("local.settings.json", optional: true, reloadOnChange: true)
    .AddEnvironmentVariables()
    .Build();

var host = new HostBuilder()
    .ConfigureFunctionsWorkerDefaults()
    .ConfigureServices(services => {
        services.AddApplicationInsightsTelemetryWorkerService();
        services.ConfigureFunctionsApplicationInsights();
        services.AddSingleton<IVectorStore, CognitiveSearch>();
        services.AddSingleton<IChunker, SimpleChunker>();
        services.AddSingleton(new KernelBuilder()
            .WithAzureOpenAIChatCompletionService(configuration["OPENAI_DEPLOYMENT_NAME"], configuration["OPENAI_API_ENDPOINT"], new DefaultAzureCredential())
            .WithAzureOpenAITextEmbeddingGenerationService(configuration["OPENAI_EMBEDDINGS_DEPLOYMENT_NAME"], configuration["OPENAI_API_ENDPOINT"], new DefaultAzureCredential())
            .Build());
        services.AddSingleton<IEmbeddings, AzureOpenAIEmbeddingsGenerator>();
        services.AddSingleton(s =>
        {
            var loggerFactory = s.GetRequiredService<ILoggerFactory>();
            var vectorStore = s.GetRequiredService<IVectorStore>();
            var embeddingsGenerator = s.GetRequiredService<IEmbeddings>();
            var chunker = s.GetRequiredService<IChunker>();
            
            return new ImporterService(new List<IImporter>
            {
                new GenericImporter(loggerFactory.CreateLogger<GenericImporter>(), vectorStore, embeddingsGenerator, chunker),
            });
        });
            
    })
    .Build();

host.Run();
