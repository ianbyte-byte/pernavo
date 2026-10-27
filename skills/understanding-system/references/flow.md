# Data moving between programs

Use the same walk as Ghemawat, Gobioff, and Leung, “The Google File System”, SOSP 2003,
section 2.4, and the data labels on Figure 1. Boxes are programs or queues. The edge text is
the data that moves, such as “chunk data”, not a sentence and not a column list.
<http://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/gfs.pdf>

This figure does not show status values. Status belongs in [state](state.md).

```mermaid
flowchart LR
  a["<程序甲>"] -->|"<数据名>"| b["<程序乙>"]
  b -->|"<数据名>"| c["<程序丙>"]
```

## 数据流转

结合图 1 看一次<操作名>。<谁把哪份数据交给谁。谁写入哪张表。谁在返回之后才读取下一份数据。返回时哪一项可能尚未发生。>投递和消费见 `<路径>`。

An unread producer or consumer stays off the figure. The paragraph’s last sentence names the
directory that was not read.
