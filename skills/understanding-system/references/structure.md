# Runnable parts and one operation

Follow Ghemawat, Gobioff, and Leung, “The Google File System”, SOSP 2003, sections 2.3 and 2.4.
The Princeton copy is <http://www.cs.princeton.edu/courses/archive/fall09/cos518/papers/gfs.pdf>.

Section 2.3 names the parts and points at the figure: “A GFS cluster consists of a single
master and multiple chunkservers and is accessed by multiple clients, as shown in Figure 1.”
The caption is “Figure 1: GFS Architecture”. The boxes are names. Section 2.4 then walks one
read in time and refers back to that figure.

Use the names of the programs, stores, and queues that the source actually contains. A C4
container is a runnable application or a data store. It is not a Docker container. Do not draw
a component inside a part the question did not name. Do not write a code note for every
directory.

Scene for the figure, one rectangle per runnable part:

```json
{
  "title": "<系统名>的组成",
  "nodes": [
    {"id": "a", "text": "<部分甲>", "shape": "rectangle"},
    {"id": "b", "text": "<部分乙>", "shape": "rectangle"},
    {"id": "c", "text": "<部分丙>", "shape": "rectangle"}
  ],
  "edges": [
    {"from": "a", "to": "b", "text": ""},
    {"from": "b", "to": "c", "text": ""}
  ]
}
```

## 结构

<系统名>由<部分甲>、<部分乙>和<部分丙>组成，如图 1。<谁不直接调用谁。>

<部分甲><做一件事>。见 `<路径>`。<部分乙><做一件事>。见 `<路径>`。

## 一次<操作名>

结合图 1 看一次<操作名>。<调用方把什么交给谁。谁写入什么。谁在返回之后才继续。返回时哪一项可能尚未发生。>

Replace every angle-bracket slot with the system under study. Drop a part the source does not
show.
