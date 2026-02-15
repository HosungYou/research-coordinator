/**
 * utils.js
 *
 * Shared utilities for Diverga v9.0 MCP infrastructure.
 */

/**
 * Deep merge two objects. Arrays and primitives in source overwrite target.
 * Nested plain objects are recursively merged.
 */
export function deepMerge(target, source) {
  const result = { ...target };
  for (const key of Object.keys(source)) {
    if (
      source[key] !== null &&
      typeof source[key] === 'object' &&
      !Array.isArray(source[key]) &&
      target[key] !== null &&
      typeof target[key] === 'object' &&
      !Array.isArray(target[key])
    ) {
      result[key] = deepMerge(target[key], source[key]);
    } else {
      result[key] = source[key];
    }
  }
  return result;
}
