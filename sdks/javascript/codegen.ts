import type { CodegenConfig } from '@graphql-codegen/cli'

const config: CodegenConfig = {
  schema: '../../schema.graphql',
  documents: ['src/**/*.mjs'],
  ignoreNoDocuments: true,
  generates: {
    /*
    './src/graphql/': {
      preset: 'client',
      config: {
        documentMode: 'string'
      }
    },
    './schema.graphql': {
      plugins: ['schema-ast'],
      config: {
        includeDirectives: true
      }
    },
    */
    "./demo/output.mjs": {
      "plugins": [
        "./scripts/codegen.cjs"
      ]
    }
  }
}

export default config
