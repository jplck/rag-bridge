using System;
using Microsoft.Azure.Functions.Worker;
using Microsoft.Extensions.Logging;

namespace Company.Function
{
    public class TimerImporter
    {
        private readonly ILogger _logger;

        private readonly ImporterService _importerService;

        public TimerImporter(ILoggerFactory loggerFactory, ImporterService importerService)
        {
            _logger = loggerFactory.CreateLogger<TimerImporter>();
            _importerService = importerService;
        }

        [Function("TimerImporter")]
        public async Task Run([TimerTrigger("15 * * * * *")] TimerInfo myTimer)
        {
            _logger.LogInformation($"C# Timer trigger function executed at: {DateTime.Now}");
            
            if (myTimer.ScheduleStatus is not null)
            {
                _logger.LogInformation($"Next timer schedule at: {myTimer.ScheduleStatus.Next}");
            }

            await _importerService.RunAsync();
        }
    }
}
