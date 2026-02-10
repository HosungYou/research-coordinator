/**
 * Checkpoint Enforcer Hook
 * Ensures human checkpoints are respected in research workflow
 */

import type { PluginContext, HookResult, ToolParams, CheckpointPrompt } from '../types';
import { CHECKPOINTS } from '../checkpoints';
import { loadContext } from './context-manager';

/**
 * Map of tool actions to checkpoints they should trigger
 */
const CHECKPOINT_TRIGGERS: Record<string, string[]> = {
  // Research direction decisions
  'research_question': ['CP_RESEARCH_DIRECTION', 'CP_VS_001'],
  'refine_question': ['CP_RESEARCH_DIRECTION', 'CP_VS_001'],

  // Paradigm selection
  'select_paradigm': ['CP_PARADIGM_SELECTION'],
  'methodology_selection': ['CP_PARADIGM_SELECTION'],

  // Theory selection
  'select_theory': ['CP_THEORY_SELECTION', 'CP_VS_001'],
  'framework_design': ['CP_THEORY_SELECTION', 'CP_VS_001'],

  // Methodology approval
  'design_methodology': ['CP_METHODOLOGY_APPROVAL'],
  'approve_design': ['CP_METHODOLOGY_APPROVAL'],

  // Analysis
  'start_analysis': ['CP_ANALYSIS_PLAN'],
  'analyze': ['CP_ANALYSIS_PLAN'],

  // Quality review
  'quality_assessment': ['CP_QUALITY_REVIEW'],
  'assess_quality': ['CP_QUALITY_REVIEW'],

  // VS methodology
  'vs_selection': ['CP_VS_001', 'CP_VS_003'],
  'select_direction': ['CP_VS_001', 'CP_VS_003'],
};

/**
 * Check if checkpoint is already completed
 */
function isCheckpointCompleted(checkpointId: string, context: PluginContext): boolean {
  const researchContext = loadContext();
  if (!researchContext) return false;
  return researchContext.completedCheckpoints.includes(checkpointId);
}

/**
 * Get checkpoint definition
 */
function getCheckpointDefinition(checkpointId: string) {
  return CHECKPOINTS.find(cp => cp.id === checkpointId);
}

/**
 * Create checkpoint prompt for user
 */
function createCheckpointPrompt(checkpointId: string): CheckpointPrompt | null {
  const checkpoint = getCheckpointDefinition(checkpointId);
  if (!checkpoint) return null;

  return {
    id: checkpoint.id,
    level: checkpoint.level,
    message: `
${checkpoint.icon} **${checkpoint.name}** (${checkpoint.level})

${checkpoint.whatToAsk}

_When: ${checkpoint.when}_
`,
    options: [
      { id: 'approve', label: 'Approve / 승인', description: 'Proceed with current direction' },
      { id: 'modify', label: 'Modify / 수정', description: 'Request changes before proceeding' },
      { id: 'cancel', label: 'Cancel / 취소', description: 'Stop and reconsider' },
    ],
  };
}

/**
 * Main checkpoint enforcer hook
 */
export async function checkpointEnforcer(
  params: ToolParams,
  context: PluginContext
): Promise<HookResult> {
  // Get tool action
  const action = params.arguments?.action as string;
  const toolName = params.tool;

  // Check if this action triggers any checkpoints
  const triggerKey = action || toolName;
  const checkpointIds = CHECKPOINT_TRIGGERS[triggerKey] || [];

  if (checkpointIds.length === 0) {
    // No checkpoint required
    return { proceed: true };
  }

  // Check each checkpoint
  for (const checkpointId of checkpointIds) {
    const checkpoint = getCheckpointDefinition(checkpointId);
    if (!checkpoint) continue;

    // Skip if already completed
    if (isCheckpointCompleted(checkpointId, context)) {
      continue;
    }

    // For REQUIRED checkpoints, always stop
    if (checkpoint.level === 'REQUIRED') {
      const prompt = createCheckpointPrompt(checkpointId);
      return {
        proceed: false,
        message: `🔴 CHECKPOINT HALT: ${checkpoint.name}`,
        checkpoint: prompt || undefined,
      };
    }

    // For RECOMMENDED checkpoints, pause and suggest
    if (checkpoint.level === 'RECOMMENDED') {
      const prompt = createCheckpointPrompt(checkpointId);
      return {
        proceed: false,
        message: `🟠 CHECKPOINT PAUSE: ${checkpoint.name} (recommended)`,
        checkpoint: prompt || undefined,
      };
    }

    // For OPTIONAL checkpoints, just note it
    // (but still continue)
  }

  return { proceed: true };
}

/**
 * Mark checkpoint as completed
 */
export function completeCheckpoint(
  checkpointId: string,
  selectedOption: string,
  context: PluginContext
): void {
  const researchContext = loadContext();
  if (!researchContext) return;

  // Add to completed
  if (!researchContext.completedCheckpoints.includes(checkpointId)) {
    researchContext.completedCheckpoints.push(checkpointId);
  }

  // Remove from pending
  researchContext.pendingCheckpoints = researchContext.pendingCheckpoints.filter(
    cp => cp !== checkpointId
  );

  // Record decision
  researchContext.decisions.push({
    checkpoint: checkpointId,
    timestamp: new Date().toISOString(),
    optionsPresented: ['approve', 'modify', 'cancel'],
    selected: selectedOption,
  });

  // Save context
  // (Context manager will handle persistence)
}

/**
 * Get pending checkpoints for current stage
 */
export function getPendingCheckpoints(context: PluginContext): string[] {
  const researchContext = loadContext();
  if (!researchContext) return [];
  return researchContext.pendingCheckpoints;
}

/**
 * Reset checkpoint (for testing/debugging)
 */
export function resetCheckpoint(checkpointId: string, context: PluginContext): void {
  const researchContext = loadContext();
  if (!researchContext) return;

  researchContext.completedCheckpoints = researchContext.completedCheckpoints.filter(
    cp => cp !== checkpointId
  );
}

/**
 * Agent prerequisites mapping
 * Maps agent IDs to checkpoint IDs that must be completed before the agent can start
 */
export const AGENT_PREREQUISITES: Record<string, string[]> = {
  'A1': [],
  'A2': ['CP_RESEARCH_DIRECTION'],
  'A3': ['CP_RESEARCH_DIRECTION'],
  'A4': [],
  'A5': [],
  'A6': ['CP_RESEARCH_DIRECTION'],
  'B1': ['CP_RESEARCH_DIRECTION'],
  'B2': ['CP_RESEARCH_DIRECTION'],
  'B3': [],
  'B4': [],
  'B5': [],
  'C1': ['CP_PARADIGM_SELECTION', 'CP_RESEARCH_DIRECTION'],
  'C2': ['CP_PARADIGM_SELECTION', 'CP_RESEARCH_DIRECTION'],
  'C3': ['CP_PARADIGM_SELECTION', 'CP_RESEARCH_DIRECTION'],
  'C5': ['CP_RESEARCH_DIRECTION', 'CP_METHODOLOGY_APPROVAL'],
  'C6': ['CP_METHODOLOGY_APPROVAL'],
  'C7': ['CP_METHODOLOGY_APPROVAL'],
  'D1': ['CP_METHODOLOGY_APPROVAL'],
  'D2': ['CP_METHODOLOGY_APPROVAL'],
  'D4': ['CP_METHODOLOGY_APPROVAL'],
  'E1': ['CP_METHODOLOGY_APPROVAL'],
  'E2': ['CP_METHODOLOGY_APPROVAL'],
  'E3': ['CP_METHODOLOGY_APPROVAL'],
  'E5': ['CP_METHODOLOGY_APPROVAL'],
  'G3': [],
  'G5': [],
  'G6': ['CP_HUMANIZATION_REVIEW'],
  'H1': ['CP_PARADIGM_SELECTION'],
  'H2': ['CP_PARADIGM_SELECTION'],
  'I0': [],
  'I1': [],
  'I2': ['SCH_DATABASE_SELECTION'],
  'I3': ['SCH_SCREENING_CRITERIA'],
};

/**
 * Checkpoint dependency order for sorting prerequisites
 */
const CHECKPOINT_DEPENDENCY_ORDER: string[][] = [
  // Level 0 (entry points)
  ['CP_RESEARCH_DIRECTION', 'CP_PARADIGM_SELECTION'],
  // Level 1
  ['CP_THEORY_SELECTION', 'CP_METHODOLOGY_APPROVAL'],
  // Level 2
  ['CP_ANALYSIS_PLAN', 'CP_SCREENING_CRITERIA', 'CP_SAMPLING_STRATEGY', 'CP_CODING_APPROACH', 'CP_THEME_VALIDATION', 'CP_INTEGRATION_STRATEGY', 'CP_QUALITY_REVIEW'],
  // Level 3
  ['SCH_DATABASE_SELECTION', 'CP_HUMANIZATION_REVIEW', 'CP_VS_001', 'CP_VS_002', 'CP_VS_003'],
  // Level 4
  ['SCH_SCREENING_CRITERIA', 'CP_HUMANIZATION_VERIFY'],
  // Level 5
  ['SCH_RAG_READINESS'],
];

/**
 * Get dependency level for a checkpoint
 */
function getCheckpointLevel(checkpointId: string): number {
  for (let level = 0; level < CHECKPOINT_DEPENDENCY_ORDER.length; level++) {
    if (CHECKPOINT_DEPENDENCY_ORDER[level].includes(checkpointId)) {
      return level;
    }
  }
  return 999; // Unknown checkpoint, sort last
}

/**
 * Sort checkpoints by dependency order
 */
function sortByDependencyOrder(checkpointIds: string[]): string[] {
  return [...checkpointIds].sort((a, b) => getCheckpointLevel(a) - getCheckpointLevel(b));
}

/**
 * Collect union of prerequisites for multiple agents
 * Used when multiple agents are triggered simultaneously
 */
export function collectPrerequisites(agentIds: string[]): string[] {
  const union = new Set<string>();
  for (const id of agentIds) {
    const prereqs = AGENT_PREREQUISITES[id] || [];
    for (const prereq of prereqs) {
      union.add(prereq);
    }
  }
  return sortByDependencyOrder([...union]);
}
