"""
Diverga QA Agent Tracker
=========================

Tracks agent invocations during test execution.
Validates correct agent selection and model tier usage.
"""

import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class AgentInvocation:
    """Record of a single agent invocation."""
    agent_id: str
    model_tier: str
    timestamp: datetime = field(default_factory=datetime.now)

    # Invocation details
    trigger_keyword: str | None = None
    prompt_snippet: str | None = None

    # Timing
    response_time_seconds: float | None = None

    # Validation
    is_correct_agent: bool = True
    is_correct_tier: bool = True
    execution_order: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "agent_id": self.agent_id,
            "model_tier": self.model_tier,
            "timestamp": self.timestamp.isoformat(),
            "trigger_keyword": self.trigger_keyword,
            "response_time_seconds": self.response_time_seconds,
            "is_correct_agent": self.is_correct_agent,
            "is_correct_tier": self.is_correct_tier,
            "execution_order": self.execution_order,
        }


class AgentTracker:
    """
    Tracks and validates agent invocations during Diverga QA testing.
    Maps keywords to expected agents and validates model tier selection.
    """

    # Agent keyword mappings (from CLAUDE.md)
    AGENT_KEYWORDS = {
        # Category A: Foundation
        "diverga:a1": ["research question", "RQ", "refine question", "연구 질문", "연구문제"],
        "diverga:a2": ["theoretical framework", "theory", "conceptual model", "이론적 프레임워크"],
        "diverga:a3": ["devil's advocate", "critique", "counterargument", "반론", "비판적 검토"],
        "diverga:a4": ["IRB", "ethics", "informed consent", "research ethics", "연구 윤리"],
        "diverga:a5": ["paradigm", "ontology", "epistemology", "worldview", "패러다임"],
        "diverga:a6": ["conceptual framework", "visualize framework", "개념적 프레임워크"],

        # Category B: Evidence
        "diverga:b1": ["systematic review", "literature search", "PRISMA", "체계적 문헌고찰"],
        "diverga:b2": ["quality appraisal", "RoB", "GRADE", "bias assessment", "품질 평가"],
        "diverga:b3": ["effect size", "extract effect", "Cohen's d", "Hedges' g", "효과크기"],
        "diverga:b4": ["research trends", "emerging topics", "research radar", "연구 동향"],
        "diverga:b5": ["batch PDF", "parallel processing", "multiple PDFs", "PDF 일괄 처리"],

        # Category C: Design & Meta-Analysis
        "diverga:c1": ["quantitative design", "experimental design", "RCT", "양적 연구 설계"],
        "diverga:c2": ["qualitative design", "phenomenology", "grounded theory", "질적 연구 설계"],
        "diverga:c3": ["mixed methods", "sequential design", "convergent", "혼합방법"],
        "diverga:c4": ["intervention materials", "experimental materials", "중재 자료"],
        "diverga:c5": ["meta-analysis", "pooled effect", "heterogeneity", "메타분석"],
        "diverga:c6": ["data extraction", "PDF extract", "extract data", "데이터 추출"],
        "diverga:c7": ["error prevention", "validation", "data check", "오류 방지"],

        # Category D: Data Collection
        "diverga:d1": ["sampling", "sample size", "G*Power", "표집"],
        "diverga:d2": ["interview", "focus group", "interview protocol", "인터뷰"],
        "diverga:d3": ["observation", "observation protocol", "관찰"],
        "diverga:d4": ["instrument", "measurement", "scale development", "측정 도구"],

        # Category E: Analysis
        "diverga:e1": ["statistical analysis", "ANOVA", "regression", "SEM", "통계 분석"],
        "diverga:e2": ["qualitative coding", "thematic analysis", "coding", "질적 코딩"],
        "diverga:e3": ["mixed methods integration", "joint display", "혼합방법 통합"],
        "diverga:e4": ["R code", "Python code", "analysis code", "R 코드"],
        "diverga:e5": ["sensitivity analysis", "robustness check", "민감도 분석"],

        # Category F: Quality
        "diverga:f1": ["consistency check", "internal consistency", "일관성 검토"],
        "diverga:f2": ["checklist", "CONSORT", "STROBE", "COREQ", "체크리스트"],
        "diverga:f3": ["reproducibility", "replication", "OSF", "재현성"],
        "diverga:f4": ["bias detection", "trustworthiness", "편향 탐지"],
        "diverga:f5": ["humanization verify", "AI text check", "휴먼화 검증"],

        # Category G: Communication
        "diverga:g1": ["journal match", "where to publish", "target journal", "저널 매칭"],
        "diverga:g2": ["academic writing", "manuscript", "write paper", "학술 글쓰기"],
        "diverga:g3": ["peer review", "reviewer response", "revision", "동료 심사"],
        "diverga:g4": ["preregistration", "OSF", "pre-register", "사전등록"],
        "diverga:g5": ["AI pattern", "check AI writing", "style audit", "AI 패턴"],
        "diverga:g6": ["humanize", "humanization", "natural writing", "휴먼화"],

        # Category H: Specialized
        "diverga:h1": ["ethnography", "fieldwork", "participant observation", "민족지학"],
        "diverga:h2": ["action research", "participatory", "practitioner", "실행연구"],
    }

    # Model tier assignments
    AGENT_TIERS = {
        # HIGH (Opus)
        "diverga:a1": "opus", "diverga:a2": "opus", "diverga:a3": "opus",
        "diverga:a5": "opus", "diverga:b5": "opus",
        "diverga:c1": "opus", "diverga:c2": "opus", "diverga:c3": "opus",
        "diverga:c5": "opus", "diverga:d4": "opus",
        "diverga:e1": "opus", "diverga:e2": "opus", "diverga:e3": "opus",
        "diverga:g3": "opus", "diverga:g6": "opus",
        "diverga:h1": "opus", "diverga:h2": "opus",

        # MEDIUM (Sonnet)
        "diverga:a4": "sonnet", "diverga:a6": "sonnet",
        "diverga:b1": "sonnet", "diverga:b2": "sonnet",
        "diverga:c4": "sonnet", "diverga:c6": "sonnet", "diverga:c7": "sonnet",
        "diverga:d1": "sonnet", "diverga:d2": "sonnet",
        "diverga:e5": "sonnet",
        "diverga:f3": "sonnet", "diverga:f4": "sonnet",
        "diverga:g1": "sonnet", "diverga:g2": "sonnet", "diverga:g4": "sonnet",
        "diverga:g5": "sonnet",

        # LOW (Haiku)
        "diverga:b3": "haiku", "diverga:b4": "haiku",
        "diverga:d3": "haiku",
        "diverga:e4": "haiku",
        "diverga:f1": "haiku", "diverga:f2": "haiku", "diverga:f5": "haiku",
    }

    # Legacy agent ID mappings
    LEGACY_AGENT_MAP = {
        "C5-MetaAnalysisMaster": "diverga:c5",
        "C6-DataIntegrityGuard": "diverga:c6",
        "C7-ErrorPreventionEngine": "diverga:c7",
        "A1-ResearchQuestionRefiner": "diverga:a1",
        "A2-TheoreticalFrameworkArchitect": "diverga:a2",
        "B1-SystematicLiteratureScout": "diverga:b1",
        "G5-AcademicStyleAuditor": "diverga:g5",
        "G6-AcademicStyleHumanizer": "diverga:g6",
    }

    def __init__(self):
        """Initialize agent tracker."""
        self.invocations: list[AgentInvocation] = []
        self.invocation_order = 0

    def reset(self):
        """Reset tracker state."""
        self.invocations = []
        self.invocation_order = 0

    def detect_agent_from_keywords(self, text: str) -> list[tuple[str, str]]:
        """
        Detect which agent(s) should be triggered based on keywords in text.

        Args:
            text: User input or context text

        Returns:
            List of (agent_id, matched_keyword) tuples
        """
        text_lower = text.lower()
        matches = []

        for agent_id, keywords in self.AGENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    matches.append((agent_id, keyword))
                    break  # Only one match per agent

        return matches

    def normalize_agent_id(self, agent_id: str) -> str:
        """Normalize agent ID to diverga:XX format."""
        if agent_id in self.LEGACY_AGENT_MAP:
            return self.LEGACY_AGENT_MAP[agent_id]
        if not agent_id.startswith("diverga:"):
            # Try to extract agent code
            match = re.search(r"([A-H]\d)", agent_id, re.IGNORECASE)
            if match:
                return f"diverga:{match.group(1).lower()}"
        return agent_id.lower()

    def get_expected_tier(self, agent_id: str) -> str:
        """Get expected model tier for an agent."""
        normalized = self.normalize_agent_id(agent_id)
        return self.AGENT_TIERS.get(normalized, "sonnet")  # Default to sonnet

    def record_invocation(
        self,
        agent_id: str,
        model_tier: str,
        trigger_keyword: str | None = None,
        response_time: float | None = None,
    ) -> AgentInvocation:
        """
        Record an agent invocation.

        Args:
            agent_id: Agent identifier
            model_tier: Model tier used (opus/sonnet/haiku)
            trigger_keyword: Keyword that triggered invocation
            response_time: Response time in seconds

        Returns:
            AgentInvocation record
        """
        self.invocation_order += 1
        normalized_id = self.normalize_agent_id(agent_id)
        expected_tier = self.get_expected_tier(normalized_id)

        invocation = AgentInvocation(
            agent_id=normalized_id,
            model_tier=model_tier.lower(),
            trigger_keyword=trigger_keyword,
            response_time_seconds=response_time,
            is_correct_tier=model_tier.lower() == expected_tier,
            execution_order=self.invocation_order,
        )

        self.invocations.append(invocation)
        return invocation

    def validate_invocation(
        self,
        expected_agent: str,
        expected_tier: str | None = None,
    ) -> tuple[bool, list[str]]:
        """
        Validate that expected agent was invoked with correct tier.

        Args:
            expected_agent: Expected agent ID
            expected_tier: Expected model tier (optional)

        Returns:
            Tuple of (is_valid, list of issues)
        """
        issues = []
        normalized = self.normalize_agent_id(expected_agent)

        # Check if agent was invoked
        matching = [inv for inv in self.invocations if inv.agent_id == normalized]

        if not matching:
            issues.append(f"AGENT_NOT_INVOKED: {expected_agent} was not called")
            return False, issues

        # Check tier if specified
        if expected_tier:
            for inv in matching:
                if inv.model_tier != expected_tier.lower():
                    issues.append(
                        f"WRONG_TIER: {expected_agent} used {inv.model_tier} "
                        f"instead of {expected_tier}"
                    )

        return len(issues) == 0, issues

    def validate_sequence(
        self,
        expected_sequence: list[str],
    ) -> tuple[bool, list[str]]:
        """
        Validate agents were invoked in expected sequence.

        Args:
            expected_sequence: List of agent IDs in expected order

        Returns:
            Tuple of (is_valid, list of issues)
        """
        issues = []
        normalized_expected = [self.normalize_agent_id(a) for a in expected_sequence]

        # Get actual sequence
        actual_sequence = [inv.agent_id for inv in self.invocations]

        # Check sequence
        expected_idx = 0
        for actual in actual_sequence:
            if expected_idx < len(normalized_expected):
                if actual == normalized_expected[expected_idx]:
                    expected_idx += 1

        # Check all expected agents were seen
        if expected_idx < len(normalized_expected):
            missing = normalized_expected[expected_idx:]
            for agent in missing:
                issues.append(f"MISSING_AGENT: {agent} was not invoked")

        return len(issues) == 0, issues

    def get_invocation_summary(self) -> dict[str, Any]:
        """Get summary of all invocations."""
        return {
            "total_invocations": len(self.invocations),
            "agents_invoked": list(set(inv.agent_id for inv in self.invocations)),
            "tiers_used": {
                "opus": sum(1 for inv in self.invocations if inv.model_tier == "opus"),
                "sonnet": sum(1 for inv in self.invocations if inv.model_tier == "sonnet"),
                "haiku": sum(1 for inv in self.invocations if inv.model_tier == "haiku"),
            },
            "tier_accuracy": sum(1 for inv in self.invocations if inv.is_correct_tier) / len(self.invocations) * 100 if self.invocations else 100.0,
            "invocations": [inv.to_dict() for inv in self.invocations],
        }
