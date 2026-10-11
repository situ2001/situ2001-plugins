# OpenAI 官方博客与 situ2001 本机工作流对照

研究日期：2026-10-10。仓库：`/home/situ/agent-plugins`，其 README 确认 marketplace 名为 `situ2001-plugins`。本报告记录建议，不修改配置、hooks 或 skills。

阅读范围：读取 [OpenAI Developer Blog 当前索引](https://developers.openai.com/blog)列出的全部 **30 篇文章正文**，并补读两篇 OpenAI 公司工程博文；不是宣称读完 OpenAI 公司博客全部历史文章。下方先详细对照直接相关的文章，末尾逐篇记录全部开发者博客的适用判断。示例中的旧模型、API 参数和权限策略不自动成为本机配置建议。

最先建议处理：**安装脚本依赖缺失、Linux 路径不适用、两个 hook 的解析误拦截**。这些已有本机证据。缩短 skills、调整模型角色与降低推理强度属于值得验证的优化，尚无本次 A/B 实验结果。

## 本机基线与证据边界

- 仓库 revision：`ad5282f3b1e568f9df4a2d133fd3f54c46e78afe`；开始时已有未跟踪的 `skills/agent-team/tests/__pycache__/`，本次保留。
- CLI：`codex-cli 0.160.0`。`~/.codex/config.toml`：`model = "gpt-6.1-sol"`、`model_reasoning_effort = "medium"`、`approval_policy = "never"`、`sandbox_mode = "danger-full-access"`。`/home/situ` 被标记 trusted；trusted 不是文件访问范围限制。
- 个人 marketplace：`~/.agents/plugins/marketplace.json` → `./plugins/agent-plugins`；`~/plugins/agent-plugins` 是指向本仓库的 symlink。`situ2001@situ2001-plugins` 在配置中 enabled。
- 插件缓存版本：`1.1.0+261008155529`。源与缓存的全部 **15 份 SKILL.md 逐字节一致**，本次没有发现 skill 源已更新而安装缓存落后的问题。没有据此断言所有非 skill 文件或活跃会话都已同步。
- 磁盘还有 **39 个全局 skills**，来自 `~/.agents/skills`。插件根 skill 正文合计 67,723 bytes。安装数量、正文体积、当前技能目录和每个任务实际加载量是不同概念；这些 bytes 不是每次调用的提示词 token 数。
- Claude 的非敏感配置显示其主模型为 DeepSeek，子代理模型另设。OpenAI 模型博文中的表现结论不能直接套到 Claude 的这个配置。研究文档不保存凭据。
- `hooks/hooks.json` 有 SessionStart 指令注入与两个 Bash PreToolUse 检查；配置有相应 hook trust 记录。本次脚本输入回放验证了解析行为，没有启动另一轮真实 agent 会话来证明每种工具路径的 hook 覆盖。

当前官方 [hooks 契约](https://learn.chatgpt.com/docs/hooks)明确 Bash 使用 `tool_input.command`，并说明 hooks 默认开启、插件安装与 hook trust 是不同步骤。因此不建议凭空增加 `cmd` 兼容分支，也不建议把缺少 `[features].hooks = true` 判为配置故障。

## 优先行动：改什么、为什么、如何验收

| 顺序 | 要处理的具体位置 | 建议改动 | 验收依据 |
| --- | --- | --- | --- |
| 先处理 | [plugin setup](../../skills/situ2001-plugin-setup/SKILL.md) 的四个 `plugin-creator/scripts/` 路径 | 它们在本机均不存在。把必要流程改为经核实的当前 CLI 或插件自带的小脚本；现有 `scripts/refresh-plugin-version.py` 继续拥有本仓库版本格式 | 用独立临时 marketplace/配置目录验证初次安装和刷新；不为了测试覆盖本人的已安装插件 |
| 先处理 | [obsidian-vault](../../skills/obsidian-vault/SKILL.md) 第 13 行 | 配置一个明确的本机 vault 路径，沿用读取其 AGENTS.md 的规则。当前 `/home/situ/Library/Mobile Documents/.../situ-vault` 不存在；不要猜一个 Linux 路径或搜索整个磁盘里的私人笔记 | 配置值指向存在的 vault，可读取根 AGENTS.md；未配置时明确缺少什么 |
| 先处理 | 两个 [hook 脚本](../../hooks/scripts/) | 按实际命令位置和参数范围解析，避免把另一条命令的 flag 或引用数据当成目标命令 | 下面的合法反例放行，实际 `rg -rn` 和超范围删除继续拒绝 |
| 随后处理 | [grilling-focused-with-docs](../../skills/grilling-focused-with-docs/SKILL.md) | 将只存在于特定运行时的 “Call the Skill tool twice” 改为读取并应用两个基础 skill 的语义；保留显式触发要求 | 在 Codex 与 Claude 分别显式调用，确认两个基础流程确实被加载，而非仅口头声称使用 |
| 随后验证 | [behavior-verification](../../skills/behavior-verification/SKILL.md)、[agent-team](../../skills/agent-team/SKILL.md) 等长根文档 | 保留核心契约、触发和完成条件，把具体执行与报告细则按任务分支放 references；不要按固定字数截断关键要求 | 用同一批任务对照读取分支、结果正确性与耗时，精简不能丢失验收和授权语义 |
| 随后验证 | [agent-team 的模型表](../../skills/agent-team/references/codex-builtin.md) | 默认 Sol Medium 可继续使用；复杂执行/独立审查再考虑 High，窄范围信息搜集可试 Luna。当前固定所有执行者 Sol High 是个人策略，不是官方保证的最优组合 | 使用相同 revision、提示、输入、验收，分别比较成功、误修改、完成耗时和 token；保留失败样本 |
| 长任务采用 | [handoff](../../skills/situ-handoff/SKILL.md) 与项目 docs | 维护一个项目内状态入口，包含目标、现状、验收命令、决策和下一步；handoff 引用入口。macOS 默认保存位置不存在时，当前 skill 的 cwd fallback 已定义，应明确告知实际保存位置 | 新会话只用这些入口能恢复未完成事项；不把四份文件模板强加到小任务 |

这里的路径配置处理的是已经存在的 macOS/Linux 差异；不是要求增加一套猜测路径、重试或自动恢复框架。模型调整也不需要立即改变全局默认值。当前官方 [Subagents 文档](https://learn.chatgpt.com/docs/agent-configuration/subagents)提供角色配置与继承机制；实际 spawn 能力仍以当前工具声明为准。

证据约定：**已观察**指实际读取的本地文件；**官方观点**指链接文章正文；**建议/推断**是结合两者得出的判断，不代表官方要求。文章发布时间取官方索引或正文。博客讲述的实现有时间背景，不能替代当前产品配置参考。

## 重点文章逐篇对照

### 2026-09-11：Rethinking skills and prompts for GPT-6 Astra

[官方全文](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra)

官方观点：skills 的 description 应简短且准确，多个流程的根文档应作为 router；旧模型需要的详细步骤、全库预读、审批提示和反复测试要求，在 Astra 上可能增加上下文和过早停止。应写清完成边界，并按所用模型审视旧指令。

已观察：`skills/agent-team/SKILL.md:14` 已按运行时只读一份 guide；`skills/behavior-verification/SKILL.md:28` 允许已有证据足够时停止验证；`skills/setup-my-skills/SKILL.md:22` 默认安装上游全部 skills。`skills/agent-team/SKILL.md:12` 区分 Astra 导演与 Sol 执行者。

建议：保留已有按需加载和聚焦验证；优先审计全量上游安装带来的实际路由负担。不要直接把 Astra 特性推广成 Sol 6.1 Medium 的行为结论。以相同任务比较精简前后，再决定删除哪些提示。

### 2026-01-22：Testing Agent Skills Systematically with Evals

[官方全文](https://developers.openai.com/blog/eval-skills)

官方观点：先定义可检查结果，再用显式、隐式、带上下文的触发样例及不应触发的反例验证 skill；`codex exec --json` 保存轨迹，确定性检查优先，必要时用 `--output-schema` 做结构化评审。较重运行检查按收益增加。

已观察：仓库有 session 提取器和 agent-team wait 的脚本测试；没有发现统一的 skills 路由评估目录。`AGENTS.md` 所列 quick_validate 是文档/包结构验证，不能证明模型选对了 skill。

建议：从实际易混淆的边界建立回归样例：`benchmark-workload` 对实际运行资源；`codex-session-analysis` 对历史会话；`show-me-the-architecture` 对现有架构讲解；`frontend-demo-preview` 对临时预览。检查是否选对 skill、产物是否满足要求、有无未经要求的修改。先保存事实和逐项通过结果，无需发明综合质量分数。

### 2026-03-09：Using skills to accelerate OSS maintenance

[官方全文](https://developers.openai.com/blog/skills-agents-sdk)

官方观点：仓库政策、窄职责 skills、确定性脚本与模型判断配合；通过 if/then 指定必要验证，文档工作不用完整运行验证。当地工作流稳定后再迁到 CI。公开输入的自动化应处理真实的触发器、凭据与权限边界。

已观察：本仓库 `AGENTS.md` 已把版本刷新和校验限定在插件实际改动后；`scripts/refresh-plugin-version.py` 封装时间戳机制。`hooks/scripts/` 包含搜索参数和删除范围检查。

建议：继续保持条件式验证，把重复的插件发布校验收敛成一个有明确输入/输出的脚本；在稳定本地流程和记录真实失败后再考虑 CI。不要为一份研究文档触发重装插件。自动化 release review 应审具体 diff 和契约，不以假设故障阻塞。

### 2026-02-23：Run long horizon tasks with Codex

[官方全文](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex)

官方观点：长期执行依赖可复读的规格、里程碑、验收和状态；文章的 25 小时、13M tokens 属 GPT-5.3-Codex Extra High 实验，作者明确未宣称生产就绪。

已观察：`skills/situ-handoff/SKILL.md:10` 记录目标、决策、进展和后续行动，但主要是换会话交接；`skills/agent-team/SKILL.md:34` 已要求 outcome、authority、ownership、return contract。

建议：对确实跨多个阶段的任务，把规格、当前里程碑、验收命令与决策存于当前项目中的一个可恢复文档；小任务继续轻量。交接引用这个持续维护的状态，不重新复制完整聊天。不把实验运行时间、token 数或文件堆栈当作个人任务标准。

### 2026-02-11：Shell + Skills + Compaction

[官方全文](https://developers.openai.com/blog/skills-shell-tips)

官方观点：description 决定路由，负例有助于区分相邻任务，模板按需加载；Responses API 长任务可复用容器、继续响应并压缩上下文。hosted shell 的网络策略、domain secrets 和 `/mnt/data` 属其执行边界。

已观察：`skills/codex-session-analysis/SKILL.md` 与 `skills/benchmark-workload/SKILL.md` 都有明确反例；references 已用于详细流程。当前任务操作的是本地目录。

建议：结合较新的 Astra 文，description 留任务、触发点和必要的一条排除语；更多负例放 references 或 eval 样例。不要把 API 的 `previous_response_id`、`network_policy` 或 `/mnt/data` 搬成 Codex CLI 配置。网络与凭据隔离应根据实际调用工具的契约处理。

### 2026-07-20：Custom Code Review rules for Codex

[官方全文](https://developers.openai.com/blog/custom-code-review-rules-for-codex)

官方观点：在适用范围的 `AGENTS.md` 写少量重要且不明显的不变量，同时写清安全路径；用应触发、合法反例和无关改动检查规则。机械检查放 CI，规则承载难编码的判断。

已观察：根 `AGENTS.md` 已解释双 manifest 一致、Codex UTC timestamp、Claude 版本语义、重装顺序。这些都是插件更改容易漏掉的项目契约。

建议：新增审阅用的条件式条目时，优先覆盖 manifest 描述/版本一致、源文件与安装缓存关系、skill 的跨运行时可执行性；要求 findings 引用违反的具体契约和改变行为的路径。UTC 格式等确定性部分由脚本检查，不让模型每次重新判断。

### 2026-08-25：Automating repetitive work at OpenAI with Codex

[官方全文](https://developers.openai.com/blog/automating-repetitive-work-at-openai-with-codex)

官方观点：Runme 把意图、计划、执行、结果与决策放同一 notebook，索引帮助后续发现；人参与重要选择，重复执行交给 agent。其示例的计划审批用于实际评测运营工作，不是所有本地任务都必须审批。

已观察：本插件已具备 handoff、research 文件、session analysis 和重点访谈；`skills/situ-handoff/SKILL.md:23` 默认路径属于 macOS，并有落到当前目录的约定。

建议：以项目 Markdown 和本地索引先实现可检索的运行记录，积累能改善下一次执行的决策与已知失败。没有 notebook 协同需求时无需引入 Runme 或 Google Drive。授权明确的可逆执行继续完成；把必须人决策的边界写成具体动作。

### 2026-08-19：Codex as a platform

[官方全文](https://developers.openai.com/blog/codex-as-a-platform)

官方观点：复用 Codex harness 的 agent loop；一次性自动化用 exec，程序启动/恢复工作用 SDK，持续交互产品用 app-server。产品仍拥有业务上下文、记录和动作批准。

已观察：当前仓库交付的是个人 skills 和 hooks，不是包含持续对话 UI 的产品；agent-team 的 references 已分别处理内建协作与 Herdr。

建议：未来要自动运行插件评估或校验，先选 `codex exec`；只有需要持续任务界面、流式事件、interrupt 和权限交互才评估 app-server。不要为现有技能集合重造 agent runtime。

### 2026-02-11：Harness engineering

[官方全文](https://openai.com/index/harness-engineering/)

官方观点：简短入口映射到仓库知识；复杂任务有可恢复计划；有价值的规则用机械检查落实；调试依赖 agent 可观察的 UI、日志、指标。作者强调其端到端自主行为依赖特定工具与结构。

已观察：已有 `docs/research`、hooks 脚本、behavior-verification references；README 尚是最小安装入口。

建议：README 加只读导航，指出配置/版本、hook 契约、技能适用范围与相关研究的位置。现有删除/rg 检查属于具体操作边界，可评估其真实输入覆盖；不照搬博客的质量打分、固定架构层、任意文件上限或自动合并策略。

### 2026-01-23：Unrolling the Codex agent loop

[官方全文](https://openai.com/index/unrolling-the-codex-agent-loop/)

官方观点：harness 拼装模型指令、权限、项目文档与 skill 元数据，工具结果继续进入上下文；精确前缀影响缓存；该文写作时 CLI 采用无状态请求与自动压缩。CLI shell 的沙箱不等于 MCP 工具的边界。

已观察：本仓库的 SessionStart 注入 coding guidance；其余技能按任务读。阅读硬编码工具名与实际运行时工具是否一致，可比盲目增加提示更直接。

建议：用真实会话确认启动时可见技能与实际加载内容，不从磁盘安装数推导模型看到的数。比较精简前后缓存/输入/耗时，并避免无必要地在同一任务中改变模型和工具集合。该文的 1 月实现细节须以当前 CLI 行为复核。

## 从文章映射到本机的改进维度

下面是结合文件和文章的建议，未宣称已经实际改变或跑完模型行为评估。

| 维度 | 本地证据 | 具体建议 | 怎样判断有效 |
| --- | --- | --- | --- |
| 技能选择与上下文 | setup-my-skills 默认安装全部上游；多个 personal skills 已有窄触发 | 先列出安装、当前可见、实际选用三个清单；只处理重叠或误触发的项，保留显式调用入口 | 相同提示的正例选对、反例不误选；输入和读取文件减少 |
| 渐进加载 | agent-team 按 runtime 读取一份 guide；behavior-verification 分宿主 references | 保留此结构；只把确实重复且长的分支从根文档移到引用 | 任务只读取相关分支；关键条件仍可找到 |
| 自主性与完成定义 | agent-team 已认可已有确认，区分可逆细节与新方向 | 对已确认需求避免重复访谈；具体列出需要人决策的动作，执行者完成其 scope 的运行和修复 | 不重复请求已授权步骤；所有已承诺验收有证据 |
| 跨运行时契约 | grilling-focused-with-docs 第 7 行要求 Skill tool twice；Codex 当前以文件读 skill | 改为工作流语义和可访问资源引用；运行时专有工具放 adapter/reference | 显式调用后两个基础工作流均被实际读取与使用 |
| 安装依赖闭合 | situ2001-plugin-setup 第 15、30、50、51 行引用本机不存在的 plugin-creator helpers；本仓库 refresh 脚本存在 | 先替换已不可执行的 helper 依赖；用确认可用的当前 CLI 或插件自有小 helper，保持既有 manifest/marketplace 契约 | 初次安装与刷新都能实际完成，不依赖机器上未安装的私有脚本 |
| 行为评估 | quick_validate 检查结构；已有少量脚本单测与 session extractor | 从实际易混淆边界建立 trace+artifact 回归，用确定性事实优先 | 路由、scope、产物、边界错误能单独定位 |
| 验证强度 | behavior-verification 第 28 行反对无意义新 harness | 保留聚焦契约；重流程只服务复杂任务或具体失败 | 原始失败和修复能被相同验收区分，普通文案不触发额外测试 |
| 持续知识与本机路径 | handoff 优先 macOS vault，Linux 使用 fallback；research 已有仓库位置 | 把项目长任务状态存项目内；个人 vault 用用户已确认的本机路径配置，避免到处复制路径 | 新会话能按链接恢复，定位到本机真实目录 |
| 发布与审阅 | AGENTS 双 manifest、UTC version、验证后重装 | 保留契约；重复校验做小 CLI，审阅关注行为风险而非格式重复劳动 | 无变更时不刷新版本；有变更时源与发布产物可追溯 |
| 安全与工具边界 | hooks/hooks.json 仅声明 Bash matcher；实际工具和输入字段需复核 | 验证平台真实 hook payload、可信配置与可写目录；对不可信输入用独立隔离运行 | 受支持的输入实际阻止目标命令，正常命令通过；不误称 shell hook 覆盖 MCP |
| 模型与成本 | agent-team 指定 Astra Medium 与 Sol High；博客实验使用不同代际模型 | 保持可比较任务和验收，分别观察执行/导演；用 session-analysis 事实决定配置 | 比较完成率、耗时、命令/输入量；API 成本不冒充订阅账单 |

### 已观察的 hook 误拦截

主审查已用当前官方 Bash hook 的 `tool_input.command` JSON 契约，将输入交给两个 Python hook；只执行 hook 脚本，未执行字符串中的命令。

- `rg pattern .; grep -rn pattern .` 被 rg hook 拒绝：脚本发现任何 `rg` token 后扫描整串 flags，把后续合法 `grep -rn` 当成 rg 参数。源码依据：`hooks/scripts/check-rg-footgun.py:48` 和第 53 行。`rg pattern .; printf %s -rn` 也被误拒绝。
- `printf '%s %s' 'rm' '/tmp/situ-unused-path'` 被 deletion hook 拒绝：引用的数据被视为删除命令与目标。

建议将解析范围限定到实际命令位置及其参数，加入以上反例回归，保留现有有依据的目标约束。`command` 字段符合当前官方 hook 契约，不能把缺少 `cmd` 支持当作已证实缺陷。脚本回放证明解析行为，尚不能证明插件在每个真实工具调用里都执行了 hook。具体回放记录由主审查附入。

## 建议实施顺序

1. 先核对实际配置、skill 可见性、hook 输入契约与本机路径。发现契约差异时先修该差异。
2. 为最常用且易混淆的 skills 记录触发正反例与验收；先记录当前版本基线。
3. 只精简有重叠、误路由或反复停工证据的 description/根流程；保留用户要求的审批边界和验收。
4. 稳定后封装插件校验、积累长期任务状态与运行记录；是否上 CI、SDK、app-server、Runme 由实际需求决定。

以上是可 review 的建议顺序，未自行安排定时任务、更新依赖、重装插件或发布仓库。

## Developer Blog 全部 30 篇的逐篇阅读记录

顺序按研究当日索引排列。每一行是基于正文的适用判断：相关程度低的文章也读取了正文，但不为了覆盖文章而给本机增加无需求的配置。下列建议是本报告的映射，不是 OpenAI 要求本插件采用的架构。

| 文章 | 正文要点与本机对应建议 |
| --- | --- |
| [Bringing my LED display to life with GPT-Live-1 and Codex](https://developers.openai.com/blog/bringing-my-led-display-to-life) | 语音、研究与渲染分工；一次故障源于交接只传最新消息。agent-team brief 应保留当前任务相关的指代和既有结果，不能只转发一句新指令；没有硬件/语音需求时无需引入 GPT-Live。 |
| [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra) | 精简描述、根文档作为路由、重审旧指令。优先精简误触发或重复流程，Astra 专属行为不直接推广到 Sol。 |
| [Architectural visualization with Astra](https://developers.openai.com/blog/architectural-visualization-with-astra) | 可编辑模型、预览渲染和实际交互提供不同证据。你的 behavior-verification 应继续区分截图、状态检查与真实交互；普通工程项目无需增加 Blender。 |
| [Building games with Astra](https://developers.openai.com/blog/how-to-build-games-with-astra) | 固定场景、可观察状态、真实控制路径与资源指标共同支持修复。frontend-demo-preview 可提供复现入口；benchmark-workload 要保留相同场景，并区分软件渲染测量与硬件 GPU 帧率。 |
| [Meet Rosalind Workbench](https://developers.openai.com/blog/rosalind-workbench) | 问题、专业工具、分析与证据相连。可借鉴研究记录的可追溯性；未观察到生命科学需求，不提出模型或工具安装建议。 |
| [Automating repetitive work at OpenAI with Codex](https://developers.openai.com/blog/automating-repetitive-work-at-openai-with-codex) | 执行时积累可检索记录和决策。现有 docs/research 与 handoff 足以开始；仅有实际 notebook 协作需求时再引入 Runme。 |
| [Meet the winners of OpenAI Build Week](https://developers.openai.com/blog/build-week-winners) | 多个案例把模型理解与确定性的领域计算分开。对 hooks 的命令判断应执行可复现检查，不用模型“觉得安全”代替语义；不把获奖案例当个人工作流的性能证据。 |
| [Scaling cyber defenders with Daybreak](https://developers.openai.com/blog/scaling-cyber-defenders-with-daybreak) | 从可信发现、复现到补丁与回归验证。保留 de-defend/behavior-verification 的证据链；凭据与工具边界按实际操作处理。没有当前扫描任务时不强制装 Security 插件。 |
| [Codex as a platform](https://developers.openai.com/blog/codex-as-a-platform) | exec、SDK、app-server 服务不同集成深度。插件评估先用 exec；尚无持续产品界面需求，不重造 runtime。 |
| [Custom Code Review rules for Codex](https://developers.openai.com/blog/custom-code-review-rules-for-codex) | 少量重要不变量、合法路径与正反例。把双 manifest 和发布版本语义作为条件式审阅重点，机械格式用脚本验证。 |
| [Mastering remote engineering work from your phone](https://developers.openai.com/blog/mastering-codex-remote-for-engineering) | 执行环境、Queue/Steer、侧聊、Plan/Goal、review 各有角色。长任务先确定正确 repo/worktree；新任务与纠正当前方向要区分。移动端可用性需实际账户/host 验证，不据博客宣称已开通。 |
| [Making private MCP servers reachable without making them public](https://developers.openai.com/blog/connect-private-mcp-servers-to-openai-products) | 客户端主动出站、配置目标明确，工具连接不变成宽泛网络桥。未来确需从云端访问本地服务时考虑这一路径；现有本地 skills 不需要 tunnel。 |
| [How Perplexity Brought Voice Search to Millions](https://developers.openai.com/blog/realtime-perplexity-computer) | 小块上下文、正确消息角色、统一音频合同与真实环境测试。复用“只传相关事实、保持角色语义”的交接原则；其 token 分块与工具数量是该案例选择，不给 Codex 加同样上限。 |
| [Designing delightful frontends with GPT-5.4](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4) | 真实文案、视觉参考、设计 tokens、浏览器反馈；简单 UI 不一定需要更多推理。frontend-demo-preview 与 reader-focused-writing 可配合，但要先有设计目标；旧模型的 Low 建议不直接修改 Sol 默认档位。 |
| [From prompts to products: One year of Responses](https://developers.openai.com/blog/one-year-of-responses) | 案例涵盖行为监测、上下文收集与分析分离、多步工具产品。用 session-analysis 把配置版本与真实失败联系起来；案例不是某一种多代理拓扑普遍更好的证据。 |
| [Using skills to accelerate OSS maintenance](https://developers.openai.com/blog/skills-agents-sdk) | 本地政策、skills、脚本和条件式检查配合。先稳定自己的插件验证入口，再考虑 CI；不把全部测试套到文档编辑。 |
| [Building frontend UIs with Codex and Figma](https://developers.openai.com/blog/building-frontend-uis-with-codex-and-figma) | 设计上下文进入代码，运行 UI 可回到可编辑画布。仅在项目确实以 Figma 为设计来源时接入；临时 preview 本身不构成安装理由。 |
| [Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex) | 持久目标、里程碑验收、修复与状态使长任务可恢复。扩展项目状态入口；25 小时实验不是推荐时长或个人生产力承诺。 |
| [Shell + Skills + Compaction](https://developers.openai.com/blog/skills-shell-tips) | 清晰触发、模板、复用执行环境和压缩。将有用的路由经验用于 skills；hosted shell 与 Responses 参数不能冒充本地 CLI 选项。 |
| [15 lessons learned building ChatGPT Apps](https://developers.openai.com/blog/15-lessons-building-chatgpt-apps) | 用户、模型、widget 各自需要不同信息；主机测试与本地模拟边界不同。保持 Demo 可拆除与验证边界说明；Apps 的 CSP/widgetState 不适用于当前普通 skill 包。 |
| [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | 检查技能触发、行为与产物，而不只检查 SKILL.md 格式。添加实际任务正反例，复用 session traces。 |
| [Supercharging Codex with JetBrains MCP at Skyscanner](https://developers.openai.com/blog/skyscanner-codex-jetbrains-mcp) | IDE diagnostics/run configurations 缩短反馈循环。若常用 IDE 已有运行配置，让 agent 复用；未确认本机使用 JetBrains，不建议直接安装。 |
| [OpenAI for Developers in 2025](https://developers.openai.com/blog/openai-for-developers-2025) | 年度模型/API/工具综述，文中另标记 Codex MCP server 已移除。技能里的集成命令和绝对 helper 路径也应核对当前可用性；年末模型推荐不是 2026 年默认。 |
| [Updates for developers building with voice](https://developers.openai.com/blog/updates-audio-models) | 音频快照改进需重跑真实噪声、静默与工具流程。当前未观察到语音应用配置，不据此调整 Codex 模型；今后音频项目应核对当时有效版本。 |
| [What makes a great ChatGPT app](https://developers.openai.com/blog/what-makes-a-great-chatgpt-app) | 能力应围绕具体任务，工具表面清晰，明确意图无需重复提问。可映射到 skill 触发与完成范围；know/do/show 是 Apps 设计思路，不是本插件新增评分字段。 |
| [Using Codex for education at Dagster Labs](https://developers.openai.com/blog/codex-for-documentation-dagster) | 贡献指南让文档可导航，可运行结果检查文档是否足以指导使用。安装技能应做从文档到实际完成的 smoke check；单个成功不证明所有安装场景。 |
| [How Codex ran OpenAI DevDay 2025](https://developers.openai.com/blog/codex-at-devday) | 独立任务并行、视觉迭代、代码 review，也有由多代理改为单代理的案例。保留明确写入所有权；不把多开终端数量当吞吐优化依据。 |
| [Why we built the Responses API](https://developers.openai.com/blog/responses-api) | 持续推理状态、工具输出 items 与审计轨迹。将可观察输出用于研究与评估；不把日志中的摘要当作原始隐藏推理，也不要求现有 CLI 重写 API 层。 |
| [Developer notes on the Realtime API](https://developers.openai.com/blog/realtime-api) | 更强遵循指令会放大旧提示的边界问题，语音 GA 有其独立合同。可借鉴“升级后重新测提示”；文中时长、窗口与参数属于当时的 Realtime，不设为 Codex 限制。 |
| [Hello, world! Introducing our developer blog](https://developers.openai.com/blog/intro) | 定义博客为工程背景和实践经验，与 docs/changelog 不同。先用博客理解方向，再用当前配置文档与本机事实确认可执行建议。 |

## Hook 回放记录与复现方法

源码为上方记录的 revision，执行对象是原始 Python 脚本；没有复制算法、运行字符串中的 shell 命令或进行删除。

| 输入 | 脚本输出 | 结论 |
| --- | --- | --- |
| `rg -n pattern .` | allow | 合法搜索放行 |
| `rg -rn pattern .` | deny | 目标误用被拒绝 |
| `rg pattern .; grep -rn pattern .` | deny | 合法第二条命令被误判为 rg flag |
| `rg pattern .; printf '%s' '-rn'` | deny | 普通输出参数被误判为 rg flag |
| `printf '%s %s' 'rm' '/tmp/situ-unused-path'` | deny | 引用数据被误判为删除命令 |
| `rm scratch-file` | allow | 工作目录内的字面目标放行 |
| `rm /tmp/situ-unused-path` | deny | 工作目录外的字面目标被拒绝 |
| `cd /tmp; rm situ-unused-path` | allow | 符合脚本明确写出的 literal cd 改变后续边界语义，不能把它另算成已证实缺陷 |

以下只重放前三个关键用例，输出当前 decision，可在不执行待检查命令的情况下复核。**这不是完整的 shell 解析测试，也没有验证 Codex 安装后的实时 hook 调用。**

```bash
python3 - <<'PY'
import json
import subprocess
from pathlib import Path

root = Path('/home/situ/agent-plugins')
cases = [
    ('check-rg-footgun.py', 'rg -rn pattern .'),
    ('check-rg-footgun.py', 'rg pattern .; grep -rn pattern .'),
    ('check-deletion-scope.py', "printf '%s %s' 'rm' '/tmp/situ-unused-path'"),
]
for script, command in cases:
    payload = {
        'hook_event_name': 'PreToolUse',
        'tool_name': 'Bash',
        'cwd': str(root),
        'tool_input': {'command': command},
    }
    run = subprocess.run(
        ['python3', str(root / 'hooks/scripts' / script)],
        input=json.dumps(payload), text=True, capture_output=True, check=True,
    )
    output = json.loads(run.stdout)
    decision = output.get('hookSpecificOutput', {}).get('permissionDecision', 'allow')
    print(script, repr(command), decision)
PY
```

## 保留现有做法与验证限制

值得保留：agent-team 只在显式请求时触发；behavior-verification 使用独立验收依据、按失败机制选择验证环境；de-defend 要求限制有具体来源；manifest 版本由现有脚本生成；handoff 区分已完成、建议与未验证事项。这些已经符合官方文章中的多项实践。

本次没有运行收费模型评估、调整全局权限、变更模型、安装第三方 app、访问账户控制台或发布代码。对没有具体需求的 Figma、JetBrains、tunnel、语音和生命科学工具，只记录适用条件。`danger-full-access` 与 `never` 是本机事实；若以后引入不可信仓库/外部输入，可为该场景单独选择隔离环境，不必为了本次研究改变日常已授权工作流。

阅读配置时一个明文 token 被意外带入工具输出，本报告未收录其值。建议撤销并替换这个凭据；后续配置审查仅输出允许公开的模型、路径与权限字段。
