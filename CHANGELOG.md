# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.2.0] - 2026-04-15

### Added
- `--prompt-files` parameter for `qianfan_chat.py`: supports per-model prompt files for batch parallel calls (e.g., `--prompt-files model1:/path1,model2:/path2`), enabling parallel cross-review in a single invocation
- `--retry` parameter for `qianfan_chat.py`: built-in retry for failed API requests (default: 0)
- Placeholder legend in `references/prompts.md` documenting all `{{VAR}}` template variables

### Changed
- Shortened SKILL.md frontmatter `description` for better Agent matching efficiency
- Added `version` field to SKILL.md frontmatter
- Reordered strategy sections to A → B → A+B → C (simple to composite) for clearer reading flow
- Strategy B cross-review now shows parallel Bash calls and `--prompt-files` usage instead of serial examples
- Strategy A+B cross-review updated to reference `--prompt-files` for non-native model parallel calls
- Unified prompt template placeholders to `{{VAR}}` syntax with a reference table
- Expanded all report format templates to show complete D1-D8 dimension rows
- Aligned README_EN.md output examples with README.md (full dimension tables)
- Fixed install commands in both READMEs: added manual clone fallback, noted `references/` and `scripts/` directories
- Set worker threads as daemon threads in `qianfan_chat.py` to prevent resource leaks
- Added `*.tmp` and `/tmp/` to `.gitignore`

## [2.1.0] - 2026-04-15

### Added
- Strategy B: Qianfan API multi-model evaluation — calls multiple real models (ernie-5.0, deepseek-v3.2, qwen3.5, glm-5.1) via Baidu Qianfan LLM platform API
- `scripts/qianfan_chat.py`: zero-dependency Python script for Qianfan API calls, supports single-model and batch-parallel modes
- Three-level automatic degradation chain: A (subagent parallel) → B (Qianfan API) → C (serial multi-perspective)
- Qianfan API configuration via `QIANFAN_BEARER_TOKEN` environment variable

### Changed
- Renamed Strategy B (serial multi-perspective) to Strategy C to accommodate new Qianfan API strategy
- Strategy selection is now fully automatic and transparent to users — users only choose single vs multi-model
- Updated prompt templates to annotate Strategy B reuse (same templates as Strategy A)
- Updated report format references for A/B/C naming

## [2.0.0] - 2026-04-14

### Added
- Multi-model cross-validation: parallel independent evaluation by multiple models
- Pairwise peer review: each model reviews others' scores, challenges disagreements >= 2 points with evidence
- Arbitration: designated arbiter synthesizes all evaluations and peer reviews into authoritative final verdict
- Serial multi-perspective fallback (Strategy C): same model evaluates as Strict/Pragmatic/Expert reviewers when Strategy A/B fail
- Automatic strategy selection: falls back to Strategy B then C only when previous strategy explicitly fails or is unavailable; no platform-name-based assumptions
- Consensus indicators: each dimension labeled as "Unanimous", "Majority", or "Arbitrated"
- Interactive model selection: proactively asks user to specify main model and evaluator list before using defaults
- Multi-model and multi-perspective evaluation report formats
- Cost guidance for multi-model mode (approximately 7x single-model token usage)

### Changed
- Default models changed to cross-vendor mix: main model Claude Opus 4.6, evaluators Claude Sonnet 4.6 + GLM-5 + MiniMax-M2-Stable
- Model selection is now user-first: always ask user before falling back to defaults
- Restructured SKILL.md: extracted evaluation dimensions and scoring into standalone sections (single source of truth)
- Dual-mode workflow: single-model (default, backward-compatible) and multi-model (opt-in)
- Updated description in frontmatter to mention cross-validation capability and trigger words

## [1.0.0] - 2026-04-13

### Added
- Initial release of skill-evaluator
- 8-dimension evaluation framework with weighted scoring
- Grade mapping system (S/A/B/C/D)
- Multi-Skill side-by-side comparison support
- Actionable improvement suggestions for weak dimensions
