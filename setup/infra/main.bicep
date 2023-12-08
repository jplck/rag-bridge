@description('Location resources.')
param location string = 'westeurope'

@description('Define the project name')
param projectName string

targetScope = 'subscription'

resource rg 'Microsoft.Resources/resourceGroups@2021-01-01' = {
  name: '${projectName}-rg'
  location: location
}

module logging 'logging.bicep' = {
  name: 'logging'
  scope: rg
  params: {
    location: location
    logAnalyticsWorkspaceName: 'log-${projectName}'
    applicationInsightsName: 'appi-${projectName}'
  }
}

module indexer_func_storage 'storage.bicep' = {
  name: 'indexer_func_storage'
  scope: rg
  params: {
    location: location
    storageAccountName: 'indexerfuncstor${projectName}'
    containerNames: []
  }
}

module memory_storage 'storage.bicep' = {
  name: 'memory_storage'
  scope: rg
  params: {
    location: location
    storageAccountName: 'memory${projectName}'
    containerNames: []
  }
}


module indexer_func 'indexer.bicep' = {
  name: 'indexer_func'
  scope: rg
  params: {
    location: location
    webJobStorageAccountName: indexer_func_storage.outputs.storageAccountName
    applicationInsightsName: logging.outputs.appInsightsName
    appName: 'indexerfunc${projectName}'
  }
}

module ai 'ai.bicep' = {
  name: 'ai'
  scope: rg
  params: {
    location: location
    openaiDeploymentName: 'openai-${projectName}'
    projectName: projectName
  }
}
