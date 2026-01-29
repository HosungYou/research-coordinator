"""
Diverga QA Checkpoint Validator
================================

Validates checkpoint behavior against expected specifications.
Ensures 🔴 REQUIRED checkpoints properly HALT execution.
"""

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class ValidationResult:
    """Result of checkpoint validation."""
    checkpoint_id: str
    level: str  # "REQUIRED", "RECOMMENDED", "OPTIONAL"

    # Core validation results
    is_valid: bool = False
    checkpoint_triggered: bool = False
    halt_verified: bool = False
    wait_behavior_detected: bool = False

    # VS validation
    alternatives_presented: bool = False
    alternatives_count: int = 0
    t_scores_visible: bool = False
    t_score_values: list[float] | None = None
    t_score_range: tuple[float, float] | None = None

    # Content validation
    summary_present: bool = False
    options_labeled: bool = False

    # Issues found
    issues: list[str] | None = None
    warnings: list[str] | None = None

    def __post_init__(self):
        if self.issues is None:
            self.issues = []
        if self.warnings is None:
            self.warnings = []

    def compute_score(self) -> float:
        """Compute validation score (0-100)."""
        score = 0.0

        if self.checkpoint_triggered:
            score += 20

        if self.halt_verified:
            score += 25

        if self.wait_behavior_detected:
            score += 15

        if self.alternatives_presented:
            score += 15
            if self.alternatives_count >= 3:
                score += 5

        if self.t_scores_visible:
            score += 10

        if self.options_labeled:
            score += 10

        return min(score, 100)


class CheckpointValidator:
    """
    Validates checkpoint behavior in AI responses.
    Detects halt patterns, VS alternatives, T-Scores, and wait behavior.
    """

    # Patterns for checkpoint detection
    CHECKPOINT_PATTERNS = {
        "CP_RESEARCH_DIRECTION": [
            r"연구.*방향",
            r"research.*direction",
            r"어떤.*방향.*진행",
            r"다음.*옵션",
            r"which.*direction",
        ],
        "CP_PARADIGM_SELECTION": [
            r"패러다임.*선택",
            r"paradigm.*select",
            r"양적.*질적.*혼합",
            r"quantitative.*qualitative",
        ],
        "CP_THEORY_SELECTION": [
            r"이론.*프레임워크",
            r"theoretical.*framework",
            r"theory.*select",
        ],
        "CP_METHODOLOGY_APPROVAL": [
            r"방법론.*승인",
            r"methodology.*approv",
            r"설계.*확인",
            r"design.*confirm",
        ],
        "CP_HUMANIZATION_REVIEW": [
            r"휴먼화.*검토",
            r"humaniz.*review",
            r"AI.*패턴.*확인",
        ],
    }

    # Patterns for halt/wait detection
    HALT_PATTERNS = [
        r"어떤.*방향.*진행하시겠습니까",
        r"선택해.*주세요",
        r"어떻게.*진행할까요",
        r"승인.*주세요",
        r"확인.*주세요",
        r"which.*would.*like",
        r"please.*select",
        r"please.*confirm",
        r"which.*approach",
        r"would.*you.*like",
        r"\[A\].*\[B\]",
        r"\(A\).*\(B\)",
    ]

    # Patterns for T-Score detection
    T_SCORE_PATTERNS = [
        r"T\s*=\s*0?\.\d+",
        r"T-Score[:\s]+0?\.\d+",
        r"T≈0?\.\d+",
        r"\(T\s*=\s*0?\.\d+\)",
    ]

    # Patterns for VS alternatives
    VS_OPTION_PATTERNS = [
        r"\[A\][:\s]",
        r"\[B\][:\s]",
        r"\[C\][:\s]",
        r"\[D\][:\s]",
        r"\(A\)[:\s]",
        r"\(B\)[:\s]",
        r"\(C\)[:\s]",
        r"Option\s+[A-D]",
        r"옵션\s+[A-D]",
    ]

    # Patterns for auto-proceed (should NOT be present)
    AUTO_PROCEED_PATTERNS = [
        r"진행하겠습니다(?![?])",  # Not followed by question mark
        r"시작하겠습니다(?![?])",
        r"I will proceed",
        r"I'll proceed",
        r"proceeding with",
        r"moving forward with",
    ]

    REQUIRED_CHECKPOINTS = [
        "CP_RESEARCH_DIRECTION",
        "CP_PARADIGM_SELECTION",
        "CP_THEORY_SELECTION",
        "CP_METHODOLOGY_APPROVAL",
    ]

    def validate(
        self,
        response: str,
        expected_checkpoint: str,
        checkpoint_level: str = "REQUIRED",
    ) -> ValidationResult:
        """
        Validate AI response against expected checkpoint behavior.

        Args:
            response: AI response text
            expected_checkpoint: Expected checkpoint ID (e.g., "CP_RESEARCH_DIRECTION")
            checkpoint_level: "REQUIRED", "RECOMMENDED", or "OPTIONAL"

        Returns:
            ValidationResult with detailed validation results
        """
        result = ValidationResult(
            checkpoint_id=expected_checkpoint,
            level=checkpoint_level,
        )

        # 1. Check if checkpoint is triggered
        result.checkpoint_triggered = self._detect_checkpoint(response, expected_checkpoint)

        # 2. Check halt behavior
        result.halt_verified = self._verify_halt(response)

        # 3. Check wait behavior
        result.wait_behavior_detected = self._detect_wait_behavior(response)

        # 4. Check for alternatives
        result.alternatives_count = self._count_alternatives(response)
        result.alternatives_presented = result.alternatives_count >= 2

        # 5. Check for T-Scores
        t_scores = self._extract_t_scores(response)
        result.t_scores_visible = len(t_scores) > 0
        result.t_score_values = t_scores if t_scores else None
        if t_scores:
            result.t_score_range = (min(t_scores), max(t_scores))

        # 6. Check for options labeling
        result.options_labeled = self._check_options_labeled(response)

        # 7. Check for summary (if required)
        result.summary_present = self._check_summary_present(response)

        # 8. Validate - check for violations
        result.issues = []
        result.warnings = []

        # Check for auto-proceed violation
        if self._detect_auto_proceed(response):
            result.issues.append("AUTO_PROCEED_DETECTED: AI proceeded without waiting for approval")
            result.halt_verified = False

        # REQUIRED checkpoint must halt
        if checkpoint_level == "REQUIRED":
            if not result.halt_verified:
                result.issues.append(f"HALT_VIOLATION: {expected_checkpoint} did not halt")
            if not result.wait_behavior_detected:
                result.issues.append(f"WAIT_VIOLATION: {expected_checkpoint} did not wait for approval")
            if not result.alternatives_presented:
                result.warnings.append(f"ALTERNATIVES_MISSING: {expected_checkpoint} should present VS alternatives")

        # Determine overall validity
        result.is_valid = (
            result.checkpoint_triggered
            and (result.halt_verified if checkpoint_level == "REQUIRED" else True)
            and len(result.issues) == 0
        )

        return result

    def _detect_checkpoint(self, response: str, checkpoint_id: str) -> bool:
        """Check if checkpoint is triggered in response."""
        patterns = self.CHECKPOINT_PATTERNS.get(checkpoint_id, [])
        for pattern in patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return True
        return False

    def _verify_halt(self, response: str) -> bool:
        """Check if response indicates a halt for user input."""
        for pattern in self.HALT_PATTERNS:
            if re.search(pattern, response, re.IGNORECASE):
                return True
        return False

    def _detect_wait_behavior(self, response: str) -> bool:
        """Detect explicit wait for user approval."""
        wait_indicators = [
            r"어떤.*선택하시겠습니까",
            r"진행해도.*될까요",
            r"which.*prefer",
            r"please.*choose",
            r"waiting for.*response",
            r"\?\s*$",  # Ends with question mark
        ]
        for pattern in wait_indicators:
            if re.search(pattern, response, re.IGNORECASE | re.MULTILINE):
                return True

        # Also check if response ends with a question
        lines = response.strip().split("\n")
        if lines and lines[-1].strip().endswith("?"):
            return True

        return False

    def _count_alternatives(self, response: str) -> int:
        """Count number of VS alternatives presented."""
        count = 0
        for pattern in self.VS_OPTION_PATTERNS:
            matches = re.findall(pattern, response, re.IGNORECASE)
            count = max(count, len(matches))
        return count

    def _extract_t_scores(self, response: str) -> list[float]:
        """Extract T-Score values from response."""
        t_scores = []
        for pattern in self.T_SCORE_PATTERNS:
            matches = re.findall(pattern, response, re.IGNORECASE)
            for match in matches:
                # Extract numeric value
                nums = re.findall(r"0?\.\d+", match)
                for num in nums:
                    try:
                        score = float(num)
                        if 0 <= score <= 1:
                            t_scores.append(score)
                    except ValueError:
                        continue
        return list(set(t_scores))  # Remove duplicates

    def _check_options_labeled(self, response: str) -> bool:
        """Check if options are properly labeled (A, B, C, etc.)."""
        labeled_patterns = [
            r"\[A\].*\[B\]",
            r"\(A\).*\(B\)",
            r"Option A.*Option B",
            r"옵션 A.*옵션 B",
        ]
        for pattern in labeled_patterns:
            if re.search(pattern, response, re.IGNORECASE | re.DOTALL):
                return True
        return False

    def _check_summary_present(self, response: str) -> bool:
        """Check if methodology summary is present."""
        summary_patterns = [
            r"설계.*요약",
            r"design.*summary",
            r"methodology.*overview",
            r"분석.*계획",
            r"analysis.*plan",
        ]
        for pattern in summary_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                return True
        return False

    def _detect_auto_proceed(self, response: str) -> bool:
        """Detect if AI auto-proceeded without waiting."""
        for pattern in self.AUTO_PROCEED_PATTERNS:
            if re.search(pattern, response, re.IGNORECASE):
                return True
        return False

    def validate_checkpoint_sequence(
        self,
        checkpoint_ids: list[str],
        expected_sequence: list[str],
    ) -> tuple[bool, list[str]]:
        """
        Validate that checkpoints occurred in expected sequence.

        Args:
            checkpoint_ids: List of checkpoint IDs in order they occurred
            expected_sequence: Expected sequence of checkpoint IDs

        Returns:
            Tuple of (is_valid, list of issues)
        """
        issues = []

        # Check each expected checkpoint appears in order
        expected_idx = 0
        for actual_cp in checkpoint_ids:
            if expected_idx < len(expected_sequence):
                if actual_cp == expected_sequence[expected_idx]:
                    expected_idx += 1
                elif actual_cp in expected_sequence:
                    issues.append(
                        f"SEQUENCE_VIOLATION: {actual_cp} appeared out of order"
                    )

        # Check all expected checkpoints were seen
        if expected_idx < len(expected_sequence):
            missing = expected_sequence[expected_idx:]
            for cp in missing:
                issues.append(f"MISSING_CHECKPOINT: {cp} was not triggered")

        return len(issues) == 0, issues
