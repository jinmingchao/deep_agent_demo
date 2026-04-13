---
name: mysql-ycyt
description: |
  在 YCYT 业务 MySQL（rds_ycyt_ctr / rds_ycyt_pay）中执行只读查询，用于检索合同及相关业务数据。
  当用户需要查合同、订单履约、库表结构、业务表数据或跑分析型 SELECT 时使用；关键词如「合同」「YCYT」「ctr 库」「pay 库」「MySQL」「查表」「SQL」。
license: MIT
allowed-tools: mysql_ycyt_query
---

# YCYT MySQL 查询 Skill（合同与业务只读查询）

## When to Use

- 用户要**从库里看合同或关联业务信息**（列表、详情、状态、时间范围统计等）。
- 需要**确认有哪些表/字段**（`SHOW TABLES`、`DESCRIBE` / `SHOW COLUMNS`）。
- 需要在 **ctr** 或 **pay** 库上做**只读**分析（`SELECT`、含 `WITH` 的只读查询等）。

## 库与职责（路由提示）

| 参数 `database` | 含义 | 合同相关查询时的建议 |
|-----------------|------|------------------------|
| `ctr` | 对应配置中的 **CTR 业务库**（`rds_ycyt_ctr`） | **优先**：合同主数据、签约、审批、客户/项目侧控制类表通常在此库。 |
| `pay` | 对应配置中的 **PAY 业务库**（`rds_ycyt_pay`） | 支付、对账、流水等与**履约/资金**强相关的表；与合同联查时按需选用。 |

实际表名以线上为准；不确定时先用 `SHOW TABLES` / `LIKE` 过滤（如 `%contract%`、`%order%`、`%agreement%` 等英文常见命名，或你们库内的中文拼音/缩写表名）。

## Instructions

1. **明确目标**：要查的是合同维度、还是支付/对账维度，初步决定用 `ctr` 还是 `pay`；跨库问题可**分两次**调用工具分别查询再在回答中合并说明。
2. **探路（推荐）**：若表名未知，先执行只读语句，例如：
   - `SHOW TABLES;` 或 `SHOW TABLES LIKE '%关键字%';`
   - `DESCRIBE 表名;` 或 `SHOW CREATE TABLE 表名;`（只读，允许）
3. **业务查询**：编写**单条** `SELECT`（可带 `WHERE`、`JOIN`、`LIMIT`；需要时用 `WITH` 子句但结果须为只读查询）。
4. **调用工具**：调用 **`mysql_ycyt_query`**，传入：
   - **`database`**：`ctr` 或 `pay`（或完整库名 `rds_ycyt_ctr` / `rds_ycyt_pay`，与工具实现一致）。
   - **`sql`**：上述单条只读 SQL。
5. **整理回复**：把工具返回的行摘要给用户；若行数多，概括字段含义与结论，避免逐行堆砌。

## 工具约束（与 `mysql_ycyt_query` 一致）

- **仅只读**：允许以 `SELECT`、`SHOW`、`DESCRIBE`/`DESC`、`EXPLAIN`、以及 `WITH … SELECT` 等形式开头的只读语句。
- **禁止**：`INSERT`/`UPDATE`/`DELETE`/`DDL`/多语句批量等写操作。
- **结果集**：工具侧可能对返回行数做上限截断；分析时请考虑在 SQL 中加合理 `LIMIT` 与条件过滤。
- **依赖**：需环境已安装 `pymysql`；连接信息与 `src/utils/env_util.py` 一致（由仓库根目录或 `src/.env` 中的 `YCYT_DATABASE_*` 提供，`agent_skill_demo` 通过同模块导入）。

## Limitations

- 本 Skill **不提供**法律解释或合同效力判断；仅做**数据查询与展示**层面的协助。
- 不得编造表名或字段；以 `SHOW`/`DESCRIBE` 与真实查询结果为准。
- 生产数据涉及隐私与合规，回复中注意脱敏与最小必要原则。
