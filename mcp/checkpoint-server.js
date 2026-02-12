#!/usr/bin/env node

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { readFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createCheckpointLogic } from './lib/checkpoint-logic.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const PREREQ_MAP = JSON.parse(readFileSync(join(__dirname, 'agent-prerequisite-map.json'), 'utf8'));

// Resolve .research/ path relative to cwd (project root)
function getResearchDir() {
  const dir = join(process.cwd(), '.research');
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  return dir;
}

const logic = createCheckpointLogic(PREREQ_MAP, getResearchDir());
const {
  checkPrerequisites,
  markCheckpoint,
  checkpointStatus,
  priorityRead,
  priorityWrite,
  projectStatus,
  decisionAdd,
} = logic;

// --- MCP Server Setup ---

const server = new Server(
  { name: 'diverga-checkpoint', version: '1.0.0' },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: 'diverga_check_prerequisites',
      description: 'Check if all prerequisites are met for an agent before execution. Returns approval status and missing checkpoints.',
      inputSchema: {
        type: 'object',
        properties: {
          agent_id: { type: 'string', description: 'Agent ID (e.g., "c5", "a1", "i2")' }
        },
        required: ['agent_id']
      }
    },
    {
      name: 'diverga_mark_checkpoint',
      description: 'Record that a checkpoint has been passed with the human decision and rationale.',
      inputSchema: {
        type: 'object',
        properties: {
          checkpoint_id: { type: 'string', description: 'Checkpoint ID (e.g., "CP_RESEARCH_DIRECTION")' },
          decision: { type: 'string', description: 'The decision made by the researcher' },
          rationale: { type: 'string', description: 'Rationale for the decision' }
        },
        required: ['checkpoint_id', 'decision', 'rationale']
      }
    },
    {
      name: 'diverga_checkpoint_status',
      description: 'Get the status of all checkpoints: which are passed, pending, and which agents are blocked.',
      inputSchema: { type: 'object', properties: {} }
    },
    {
      name: 'diverga_priority_read',
      description: 'Read the priority context summary (max 500 chars). Used for context recovery after compression.',
      inputSchema: { type: 'object', properties: {} }
    },
    {
      name: 'diverga_priority_write',
      description: 'Write/update the priority context summary (max 500 chars).',
      inputSchema: {
        type: 'object',
        properties: {
          context: { type: 'string', description: 'Priority context text (max 500 chars)' }
        },
        required: ['context']
      }
    },
    {
      name: 'diverga_project_status',
      description: 'Get full project status including research state, checkpoints, and recent decisions.',
      inputSchema: { type: 'object', properties: {} }
    },
    {
      name: 'diverga_decision_add',
      description: 'Record a research decision with checkpoint reference, selection, and rationale.',
      inputSchema: {
        type: 'object',
        properties: {
          checkpoint_id: { type: 'string', description: 'Related checkpoint ID' },
          selected: { type: 'string', description: 'The selected option' },
          rationale: { type: 'string', description: 'Why this was chosen' },
          alternatives_considered: {
            type: 'array',
            items: { type: 'string' },
            description: 'Other options that were considered'
          }
        },
        required: ['checkpoint_id', 'selected', 'rationale']
      }
    }
  ]
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  try {
    let result;
    switch (name) {
      case 'diverga_check_prerequisites':
        result = checkPrerequisites(args.agent_id);
        break;
      case 'diverga_mark_checkpoint':
        result = markCheckpoint(args.checkpoint_id, args.decision, args.rationale);
        break;
      case 'diverga_checkpoint_status':
        result = checkpointStatus();
        break;
      case 'diverga_priority_read':
        result = priorityRead();
        break;
      case 'diverga_priority_write':
        result = priorityWrite(args.context);
        break;
      case 'diverga_project_status':
        result = projectStatus();
        break;
      case 'diverga_decision_add':
        result = decisionAdd(args.checkpoint_id, args.selected, args.rationale, args.alternatives_considered);
        break;
      default:
        return { content: [{ type: 'text', text: `Unknown tool: ${name}` }], isError: true };
    }
    return { content: [{ type: 'text', text: JSON.stringify(result, null, 2) }] };
  } catch (error) {
    return { content: [{ type: 'text', text: `Error: ${error.message}` }], isError: true };
  }
});

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
