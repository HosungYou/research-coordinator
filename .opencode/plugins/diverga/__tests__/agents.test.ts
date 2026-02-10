/**
 * Unit Tests for agents.ts
 * Tests that all agents have prerequisites field and match checkpoint-enforcer.ts
 */

import { describe, it, expect } from 'vitest';
import { AGENT_REGISTRY, getAgent, listAgents, getAgentsByCategory, getAgentsByTier } from '../agents';
import { AGENT_PREREQUISITES } from '../hooks/checkpoint-enforcer';

describe('agents.ts', () => {
  describe('prerequisites field in AGENT_REGISTRY', () => {
    it('should have prerequisites field for all agents', () => {
      Object.values(AGENT_REGISTRY).forEach(agent => {
        expect(agent).toHaveProperty('prerequisites');
        expect(Array.isArray(agent.prerequisites)).toBe(true);
      });
    });

    it('should have valid checkpoint IDs in prerequisites', () => {
      const validCheckpoints = [
        'CP_RESEARCH_DIRECTION',
        'CP_PARADIGM_SELECTION',
        'CP_METHODOLOGY_APPROVAL',
      ];

      Object.values(AGENT_REGISTRY).forEach(agent => {
        agent.prerequisites?.forEach(prereq => {
          expect(validCheckpoints).toContain(prereq);
        });
      });
    });

    it('should match AGENT_PREREQUISITES mapping', () => {
      Object.entries(AGENT_REGISTRY).forEach(([id, agent]) => {
        expect(AGENT_PREREQUISITES).toHaveProperty(id);
        expect(agent.prerequisites).toEqual(AGENT_PREREQUISITES[id]);
      });
    });

    it('should have entry point agents with empty prerequisites', () => {
      const entryPoints = [
        { id: 'A1', name: 'Research Question Refiner' },
        { id: 'A4', name: 'Research Ethics Advisor' },
        { id: 'A5', name: 'Paradigm & Worldview Advisor' },
        { id: 'B3', name: 'Effect Size Extractor' },
        { id: 'B4', name: 'Research Radar' },
        { id: 'E4', name: 'Analysis Code Generator' },
        { id: 'G3', name: 'Peer Review Strategist' },
      ];

      entryPoints.forEach(({ id }) => {
        const agent = AGENT_REGISTRY[id];
        expect(agent.prerequisites).toEqual([]);
      });
    });

    it('should have A2 requiring CP_RESEARCH_DIRECTION', () => {
      const agent = AGENT_REGISTRY['A2'];
      expect(agent.prerequisites).toEqual(['CP_RESEARCH_DIRECTION']);
    });

    it('should have design consultants requiring paradigm selection', () => {
      const designConsultants = ['C1', 'C2', 'C3'];

      designConsultants.forEach(id => {
        const agent = AGENT_REGISTRY[id];
        expect(agent.prerequisites).toContain('CP_PARADIGM_SELECTION');
        expect(agent.prerequisites).toContain('CP_RESEARCH_DIRECTION');
      });
    });

    it('should have specialized agents with paradigm prerequisites', () => {
      expect(AGENT_REGISTRY['H1'].prerequisites).toEqual(['CP_PARADIGM_SELECTION']);
      expect(AGENT_REGISTRY['H2'].prerequisites).toEqual(['CP_PARADIGM_SELECTION']);
    });

    it('should have no duplicate prerequisites for any agent', () => {
      Object.values(AGENT_REGISTRY).forEach(agent => {
        const uniquePrereqs = new Set(agent.prerequisites);
        expect(uniquePrereqs.size).toBe(agent.prerequisites?.length || 0);
      });
    });

    it('should have specialized agents with appropriate prerequisites', () => {
      expect(AGENT_REGISTRY['H1'].prerequisites).toEqual(['CP_PARADIGM_SELECTION']);
      expect(AGENT_REGISTRY['H2'].prerequisites).toEqual(['CP_PARADIGM_SELECTION']);
    });

    it('should have meta-analysis agents with correct prerequisites', () => {
      expect(AGENT_REGISTRY['C5'].prerequisites).toEqual([
        'CP_RESEARCH_DIRECTION',
        'CP_METHODOLOGY_APPROVAL',
      ]);
    });

    it('should have analysis code generator with no prerequisites', () => {
      expect(AGENT_REGISTRY['E4'].prerequisites).toEqual([]);
    });
  });

  describe('Agent helper functions', () => {
    it('should return agent by ID with getAgent()', () => {
      const agent = getAgent('A1');
      expect(agent).toBeDefined();
      expect(agent?.id).toBe('A1');
      expect(agent?.prerequisites).toBeDefined();
    });

    it('should return agent with case-insensitive ID', () => {
      const agent = getAgent('a1');
      expect(agent).toBeDefined();
      expect(agent?.id).toBe('A1');
    });

    it('should return all agents with listAgents()', () => {
      const agents = listAgents();
      expect(agents.length).toBeGreaterThan(0);
      agents.forEach(agent => {
        expect(agent.prerequisites).toBeDefined();
      });
    });

    it('should return agents by category', () => {
      const categoryA = getAgentsByCategory('A - Research Foundation');
      expect(categoryA.length).toBeGreaterThan(0);
      categoryA.forEach(agent => {
        expect(agent.prerequisites).toBeDefined();
      });
    });

    it('should return agents by tier', () => {
      const highTier = getAgentsByTier('HIGH');
      expect(highTier.length).toBeGreaterThan(0);
      highTier.forEach(agent => {
        expect(agent.prerequisites).toBeDefined();
      });
    });
  });

  describe('Cross-file consistency', () => {
    it('should have all agents in AGENT_PREREQUISITES present in AGENT_REGISTRY', () => {
      Object.keys(AGENT_PREREQUISITES).forEach(agentId => {
        expect(AGENT_REGISTRY).toHaveProperty(agentId);
      });
    });

    it('should have all agents in AGENT_REGISTRY present in AGENT_PREREQUISITES', () => {
      Object.keys(AGENT_REGISTRY).forEach(agentId => {
        expect(AGENT_PREREQUISITES).toHaveProperty(agentId);
      });
    });

    it('should have matching prerequisite arrays', () => {
      Object.entries(AGENT_REGISTRY).forEach(([id, agent]) => {
        const enforcerPrereqs = AGENT_PREREQUISITES[id];
        expect(agent.prerequisites).toEqual(enforcerPrereqs);
      });
    });
  });

  describe('Agent categories', () => {
    it('should have Category H agents for specialized approaches', () => {
      const categoryH = ['H1', 'H2'];

      categoryH.forEach(id => {
        const agent = AGENT_REGISTRY[id];
        expect(agent).toBeDefined();
        expect(agent.prerequisites).toBeDefined();
        expect(agent.category).toContain('H -');
      });
    });

    it('should have Category G agents for publication', () => {
      const categoryG = ['G3'];

      categoryG.forEach(id => {
        const agent = AGENT_REGISTRY[id];
        expect(agent).toBeDefined();
        expect(agent.category).toContain('G -');
      });
    });
  });

  describe('Agent structure validation', () => {
    it('should have all required fields for each agent', () => {
      Object.values(AGENT_REGISTRY).forEach(agent => {
        expect(agent).toHaveProperty('id');
        expect(agent).toHaveProperty('name');
        expect(agent).toHaveProperty('icon');
        expect(agent).toHaveProperty('category');
        expect(agent).toHaveProperty('tier');
        expect(agent).toHaveProperty('claudeModel');
        expect(agent).toHaveProperty('vsLevel');
        expect(agent).toHaveProperty('description');
        expect(agent).toHaveProperty('triggers');
        expect(agent).toHaveProperty('checkpoints');
        expect(agent).toHaveProperty('prerequisites');
      });
    });

    it('should have valid model routing', () => {
      Object.values(AGENT_REGISTRY).forEach(agent => {
        expect(['opus', 'sonnet', 'haiku']).toContain(agent.claudeModel);
        expect(['Full', 'Enhanced', 'Light']).toContain(agent.vsLevel);
        expect(['HIGH', 'MEDIUM', 'LOW']).toContain(agent.tier);
      });
    });
  });
});
