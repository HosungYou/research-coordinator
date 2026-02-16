#!/usr/bin/env node

/**
 * diverga-server.js
 *
 * Unified MCP entry point for Diverga v9.0.
 * Wires 3 split servers (checkpoint, memory, comm) to @modelcontextprotocol/sdk.
 * Replaces the monolithic checkpoint-server.js from v8.x.
 *
 * 16 tools total:
 *   - 3 checkpoint tools (backward-compatible with v8)
 *   - 7 memory tools (project state, decisions, priority context)
 *   - 6 comm tools (agent messaging, broadcast)
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { readFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

import { createCheckpointServer } from './servers/checkpoint-server.js';
import { createMemoryServer } from './servers/memory-server.js';
import { createCommServer } from './servers/comm-server.js';
import { createSqliteServers } from './lib/sqlite-servers.js';
import { createToolRegistry } from './lib/tool-registry.js';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ---------------------------------------------------------------------------
// Resolve paths and config
// ---------------------------------------------------------------------------

const PREREQ_MAP = JSON.parse(
  readFileSync(join(__dirname, 'agent-prerequisite-map.json'), 'utf8')
);

const BACKEND = process.env.DIVERGA_BACKEND || 'yaml';
const researchDir = process.cwd();

// ---------------------------------------------------------------------------
// Initialize servers (YAML or SQLite backend)
// ---------------------------------------------------------------------------

let checkpointServer, memoryServer, commServer;

if (BACKEND === 'sqlite') {
  // SQLite backend — ACID-safe for parallel agent execution
  const dbPath = join(researchDir, '.research', 'diverga.db');
  if (!existsSync(join(researchDir, '.research'))) {
    mkdirSync(join(researchDir, '.research'), { recursive: true });
  }
  const isNewDb = !existsSync(dbPath);
  const servers = createSqliteServers(dbPath, PREREQ_MAP);
  checkpointServer = servers.checkpointServer;
  memoryServer = servers.memoryServer;
  commServer = servers.commServer;

  // Auto-migrate from YAML/JSON on first run
  if (isNewDb) {
    const result = servers.migrateFromYaml(researchDir);
    if (result.migrated > 0) {
      process.stderr.write(
        `[diverga] Migrated ${result.migrated} items from YAML/JSON to SQLite\n`
      );
    }
  }

  // Graceful shutdown
  process.on('SIGINT', () => { servers.close(); process.exit(0); });
  process.on('SIGTERM', () => { servers.close(); process.exit(0); });
} else {
  // YAML/JSON backend — default, backward-compatible with v8.x
  const researchPath = join(researchDir, 'research');
  const systemPath = join(researchDir, '.research');
  if (!existsSync(researchPath)) mkdirSync(researchPath, { recursive: true });
  if (!existsSync(systemPath)) mkdirSync(systemPath, { recursive: true });

  checkpointServer = createCheckpointServer(PREREQ_MAP, researchDir);
  memoryServer = createMemoryServer(researchDir);
  commServer = createCommServer(researchDir);
}

// ---------------------------------------------------------------------------
// Create tool registry
// ---------------------------------------------------------------------------

const { tools, dispatch } = createToolRegistry(checkpointServer, memoryServer, commServer);

// ---------------------------------------------------------------------------
// MCP Server
// ---------------------------------------------------------------------------

const server = new Server(
  { name: 'diverga', version: '9.0.0' },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools,
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;
  try {
    const result = await dispatch(name, args || {});
    return {
      content: [{ type: 'text', text: JSON.stringify(result, null, 2) }],
    };
  } catch (error) {
    return {
      content: [{ type: 'text', text: `Error: ${error.message}` }],
      isError: true,
    };
  }
});

// ---------------------------------------------------------------------------
// Start
// ---------------------------------------------------------------------------

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main().catch(console.error);
