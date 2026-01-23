#!/bin/bash
# =============================================================================
# Research Coordinator - 전체 플러그인 일괄 설치 스크립트
# =============================================================================
#
# 사용법:
#   curl -sL https://raw.githubusercontent.com/HosungYou/research-coordinator/main/scripts/install-all-plugins.sh | bash
#
# 또는 로컬에서:
#   ./scripts/install-all-plugins.sh
#
# =============================================================================

set -e

echo "=============================================="
echo "  Research Coordinator Plugin Installer"
echo "  Version: 2.0.1"
echo "=============================================="
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 플러그인 목록
PLUGINS=(
    "research-coordinator:Master Coordinator"
    "01-research-question-refiner:Research Question Refiner"
    "02-theoretical-framework-architect:Theoretical Framework Architect"
    "03-devils-advocate:Devil's Advocate"
    "04-research-ethics-advisor:Research Ethics Advisor"
    "05-systematic-literature-scout:Systematic Literature Scout"
    "06-evidence-quality-appraiser:Evidence Quality Appraiser"
    "07-effect-size-extractor:Effect Size Extractor"
    "08-research-radar:Research Radar"
    "09-research-design-consultant:Research Design Consultant"
    "10-statistical-analysis-guide:Statistical Analysis Guide"
    "11-analysis-code-generator:Analysis Code Generator"
    "12-sensitivity-analysis-designer:Sensitivity Analysis Designer"
    "13-internal-consistency-checker:Internal Consistency Checker"
    "14-checklist-manager:Checklist Manager"
    "15-reproducibility-auditor:Reproducibility Auditor"
    "16-bias-detector:Bias Detector"
    "17-journal-matcher:Journal Matcher"
    "18-academic-communicator:Academic Communicator"
    "19-peer-review-strategist:Peer Review Strategist"
    "20-preregistration-composer:Preregistration Composer"
)

# claude CLI 확인
if ! command -v claude &> /dev/null; then
    echo -e "${RED}Error: claude CLI not found${NC}"
    echo "Please install Claude Code first: https://claude.ai/code"
    exit 1
fi

echo -e "${BLUE}Step 1/3: 마켓플레이스 추가 중...${NC}"
echo ""

# 마켓플레이스가 이미 추가되어 있는지 확인
if claude plugin marketplace list 2>&1 | grep -q "research-coordinator-skills"; then
    echo -e "${GREEN}✓ 마켓플레이스가 이미 추가되어 있습니다${NC}"
else
    if claude plugin marketplace add HosungYou/research-coordinator 2>&1; then
        echo -e "${GREEN}✓ 마켓플레이스 추가 완료${NC}"
    else
        echo -e "${RED}✗ 마켓플레이스 추가 실패${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}Step 2/3: 플러그인 설치 중 (21개)...${NC}"
echo ""

SUCCESS=0
FAILED=0
SKIPPED=0

for item in "${PLUGINS[@]}"; do
    IFS=':' read -r plugin_name plugin_desc <<< "$item"

    # 이미 설치되어 있는지 확인
    if claude plugin list 2>&1 | grep -q "${plugin_name}@research-coordinator-skills"; then
        echo -e "${YELLOW}○ ${plugin_name}${NC} (이미 설치됨)"
        ((SKIPPED++))
    else
        if claude plugin install "$plugin_name" 2>&1 | grep -q "Successfully installed"; then
            echo -e "${GREEN}✓ ${plugin_name}${NC} - ${plugin_desc}"
            ((SUCCESS++))
        else
            echo -e "${RED}✗ ${plugin_name}${NC} - 설치 실패"
            ((FAILED++))
        fi
    fi
done

echo ""
echo -e "${BLUE}Step 3/3: 설치 결과 요약${NC}"
echo ""
echo "=============================================="
echo -e "  ${GREEN}성공${NC}: $SUCCESS"
echo -e "  ${YELLOW}이미 설치됨${NC}: $SKIPPED"
echo -e "  ${RED}실패${NC}: $FAILED"
echo -e "  총: $((SUCCESS + SKIPPED + FAILED)) / ${#PLUGINS[@]}"
echo "=============================================="
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}모든 플러그인이 설치되었습니다!${NC}"
    echo ""
    echo "사용 방법:"
    echo "  /research-coordinator     # 마스터 코디네이터"
    echo "  /research-question-refiner  # 개별 에이전트"
    echo ""
else
    echo -e "${YELLOW}일부 플러그인 설치에 실패했습니다.${NC}"
    echo "다시 시도하려면: ./scripts/install-all-plugins.sh"
fi
