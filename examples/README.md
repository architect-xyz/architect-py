# Async and sync clients

The python has both a sync version of the client and and async version based on `asyncio`.  The async version of the client is original, and the sync version is derived from it.   To use the sync flavor of the client, import from `architect_py.client` and import the `Client` instead. 

In the sync client, streaming and subscription methods are not available. 

# Tips

The best way to code to the API is with an IDE that does type checking (e.g. VSCode with the Pylance extension).  The package is well-typed, and if your code typechecks its highly likely to be correct and work. 

The scripts are meant for educational purposes and should NOT be run in production.
