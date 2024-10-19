import type { CodegenConfig } from '@graphql-codegen/cli';

const config: CodegenConfig = {
  schema: '../../schema.graphql',
  documents: ['src/**/*.mjs'],
  ignoreNoDocuments: true,
  hooks: {
    afterAllFileWrite: ['biome format --write'],
  },
  generates: {
    /**
     * This emitter has a bug that we have to manually patch. Only need to
     * enable it whenever updating the schema.
     * https://github.com/dotansimha/graphql-code-generator/issues/10176
     *
    './src/graphql/': {
      preset: 'client',
      config: {
        documentMode: 'string',
        scalars: {
          Date: 'string',
          DateTime: 'string',
          Decimal: 'string',
          AccountId: 'string',
          UserId: 'string',
          OrderId: 'string',
          MarketId: 'string',
          VenueId: 'string',
          RouteId: 'string',
          ProductId: 'string',
          ComponentId: 'string',
          FillId: 'string',

          Dir: "'buy' | 'sell'",
          Str: 'string',
          OrderSource: 'string',
        },
      },
    },
    */
    './schema.graphql': {
      plugins: ['schema-ast'],
      config: {
        includeDirectives: true,
      },
    },
    './src/sdk.mjs': {
      plugins: ['./codegen/codegen.cjs'],
      config: { mode: 'production' },
    },
    './demo/output.mjs': {
      plugins: ['./codegen/codegen.cjs'],
      config: { mode: 'debugging' },
    },
  },
};

export default config;
