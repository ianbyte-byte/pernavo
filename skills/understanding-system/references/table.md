# One table

Follow Chen, “The Entity-Relationship Model—Toward a Unified View of Data”, ACM TODS 1(1),
1976, Figure 4. One row is one entity. One column is one attribute. Codd, “A Relational Model
of Data for Large Shared Data Banks”, CACM 1970, requires each relation to declare its primary
key. <https://www.csc.lsu.edu/~chen/pdf/erd-5-pages.pdf>

Show one table, the one the question names. Column order follows the source definition. Mark
the primary key. A column that points at another table is named here; the association itself
belongs in [er](er.md), and only when the question asks for it.

```markdown
## 表

表 1 <表名>。一行是<一条记录代表什么>。主键是 `<列>`。

| 列 | 含义 | 键 |
|---|---|---|
| <列> | <含义> | 主键 |
| <列> | <含义> | |

<这张表保存什么。>定义见 `<路径>`。
```

Do not list tables the question did not name.
