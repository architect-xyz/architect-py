import type { CodegenConfig } from '@graphql-codegen/cli';

const config: CodegenConfig = {
  schema: '../../schema.graphql',
  documents: ['src/**/*.mjs'],
  ignoreNoDocuments: true,
  hooks: {
    afterAllFileWrite: ['biome format --write'],
  },
  generates: {
    /*
    './src/graphql/': {
      preset: 'client',
      config: {
        documentMode: 'string',
        scalars: {
          // TODO: add additional scalar mapping
          DateTime: 'string',
          Decimal: 'string',
          AccountId: 'string',
          UserId: 'string',
          OrderId: 'string',
          MarketId: 'string',
          VenueId: 'string',
          RouteId: 'string',
          ProductId: 'string',
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
    './src/sdk.mjs': { plugins: ['./scripts/codegen.cjs'] },
    './demo/output.mjs': { plugins: ['./scripts/codegen.cjs'] },
  },
};

export default config;
