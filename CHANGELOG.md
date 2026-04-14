# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.0.0] - 2026-04-14

### Added
- Multi-model cross-validation: parallel independent evaluation by multiple models
- Pairwise peer review: each model reviews others' scores, challenges disagreements >= 2 points with evidence
- Arbitration: designated arbiter synthesizes all evaluations and peer reviews into authoritative final verdict
- Serial multi-perspective fallback (Strategy B): same model evaluates as Strict/Pragmatic/Expert reviewers when Strategy A fails
- Automatic strategy selection: falls back to Strategy B only when Strategy A explicitly fails or reports unsupported; no platform-name-based assumptions
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
