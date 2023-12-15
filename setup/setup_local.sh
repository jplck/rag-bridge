#!/bin/bash

set -e

PROJECT_NAME="$1"

if [ "$PROJECT_NAME" == "" ]; then
echo "No project name provided - aborting"
exit 0;
fi

RESOURCE_GROUP="$PROJECT_NAME-rg"
OAI_RESOURCE_NAME="openai-$PROJECT_NAME"
SEARCH_RESOURCE_NAME="search-$PROJECT_NAME"
MEMORY_STORAGE_ACCOUNT_NAME="memory$PROJECT_NAME"

#az cli command to get primary endpoint for openai
OPENAI_ENDPOINT=$(az cognitiveservices account show --name $OAI_RESOURCE_NAME --resource-group $RESOURCE_GROUP --query "properties.endpoint" --output tsv)

#get the key for openai
OPENAI_KEY=$(az cognitiveservices account keys list --name $OAI_RESOURCE_NAME --resource-group $RESOURCE_GROUP --query "key1" --output tsv)

#az cli command to get primary endpoint for azure search
SEARCH_ENDPOINT="https://$SEARCH_RESOURCE_NAME.search.windows.net"

#get the key for azure search
SEARCH_KEY=$(az search admin-key show --resource-group $RESOURCE_GROUP --service-name $SEARCH_RESOURCE_NAME --query "primaryKey" --output tsv)

#create json file with all the endpoints
cat <<EOF > ../src/local.settings.json
{
    "IsEncrypted": false,
     "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
        "OPENAI_DEPLOYMENT_NAME": "completion",
        "OPENAI_EMBEDDINGS_DEPLOYMENT_NAME": "embedding",
        "COGNITIVE_SEARCH_ENDPOINT": "$SEARCH_ENDPOINT",
        "COGNITIVE_SEARCH_KEY": "$SEARCH_KEY",
        "COGNITIVE_SEARCH_INDEX_NAME": "cognitive-search",
        "SEMANTIC_CONFIG_NAME": "semantic-config",
        "VECTOR_CONFIG_NAME": "vector-config",
        "OPENAI_API_TYPE": "azure",
        "OPENAI_API_KEY": "$OPENAI_KEY",
        "AZURE_OPENAI_ENDPOINT": "$OPENAI_ENDPOINT",
        "OPENAI_API_VERSION": "2023-05-15",
        "DATA_ENPOINT_URL": "[ADD DATA ENDPOINT URL HERE]",
    }
}
EOF

echo "Done creating local.settings.json files."