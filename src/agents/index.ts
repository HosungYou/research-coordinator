/**
 * Diverga Agent Runtime - Agents Module
 *
 * Main export for the agents module.
 * Re-exports all agent-related types, utilities, and definitions.
 */

// Type exports
export type {
  ModelType,
  VSLevel,
  TierLevel,
  CategoryId,
  CategoryInfo,
  CheckpointConfig,
  VSConfig,
  AgentConfig,
  AgentMetadata,
  SkillFrontmatter,
  ParsedSkillFile,
  AgentIdMapping,
  AgentRegistry,
} from './types.js';

export {
  CATEGORIES,
  MODEL_TIERS,
  CATEGORY_TOOLS,
} from './types.js';

// Prompt loader exports
export {
  getPackageDir,
  getSkillsDir,
  parseYamlFrontmatter,
  extractMarkdownContent,
  parseSkillFile,
  loadAgentPrompt,
  loadAgentMetadata,
  scanAgentDirectories,
  VS_INJECTION,
  CHECKPOINT_INJECTION,
  buildEnhancedPrompt,
} from './prompt-loader.js';

// Agent definitions exports
export {
  AGENT_MAPPINGS,
  getAgentDefinitions,
  getAgent,
  getAgentIds,
  getAgentMappings,
  findAgentByTrigger,
  getAgentsByCategory,
  getAgentsByTier,
} from './definitions.js';
