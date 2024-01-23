param location string = 'westeurope'
param openAiAccountName string
param openAISku string = 'S0'
param searchSku string = 'standard'
param projectName string
param aiSearchName string

resource openAIAccount 'Microsoft.CognitiveServices/accounts@2023-05-01' = {
  name: openAiAccountName
  location: location
  kind: 'OpenAI'
  sku: {
    name: openAISku
  }
  properties: {
    customSubDomainName: 'coreai-${projectName}'
    publicNetworkAccess: 'Enabled'
  }
}

resource deploymentModel1 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: openAIAccount
  name: 'completion'
  properties: {
    model: {
      name: 'gpt-35-turbo'
      version: '0301'
      format: 'OpenAI'
    }
  }
  sku: {
    name: 'Standard'
    capacity: 50
  }
}

resource deploymentEmbeddings 'Microsoft.CognitiveServices/accounts/deployments@2023-05-01' = {
  parent: openAIAccount
  dependsOn: [deploymentModel1]
  name: 'embedding'
  properties: {
    model: {
      name: 'text-embedding-ada-002'
      version: '2'
      format: 'OpenAI'
    }
  }
  sku: {
    name: 'Standard'
    capacity: 50
  }
}

resource search 'Microsoft.Search/searchServices@2021-04-01-preview' = {
  name: aiSearchName
  location: location
  sku: {
    name: searchSku
  }
  properties: {
    replicaCount: 1
    partitionCount: 1
    hostingMode: 'default'
    semanticSearch: 'free'
  }
}

output openaiDeploymentEndpoint string = openAIAccount.properties.endpoint
