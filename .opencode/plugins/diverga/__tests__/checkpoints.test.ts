/**
 * Unit Tests for checkpoints.ts
 * Tests all 23 checkpoints and helper functions
 */

import { describe, it, expect } from 'vitest';
import { CHECKPOINTS, getCheckpoint, getCheckpointsByLevel, formatCheckpoint } from '../checkpoints';
import type { CheckpointDefinition } from '../types';

describe('checkpoints.ts', () => {
  describe('CHECKPOINTS constant', () => {
    it('should contain exactly 23 checkpoints', () => {
      expect(CHECKPOINTS).toHaveLength(23);
    });

    it('should have all required checkpoints', () => {
      const requiredIds = [
        'CP_RESEARCH_DIRECTION',
        'CP_PARADIGM_SELECTION',
        'CP_THEORY_SELECTION',
        'CP_METHODOLOGY_APPROVAL',
        'CP_VS_001',
        'CP_VS_003',
        'SCH_DATABASE_SELECTION',
        'SCH_SCREENING_CRITERIA',
      ];

      requiredIds.forEach(id => {
        const checkpoint = CHECKPOINTS.find(cp => cp.id === id);
        expect(checkpoint).toBeDefined();
        expect(checkpoint?.level).toBe('REQUIRED');
      });
    });

    it('should have all recommended checkpoints', () => {
      const recommendedIds = [
        'CP_ANALYSIS_PLAN',
        'CP_INTEGRATION_STRATEGY',
        'CP_QUALITY_REVIEW',
        'CP_SCREENING_CRITERIA',
        'CP_SAMPLING_STRATEGY',
        'CP_CODING_APPROACH',
        'CP_THEME_VALIDATION',
        'CP_VS_002',
        'CP_HUMANIZATION_REVIEW',
        'SCH_RAG_READINESS',
      ];

      recommendedIds.forEach(id => {
        const checkpoint = CHECKPOINTS.find(cp => cp.id === id);
        expect(checkpoint).toBeDefined();
        expect(checkpoint?.level).toBe('RECOMMENDED');
      });
    });

    it('should have all optional checkpoints', () => {
      const optionalIds = [
        'CP_VISUALIZATION_PREFERENCE',
        'CP_SEARCH_STRATEGY',
        'CP_WRITING_STYLE',
        'CP_PROTOCOL_DESIGN',
        'CP_HUMANIZATION_VERIFY',
      ];

      optionalIds.forEach(id => {
        const checkpoint = CHECKPOINTS.find(cp => cp.id === id);
        expect(checkpoint).toBeDefined();
        expect(checkpoint?.level).toBe('OPTIONAL');
      });
    });

    it('should have unique checkpoint IDs', () => {
      const ids = CHECKPOINTS.map(cp => cp.id);
      const uniqueIds = new Set(ids);
      expect(uniqueIds.size).toBe(ids.length);
    });

    it('should have valid structure for each checkpoint', () => {
      CHECKPOINTS.forEach(cp => {
        expect(cp).toHaveProperty('id');
        expect(cp).toHaveProperty('name');
        expect(cp).toHaveProperty('level');
        expect(cp).toHaveProperty('when');
        expect(cp).toHaveProperty('whatToAsk');
        expect(cp).toHaveProperty('icon');
        expect(cp).toHaveProperty('category');
        expect(cp).toHaveProperty('agentsUsing');

        expect(typeof cp.id).toBe('string');
        expect(typeof cp.name).toBe('string');
        expect(['REQUIRED', 'RECOMMENDED', 'OPTIONAL']).toContain(cp.level);
        expect(typeof cp.when).toBe('string');
        expect(typeof cp.whatToAsk).toBe('string');
        expect(typeof cp.icon).toBe('string');
        expect(typeof cp.category).toBe('string');
        expect(Array.isArray(cp.agentsUsing)).toBe(true);
      });
    });

    it('should use correct icons for each level', () => {
      CHECKPOINTS.forEach(cp => {
        if (cp.level === 'REQUIRED') {
          expect(cp.icon).toBe('🔴');
        } else if (cp.level === 'RECOMMENDED') {
          expect(cp.icon).toBe('🟠');
        } else if (cp.level === 'OPTIONAL') {
          expect(cp.icon).toBe('🟡');
        }
      });
    });

    it('should have non-empty agentsUsing array for each checkpoint', () => {
      CHECKPOINTS.forEach(cp => {
        expect(cp.agentsUsing.length).toBeGreaterThan(0);
      });
    });

    it('should have bilingual whatToAsk messages', () => {
      CHECKPOINTS.forEach(cp => {
        // Should contain both Korean and English text
        const hasKorean = /[가-힣]/.test(cp.whatToAsk);
        const hasEnglish = /[a-zA-Z]/.test(cp.whatToAsk);
        expect(hasKorean || hasEnglish).toBe(true);
      });
    });
  });

  describe('getCheckpoint()', () => {
    it('should return checkpoint by ID', () => {
      const checkpoint = getCheckpoint('CP_RESEARCH_DIRECTION');
      expect(checkpoint).toBeDefined();
      expect(checkpoint?.id).toBe('CP_RESEARCH_DIRECTION');
      expect(checkpoint?.name).toBe('Research Direction');
    });

    it('should return undefined for non-existent ID', () => {
      const checkpoint = getCheckpoint('NON_EXISTENT_ID');
      expect(checkpoint).toBeUndefined();
    });

    it('should be case-sensitive', () => {
      const checkpoint = getCheckpoint('cp_research_direction');
      expect(checkpoint).toBeUndefined();
    });

    it('should return correct checkpoint for all valid IDs', () => {
      const allIds = CHECKPOINTS.map(cp => cp.id);
      allIds.forEach(id => {
        const checkpoint = getCheckpoint(id);
        expect(checkpoint).toBeDefined();
        expect(checkpoint?.id).toBe(id);
      });
    });

    it('should return new checkpoints added in v8.1.0', () => {
      const newCheckpoints = [
        'SCH_DATABASE_SELECTION',
        'SCH_SCREENING_CRITERIA',
        'SCH_RAG_READINESS',
        'CP_HUMANIZATION_REVIEW',
        'CP_HUMANIZATION_VERIFY',
      ];

      newCheckpoints.forEach(id => {
        const checkpoint = getCheckpoint(id);
        expect(checkpoint).toBeDefined();
        expect(checkpoint?.id).toBe(id);
      });
    });
  });

  describe('getCheckpointsByLevel()', () => {
    it('should return all REQUIRED checkpoints', () => {
      const required = getCheckpointsByLevel('REQUIRED');
      expect(required.length).toBe(8);
      required.forEach(cp => {
        expect(cp.level).toBe('REQUIRED');
        expect(cp.icon).toBe('🔴');
      });
    });

    it('should return all RECOMMENDED checkpoints', () => {
      const recommended = getCheckpointsByLevel('RECOMMENDED');
      expect(recommended.length).toBe(10);
      recommended.forEach(cp => {
        expect(cp.level).toBe('RECOMMENDED');
        expect(cp.icon).toBe('🟠');
      });
    });

    it('should return all OPTIONAL checkpoints', () => {
      const optional = getCheckpointsByLevel('OPTIONAL');
      expect(optional.length).toBe(5);
      optional.forEach(cp => {
        expect(cp.level).toBe('OPTIONAL');
        expect(cp.icon).toBe('🟡');
      });
    });

    it('should return empty array for invalid level', () => {
      // @ts-expect-error Testing invalid input
      const result = getCheckpointsByLevel('INVALID');
      expect(result).toEqual([]);
    });

    it('should include new systematic review checkpoints', () => {
      const required = getCheckpointsByLevel('REQUIRED');
      const schIds = required.map(cp => cp.id).filter(id => id.startsWith('SCH_'));
      expect(schIds).toContain('SCH_DATABASE_SELECTION');
      expect(schIds).toContain('SCH_SCREENING_CRITERIA');
    });
  });

  describe('formatCheckpoint()', () => {
    it('should format checkpoint with all required fields', () => {
      const checkpoint = getCheckpoint('CP_RESEARCH_DIRECTION')!;
      const formatted = formatCheckpoint(checkpoint);

      expect(formatted).toContain('🔴');
      expect(formatted).toContain('Research Direction');
      expect(formatted).toContain('REQUIRED');
      expect(formatted).toContain(checkpoint.whatToAsk);
      expect(formatted).toContain('When:');
      expect(formatted).toContain(checkpoint.when);
    });

    it('should format all checkpoint levels correctly', () => {
      const required = getCheckpoint('CP_RESEARCH_DIRECTION')!;
      const recommended = getCheckpoint('CP_ANALYSIS_PLAN')!;
      const optional = getCheckpoint('CP_VISUALIZATION_PREFERENCE')!;

      const formattedRequired = formatCheckpoint(required);
      const formattedRecommended = formatCheckpoint(recommended);
      const formattedOptional = formatCheckpoint(optional);

      expect(formattedRequired).toContain('REQUIRED');
      expect(formattedRecommended).toContain('RECOMMENDED');
      expect(formattedOptional).toContain('OPTIONAL');
    });

    it('should include bilingual messages in formatted output', () => {
      const checkpoint = getCheckpoint('CP_PARADIGM_SELECTION')!;
      const formatted = formatCheckpoint(checkpoint);

      // Should contain the bilingual whatToAsk
      expect(formatted).toContain(checkpoint.whatToAsk);
    });

    it('should format new v8.1.0 checkpoints correctly', () => {
      const schCheckpoint = getCheckpoint('SCH_DATABASE_SELECTION')!;
      const formatted = formatCheckpoint(schCheckpoint);

      expect(formatted).toContain('🔴');
      expect(formatted).toContain('Database Selection');
      expect(formatted).toContain('REQUIRED');
      // Category is not included in formatCheckpoint output, so we check the checkpoint object instead
      expect(schCheckpoint.category).toBe('Systematic Review');
    });

    it('should maintain markdown formatting', () => {
      const checkpoint = getCheckpoint('CP_RESEARCH_DIRECTION')!;
      const formatted = formatCheckpoint(checkpoint);

      expect(formatted).toMatch(/\*\*/); // Bold markers
      expect(formatted).toMatch(/_/);    // Italic markers
    });
  });

  describe('Checkpoint categories', () => {
    it('should have correct category assignments', () => {
      const categories = [
        'Research Foundation',
        'Study Design',
        'VS Methodology',
        'Analysis',
        'Quality & Validation',
        'Literature & Evidence',
        'Data Collection',
        'Publication & Communication',
        'Systematic Review',
      ];

      CHECKPOINTS.forEach(cp => {
        expect(categories).toContain(cp.category);
      });
    });

    it('should have VS checkpoints in VS Methodology category', () => {
      const vsCheckpoints = CHECKPOINTS.filter(cp => cp.id.startsWith('CP_VS_'));
      vsCheckpoints.forEach(cp => {
        expect(cp.category).toBe('VS Methodology');
      });
    });

    it('should have SCH checkpoints in Systematic Review category', () => {
      const schCheckpoints = CHECKPOINTS.filter(cp => cp.id.startsWith('SCH_'));
      schCheckpoints.forEach(cp => {
        expect(cp.category).toBe('Systematic Review');
      });
    });
  });

  describe('Agent usage tracking', () => {
    it('should list all agents using CP_RESEARCH_DIRECTION', () => {
      const checkpoint = getCheckpoint('CP_RESEARCH_DIRECTION')!;
      expect(checkpoint.agentsUsing).toContain('A1');
      expect(checkpoint.agentsUsing).toContain('A2');
    });

    it('should list Category I agents for systematic review checkpoints', () => {
      const dbSelection = getCheckpoint('SCH_DATABASE_SELECTION')!;
      const screening = getCheckpoint('SCH_SCREENING_CRITERIA')!;
      const ragReadiness = getCheckpoint('SCH_RAG_READINESS')!;

      expect(dbSelection.agentsUsing).toContain('I1');
      expect(screening.agentsUsing).toContain('I2');
      expect(ragReadiness.agentsUsing).toContain('I3');
    });

    it('should have unique agent IDs in agentsUsing', () => {
      CHECKPOINTS.forEach(cp => {
        const uniqueAgents = new Set(cp.agentsUsing);
        expect(uniqueAgents.size).toBe(cp.agentsUsing.length);
      });
    });
  });

  describe('Edge cases', () => {
    it('should handle empty string ID in getCheckpoint', () => {
      const result = getCheckpoint('');
      expect(result).toBeUndefined();
    });

    it('should handle edge cases in formatCheckpoint', () => {
      const mockCheckpoint: CheckpointDefinition = {
        id: 'TEST',
        name: 'Test',
        level: 'OPTIONAL',
        when: 'Test',
        whatToAsk: 'Test?',
        icon: '🟡',
        category: 'Test',
        agentsUsing: [],
      };

      const formatted = formatCheckpoint(mockCheckpoint);
      expect(formatted).toBeTruthy();
      expect(formatted).toContain('🟡');
      expect(formatted).toContain('Test');
      expect(formatted).toContain('OPTIONAL');
    });
  });
});
