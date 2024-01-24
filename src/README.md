# rag-bridge

DISCLAIMER: Do not use in production.

![Overview architecture](/architecture/overview.png)

## Steps to run the project
1. Create infrastructure by running ./setup/deploy.sh PROJECT_NAME LOCATION. Please change PROJECT_NAME and LOCATION accordingly.
2. For local developmen run ./setup/setup_local.sh PROJECT_NAME. This will get all the connection information (strings and secrets) so you can run the application from your local machine. To see the results of this step, check the local_settings.json in your src directory.
3. To test without real data you can use the prompt below to create a test.json in the docs directory.
4. You can start the application with a click on F5 or the debug menu.
5. After you app is running, you can test it by opening up the samples.http file and running the POST request from there. 

Promt for test.json creation: 
generate a json file that contains a json array exlaining different methods to apply for "Baustrom" in form of a FAQ. Add 10 question/asnwer combinations to that json array. The json should contain a title and content plus a unique id. Be very descriptive in you answers. Do not add a root element.
