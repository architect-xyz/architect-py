/**
 * JSDoc emitter module
 * @module JSDoc Emitters
 * @see module:scripts/emit/jsdoc
 */
const { Kind, GraphQLScalarType } = require('graphql');
const {
  grosslyHandleMMNames,
  isPrimitive,
  resolveReturnType,
  resolveArgs,
} = require('./shared.cjs');

/**
 * Generates jsdoc based typemap for emitted file.
 *
 * @param {ReturnType<import('graphql').GraphQLSchema['getTypeMap']>} typemap
 */
function typemap(typemap) {
  let scalars = ['/**'];
  let nonScalars = [];
  Object.entries(typemap).forEach(([key, type]) => {
    // TODO: handle multiline descriptions better
    let description = type.description
      ? ' - ' + type.description.split('\n')[0]
      : '';
    if (type instanceof GraphQLScalarType) {
      return scalars.push(
        ` * @typedef { import('../src/graphql/graphql.ts').Scalars['${key}']['output'] } ${key}${description} `,
      );
    } else {
      // ignore graphql native types
      if (key.startsWith('__')) return;

      // TODO: Handle double uppercase the same as the builtin codegen
      return nonScalars.push(
        ` * @typedef { import('../src/graphql/graphql.ts').${grosslyHandleMMNames(key)} } ${grosslyHandleMMNames(key)}${description} `,
      );
    }
  });
  return scalars.join('\n') + '\n *\n' + nonScalars.join('\n') + '\n */\n';
}

/***
 * Generate JSDoc param
 * @param {import('graphql').InputValueDefinitionNode} param
 */
function param(param) {
  const type = kind(param.type);
  // TODO: handle NON_NULL Arrays
  const paramName =
    param.type.kind === Kind.NON_NULL_TYPE
      ? param.name.value
      : `[${param.name.value}]`;
  const description = param.description ? ' ' + param.description.value : '';
  return `@param {${type}} ${paramName}${description}`;
}

/**
 * Generate API docblock
 * @param {import('graphql').FieldDefinitionNode} node
 */
function docblock(node) {
  const isList =
    node.type.kind === Kind.LIST_TYPE ||
    (node.type.kind === Kind.NON_NULL_TYPE &&
      node.type.type.kind === Kind.LIST_TYPE);

  const returnType = resolveReturnType(node);
  const isScalar = isPrimitive(returnType);
  let code = ['/**', node.description?.value].filter(Boolean);

  if (!isScalar) {
    code.push(
      `@template {keyof import('../src/graphql/graphql.ts').${returnType}} Fields`,
    );
    code.push(
      `@param {Array<Fields>} fields Fields to select in response type`,
    );
  }
  const args = resolveArgs(node);

  if (args) {
    code.push(...args.map(param));
  }

  // TODO: update to this sort of syntax to reuse the other codegen emit
  // * @returns {Promise<import('../src/graphql/graphql.ts').MutationRoot['createMmAlgo']>}
  const returnTypeDef = isScalar
    ? `@returns {Promise<${returnType}${isList ? '[]' : ''}>}`
    : `@returns {Promise<Pick<${returnType}, Fields | '__typename'>${isList ? '[]' : ''}>}`;
  code.push(returnTypeDef);

  return code.join('\n * ') + '\n **/';
}

/***
 * Generate kind syntax for jsdoc
 * @param {import('graphql').InputValueDefinitionNode['type'} t
 */
function kind(t) {
  switch (t.kind) {
    case Kind.NON_NULL_TYPE: {
      // console.log(t, omitLoc(t));
      // TODO: if not required, emit `[paramName]` syntax
      return kind(t.type);
    }
    case Kind.LIST_TYPE: {
      // console.log(t, omitLoc(t));
      return `${kind(t.type)}[]`;
    }
    case Kind.NAMED_TYPE:
      return grosslyHandleMMNames(t.name.value);
    default:
      throw new TypeError(`Unexpected kind type k`);
  }
}

module.exports = {
  typemap,
  docblock,
  param,
};
