# skill-evaluator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) | [中文](README.md)

An AI Agent Skill for evaluating the quality of other Skills. It scores Skills across 8 weighted dimensions, identifies weaknesses, provides actionable improvement suggestions, and supports side-by-side comparison of multiple Skills. **Supports multi-model cross-validation** where multiple models evaluate independently, challenge each other's scores, and an arbiter produces the authoritative verdict. Provides three execution strategies (subagent parallel → Qianfan API → serial multi-perspective) with automatic degradation to ensure cross-platform availability.

Compatible with any AI Agent platform that supports the Skill mechanism, including Claude Code, Ducc, Xiaolongxia, and others.

## Features

- **Multi-dimensional scoring** — 8 weighted dimensions, 0-10 each
- **Grade mapping** — Composite score maps to S/A/B/C/D grades
- **Actionable feedback** — Problem description, impact analysis, and concrete suggestions for each weak dimension
- **Multi-Skill comparison** — Side-by-side scoring table, strengths/weaknesses analysis, and ranking
- **Multi-model cross-validation** — Multiple models evaluate independently, then peer-review each other, with a final arbiter verdict for authoritative results
- **Qianfan API multi-model** — Calls multiple real models (ernie-5.0, deepseek-v3.2, qwen3.5, glm-5.1) via Baidu Qianfan LLM platform API, no subagent dependency
- **Serial multi-perspective fallback** — Auto-switches when Strategy A/B are unavailable: same model evaluates as Strict/Pragmatic/Expert reviewers, then cross-reviews and arbitrates
- **Automatic strategy degradation** — A (subagent parallel) → B (Qianfan API) → C (serial multi-perspective), transparent to users
- **Customizable models** — Prompts user to choose models first; Strategy A defaults to Claude Opus 4.6 + Sonnet 4.6 / GLM-5 / MiniMax-M2-Stable, Strategy B defaults to ernie-5.0 / deepseek-v3.2 / qwen3.5 / glm-5.1

## Evaluation Dimensions

| Dimension | Weight | Description |
|-----------|--------|-------------|
| D1. Metadata Quality | 15% | Quality of `name` and `description` in YAML frontmatter |
| D2. Execution Guidance Clarity | 15% | Whether the Agent knows how to execute after loading |
| D3. Domain Knowledge Density | 15% | Whether it embeds expert knowledge unavailable to a general Agent |
| D4. Workflow Completeness | 15% | End-to-end workflow with branching and error handling |
| D5. Input/Output Clarity | 10% | Whether users know what to provide and what to expect |
| D6. Resource Utilization | 10% | Use of scripts, references, and assets |
| D7. Writing Quality | 10% | Structure clarity, readability, and precision |
| D8. Scope & Focus | 10% | Whether it focuses on a single coherent problem domain |

## Grade Scale

| Score | Grade | Meaning |
|-------|-------|---------|
| 9.0-10 | S | Outstanding — benchmark-level Skill |
| 7.5-8.9 | A | Excellent — ready to use, minor polish needed |
| 6.0-7.4 | B | Adequate — usable but with clear room for improvement |
| 4.0-5.9 | C | Weak — needs significant rework |
| 0-3.9 | D | Poor — fundamental issues, consider redesigning |

## Installation

### Claude Code / Ducc

```bash
# If the platform supports the skill install command
claude skill install skill-evaluator --from github:sunxingboo/skill-evaluator

# Or clone manually
git clone https://github.com/sunxingboo/skill-evaluator.git ~/.claude/skills/skill-evaluator
```

### Manual

Copy `SKILL.md` along with `references/` and `scripts/` directories to your Agent's skill directory:

```bash
git clone https://github.com/sunxingboo/skill-evaluator.git ~/.claude/skills/skill-evaluator
```

## Configuration

### Qianfan API (Strategy B)

Strategy B calls multiple real models via the Baidu Qianfan LLM platform API. Set up the authentication token first:

```bash
export QIANFAN_BEARER_TOKEN="bce-v3/your-token-here"
```

If the token is not configured, Strategy B is unavailable and multi-model mode will automatically degrade to Strategy C (serial multi-perspective).

## Usage

```
/skill-evaluator
```

Or describe your intent in natural language:

### Evaluate a Single Skill

> Evaluate the skill `my-awesome-skill`

### Compare Multiple Skills

> Compare `skill-a` and `skill-b`, which one is better?

### Evaluate by Path

> Evaluate the skill at `~/projects/my-skill/SKILL.md`

### Multi-Model Cross-Validation

> Evaluate `my-awesome-skill` with multi-model cross-validation

You'll be asked whether to customize the main model and evaluator model list first. Skip to use defaults.

### Custom Model List

> Evaluate `my-awesome-skill` using sonnet and GLM-5

### Specify Main Model (Arbiter)

> Evaluate `my-awesome-skill` with multi-model, use sonnet as main model

### Multi-Perspective Mode

> Evaluate `my-awesome-skill` with multi-perspective mode

## Cross-Validation Pipeline

Automatically selects execution strategy based on actual results (A → B → C degradation):

### Strategy A: Parallel Multi-Model (Default)

```
┌──────────────────────────────────────────────────────┐
│  Phase 0: Confirm Model Config (ask user)            │
│                                                      │
│  Main model (arbiter): default Claude Opus 4.6       │
│  Evaluators: default Sonnet 4.6 / GLM-5 / MiniMax   │
│                                                      │
├──────────────────────────────────────────────────────┤
│  Phase 1: Parallel Independent Evaluation            │
│                                                      │
│  ┌──────────┐  ┌───────┐  ┌──────────────┐          │
│  │ Sonnet   │  │ GLM-5 │  │ MiniMax-M2   │          │
│  │ 4.6 eval │  │ eval  │  │ Stable eval  │          │
│  └────┬─────┘  └───┬───┘  └──────┬───────┘          │
│       │            │             │                   │
├───────┴────────────┴─────────────┴───────────────────┤
│  Phase 2: Pairwise Peer Review                       │
│                                                      │
│  Sonnet reviews GLM-5/MiniMax scores                 │
│  GLM-5 reviews Sonnet/MiniMax scores                 │
│  MiniMax reviews Sonnet/GLM-5 scores                 │
│                                                      │
│  Flag disagreements >= 2 points                      │
│                                                      │
├──────────────────────────────────────────────────────┤
│  Phase 3: Arbitration                                │
│                                                      │
│  ┌──────────────────────────────────────┐            │
│  │  Main model (default: Opus 4.6)     │            │
│  │  synthesizes all evaluations        │            │
│  │  + peer reviews                     │            │
│  │                                     │            │
│  │  Unanimous → average                │            │
│  │  Majority  → adopt majority         │            │
│  │  Disputed  → judge by evidence      │            │
│  └──────────────────────────────────────┘            │
│                                                      │
│  Output: final scores + consensus                    │
│          + improvement suggestions                   │
└──────────────────────────────────────────────────────┘
```

### Strategy B: Qianfan API Multi-Model (Fallback when Strategy A fails)

```
┌──────────────────────────────────────────────────────┐
│  Phase 0: Confirm Model Config (ask user)            │
│                                                      │
│  Main model (arbiter): current Agent itself           │
│  Evaluators: ernie-5.0 / deepseek-v3.2 /            │
│              qwen3.5 / glm-5.1                       │
│                                                      │
├──────────────────────────────────────────────────────┤
│  Phase 1: Qianfan API Parallel Evaluation            │
│                                                      │
│  python scripts/qianfan_chat.py --models ...         │
│                                                      │
│  ┌──────────┐  ┌──────────┐  ┌────────┐  ┌───────┐  │
│  │ ernie    │  │ deepseek │  │ qwen   │  │ glm   │  │
│  │ -5.0     │  │ -v3.2    │  │ 3.5    │  │ -5.1  │  │
│  └────┬─────┘  └────┬─────┘  └───┬────┘  └───┬───┘  │
│       │             │            │            │      │
├───────┴─────────────┴────────────┴────────────┴──────┤
│  Phase 2: Qianfan API Peer Review                    │
│                                                      │
│  Each model reviews others' scores                   │
│  Flag disagreements >= 2 points                      │
│                                                      │
├──────────────────────────────────────────────────────┤
│  Phase 3: Arbitration (main Agent)                   │
│                                                      │
│  Unanimous → average                                 │
│  Majority  → adopt majority                          │
│  Disputed  → judge by evidence                       │
│                                                      │
│  Output: final scores + consensus                    │
│          + improvement suggestions                   │
└──────────────────────────────────────────────────────┘
```

### Strategy C: Serial Multi-Perspective (Fallback when Strategy A/B unavailable)

```
┌─────────────────────────────────────────────┐
│  Phase 1: Serial Multi-Perspective Eval     │
│                                             │
│   ┌────────────┐                            │
│   │  Strict    │ → norms, edge cases        │
│   │  Reviewer  │                            │
│   └─────┬──────┘                            │
│         ↓                                   │
│   ┌────────────┐                            │
│   │ Pragmatic  │ → usability, UX            │
│   │  Reviewer  │                            │
│   └─────┬──────┘                            │
│         ↓                                   │
│   ┌────────────┐                            │
│   │  Expert    │ → depth, professionalism   │
│   │  Reviewer  │                            │
│   └─────┬──────┘                            │
│         │                                   │
├─────────┴───────────────────────────────────┤
│  Phase 2: Self Cross-Review                 │
│                                             │
│   Compare 3 perspectives, flag gaps >= 2    │
│   Analyze disagreement reasons              │
│                                             │
├─────────────────────────────────────────────┤
│  Phase 3: Arbitration                       │
│                                             │
│   Unanimous → average                       │
│   Majority  → adopt majority                │
│   Disputed  → judge by evidence             │
│                                             │
│   Output: final scores + consensus          │
│           + improvement suggestions         │
└─────────────────────────────────────────────┘
```

## Output Examples

### Single-Model Evaluation

```
## Skill Evaluation Report

### my-awesome-skill

**Composite Score: 7.8 / 10 (Grade A)**

| Dimension | Score | Notes |
|-----------|-------|-------|
| D1. Metadata Quality | 8/10 | Clear description with trigger conditions |
| D2. Execution Guidance Clarity | 7/10 | Good for most cases, lacks error handling |
| D3. Domain Knowledge Density | 9/10 | Rich expert knowledge and best practices |
| D4. Workflow Completeness | 8/10 | Complete multi-step workflow |
| D5. Input/Output Clarity | 7/10 | Has output format, missing input examples |
| D6. Resource Utilization | 7/10 | N/A — no resources needed |
| D7. Writing Quality | 8/10 | Well-structured, logical flow |
| D8. Scope & Focus | 8/10 | Focused on a single problem domain |

#### Issues & Suggestions
1. **D2. Execution Guidance Clarity**: Missing error handling → Add branching for incomplete input
2. **D5. Input/Output Clarity**: Missing input examples → Add 2-3 concrete input examples in usage section
```

### Multi-Model Cross-Validation

```
## Skill Evaluation Report (Multi-Model Cross-Validation)

### my-awesome-skill

> Main Model: Claude Opus 4.6 | Evaluators: Claude Sonnet 4.6, GLM-5, MiniMax-M2-Stable

#### Independent Evaluations

##### Sonnet 4.6 Evaluation
| Dimension | Score | Notes |
|-----------|-------|-------|
| D1. Metadata Quality | 8/10 | ... |
| D2. Execution Guidance Clarity | 7/10 | ... |
| D3. Domain Knowledge Density | 9/10 | ... |
| D4. Workflow Completeness | 8/10 | ... |
| D5. Input/Output Clarity | 7/10 | ... |
| D6. Resource Utilization | 7/10 | ... |
| D7. Writing Quality | 8/10 | ... |
| D8. Scope & Focus | 8/10 | ... |
| **Composite** | **7.9/10 (A)** | |

(GLM-5 and MiniMax-M2-Stable evaluations follow)

#### Cross-Validation Highlights

| Dimension | Disagreement | Details |
|-----------|-------------|---------|
| D3. Domain Knowledge | Sonnet(9) vs MiniMax(6) | Sonnet cites rich expert knowledge; MiniMax finds depth lacking |

> 1 dimension with significant disagreement (>= 2 points), 7 dimensions unanimous.

#### Final Arbitrated Verdict

**Final Composite Score: 7.8 / 10 (Grade A)**

| Dimension | Final Score | Consensus | Arbitration Notes |
|-----------|------------|-----------|-------------------|
| D1. Metadata Quality | 8/10 | Unanimous | All models agree |
| D3. Domain Knowledge | 8/10 | Arbitrated | Sonnet and GLM-5 scored 8-9; MiniMax scored 6; majority opinion adopted |

#### Issues & Suggestions
1. **D2. Execution Guidance** (Consensus: Unanimous): Missing error handling → Add branching logic
```

## Contributing

Pull requests are welcome.

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT — see [LICENSE](LICENSE).
