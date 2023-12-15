param location string = 'westeurope'
param openaiDeploymentName string
param openAISku string = 'S0'
param searchSku string = 'standard'
param projectName string


resource openAIAccount 'Microsoft.CognitiveServices/accounts@2022-03-01' = {
  name: openaiDeploymentName
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

resource deploymentModel1 'Microsoft.CognitiveServices/accounts/deployments@2022-10-01' = {
  parent: openAIAccount
  name: 'model1'
  properties: {
    model: {
      name: 'gpt-35-turbo'
      version: '1106'
      format: 'OpenAI'
    }
    scaleSettings: {
      scaleType: 'Standard'
    }
  }
}

resource deploymentEmbeddings 'Microsoft.CognitiveServices/accounts/deployments@2022-10-01' = {
  parent: openAIAccount
  dependsOn: [deploymentModel1]
  name: 'embedding'
  properties: {
    model: {
      name: 'text-embedding-ada-002'
      version: '2'
      format: 'OpenAI'
    }
    scaleSettings: {
      scaleType: 'Standard'
    }
  }
}

resource search 'Microsoft.Search/searchServices@2021-04-01-preview' = {
  name: 'search-${projectName}'
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
