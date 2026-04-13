# skill-evaluator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) | [English](README_EN.md)

一个用于评估 AI Agent Skill 质量的 Skill。从 8 个维度对 Skill 进行加权打分，找出不足并给出改进建议，支持多个 Skill 横向对比。

兼容所有支持 Skill 机制的 AI Agent 平台，包括但不限于 Claude Code、Ducc 等。

## 特性

- **多维度打分** — 8 个加权维度，每个维度 0-10 分
- **等级映射** — 综合得分自动映射为 S/A/B/C/D 等级
- **改进建议** — 对每个薄弱维度给出问题描述、影响分析和具体建议
- **多 Skill 对比** — 并列评分表、优劣势分析和排名

## 评估维度

| 维度 | 权重 | 说明 |
|------|------|------|
| D1. 元数据质量 | 15% | YAML frontmatter 中 `name` 和 `description` 的质量 |
| D2. 执行引导清晰度 | 15% | Skill 加载后 Agent 是否清楚如何执行 |
| D3. 领域知识密度 | 15% | 是否内嵌了通用 Agent 不具备的专业知识 |
| D4. 工作流完整性 | 15% | 是否定义了端到端的工作流，含分支和异常处理 |
| D5. 输入输出清晰度 | 10% | 用户是否知道该提供什么、能得到什么 |
| D6. 资源利用 | 10% | 对 scripts、references、assets 等附带资源的利用 |
| D7. 写作质量 | 10% | 结构清晰度、可读性和表述精确性 |
| D8. 范围与聚焦 | 10% | 是否专注解决一类问题，既不过宽也不过窄 |

## 等级标准

| 分数 | 等级 | 含义 |
|------|------|------|
| 9.0-10 | S | 卓越 — 标杆级 Skill |
| 7.5-8.9 | A | 优秀 — 可直接使用，仅需少量打磨 |
| 6.0-7.4 | B | 合格 — 可用但有明显改进空间 |
| 4.0-5.9 | C | 较弱 — 需要大幅修改 |
| 0-3.9 | D | 较差 — 存在根本性问题，建议重新设计 |

## 安装

### Claude Code / Ducc

```bash
claude skill install skill-evaluator --from github:sunxingboo/skill-evaluator
```

### 手动安装

将 `SKILL.md` 复制到你的 Agent 的 Skill 目录。以 Claude Code / Ducc 为例：

```bash
git clone https://github.com/sunxingboo/skill-evaluator.git ~/.claude/skills/skill-evaluator
```

其他 Agent 平台请将 `SKILL.md` 放置到对应的 Skill 目录下。

## 使用

通过斜杠命令调用（如果你的 Agent 支持）：

```
/skill-evaluator
```

也可以直接用自然语言描述意图：

### 评估单个 Skill

> 帮我评估一下 `my-awesome-skill` 这个 Skill

### 对比多个 Skill

> 对比 `skill-a` 和 `skill-b`，哪个设计更好

### 按路径评估

> 评估 `~/projects/my-skill/SKILL.md` 这个 Skill

## 输出示例

```
## Skill 评估报告

### my-awesome-skill

**综合得分：7.8 / 10（等级 A）**

| 维度 | 分数 | 说明 |
|------|------|------|
| D1. 元数据质量 | 8/10 | 清晰的 description，包含触发条件 |
| D2. 执行引导清晰度 | 7/10 | 多数场景有引导，缺少异常处理 |
| D3. 领域知识密度 | 9/10 | 丰富的专家知识和最佳实践 |
| D4. 工作流完整性 | 8/10 | 完整的多步骤工作流 |
| D5. 输入输出清晰度 | 7/10 | 有输出格式，缺少输入示例 |
| D6. 资源利用 | 7/10 | N/A — 无需附带资源 |
| D7. 写作质量 | 8/10 | 结构清晰，逻辑流畅 |
| D8. 范围与聚焦 | 8/10 | 聚焦于单一问题域 |

#### 问题与建议
1. **D2. 执行引导清晰度**：缺少异常情况处理指引 → 添加 "当用户输入不完整时" 的分支逻辑
2. **D5. 输入输出清晰度**：缺少输入示例 → 在使用场景部分添加 2-3 个具体输入示例
```

## 贡献

欢迎提交 Pull Request。

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 发起 Pull Request

## 许可证

本项目采用 MIT 许可证，详见 [LICENSE](LICENSE)。
