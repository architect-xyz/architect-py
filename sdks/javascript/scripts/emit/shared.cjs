/**
 * Shared utilities and helpers
 * @module Shared Utils
 * @private
 */
const { Kind } = require('graphql');

/**
 * @param {String} str
 * @returns {String}
 */
function grosslyHandleMMNames(str) {
  return str.replace(/MM/g, 'Mm');
}

/***
 * Helper to print GraphQL AST node without location information
 */
function omitLoc(t) {
  const { loc, ...withoutLoc } = t;
  return withoutLoc;
}

function capitalize(str) {
  return str[0].toUpperCase() + str.slice(1);
}

/***
 * exhaustive type matcher
 * @param {never} no
 */
function exhaustive(no) {
  throw new TypeError('Unexpected value', JSON.stringify(no));
}

function once(fn) {
  let called = false;
  let result;
  return function(...args) {
    if (called) {
      return result;
    }
    result = fn(...args);
    called = true;
    return result;
  };
}
// const logOnce = once(console.log);


/***
 * Generate graphql string for field
 * @param {import('graphql').FieldDefinitionNode['type']} nodeType
 * @returns Boolean
 */
function isPrimitive(nodeType) {
  // TODO: only NamedType
  switch (nodeType) {
    case 'String':
    case 'Boolean':
    case 'Int':
    case 'Float':
      return true;
    default:
      return false;
  }
}
/***
 * Generate graphql string for field
 * @param {import('graphql').FieldDefinitionNode} node
 */
function resolveReturnType(node) {
  const responseType = node.type;
  switch (responseType.kind) {
    case Kind.NON_NULL_TYPE:
      return resolveReturnType(responseType);
    case Kind.LIST_TYPE:
      return resolveReturnType(responseType);
    case Kind.NAMED_TYPE:
      return grosslyHandleMMNames(responseType.name.value);

    default:
      exhaustive(responseType.kind);
  }
}


module.exports = {
  grosslyHandleMMNames,
  omitLoc,
  capitalize,
  exhaustive,
  once,

  isPrimitive,
  resolveReturnType,
};
