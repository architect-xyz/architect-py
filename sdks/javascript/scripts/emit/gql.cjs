const { Kind } = require('graphql');
const {
  resolveArgs,
  isPrimitive,
  capitalize,
  exhaustive,
  grosslyHandleMMNames,
} = require('./shared.cjs');

/***
 * Generate graphql string for field
 * @param {import('graphql').FieldDefinitionNode} node
 */
function resolveReturnValue(node) {
  const responseType = node.type;
  switch (responseType.kind) {
    case Kind.NON_NULL_TYPE:
      return resolveReturnValue(responseType);
    case Kind.LIST_TYPE:
      return resolveReturnValue(responseType);
    case Kind.NAMED_TYPE:
      if (isPrimitive(responseType.name.value)) {
        return '';
      } else {
        // TODO: use fragment for fields
        return "{ __typename ${fields.join(' ')} }";
      }

    default:
      exhaustive(responseType.kind);
  }
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
      return `${kind(t.type)}!`;
    }
    case Kind.LIST_TYPE: {
      // console.log(t, omitLoc(t));
      return `[${kind(t.type)}]`;
    }
    case Kind.NAMED_TYPE:
      return t.name.value;
    default:
      throw new TypeError(`Unexpected kind type k`);
  }
}

/***
 * Generate graphql string for field
 * @param {import('graphql').FieldDefinitionNode} node
 */
function template(node) {
  const args = resolveArgs(node);
  const params = args
    ? `(${args.map((n) => `\$${n.name.value}: ${kind(n.type)}`).join(', ')})`
    : '';
  const queryParams = args
    ? `(${args.map((n) => `${n.name.value}: \$${n.name.value}`).join(', ')})`
    : '';
  const fields = resolveReturnValue(node);

  return `${capitalize(node.name.value)}${params} {
        ${node.name.value}${queryParams}${fields ? ' ' + fields : ''}
      }`;
}

module.exports = {
  template,
};
