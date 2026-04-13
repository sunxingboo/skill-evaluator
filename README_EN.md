# skill-evaluator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) | [中文](README.md)

An AI Agent Skill for evaluating the quality of other Skills. It scores Skills across 8 weighted dimensions, identifies weaknesses, provides actionable improvement suggestions, and supports side-by-side comparison of multiple Skills.

Compatible with any AI Agent platform that supports the Skill mechanism, including Claude Code, Ducc, and others.

## Features

- **Multi-dimensional scoring** — 8 weighted dimensions, 0-10 each
- **Grade mapping** — Composite score maps to S/A/B/C/D grades
- **Actionable feedback** — Problem description, impact analysis, and concrete suggestions for each weak dimension
- **Multi-Skill comparison** — Side-by-side scoring table, strengths/weaknesses analysis, and ranking

## Evaluation Dimensions

| Dimension | Weight |
|-----------|--------|
| D1. Metadata Quality | 15% |
| D2. Execution Guidance Clarity | 15% |
| D3. Domain Knowledge Density | 15% |
| D4. Workflow Completeness | 15% |
| D5. Input/Output Clarity | 10% |
| D6. Resource Utilization | 10% |
| D7. Writing Quality | 10% |
| D8. Scope & Focus | 10% |

## Installation

### Claude Code / Ducc

```bash
claude skill install skill-evaluator --from github:sunxingboo/skill-evaluator
```

### Manual

```bash
git clone https://github.com/sunxingboo/skill-evaluator.git ~/.claude/skills/skill-evaluator
```

For other Agent platforms, place `SKILL.md` in the corresponding skill directory.

## Usage

```
/skill-evaluator
```

Or describe your intent in natural language:

- **Evaluate a Skill** — "Evaluate the skill `my-awesome-skill`"
- **Compare Skills** — "Compare `skill-a` and `skill-b`, which one is better?"
- **Evaluate by path** — "Evaluate the skill at `~/projects/my-skill/SKILL.md`"

## License

MIT — see [LICENSE](LICENSE).
