# A disagreement and what aligns it

Follow Xiaomi LLM-Core, “MiMo-V2-Flash Technical Report”, arXiv:2601.02780, section 4.6.1.
<https://mimo.xiaomi.com/papers/mimo-v2-flash.pdf>

The paragraph names the fault, then the alignment, then the difference from the usual
mechanism: “MoE models suffer from inconsistent expert routing across rollout and training due
to numerical precision issues. We propose Rollout Routing Replay (R3) to train RL using the
same routed experts from rollout. ... Unlike the commonly-used radix cache in current
inference engines, our request-level prefix cache avoids re-prefilling or inter-request
output cache sharing.”

Write one disagreement. Name both sides, the value that must match, and the code that copies
or checks it. Say how that differs from the nearby mechanism a reader would otherwise assume.

```markdown
## 对齐

<甲>和<乙>会在<哪一项>上不一致，原因是<读到的原因>。见 `<路径>`。<对齐手段>让<乙>使用<甲>已经确定的<那一项>。见 `<路径>`。常见做法是<另一机制>。<这里的做法>与它的差别是<一句>。
```
