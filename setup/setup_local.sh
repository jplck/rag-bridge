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

#az cli command to get primary endpoint for openai
OPENAI_ENDPOINT=$(az cognitiveservices account show --name $OAI_RESOURCE_NAME --resource-group $RESOURCE_GROUP --query "properties.endpoint" --output tsv)

#az cli command to get primary endpoint for azure search
SEARCH_ENDPOINT="https://$SEARCH_RESOURCE_NAME.search.windows.net"

#create json file with all the endpoints
cat <<EOF > ../src/local.settings.json
{
    "IsEncrypted": false,
     "Values": {
        "AzureWebJobsStorage": "UseDevelopmentStorage=true",
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
        "OPENAI_API_ENDPOINT": "$OPENAI_ENDPOINT",
        "OPENAI_DEPLOYMENT_NAME": "model1",
        "OPENAI_EMBEDDINGS_DEPLOYMENT_NAME": "embedding",
        "COGNITIVE_SEARCH_ENDPOINT": "$SEARCH_ENDPOINT",
        "COGNITIVE_SEARCH_INDEX_NAME": "cognitive-search",
        "SEMANTIC_CONFIG_NAME": "semantic-config",
        "VECTOR_CONFIG_NAME": "vector-config"
    }
}
EOF

echo "Done creating local.settings.json files."