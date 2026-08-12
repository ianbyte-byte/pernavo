---
name: web-performance
description: >
  Review frontend and browser performance risks including render-blocking resources, main-thread
  long tasks, oversized payloads, image/font priority, layout shifts, interaction delay, and
  misleading lab-only measurements. Use for Web Vitals, LCP, INP, CLS, frontend performance,
  browser latency, page speed, or real-user performance. Require field/lab distinction and p75
  distributions; do not use a single Lighthouse score or load event as proof.
---

# Web Performance

## 审查信号

- 首屏主元素资源发现/优先级、HTML TTFB、资源下载/解码/渲染和第三方脚本分别检查；LCP 不是单独的服务器指标。
- 找主线程长任务（>50ms）、同步 JSON 解析、布局/绘制集中和事件处理过重；网络正常不代表交互正常。
- 图片/iframe/广告未预留尺寸、异步插入内容、字体替换和回访页面可能造成生命周期内 CLS；不要只测首屏 load。
- 检查 bundle、重复下载、缓存策略、压缩、预加载和请求 waterfall；按设备、网络、缓存和页面模板分层。

## 证据

- 记录 LCP、INP、CLS 的 field 与 lab 来源、p75、Good/Needs improvement/Poor 比例、浏览器/设备/网络/版本/页面维度。
- 用 Performance API 的 navigation/resource/mark/measure 和 Long Tasks 数据拆阶段；保存最终 LCP 元素、layout-shift entries、最长任务及归因。
- 发布回归必须关联版本和页面/资源变更；没有 RUM 时标记 field unavailable，不用 Lighthouse 替代。

## 来源

- MDN Performance: https://developer.mozilla.org/en-US/docs/Web/Performance
- MDN Long Tasks API: https://developer.mozilla.org/en-US/docs/Web/API/Long_Tasks_API
- web.dev Web Vitals: https://web.dev/articles/vitals
- web.dev LCP: https://web.dev/articles/lcp
- web.dev CLS: https://web.dev/articles/cls
