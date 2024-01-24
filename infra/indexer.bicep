param appName string
param location string = resourceGroup().location
param webJobStorageAccountName string
param applicationInsightsName string
param aiSearchName string
param openAiName string

var hostingPlanName = '${appName}-plan'

resource webJobStorageAccount 'Microsoft.Storage/storageAccounts@2021-08-01' existing = {
  name: webJobStorageAccountName
}

resource appInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName
}

resource aiSearch 'Microsoft.Search/searchServices@2020-08-01-preview' existing = {
  name: aiSearchName
}

resource openAI 'Microsoft.CognitiveServices/accounts@2023-05-01' existing = {
  name: openAiName
}

resource hostingPlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: hostingPlanName
  location: location
  sku: {
    name: 'Y1'
    tier: 'Dynamic'
  }
  properties: {
    reserved: true
  }
}

resource functionApp 'Microsoft.Web/sites@2022-03-01' = {
  name: appName
  location: location
  kind: 'functionapp,linux'
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: hostingPlan.id
    siteConfig: {
      appSettings: [
        {
          name: 'AzureWebJobsStorage'
          value: 'DefaultEndpointsProtocol=https;AccountName=${webJobStorageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${webJobStorageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTAZUREFILECONNECTIONSTRING'
          value: 'DefaultEndpointsProtocol=https;AccountName=${webJobStorageAccount.name};EndpointSuffix=${environment().suffixes.storage};AccountKey=${webJobStorageAccount.listKeys().keys[0].value}'
        }
        {
          name: 'WEBSITE_CONTENTSHARE'
          value: toLower(appName)
        }
        {
          name: 'FUNCTIONS_EXTENSION_VERSION'
          value: '~4'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'FUNCTIONS_WORKER_RUNTIME'
          value: 'python'
        }
        {
          name: 'OPENAI_DEPLOYMENT_NAME'
          value: 'completion'
        }
        {
          name: 'OPENAI_EMBEDDINGS_DEPLOYMENT_NAME'
          value: 'embedding'
        }
        {
          name: 'COGNITIVE_SEARCH_ENDPOINT'
          value: 'https://${aiSearch.name}.search.windows.net'
        }
        {
          name: 'COGNITIVE_SEARCH_KEY'
          value: aiSearch.listAdminKeys().primaryKey
        }
        {
          name: 'COGNITIVE_SEARCH_INDEX_NAME'
          value: 'cognitive-search'
        }
        {
          name: 'SEMANTIC_CONFIG_NAME'
          value: 'semantic-config'
        }
        {
          name: 'VECTOR_CONFIG_NAME'
          value: 'vector-config'
        }
        {
          name: 'OPENAI_API_TYPE'
          value: 'azure'
        }
        {
          name: 'OPENAI_API_KEY'
          value: openAI.listKeys().key1
        }
        {
          name: 'AZURE_OPENAI_ENDPOINT'
          value: openAI.properties.endpoint
        }
        {
          name: 'OPENAI_API_VERSION'
          value: '2023-05-15'
        }
        {
          name: 'DATA_ENPOINT_URL'
          value: '[ADD URL HERE]'
        }
      ]
      ftpsState: 'Disabled'
      minTlsVersion: '1.2'
    }
    httpsOnly: false
  }
}
