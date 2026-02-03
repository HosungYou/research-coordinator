# Diverga Memory System v7.0: Research Templates

This directory contains Jinja2 templates and schemas for automated research artifact generation.

## Directory Structure

```
templates/
├── systematic-review/          # PRISMA 2020 systematic review templates
│   ├── schema.yaml            # Stage/artifact definitions
│   ├── protocol.md.j2         # Review protocol template
│   ├── search-strategy.md.j2  # Search strategy template
│   ├── inclusion-criteria.md.j2  # Screening criteria template
│   ├── quality-assessment.md.j2  # Quality appraisal template
│   ├── synthesis-plan.md.j2   # Synthesis planning template
│   ├── prisma-diagram.md.j2   # PRISMA 2020 flow diagram
│   └── manuscript.md.j2       # Manuscript draft template
│
├── meta-analysis/              # Meta-analytic research templates
│   ├── schema.yaml            # Stage/artifact definitions
│   ├── protocol.md.j2         # Meta-analysis protocol
│   ├── extraction-form.md.j2  # Data extraction form
│   └── analysis-plan.md.j2    # Statistical analysis plan
│
└── checkpoints/
    └── default-checkpoints.yaml  # Checkpoint definitions and validation rules
```

## Template Features

### Jinja2 Template Syntax

All `.j2` files use Jinja2 templating with the following features:

#### Variable Substitution
```jinja2
{{ research_question }}
{{ databases | join(', ') }}
{{ effect_size_metric }}
```

#### Conditional Blocks
```jinja2
{% if meta_analysis %}
  Meta-analysis will be conducted.
{% else %}
  Narrative synthesis only.
{% endif %}
```

#### Loops
```jinja2
{% for criterion in inclusion_criteria %}
- {{ criterion }}
{% endfor %}
```

#### Filters
```jinja2
{{ objectives | default('To be completed') }}
{{ keywords | join(', ') }}
{{ study.name | ljust(35) }}
```

### Schema Format

Each research template type has a `schema.yaml` defining:
- **Stages**: Sequential research phases
- **Artifacts**: Documents generated at each stage
- **Dependencies**: Required inputs (`requires`)
- **Validation**: Data requirements and rules
- **Checkpoints**: Quality gates (see Checkpoints section)

Example:
```yaml
stages:
  - id: identification
    name: "Stage 1: Identification"
    artifacts:
      - id: protocol
        generates: "protocol.md"
        template: "protocol.md.j2"
        requires: []
        validation:
          required_fields: [research_question, objectives]
    checkpoints:
      - CP_RESEARCH_DIRECTION
      - CP_DATABASE_SELECTION
```

## Checkpoint System

Checkpoints are quality gates that validate research progress. Defined in `checkpoints/default-checkpoints.yaml`.

### Checkpoint Levels

| Level | Priority | Blocking | Description |
|-------|----------|----------|-------------|
| 🔴 **RED** | CRITICAL | Yes | Must complete before proceeding |
| 🟡 **YELLOW** | HIGH | No | Important validation, may proceed with caution |
| 🔵 **BLUE** | MEDIUM | No | Quality assurance checkpoint |

### Checkpoint Structure

```yaml
- id: CP_RESEARCH_DIRECTION
  name: "Research Direction Validated"
  level: RED
  description: "Research question, objectives, and scope clearly defined"
  trigger:
    - "Research question formulated"
    - "PICO/PEO framework defined"
  validation:
    required_fields: [research_question, objectives]
    rules:
      - field: research_question
        min_length: 20
        must_contain: ["?"]
  auto_actions:
    - "Generate protocol.md from template"
    - "Initialize project structure"
  next_checkpoint: CP_DATABASE_SELECTION
  typical_duration: "15-30 minutes"
```

### Standard Checkpoints

#### Systematic Review Pipeline
1. 🔴 `CP_RESEARCH_DIRECTION` - Research question validated
2. 🔴 `CP_DATABASE_SELECTION` - Databases and search strategy finalized
3. 🔴 `CP_SCREENING_CRITERIA` - Inclusion/exclusion criteria defined
4. 🟡 `CP_SCREENING_COMPLETE` - All papers screened
5. 🟡 `CP_QUALITY_APPRAISAL` - Quality assessment complete
6. 🟡 `CP_SYNTHESIS_APPROACH` - Synthesis method decided
7. 🔵 `CP_FINAL_REVIEW` - PRISMA checklist complete

#### Meta-Analysis Pipeline
1. 🔴 `CP_RESEARCH_DIRECTION` - Research question validated
2. 🔴 `CP_META_APPROACH` - Effect size metric and pooling model decided
3. 🔴 `CP_DATABASE_SELECTION` - Search strategy finalized
4. 🟡 `CP_SCREENING_COMPLETE` - Papers screened
5. 🟡 `CP_EXTRACTION_COMPLETE` - Effect sizes extracted
6. 🟡 `CP_ANALYSIS_COMPLETE` - Meta-analysis conducted
7. 🟡 `CP_HETEROGENEITY_CHECKED` - Heterogeneity explored
8. 🔵 `CP_PUBLICATION_BIAS_CHECKED` - Publication bias assessed
9. 🔵 `CP_PUBLICATION_READY` - Manuscript ready for submission

#### ScholaRAG-Specific Checkpoints
1. 🔴 `SCH_DATABASE_SELECTION` - API-accessible databases validated
2. 🔴 `SCH_SCREENING_CRITERIA` - LLM screening configured
3. 🟡 `SCH_RAG_READINESS` - PDFs downloaded, RAG ready
4. 🔵 `SCH_QUALITY_GATES` - PRISMA 2020 compliance validated

### Validation Rules

Checkpoint validation supports these rule types:

| Rule Type | Description | Example |
|-----------|-------------|---------|
| `min_length` | Minimum string length | `min_length: 20` |
| `min_value` | Minimum numeric value | `min_value: 0.70` |
| `min_items` | Minimum list length | `min_items: 2` |
| `allowed_values` | Whitelist of values | `["fixed", "random"]` |
| `must_contain` | Required substring/item | `["AND", "OR"]` |
| `must_have_keys` | Required dict keys | `["estimate", "p_value"]` |
| `must_have_columns` | Required CSV columns | `["study_id", "included"]` |
| `completeness` | Fraction of non-null values | `completeness: 1.0` |

## Usage

### For Researchers (via Claude Code)

Templates are invoked automatically by Diverga agents during research workflows. No manual template usage required.

**Example**: When you reach the "Database Selection" stage:
1. I0-ScholarAgentOrchestrator detects stage completion
2. Validates against `CP_DATABASE_SELECTION` checkpoint
3. Auto-generates `search-strategy.md` from `search-strategy.md.j2`
4. Populates template with your conversation data

### For Developers (Manual Template Rendering)

```python
from jinja2 import Environment, FileSystemLoader
import yaml

# Load template
env = Environment(loader=FileSystemLoader('templates/systematic-review'))
template = env.get_template('protocol.md.j2')

# Load data
with open('project_data.yaml') as f:
    data = yaml.safe_load(f)

# Render
output = template.render(**data)

# Save
with open('output/protocol.md', 'w') as f:
    f.write(output)
```

### For Agents (via Diverga Memory System)

```python
from diverga_memory import MemorySystem

memory = MemorySystem(project_id="my-systematic-review")

# Trigger checkpoint validation
checkpoint_result = memory.validate_checkpoint(
    checkpoint_id="CP_DATABASE_SELECTION",
    data={
        "databases": ["semantic_scholar", "openalex", "arxiv"],
        "search_terms": {...},
        "boolean_search": "(chatbot OR agent) AND language learning"
    }
)

if checkpoint_result.passed:
    # Auto-generate artifact from template
    artifact = memory.generate_artifact(
        artifact_id="search-strategy",
        template="search-strategy.md.j2",
        data=checkpoint_result.data
    )
```

## Template Variables Reference

### Common Variables (All Templates)

| Variable | Type | Description |
|----------|------|-------------|
| `research_question` | str | Primary research question |
| `generation_date` | str | ISO date of generation |
| `databases` | list[str] | Selected databases |

### Systematic Review Specific

| Variable | Type | Description |
|----------|------|-------------|
| `inclusion_criteria` | dict | Inclusion criteria by domain |
| `exclusion_criteria` | list[str] | Exclusion criteria |
| `screening_results` | DataFrame | Screening outcomes |
| `prisma_counts` | dict | PRISMA flow counts |

### Meta-Analysis Specific

| Variable | Type | Description |
|----------|------|-------------|
| `effect_size_metric` | str | Effect size type (d, r, OR) |
| `pooling_model` | str | "fixed" or "random" |
| `moderators` | list[dict] | Moderator variables |
| `heterogeneity_tests` | list[str] | Heterogeneity statistics |

## Adding New Templates

### Step 1: Create Schema

```yaml
# templates/new-type/schema.yaml
name: new-type
version: "1.0"
description: "New research type"

stages:
  - id: stage1
    name: "Stage 1: Planning"
    artifacts:
      - id: artifact1
        generates: "output.md"
        template: "output.md.j2"
        requires: []
        validation:
          required_fields: [field1, field2]
    checkpoints:
      - CP_NEW_CHECKPOINT
```

### Step 2: Create Template

```jinja2
{# templates/new-type/output.md.j2 #}
# {{ title }}

{{ content }}

---
*Generated by Diverga Memory System v7.0*
*Template: new-type/output.md.j2*
```

### Step 3: Register Checkpoint

Add to `checkpoints/default-checkpoints.yaml`:

```yaml
- id: CP_NEW_CHECKPOINT
  name: "New Checkpoint"
  level: RED
  description: "Validates new research stage"
  trigger: ["Condition met"]
  validation:
    required_fields: [field1]
    rules:
      - field: field1
        min_length: 10
  next_checkpoint: CP_NEXT_STAGE
```

### Step 4: Update Agent Detection

Add trigger keywords to I0-ScholarAgentOrchestrator or relevant agent in `AGENTS.md`.

## Maintenance

### Template Versioning

Update `version` field in `schema.yaml` when making breaking changes:
- **1.0 → 1.1**: Added optional fields (backward compatible)
- **1.1 → 2.0**: Changed required fields (breaking change)

### Testing Templates

```python
# Test template rendering with sample data
test_data = {
    "research_question": "How does X affect Y?",
    "databases": ["db1", "db2"],
    # ... other required fields
}

template = env.get_template('protocol.md.j2')
output = template.render(**test_data)

# Validate output
assert "How does X affect Y?" in output
assert "db1" in output
```

---

**Related Documentation:**
- [AGENTS.md](../AGENTS.md) - Agent system overview
- [Diverga_Memory_System_v7.md](../Diverga_Memory_System_v7.md) - Memory system specification
- [conversation-manager.md](../conversation-manager.md) - Conversation state management

**Version**: 7.0
**Last Updated**: 2026-02-03
**Maintained By**: Diverga Agent System
