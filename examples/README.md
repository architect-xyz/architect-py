# Async vs Sync Clients

The python has both a sync version of the client,. To use this flavor of the client, import from architect_py.client and import the Client instead. It is completely identical to the AsyncClient except 2 key differences:

- Not async, so if you simply remove the async/await keywords from every example
- Subscriptions do not work

# Tips

The best way to code to the API is with an IDE that does type checking (e.g. VSCode with the Pylance extension).
The package has typing throughout, and the package will generally work when the types all work out.