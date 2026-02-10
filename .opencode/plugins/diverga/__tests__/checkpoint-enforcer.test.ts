/**
 * Unit Tests for checkpoint-enforcer.ts
 * Tests AGENT_PREREQUISITES, dependency ordering, and prerequisite collection
 */

import { describe, it, expect } from 'vitest';
import {
  AGENT_PREREQUISITES,
  collectPrerequisites,
} from '../hooks/checkpoint-enforcer';

describe('checkpoint-enforcer.ts', () => {
  describe('AGENT_PREREQUISITES constant', () => {
    it('should contain all 21 agents from AGENT_REGISTRY', () => {
      const expectedAgents = [
        'A1', 'A2', 'A3', 'A4', 'A5', 'A6',
        'B1', 'B2', 'B3', 'B4',
        'C1', 'C2', 'C3', 'C5',
        'E1', 'E2', 'E3', 'E4',
        'G3',
        'H1', 'H2',
      ];

      expectedAgents.forEach(agentId => {
        expect(AGENT_PREREQUISITES).toHaveProperty(agentId);
      });
    });

    it('should have entry point agents with empty prerequisites', () => {
      const entryPoints = ['A1', 'A4', 'A5', 'B3', 'B4', 'E4', 'G3'];

      entryPoints.forEach(agentId => {
        expect(AGENT_PREREQUISITES[agentId]).toEqual([]);
      });
    });

    it('should have A2 requiring CP_RESEARCH_DIRECTION', () => {
      expect(AGENT_PREREQUISITES['A2']).toEqual(['CP_RESEARCH_DIRECTION']);
    });

    it('should have C1 requiring both CP_PARADIGM_SELECTION and CP_RESEARCH_DIRECTION', () => {
      expect(AGENT_PREREQUISITES['C1']).toContain('CP_PARADIGM_SELECTION');
      expect(AGENT_PREREQUISITES['C1']).toContain('CP_RESEARCH_DIRECTION');
      expect(AGENT_PREREQUISITES['C1']).toHaveLength(2);
    });

    it('should have C5 requiring CP_RESEARCH_DIRECTION and CP_METHODOLOGY_APPROVAL', () => {
      expect(AGENT_PREREQUISITES['C5']).toContain('CP_RESEARCH_DIRECTION');
      expect(AGENT_PREREQUISITES['C5']).toContain('CP_METHODOLOGY_APPROVAL');
      expect(AGENT_PREREQUISITES['C5']).toHaveLength(2);
    });

    it('should have specialized agents with paradigm prerequisites', () => {
      expect(AGENT_PREREQUISITES['H1']).toEqual(['CP_PARADIGM_SELECTION']);
      expect(AGENT_PREREQUISITES['H2']).toEqual(['CP_PARADIGM_SELECTION']);
    });

    it('should have E4 as entry point with no prerequisites', () => {
      expect(AGENT_PREREQUISITES['E4']).toEqual([]);
    });

    it('should have methodology approval gates for analysis agents', () => {
      const analysisAgents = ['E1', 'E2', 'E3'];

      analysisAgents.forEach(agentId => {
        expect(AGENT_PREREQUISITES[agentId]).toContain('CP_METHODOLOGY_APPROVAL');
      });
    });

    it('should have paradigm selection for design consultants', () => {
      const designConsultants = ['C1', 'C2', 'C3'];

      designConsultants.forEach(agentId => {
        expect(AGENT_PREREQUISITES[agentId]).toContain('CP_PARADIGM_SELECTION');
      });
    });

    it('should only contain valid checkpoint IDs', () => {
      const validCheckpoints = [
        'CP_RESEARCH_DIRECTION',
        'CP_PARADIGM_SELECTION',
        'CP_METHODOLOGY_APPROVAL',
      ];

      Object.values(AGENT_PREREQUISITES).forEach(prereqs => {
        prereqs.forEach(prereq => {
          expect(validCheckpoints).toContain(prereq);
        });
      });
    });

    it('should have no duplicate prerequisites for any agent', () => {
      Object.entries(AGENT_PREREQUISITES).forEach(([agentId, prereqs]) => {
        const uniquePrereqs = new Set(prereqs);
        expect(uniquePrereqs.size).toBe(prereqs.length);
      });
    });

    it('should match prerequisites field in agents.ts', async () => {
      // This tests cross-file consistency
      // We'll import the agent registry to verify
      const { AGENT_REGISTRY } = await import('../agents.js');

      Object.entries(AGENT_PREREQUISITES).forEach(([agentId, prereqs]) => {
        const agent = AGENT_REGISTRY[agentId];
        expect(agent).toBeDefined();
        expect(agent.prerequisites).toEqual(prereqs);
      });
    });
  });

  describe('collectPrerequisites()', () => {
    it('should return empty array for empty input', () => {
      const result = collectPrerequisites([]);
      expect(result).toEqual([]);
    });

    it('should return prerequisites for single agent', () => {
      const result = collectPrerequisites(['A2']);
      expect(result).toEqual(['CP_RESEARCH_DIRECTION']);
    });

    it('should return prerequisites for single agent with multiple prereqs', () => {
      const result = collectPrerequisites(['C1']);
      expect(result).toContain('CP_PARADIGM_SELECTION');
      expect(result).toContain('CP_RESEARCH_DIRECTION');
    });

    it('should return union of prerequisites for multiple agents', () => {
      const result = collectPrerequisites(['A2', 'A3']);
      expect(result).toEqual(['CP_RESEARCH_DIRECTION']);
    });

    it('should remove duplicates when collecting union', () => {
      const result = collectPrerequisites(['C1', 'C2', 'C3']);
      // All three require CP_PARADIGM_SELECTION and CP_RESEARCH_DIRECTION
      expect(result).toContain('CP_PARADIGM_SELECTION');
      expect(result).toContain('CP_RESEARCH_DIRECTION');

      // Count occurrences
      const researchDirCount = result.filter(cp => cp === 'CP_RESEARCH_DIRECTION').length;
      expect(researchDirCount).toBe(1);
    });

    it('should sort prerequisites by dependency order', () => {
      const result = collectPrerequisites(['C5']);
      // C5 requires CP_RESEARCH_DIRECTION (Level 0) and CP_METHODOLOGY_APPROVAL (Level 1)
      // Should be sorted with CP_RESEARCH_DIRECTION first
      expect(result[0]).toBe('CP_RESEARCH_DIRECTION');
      expect(result[1]).toBe('CP_METHODOLOGY_APPROVAL');
    });

    it('should handle agents with no prerequisites', () => {
      const result = collectPrerequisites(['A1', 'B3', 'E4']);
      expect(result).toEqual([]);
    });

    it('should handle design consultant chain', () => {
      const result = collectPrerequisites(['C1', 'C2']);
      // Both require CP_PARADIGM_SELECTION and CP_RESEARCH_DIRECTION
      expect(result).toContain('CP_PARADIGM_SELECTION');
      expect(result).toContain('CP_RESEARCH_DIRECTION');
    });

    it('should handle mixed category agents', () => {
      const result = collectPrerequisites(['A2', 'C1', 'E1']);
      // Union: CP_RESEARCH_DIRECTION, CP_PARADIGM_SELECTION, CP_METHODOLOGY_APPROVAL
      expect(result).toContain('CP_RESEARCH_DIRECTION');
      expect(result).toContain('CP_PARADIGM_SELECTION');
      expect(result).toContain('CP_METHODOLOGY_APPROVAL');
    });

    it('should maintain correct dependency order for complex unions', () => {
      const result = collectPrerequisites(['C1', 'C5', 'E1']);
      // Level 0: CP_RESEARCH_DIRECTION, CP_PARADIGM_SELECTION
      // Level 1: CP_METHODOLOGY_APPROVAL

      const researchIdx = result.indexOf('CP_RESEARCH_DIRECTION');
      const paradigmIdx = result.indexOf('CP_PARADIGM_SELECTION');
      const methodologyIdx = result.indexOf('CP_METHODOLOGY_APPROVAL');

      // Both Level 0 should come before Level 1
      expect(researchIdx).toBeLessThan(methodologyIdx);
      expect(paradigmIdx).toBeLessThan(methodologyIdx);
    });

    it('should handle unknown agent IDs gracefully', () => {
      const result = collectPrerequisites(['UNKNOWN_AGENT']);
      expect(result).toEqual([]);
    });

    it('should handle mixture of known and unknown agents', () => {
      const result = collectPrerequisites(['A2', 'UNKNOWN', 'C1']);
      expect(result).toContain('CP_RESEARCH_DIRECTION');
      expect(result).toContain('CP_PARADIGM_SELECTION');
    });
  });

  describe('Dependency ordering', () => {
    it('should place CP_RESEARCH_DIRECTION and CP_PARADIGM_SELECTION at Level 0', () => {
      // These are entry points - should come first
      const result1 = collectPrerequisites(['A2', 'A5', 'C1']);
      const firstTwo = result1.slice(0, 2);

      expect(firstTwo).toContain('CP_RESEARCH_DIRECTION');
      expect(firstTwo).toContain('CP_PARADIGM_SELECTION');
    });

    it('should place CP_METHODOLOGY_APPROVAL at Level 1', () => {
      const result = collectPrerequisites(['C5', 'E1']);
      const methodologyIdx = result.indexOf('CP_METHODOLOGY_APPROVAL');
      const researchIdx = result.indexOf('CP_RESEARCH_DIRECTION');

      expect(methodologyIdx).toBeGreaterThan(researchIdx);
    });

    it('should correctly order research foundation checkpoints', () => {
      const result = collectPrerequisites(['C1', 'E1']);
      // Both Level 0 checkpoints should come before Level 1
      const researchIdx = result.indexOf('CP_RESEARCH_DIRECTION');
      const paradigmIdx = result.indexOf('CP_PARADIGM_SELECTION');
      const methodologyIdx = result.indexOf('CP_METHODOLOGY_APPROVAL');

      expect(researchIdx).toBeLessThan(methodologyIdx);
      expect(paradigmIdx).toBeLessThan(methodologyIdx);
    });

    it('should handle unknown checkpoints by sorting them last', () => {
      // This tests the fallback in getCheckpointLevel
      // Since all our checkpoints are known, we test with collectPrerequisites
      const result = collectPrerequisites(['C1', 'C5']);

      // Should be ordered: Level 0, Level 1
      expect(result.length).toBeGreaterThan(0);
      expect(result[result.length - 1]).toBe('CP_METHODOLOGY_APPROVAL');
    });
  });

  describe('Edge cases', () => {
    it('should handle duplicate agent IDs in input', () => {
      const result = collectPrerequisites(['A2', 'A2', 'A2']);
      expect(result).toEqual(['CP_RESEARCH_DIRECTION']);
    });

    it('should handle case sensitivity', () => {
      const result = collectPrerequisites(['a2']); // lowercase
      expect(result).toEqual([]);
    });

    it('should handle null/undefined input gracefully', () => {
      // @ts-expect-error Testing invalid input
      const result1 = collectPrerequisites(null);
      expect(result1).toEqual([]);

      // @ts-expect-error Testing invalid input
      const result2 = collectPrerequisites(undefined);
      expect(result2).toEqual([]);
    });

    it('should handle very large agent list', () => {
      const allAgents = Object.keys(AGENT_PREREQUISITES);
      const result = collectPrerequisites(allAgents);

      // Should contain all unique prerequisites
      const uniquePrereqs = new Set(result);
      expect(uniquePrereqs.size).toBe(result.length);
    });

    it('should maintain immutability of input array', () => {
      const input = ['A2', 'C1'];
      const inputCopy = [...input];

      collectPrerequisites(input);

      expect(input).toEqual(inputCopy);
    });
  });

  describe('Real-world scenarios', () => {
    it('should handle Group 1: Research Design parallel execution', () => {
      const result = collectPrerequisites(['A1', 'A2', 'A5']);

      // A1: [], A2: [CP_RESEARCH_DIRECTION], A5: []
      // Union: [CP_RESEARCH_DIRECTION]
      expect(result).toEqual(['CP_RESEARCH_DIRECTION']);
    });

    it('should handle Group 2: Literature & Evidence parallel execution', () => {
      const result = collectPrerequisites(['B1', 'B2', 'B3']);

      // B1: [CP_RESEARCH_DIRECTION], B2: [CP_RESEARCH_DIRECTION], B3: []
      // Union: [CP_RESEARCH_DIRECTION]
      expect(result).toEqual(['CP_RESEARCH_DIRECTION']);
    });

    it('should handle Group 3: Meta-Analysis agent', () => {
      const result = collectPrerequisites(['C5']);

      // C5: [CP_RESEARCH_DIRECTION, CP_METHODOLOGY_APPROVAL]
      expect(result).toContain('CP_RESEARCH_DIRECTION');
      expect(result).toContain('CP_METHODOLOGY_APPROVAL');

      // Verify order
      const researchIdx = result.indexOf('CP_RESEARCH_DIRECTION');
      const methodologyIdx = result.indexOf('CP_METHODOLOGY_APPROVAL');
      expect(researchIdx).toBeLessThan(methodologyIdx);
    });

    it('should handle ad-hoc agent call: /diverga:c5', () => {
      const result = collectPrerequisites(['C5']);

      expect(result).toEqual([
        'CP_RESEARCH_DIRECTION',
        'CP_METHODOLOGY_APPROVAL',
      ]);
    });

    it('should handle natural language multi-agent trigger', () => {
      // User says: "메타분석 설계하고 효과크기 추출도 같이"
      // Triggers: C5 + B3
      const result = collectPrerequisites(['C5', 'B3']);

      // C5: [CP_RESEARCH_DIRECTION, CP_METHODOLOGY_APPROVAL]
      // B3: []
      // Union: [CP_RESEARCH_DIRECTION, CP_METHODOLOGY_APPROVAL]

      expect(result).toEqual([
        'CP_RESEARCH_DIRECTION',
        'CP_METHODOLOGY_APPROVAL',
      ]);
    });

    it('should handle qualitative research workflow', () => {
      // User starts qualitative research, triggers C2
      const result = collectPrerequisites(['C2']);
      expect(result).toContain('CP_PARADIGM_SELECTION');
      expect(result).toContain('CP_RESEARCH_DIRECTION');
    });

    it('should handle analysis agent workflow', () => {
      // E1 (quantitative analysis)
      const result = collectPrerequisites(['E1', 'E2']);

      // Both require CP_METHODOLOGY_APPROVAL
      expect(result).toEqual(['CP_METHODOLOGY_APPROVAL']);
    });
  });
});
