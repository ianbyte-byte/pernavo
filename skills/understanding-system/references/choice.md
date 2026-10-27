# Why this design

Follow Xiaomi LLM-Core, “MiMo-V2-Flash Technical Report”, arXiv:2601.02780, sections 2.2.1
and 2.2.2. <https://mimo.xiaomi.com/papers/mimo-v2-flash.pdf>

The paper first states what was compared and how each variant was built. A table shows the
outcomes. The next paragraph says what the table shows: “hybrid SWA (W = 128, w/o sink)
suffers noticeable performance degradation across general benchmarks, whereas introducing
attention sink bias consistently recovers or improves performance relative to the all-GA
baseline.” The explanation and its limit sit together: “We hypothesize that this arises from
a combination of better regularization and effective sparsity. ... We emphasize that these
observations and findings are empirical and derived from our specific experimental settings.”

Use a table only for the alternatives the source actually distinguishes. Say whether the
reason is written in an ADR, comment, or README, or is inferred from the code. An inferred
reason ends with the limit: it comes from the files that were read, and from the model scale,
data, and procedure those files show.

```markdown
## 这项设计

比较过的方案如下。训练或构造方式见 `<路径>`。

| 方案 | 结果 | 来源 |
|---|---|---|
| <方案甲> | <读到的差别> | `<路径>` |
| <方案乙> | <读到的差别> | `<路径>` |

表 1 <比较的是什么>

<方案甲与方案乙的差别，用表里的事实写完。> <若原因写在文档里，引那一处。若原因是从代码推出的，写推出的依据，并写明这个解释只来自已读文件所显示的规模、数据和过程。>
```
