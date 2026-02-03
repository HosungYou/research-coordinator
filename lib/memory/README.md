# Diverga Memory System v7.0

**Human-centered research context persistence with checkpoint auto-trigger, cross-session continuity, and research documentation automation.**

A sophisticated memory and context management system for long-running research projects. The Diverga Memory System enables AI research assistants to maintain full project context across conversations, automatically inject context into agent prompts, and orchestrate human-in-the-loop checkpoint decisions.

---

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Configuration](#configuration)
- [Migration Guide](#migration-guide)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)

---

## Overview

### What the Memory System Does

The Diverga Memory System solves a critical problem: **researchers shouldn't have to re-explain their project every time they want AI assistance.**

Key capabilities:

- **Context Persistence**: Store and retrieve research project state across sessions
- **Automatic Context Injection**: Diverga agents automatically receive full project context via the Task tool
- **Checkpoint Management**: Enforce human-in-the-loop decision gates at critical research stages
- **Decision Audit Trail**: Maintain complete history of research decisions with amendments and rationale
- **Research Documentation**: Generate research artifacts from templates with context awareness
- **Cross-Session Continuity**: Resume research where you left off with complete context restoration

### Core Philosophy

```
┌────────────────────────────────────────────────────────────────┐
│                    CORE PHILOSOPHY                             │
│                                                                │
│ "Researchers set direction. AI fills in context."              │
│                                                                │
│ 1. Human makes research decision at checkpoint                 │
│ 2. Decision stored in project context                          │
│ 3. Agent automatically receives context for next task          │
│ 4. Agent proceeds with full awareness                          │
│ 5. No re-explaining needed                                     │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

### Key Features

| Feature | Description | Status |
|---------|-------------|--------|
| **Context Trigger** | Keyword-based automatic context loading | ✅ Production |
| **Task Interceptor** | Context injection for diverga: agents | ✅ Production |
| **Checkpoint Trigger** | Auto-trigger decision gates | ✅ Production |
| **Dual-Tree Filesystem** | Baseline + changes separation | ✅ Production |
| **Decision Log** | Audit trail with amendments | ✅ Production |
| **Session Hooks** | Session tracking and lifecycle | ✅ Production |
| **Archive Manager** | Stage completion archiving | ✅ Production |
| **Artifact Generator** | Research documentation templates | ✅ Production |
| **Schema Validation** | Research design validation | ✅ Production |
| **Migration Tools** | v6.8 → v7.0 automatic upgrade | ✅ Production |

---

## Quick Start

### 5-Minute Setup

```python
from lib.memory import MemoryAPI
from pathlib import Path

# Initialize for your project
memory = MemoryAPI(project_root=Path("."))

# Check if context should load
if memory.should_load_context("What's my research status?"):
    print(memory.display_context())

# Intercept task calls to inject context
modified_prompt = memory.intercept_task("diverga:a1", original_prompt)

# Record checkpoint decisions
memory.record_checkpoint("CP_THEORY_SELECTION", "Approved: Social Cognitive Theory")

# Get recent decisions
decisions = memory.get_recent_decisions(limit=5)
```

### Basic Command Usage

```bash
# Check project status
python -m lib.memory.src.memory_api status

# List decisions
python -m lib.memory.src.memory_api list

# View specific decision
python -m lib.memory.src.memory_api view <decision_id>

# Initialize new project
python -m lib.memory.src.memory_api init "My Project" \
  "Does AI improve learning outcomes?" \
  "quantitative"
```

---

## Installation

### Prerequisites

- Python 3.8 or higher
- PyYAML (for YAML file handling)

### Step 1: Install Dependencies

```bash
pip install pyyaml
```

### Step 2: Add to Your Project

```bash
# Copy the memory library into your project
cp -r /path/to/diverga/lib/memory /your/project/lib/

# Or install via git submodule
git submodule add https://github.com/HosungYou/Diverga lib/diverga
```

### Step 3: Import in Your Code

```python
from lib.memory import MemoryAPI

memory = MemoryAPI(project_root=Path("."))
```

### Step 4: Verify Installation

```bash
python -m lib.memory.VERIFY_INSTALLATION
```

Expected output:
```
✅ Memory System v7.0 ready
✅ All dependencies installed
✅ Directory structure valid
```

---

## Architecture

### 3-Layer Context System

The Diverga Memory System implements three complementary layers for intelligent context management:

```
┌──────────────────────────────────────────────────────────────────┐
│                     LAYER 1: CONTEXT TRIGGER                     │
│                   Keyword-Based Auto-Loading                      │
│                                                                  │
│  User: "What's my research status?"                             │
│  System: Detects trigger keywords → Loads & displays context    │
│                                                                  │
│  Features:                                                       │
│  • English & Korean keyword detection                           │
│  • Smart context formatting                                     │
│  • Bilingual guidance for stages                                │
│  • Recent decisions display                                     │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│                   LAYER 2: TASK INTERCEPTOR                       │
│              Context Injection for diverga: Agents                │
│                                                                  │
│  Task(subagent_type="diverga:a1", prompt="...")                │
│  System: Intercepts → Detects diverga agent → Injects context  │
│                                                                  │
│  Features:                                                       │
│  • Automatic agent detection                                    │
│  • Full project state injection                                 │
│  • Recent decisions inclusion                                   │
│  • Checkpoint awareness                                         │
│  • Stage detection & awareness                                  │
└──────────────────────────────────────────────────────────────────┘
                              ↓
┌──────────────────────────────────────────────────────────────────┐
│              LAYER 3: SEMANTIC CONTEXT (Planned)                 │
│            Embedding-Based Intelligent Retrieval                 │
│                                                                  │
│  (Future) Vector embeddings of decisions + semantic search      │
│                                                                  │
│  Features:                                                       │
│  • Semantic relevance ranking                                   │
│  • Context compression for token efficiency                     │
│  • Intelligent context filtering                                │
└──────────────────────────────────────────────────────────────────┘
```

### Filesystem Structure

```
project-root/
├── .research/                          # Core memory directory
│   ├── project-state.yaml              # Project metadata (REQUIRED)
│   ├── decision-log.yaml               # Decision audit trail
│   ├── checkpoints.yaml                # Checkpoint definitions & status
│   │
│   ├── baselines/                      # Baseline research state
│   │   ├── v6.8_backup/
│   │   └── initial_setup/
│   │
│   ├── changes/                        # Active changes (stage-organized)
│   │   └── current/
│   │       ├── theory_map.yaml         # Foundation stage
│   │       ├── hypothesis_map.yaml     # Design stage
│   │       ├── statistical_plan.yaml   # Methodology stage
│   │       └── analysis_results.yaml   # Analysis stage
│   │
│   └── sessions/                       # Session history
│       ├── session_2024_01_01.yaml
│       ├── session_2024_01_02.yaml
│       └── current.yaml
│
├── .claude/
│   └── state/
│       └── scholarag-checkpoints.json  # Checkpoint state
│
└── [your project files...]
```

### Data Flow Diagram

```
Research Project
      │
      ├─→ User: "What's my status?"
      │         │
      │         ├─→ Layer 1: Context Trigger
      │         │   └─→ Match keywords → Load .research/ files
      │         │       └─→ Display formatted context
      │         │
      │         └─→ User sees: Project status + Decisions + Next steps
      │
      ├─→ Task(diverga:a1, "Refine theory")
      │         │
      │         ├─→ Layer 2: Task Interceptor
      │         │   ├─→ Detect "diverga:a1"
      │         │   ├─→ Find .research/ folder
      │         │   ├─→ Load: project-state.yaml + decision-log.yaml
      │         │   ├─→ Detect current stage
      │         │   ├─→ Inject context into prompt
      │         │   │
      │         │   └─→ Enhanced prompt:
      │         │       "CONTEXT: Project X, Stage Y, Last decision Z"
      │         │       "Your task: Refine theory"
      │         │
      │         └─→ Agent receives full context ✓
      │
      └─→ Record Decision
                │
                ├─→ Decision made at checkpoint
                ├─→ Save to decision-log.yaml
                ├─→ Update project-state.yaml
                ├─→ Session hooks trigger
                │
                └─→ Context ready for next agent call
```

### Component Interaction Map

```
┌─────────────────────────────────────────────────────────────────────┐
│                          MemoryAPI (Facade)                        │
│                                                                     │
│  • should_load_context()        • intercept_task()                 │
│  • display_context()            • run_command()                     │
│  • check_checkpoint()           • record_checkpoint()               │
│  • add_decision()               • amend_decision()                  │
│  • initialize_project()         • get_project_state()               │
└─────────────────────────────────────────────────────────────────────┘
    │              │              │           │            │
    ↓              ↓              ↓           ↓            ↓
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ Context  │ │   Task   │ │Checkpoint│ │ Decision │ │ Session  │
│ Trigger  │ │   Intcpt │ │ Trigger  │ │   Log    │ │  Hooks   │
└──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘
    │              │              │           │            │
    │              │              │           │            │
    └──────────────┴──────────────┴───────────┴────────────┘
                         │
                         ↓
        ┌────────────────────────────────┐
        │    Filesystem State Manager     │
        │    (reads/writes .research/)    │
        └────────────────────────────────┘
                         │
                         ↓
        ┌────────────────────────────────┐
        │        .research/ Files         │
        │  (project-state, decisions,    │
        │   checkpoints, sessions)       │
        └────────────────────────────────┘
```

---

## API Reference

### MemoryAPI Main Class

The primary interface for all memory system operations.

```python
from lib.memory import MemoryAPI
from pathlib import Path

memory = MemoryAPI(project_root=Path("."))
```

#### Core Methods

##### Context Operations

**`should_load_context(message: str) -> bool`**

Check if a message contains trigger keywords for automatic context loading.

```python
if memory.should_load_context("What's my research status?"):
    context = memory.display_context()
```

**Parameters:**
- `message` (str): User message to check

**Returns:** `bool` - True if message contains context trigger keywords

**Supported Keywords:**
- English: "my research", "research status", "where was I", "continue research", "current stage"
- Korean: "내 연구", "연구 진행", "어디까지", "연구 계속", "지금 단계"

---

**`display_context() -> str`**

Load and format full research context for display.

```python
context_display = memory.display_context()
print(context_display)
```

**Returns:** `str` - Formatted context with project status, decisions, and guidance

**Example Output:**
```markdown
# 🎯 Your Research Context

## 📊 Project Status
**Project:** AI-Assisted Learning Meta-Analysis
**Research Question:** What is the effect of AI-assisted learning...
**Current Stage:** evidence
**Paradigm:** quantitative

## 📋 Recent Decisions
- **Research Question** (2026-02-03 10:30)
  Selected: Narrowed scope to K-12 learners

## 🚦 Pending Checkpoints
🔴 **CP_THEORY_SELECTION** (REQUIRED)
```

---

##### Task Interception

**`intercept_task(subagent_type: str, prompt: str) -> str`**

Intercept and enhance a task prompt with research context.

```python
modified = memory.intercept_task("diverga:a1", "Refine the research question")
# modified now includes full project context
```

**Parameters:**
- `subagent_type` (str): Agent type (e.g., "diverga:a1")
- `prompt` (str): Original prompt text

**Returns:** `str` - Enhanced prompt with injected context (or original if not a diverga agent)

---

**`run_command(command: str, args: List[str] = None) -> str`**

Execute CLI commands.

```python
# Show project status
result = memory.run_command("status")

# List decisions
result = memory.run_command("list")

# View specific decision
result = memory.run_command("view", ["decision_id_123"])

# Initialize project
result = memory.run_command("init", ["Project Name", "Research Question", "quantitative"])
```

**Commands:**
| Command | Args | Description |
|---------|------|-------------|
| `status` | None | Display project context |
| `list` | None | List recent decisions |
| `view` | `[decision_id]` | Show specific decision |
| `init` | `[name, question, paradigm]` | Initialize new project |

---

##### Session Management

**`start_session() -> str`**

Begin a new research session and return session ID.

```python
session_id = memory.start_session()
# Returns: "session_1" or similar
```

**Returns:** `str` - Session identifier

---

**`end_session() -> None`**

End current session and save data.

```python
memory.end_session()
```

---

**`get_current_session() -> Optional[Dict]`**

Retrieve current session data.

```python
session_data = memory.get_current_session()
print(session_data.get("checkpoints_reached"))
```

**Returns:** `Dict` with session metadata or None

---

##### Checkpoint Management

**`check_checkpoint(agent_id: str, action: str) -> Optional[str]`**

Check if a checkpoint should trigger for an agent action.

```python
checkpoint_prompt = memory.check_checkpoint("a1", "finalize_theory")
if checkpoint_prompt:
    print("Checkpoint triggered!")
    print(checkpoint_prompt)
```

**Parameters:**
- `agent_id` (str): Agent performing the action
- `action` (str): Action being performed

**Returns:** `Optional[str]` - Checkpoint prompt if triggered, None otherwise

---

**`record_checkpoint(checkpoint_id: str, decision: str) -> None`**

Record a checkpoint decision.

```python
memory.record_checkpoint(
    "CP_THEORY_SELECTION",
    "Selected Social Cognitive Theory for learning outcomes"
)
```

**Parameters:**
- `checkpoint_id` (str): Checkpoint identifier
- `decision` (str): Decision made at this checkpoint

---

**`get_pending_checkpoints() -> List[str]`**

Get all pending checkpoints.

```python
pending = memory.get_pending_checkpoints()
for cp_id in pending:
    print(f"Pending: {cp_id}")
```

**Returns:** `List[str]` - Checkpoint IDs waiting for completion

---

##### Decision Management

**`add_decision(checkpoint: str, selected: str, rationale: str, alternatives: List[Dict] = None) -> str`**

Record a new research decision.

```python
decision_id = memory.add_decision(
    checkpoint="CP_PARADIGM",
    selected="Quantitative experimental design",
    rationale="Research question requires causal inference",
    alternatives=[
        {"name": "Qualitative", "note": "Could explore mechanisms"},
        {"name": "Mixed methods", "note": "Would require both teams"}
    ]
)
```

**Parameters:**
- `checkpoint` (str): Checkpoint where decision was made
- `selected` (str): Selected option
- `rationale` (str): Explanation for the choice
- `alternatives` (List[Dict], optional): Other options considered

**Returns:** `str` - Decision ID for future reference

---

**`amend_decision(decision_id: str, new_selected: str, new_rationale: str) -> str`**

Modify an existing decision (preserves history).

```python
new_id = memory.amend_decision(
    decision_id="dec_123",
    new_selected="Mixed methods design",
    new_rationale="Added qualitative interviews after feedback"
)
```

**Parameters:**
- `decision_id` (str): ID of decision to amend
- `new_selected` (str): Updated selection
- `new_rationale` (str): Explanation for the change

**Returns:** `str` - New decision ID with amendment linked

---

**`get_recent_decisions(limit: int = 5) -> List[Dict]`**

Retrieve recent decisions.

```python
decisions = memory.get_recent_decisions(limit=10)
for dec in decisions:
    print(f"{dec['checkpoint']}: {dec['decision']['selected']}")
```

**Parameters:**
- `limit` (int): Maximum decisions to return (default: 5)

**Returns:** `List[Dict]` - Recent decision records

---

##### Project Management

**`initialize_project(name: str, question: str, paradigm: str) -> bool`**

Initialize a new research project.

```python
success = memory.initialize_project(
    name="AI in Education Meta-Analysis",
    question="What is the effect of AI-assisted learning on student outcomes?",
    paradigm="quantitative"
)
```

**Parameters:**
- `name` (str): Project name
- `question` (str): Research question
- `paradigm` (str): Research paradigm ("quantitative", "qualitative", or "mixed")

**Returns:** `bool` - Success indicator

---

**`get_project_state() -> Dict`**

Get current project state.

```python
state = memory.get_project_state()
print(f"Project: {state['project_name']}")
print(f"Stage: {state['current_stage']}")
```

**Returns:** `Dict` with project metadata

---

**`get_current_stage() -> str`**

Get current research stage.

```python
stage = memory.get_current_stage()
# Returns: "foundation", "evidence", "design", "collection", or "analysis"
```

**Returns:** `str` - Current stage name

---

**`is_initialized() -> bool`**

Check if project is initialized.

```python
if memory.is_initialized():
    print("Project is ready")
else:
    print("Initialize project first")
```

**Returns:** `bool` - True if project has been initialized

---

##### Documentation & Archiving

**`generate_artifact(artifact_id: str) -> Optional[Path]`**

Generate research documentation artifact.

```python
path = memory.generate_artifact("methodology_section")
if path:
    print(f"Generated: {path}")
```

**Parameters:**
- `artifact_id` (str): Type of artifact to generate

**Returns:** `Optional[Path]` - Path to generated file or None if failed

---

**`archive_stage(stage_id: str, summary: Optional[str] = None) -> Optional[Path]`**

Archive a completed research stage.

```python
path = memory.archive_stage(
    stage_id="foundation",
    summary="Completed theory review and research question refinement"
)
```

**Parameters:**
- `stage_id` (str): Stage identifier
- `summary` (str, optional): Summary of stage completion

**Returns:** `Optional[Path]` - Path to archive or None if failed

---

##### Utilities

**`get_version() -> str`**

Get memory system version.

```python
version = memory.get_version()
print(f"Memory System: {version}")  # "7.0.0"
```

**Returns:** `str` - Version number

---

**`needs_migration() -> bool`**

Check if project needs migration from v6.8.

```python
if memory.needs_migration():
    print("Run migration first: memory.migrate()")
```

**Returns:** `bool` - True if legacy files detected

---

**`migrate(dry_run: bool = False) -> Dict`**

Migrate project from v6.8 to v7.0.

```python
result = memory.migrate(dry_run=True)  # Preview changes
result = memory.migrate(dry_run=False) # Execute migration
```

**Parameters:**
- `dry_run` (bool): Preview changes without applying (default: False)

**Returns:** `Dict` with migration status and details

---

### Data Models

#### ResearchContext

Complete context for a research project.

```python
from lib.memory import ResearchContext

context = ResearchContext(
    project_name="AI in Learning",
    research_question="Does AI improve learning?",
    paradigm="quantitative",
    current_stage="design"
)
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `project_name` | str | Project title |
| `research_question` | str | Primary research question |
| `paradigm` | str | "quantitative", "qualitative", or "mixed" |
| `current_stage` | str | "foundation", "evidence", "design", "collection", "analysis" |
| `recent_decisions` | List[Decision] | Last decisions (max 10 in memory) |
| `pending_checkpoints` | List[str] | Checkpoint IDs awaiting completion |
| `last_session_summary` | str | Summary of last work session |
| `created_at` | str | ISO timestamp of creation |
| `updated_at` | str | ISO timestamp of last update |
| `sessions` | List[SessionData] | Historical session records |
| `all_decisions` | Dict[str, Decision] | Complete decision history |

---

#### Checkpoint

Represents a decision gate in the research pipeline.

```python
from lib.memory import Checkpoint, CheckpointLevel

checkpoint = Checkpoint(
    id="CP_THEORY_SELECTION",
    name="Theory Selection",
    level=CheckpointLevel.REQUIRED,
    icon="🔴",
    stage="foundation",
    agents=["a1", "a2"]
)
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `id` | str | Unique checkpoint ID |
| `name` | str | Human-readable name |
| `level` | CheckpointLevel | "required", "recommended", or "optional" |
| `icon` | str | Emoji for display |
| `stage` | str | Research stage |
| `agents` | List[str] | Agent IDs that interact with this |
| `triggers` | List[CheckpointTrigger] | Conditions that activate |
| `validation` | Dict | Validation rules |
| `persistence` | str | "memory", "notepad", or "both" |

---

#### Decision

A research decision made at a checkpoint.

```python
from lib.memory import Decision

decision = Decision(
    checkpoint_id="CP_PARADIGM",
    stage="foundation",
    agent_id="a5",
    selected="Quantitative experimental design",
    rationale="Causal inference required",
    user_confirmed=True,
    alternatives=[
        {"name": "Qualitative", "note": "Exploratory only"},
        {"name": "Mixed", "note": "Resource intensive"}
    ]
)
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `checkpoint_id` | str | Associated checkpoint |
| `stage` | str | Research stage |
| `agent_id` | str | Agent making recommendation |
| `selected` | Union[str, List, Dict] | Chosen option |
| `alternatives` | List | Options considered |
| `rationale` | str | Explanation |
| `user_confirmed` | bool | Human approved |
| `timestamp` | str | ISO timestamp |
| `amendments` | List[Amendment] | Change history |

---

#### SessionData

Information about a research work session.

```python
from lib.memory import SessionData

session = SessionData(
    session_id="session_1",
    start_time="2026-02-03T10:00:00Z"
)
```

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| `session_id` | str | Unique session ID |
| `start_time` | str | ISO start timestamp |
| `end_time` | Optional[str] | ISO end timestamp |
| `checkpoints_reached` | List[str] | Checkpoint IDs in this session |
| `decisions_made` | List[str] | Decision IDs |
| `agents_invoked` | List[str] | Agent IDs used |
| `summary` | str | Session summary |

---

### Supporting Classes

#### CheckpointTrigger Model

```python
from lib.memory import CheckpointTrigger

trigger = CheckpointTrigger(
    type="decision",
    decision_key="paradigm_selected"
)
```

**Types:**
- `"decision"` - Triggered by a decision
- `"file_exists"` - Triggered by file existence
- `"stage_entry"` - Triggered on stage transition
- `"manual"` - Manually triggered

---

#### Amendment

Amendment to a previous decision.

```python
from lib.memory import Amendment

amendment = Amendment(
    decision_id="dec_123",
    new_selected="Mixed methods",
    new_rationale="Added qualitative feedback",
    amended_by="user"
)
```

---

#### ContextInjection

Context to inject into agent prompts.

```python
from lib.memory import ContextInjection

injection = ContextInjection(
    checkpoint_id="CP_123",
    stage="design",
    summary="User selected quantitative approach",
    full_context={...},
    priority="high"
)
```

---

## Configuration

### Project Initialization

Initialize a new research project:

```python
memory = MemoryAPI(project_root=Path("."))

# Method 1: Via initialize_project()
memory.initialize_project(
    name="Your Research Title",
    question="Your research question here?",
    paradigm="quantitative"  # or "qualitative" or "mixed"
)

# Method 2: Via CLI
# python -m lib.memory.src.memory_api init "Title" "Question?" "quantitative"
```

### Project State File

The system creates `.research/project-state.yaml`:

```yaml
version: "7.0.0"
project_name: "AI in Education Meta-Analysis"
research_question: "What is the effect of AI-assisted learning on student outcomes?"
paradigm: "quantitative"
current_stage: "foundation"
metadata:
  researcher: "Your Name"
  domain: "Education"
  created_at: "2026-02-03T10:00:00Z"
  last_updated: "2026-02-03T12:00:00Z"
pending_checkpoints:
  - CP_THEORY_SELECTION
  - CP_METHODOLOGY_APPROVAL
```

### Decision Log Configuration

Decisions are stored in `.research/decision-log.yaml`:

```yaml
decisions:
  - id: "dec_001"
    timestamp: "2026-02-03T10:30:00Z"
    checkpoint: "CP_RESEARCH_DIRECTION"
    stage: "foundation"
    agent: "a1"
    selected: "Narrowed scope to K-12 learners"
    rationale: "Scope too broad, need focused population"
    alternatives:
      - name: "University level"
        note: "Different learning context"
      - name: "Adult professional"
        note: "Workplace learning"
    user_confirmed: true
    metadata:
      session_id: "session_1"
    amendments: []
```

### Checkpoint Definitions

Configure checkpoints in `.research/checkpoints.yaml`:

```yaml
checkpoints:
  CP_THEORY_SELECTION:
    level: REQUIRED
    icon: "🔴"
    stage: foundation
    agents: [a1, a2]
    validation:
      required_fields: [theory_name, rationale, implications]
      min_length: 100

  CP_PARADIGM_SELECTION:
    level: RECOMMENDED
    icon: "🟠"
    stage: foundation
    agents: [a5]
```

### Environment Variables

Optional configuration via environment variables:

```bash
# Set default project root
export DIVERGA_PROJECT_ROOT=/path/to/project

# Enable debug logging
export DIVERGA_DEBUG=1

# Specify YAML implementation
export DIVERGA_YAML_BACKEND=ruamel  # or "pyyaml"
```

---

## Migration Guide

### From v6.8 to v7.0

The memory system includes automatic migration tools to upgrade existing projects.

#### Quick Migration

```python
from lib.memory import MemoryAPI, migrate_v68_to_v70

memory = MemoryAPI(project_root=Path("."))

# Check if migration needed
if memory.needs_migration():
    print("Migration needed")

    # Preview changes
    result = migrate_v68_to_v70(Path("."), dry_run=True)
    print(result)

    # Execute migration
    result = migrate_v68_to_v70(Path("."), dry_run=False)
    print("Migration complete!")
```

#### What's Changed

| Component | v6.8 | v7.0 | Migration |
|-----------|------|------|-----------|
| **Directory Structure** | `.diverga/` | `.research/` | Automatic rename |
| **Project State** | `research_state.yaml` | `project-state.yaml` | Renamed & enhanced |
| **Decisions** | `decision_log.txt` | `decision-log.yaml` | Converted to YAML with structure |
| **Checkpoints** | Manual tracking | Auto-triggering | Enhanced with triggers |
| **Sessions** | Not tracked | `.research/sessions/` | New session tracking |
| **Version Tracking** | None | `version: "7.0.0"` | Added version field |

#### Migration Steps

1. **Backup first** (critical!)
   ```bash
   cp -r .diverga .diverga.backup
   cp research_state.yaml research_state.yaml.backup
   ```

2. **Run migration**
   ```python
   migrate_v68_to_v70(Path("."), dry_run=False)
   ```

3. **Verify results**
   ```bash
   ls -la .research/  # Should show new structure
   python -m lib.memory.src.memory_api status
   ```

4. **Test agents**
   ```python
   memory = MemoryAPI(Path("."))
   context = memory.display_context()
   print(context)
   ```

#### Rollback

If migration fails:

```bash
# Restore from backup
rm -rf .research/
mv .diverga.backup .diverga
```

---

## Usage Examples

### Example 1: Basic Project Setup

```python
from lib.memory import MemoryAPI
from pathlib import Path

# Initialize
memory = MemoryAPI(project_root=Path("."))

# Create project
memory.initialize_project(
    name="AI in K-12 Learning",
    question="How does AI-assisted personalized learning affect student engagement?",
    paradigm="quantitative"
)

# Verify
print(memory.display_context())
```

---

### Example 2: Context-Aware Agent Calls

```python
from lib.memory import MemoryAPI

memory = MemoryAPI()

# Original prompt
original = "Refine the research question based on preliminary literature"

# Intercept to inject context
enhanced = memory.intercept_task("diverga:a1", original)

# Pass to agent (now with full project context)
# Task(subagent_type="diverga:a1", prompt=enhanced)
```

**Agent receives:**
```
================================================================================
DIVERGA MEMORY SYSTEM v7.0 - RESEARCH CONTEXT
================================================================================

## Current Research Context
Project: AI in K-12 Learning
Stage: foundation
Last Updated: 2026-02-03T12:00:00Z

## Recent Decisions (Last 5)
- [2026-02-03T10:30:00Z] a1: Narrowed scope to K-12 learners
  → Triggered: CP_RESEARCH_DIRECTION
- [2026-02-02T15:00:00Z] a5: Selected quantitative paradigm
  → Triggered: CP_PARADIGM_SELECTION

## Active Checkpoints
- 🔴 CP_THEORY_SELECTION (pending)
- 🟠 CP_METHODOLOGY_APPROVAL (pending)

================================================================================
ORIGINAL REQUEST
================================================================================

Refine the research question based on preliminary literature
```

---

### Example 3: Decision Recording & History

```python
from lib.memory import MemoryAPI

memory = MemoryAPI()
memory.initialize_project(
    "My Study",
    "Does X affect Y?",
    "quantitative"
)

# Record a decision
decision_id = memory.add_decision(
    checkpoint="CP_PARADIGM_SELECTION",
    selected="Experimental design (RCT)",
    rationale="Need to establish causality; survey alone insufficient",
    alternatives=[
        {"name": "Quasi-experimental", "note": "No randomization available"},
        {"name": "Correlational", "note": "Cannot infer causality"}
    ]
)

print(f"Decision recorded: {decision_id}")

# Later: Amend the decision
amended_id = memory.amend_decision(
    decision_id=decision_id,
    new_selected="Quasi-experimental design (with matching)",
    new_rationale="Randomization not feasible; matching on key covariates"
)

print(f"Decision amended, new ID: {amended_id}")

# View history
decisions = memory.get_recent_decisions(limit=10)
for dec in decisions:
    print(f"✓ {dec['checkpoint']}: {dec['decision']['selected']}")
```

---

### Example 4: Session Tracking

```python
from lib.memory import MemoryAPI

memory = MemoryAPI()

# Start a work session
session_id = memory.start_session()
print(f"Session started: {session_id}")

# Do research work...
memory.record_checkpoint("CP_THEORY_SELECTION", "Selected SCT")

# Get session info
session = memory.get_current_session()
print(f"Checkpoints reached: {session['checkpoints_reached']}")

# End session
memory.end_session()
```

---

### Example 5: Artifact Generation

```python
from lib.memory import MemoryAPI

memory = MemoryAPI()

# Generate research documentation
methods_path = memory.generate_artifact("methodology_section")
print(f"Generated: {methods_path}")

# Archive completed stage
archive_path = memory.archive_stage(
    "foundation",
    summary="Completed theory review, research question defined"
)
print(f"Archived: {archive_path}")
```

---

### Example 6: Checkpoint Management

```python
from lib.memory import MemoryAPI

memory = MemoryAPI()

# Check if checkpoint should trigger
checkpoint_prompt = memory.check_checkpoint("a1", "finalize_research_question")

if checkpoint_prompt:
    print("CHECKPOINT TRIGGERED!")
    print(checkpoint_prompt)

    # User reviews checkpoint and approves
    memory.record_checkpoint(
        "CP_RESEARCH_DIRECTION",
        "Approved: Research question is specific and measurable"
    )

# Get pending checkpoints
pending = memory.get_pending_checkpoints()
print(f"Pending: {pending}")
```

---

### Example 7: Integration with Task Tool

```python
from lib.memory import MemoryAPI

def my_task_wrapper(subagent_type: str, prompt: str, **kwargs):
    """Wrapper that injects context before calling Task tool."""
    memory = MemoryAPI()

    # Inject context if diverga agent
    enhanced_prompt = memory.intercept_task(subagent_type, prompt)

    # Call actual Task tool (implementation specific)
    # return Task(subagent_type=subagent_type, prompt=enhanced_prompt, **kwargs)

# Usage
my_task_wrapper(
    "diverga:c5",
    "Design the meta-analysis extraction template"
)
```

---

## Contributing

### Development Setup

```bash
# Clone repository
git clone https://github.com/HosungYou/Diverga.git
cd Diverga

# Set up development environment
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run linting
flake8 lib/memory
black lib/memory --check
```

### Code Style

- Follow PEP 8
- Use type hints throughout
- Document all public methods with docstrings
- Include examples in docstrings

### Testing

Add tests for new features:

```bash
# Create test file
touch tests/test_new_feature.py

# Write tests
pytest tests/test_new_feature.py -v
```

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make changes and write tests
4. Run full test suite (`pytest`)
5. Submit PR with clear description

### Bug Reports

Report bugs with:
- Python version and OS
- Error message and traceback
- Minimal reproducible example
- Expected vs. actual behavior

---

## Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'yaml'"

**Solution:**
```bash
pip install pyyaml
```

---

#### Issue: "FileNotFoundError: Missing .research/project-state.yaml"

**Solution:**
```python
memory = MemoryAPI()
memory.initialize_project("Name", "Question?", "quantitative")
```

---

#### Issue: Context not injecting

**Checklist:**
1. Is project initialized? (`memory.is_initialized()`)
2. Is subagent_type correctly formatted? (`"diverga:a1"`)
3. Is .research/ directory present?
4. Check for error messages in console

---

### Support

- **Documentation**: Full docs in this README
- **Examples**: See `examples/` directory
- **Issues**: GitHub issues on main repository
- **Contact**: Project maintainers

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| **7.0.0** | 2026-02-03 | Initial v7.0 release |
| | | • 3-layer context system |
| | | • Enhanced data models |
| | | • Session tracking |
| | | • Automatic migration from v6.8 |
| **6.8.0** | 2025-01-15 | Previous stable version |

---

## License

MIT License - Part of Diverga Research Assistant System

See `LICENSE` file for full details.

---

## Related Documentation

- **Diverga Main Docs**: `/Volumes/External SSD/Projects/Research/Diverga/CLAUDE.md`
- **Agent Definitions**: `/Volumes/External SSD/Projects/Research/Diverga/AGENTS.md`
- **Checkpoint System**: `/Volumes/External SSD/Projects/Research/Diverga/.claude/checkpoints/`
- **ScholaRAG Integration**: `/Volumes/External SSD/Projects/Research/ScholaRAG/`

---

## Quick Links

- **GitHub Repository**: https://github.com/HosungYou/Diverga
- **Main Diverga Project**: https://github.com/HosungYou/Diverga
- **Research Assistant**: https://claude.ai/code

---

**Diverga Memory System v7.0** - Making research context persistent and accessible.
