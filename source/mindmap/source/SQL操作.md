---
title: SQL操作
date: 2026-07-29 11:12:24
type: "mindmap"
---

## SQL操作

<style>
.mindmap-view-toggle {
  display: flex;
  gap: 10px;
  margin-bottom: 24px;
  flex-wrap: wrap;
  align-items: center;
}
.mindmap-toggle-btn {
  padding: 8px 22px;
  border: 2px solid #49b1f5;
  background: transparent;
  color: #49b1f5;
  border-radius: 22px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: all 0.3s ease;
  outline: none;
}
.mindmap-toggle-btn:hover {
  background: rgba(73, 177, 245, 0.1);
  transform: translateY(-1px);
}
.mindmap-toggle-btn.active {
  background: #49b1f5;
  color: #fff;
}
.mindmap-tree-text {
  background: #f6f8fa;
  border: 1px solid #e1e4e8;
  border-radius: 10px;
  padding: 20px 24px;
  font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', 'Courier New', monospace;
  font-size: 13px;
  line-height: 1.9;
  overflow-x: auto;
  white-space: pre;
  color: #24292e;
}
[data-theme="dark"] .mindmap-tree-text {
  background: #1e1e2e;
  border-color: #313244;
  color: #cdd6f4;
}
[data-theme="dark"] .mindmap-toggle-btn {
  border-color: #89b4fa;
  color: #89b4fa;
}
[data-theme="dark"] .mindmap-toggle-btn:hover {
  background: rgba(137, 180, 250, 0.15);
}
[data-theme="dark"] .mindmap-toggle-btn.active {
  background: #89b4fa;
  color: #1e1e2e;
}
/* ---- Editor ---- */
.mindmap-editor-wrapper { display: none; margin-bottom: 16px; }
.mindmap-editor-toolbar {
  display: flex; gap: 6px; flex-wrap: wrap;
  margin-bottom: 0; padding: 8px 12px;
  background: #f6f8fa; border: 1px solid #e1e4e8;
  border-radius: 10px 10px 0 0; border-bottom: none;
}
.mindmap-editor-toolbar button {
  padding: 4px 12px; border: 1px solid #d0d7de;
  background: #fff; border-radius: 6px;
  cursor: pointer; font-size: 13px; transition: all 0.2s; white-space: nowrap;
}
.mindmap-editor-toolbar button:hover { background: #49b1f5; color: #fff; border-color: #49b1f5; }
.mindmap-editor-textarea {
  width: 100%; min-height: 400px; padding: 16px;
  border: 1px solid #e1e4e8; border-radius: 0 0 10px 10px;
  font-family: 'SF Mono', 'Menlo', 'Monaco', 'Consolas', 'Courier New', monospace;
  font-size: 13px; line-height: 1.9; resize: vertical;
  background: #fff; color: #24292e; outline: none;
}
.mindmap-editor-textarea:focus { border-color: #49b1f5; box-shadow: 0 0 0 3px rgba(73,177,245,0.15); }
.mindmap-save-row { display: none; align-items: center; gap: 10px; margin-top: 12px; }
.mindmap-save-btn {
  padding: 10px 28px; border: none; background: #2da44e; color: #fff;
  border-radius: 22px; cursor: pointer; font-size: 14px; font-weight: 600;
  transition: all 0.3s; outline: none;
}
.mindmap-save-btn:hover { background: #1a7f37; transform: translateY(-1px); }
.mindmap-save-btn:disabled { background: #94d3a2; cursor: not-allowed; transform: none; }
.mindmap-save-status { font-size: 13px; }
.mindmap-save-status.success { color: #2da44e; }
.mindmap-save-status.error { color: #cf222e; }
.mindmap-token-overlay {
  display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.5); z-index: 9999; justify-content: center; align-items: center;
}
.mindmap-token-dialog {
  background: #fff; border-radius: 12px; padding: 24px;
  max-width: 440px; width: 90%; box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
.mindmap-token-dialog h3 { margin: 0 0 12px; font-size: 16px; }
.mindmap-token-dialog input {
  width: 100%; padding: 10px 12px; border: 1px solid #d0d7de;
  border-radius: 8px; font-size: 14px; margin-bottom: 8px; box-sizing: border-box;
}
.mindmap-token-dialog .hint { font-size: 12px; color: #656d76; margin-bottom: 16px; }
.mindmap-token-dialog .hint a { color: #49b1f5; }
.mindmap-token-dialog .actions { display: flex; gap: 8px; justify-content: flex-end; }
.mindmap-token-dialog .actions button {
  padding: 6px 16px; border-radius: 8px; border: 1px solid #d0d7de;
  background: #fff; cursor: pointer; font-size: 13px;
}
.mindmap-token-dialog .actions .btn-primary { background: #49b1f5; color: #fff; border-color: #49b1f5; }
[data-theme="dark"] .mindmap-editor-toolbar { background: #1e1e2e; border-color: #313244; }
[data-theme="dark"] .mindmap-editor-toolbar button { background: #313244; border-color: #45475a; color: #cdd6f4; }
[data-theme="dark"] .mindmap-editor-textarea { background: #1e1e2e; border-color: #313244; color: #cdd6f4; }
[data-theme="dark"] .mindmap-token-dialog { background: #1e1e2e; color: #cdd6f4; }
[data-theme="dark"] .mindmap-token-dialog input { background: #313244; border-color: #45475a; color: #cdd6f4; }
[data-theme="dark"] .mindmap-token-dialog .actions button { background: #313244; border-color: #45475a; color: #cdd6f4; }
</style>
<div class="mindmap-view-toggle">
  <button class="mindmap-toggle-btn active" onclick="switchMindmapView('mindmap')">🧠 思维导图</button>
  <button class="mindmap-toggle-btn" onclick="switchMindmapView('tree')">📝 原始文本</button>
  <button id="edit-btn" class="mindmap-toggle-btn" style="border-style:dashed;" onclick="enterEditMode()">✏️ 编辑</button>
  <button id="cancel-edit-btn" class="mindmap-toggle-btn" style="display:none;border-color:#cf222e;color:#cf222e;" onclick="exitEditMode(true)">✕ 取消编辑</button>
</div>

<div id="mindmap-view" class="mindmap-view-content">
{% markmap %}
- SQL语言
- 一、基础概述
  - SQL四大命令分类
    - DDL【数据定义语言/数据描述语言】
      - 操作对象：模式、基本表、索引、视图
      - 核心动词：CREATE / ALTER / DROP
      - 拓展语句：TRUNCATE TABLE（DDL）
      - 典型语句：CREATE TABLE、DROP TABLE、CREATE VIEW、DROP VIEW、CREATE INDEX、DROP INDEX、TRUNCATE TABLE
    - DML 数据操纵语言：SELECT、INSERT、UPDATE、DELETE
    - DCL 数据控制语言：GRANT(授予权限)、REVOKE(回收权限)
    - TCL 事务控制：COMMIT、ROLLBACK
  - 核心特点：高度非过程化、面向集合操作、支持交互式+嵌入式两种用法
  - 对应三级模式：基本表(模式)、视图(外模式)、索引(内模式)
- │
- 二、数据定义语言（DDL）
  - 1. 基本表操作
    - 创建表 CREATE TABLE：定义列名、数据类型、完整性约束
      - 补充：可省略数据库名，提前用USE选定当前数据库；完整写法：库名.表名
    - 修改表 ALTER TABLE：ADD新增列/约束、MODIFY改列类型、DROP删约束
      - 考点：建有索引的列不能直接修改；课本标准语法不支持修改表名
    - 删除表 DROP TABLE：删除表结构与表内全部数据
  - 2. 索引操作
    - 创建索引：CREATE [UNIQUE][CLUSTER] INDEX，支持ASC升序/DESC降序
    - 删除索引：DROP INDEX，仅移除索引定义，不影响表原始数据
  - 3. 视图操作
    - 创建视图 CREATE VIEW：基于查询语句生成虚表，不存储真实数据
    - 删除视图 DROP VIEW：仅删除视图定义，基表不受影响
  - 4. 常用数据类型【补充疑问要点】
    - 数值型：INT、SMALLINT、DECIMAL(p,q)定点高精度小数、FLOAT单精度、DOUBLE双精度浮点数
      - DECIMAL(p,q)：p总有效位数，q小数位，适合金额；关键字大小写仅代码风格，语法不强制大写
      - FLOAT、DOUBLE：遵循IEEE754，商用实现分别固定4字节、8字节；属于近似浮点数，存在精度损失；标准SQL无需书写长度参数，不可用于账务存储
      - 注意：FLOAT(M,D)、DOUBLE(M,D)仅为MySQL拓展语法，不属于标准SQL
    - 字符型：CHAR(n)定长、VARCHAR(n)变长，必须指定长度n
    - 时间类型区分
      - MySQL TIMESTAMP：存储时间，同一时间可重复，无法保证唯一性
      - SQL Server rowversion(旧名timestamp)：非时间，数据库全局自增二进制值，自动生成，每条记录唯一
    - 逻辑型（BOOLEAN布尔类型）：只有TRUE/FALSE；默认值为FALSE；不要和数值0混淆
    - 时间型：DATE日期、TIME时间、TIMESTAMP时间戳，无需填写长度
  - 【综合示例：学生选课库DDL全流程（表+索引+视图）】
- │     -- 1. 创建学生表，定义列类型与主键、唯一、非空约束
- │     CREATE TABLE Student(
- │        Sno CHAR(5) NOT NULL UNIQUE,
- │        Sname CHAR(20) UNIQUE,
- │        Ssex CHAR(1),
- │        Sage INT,
- │        Sdept CHAR(15),
- │        PRIMARY KEY (Sno)
- │     );
- │     -- 2. 修改表：新增入学时间列
- │     ALTER TABLE Student ADD Scome DATE;
- │     -- 3. 修改表：调整年龄字段数据类型
- │     ALTER TABLE Student MODIFY Sage SMALLINT;
- │     -- 4. 修改表：删除姓名的唯一性约束
- │     ALTER TABLE Student DROP UNIQUE(Sname);
- │     -- 5. 创建索引：按学号建立唯一索引
- │     CREATE UNIQUE INDEX Stusno ON Student(Sno ASC);
- │     -- 6. 创建复合索引：选课表按学号升序、课程号降序
- │     CREATE UNIQUE INDEX SCidx ON SC(Sno ASC,Cno DESC);
- │     -- 7. 删除索引
- │     DROP INDEX Stusno;
- │     -- 8. 创建视图：计算机系学生视图
- │     CREATE VIEW CS_Student AS
- │        SELECT Sno,Sname,Sage FROM Student WHERE Sdept='CS';
- │     -- 9. 删除视图
- │     DROP VIEW CS_Student;
- │     -- 10. 删除整张表
- │     DROP TABLE Student;
- │
- 三、数据查询语言（DQL - SELECT核心）
  - 完整语法框架：SELECT [DISTINCT] 目标列 FROM 表 [WHERE 行条件] [GROUP BY 分组列 [HAVING 组条件]] [ORDER BY 排序列 排序规则]
  - 标识符语法补充：[表名] 为SQL Server语法，[]用于包裹表名/列名，避免关键字冲突
  - 1. 单表查询：列筛选、条件过滤、排序、聚集统计、分组筛选
    - SQL条件匹配表达式
      - 等值比较：=、&lt;&gt;、&gt;、&lt;、&gt;=、&lt;=
      - 模糊匹配 LIKE：%任意多字符，_单个字符；搭配ESCAPE实现通配符转义；⚠️标准SQL不使用*，*仅用于SELECT查询所有列
      - 区间匹配 BETWEEN … AND …：闭区间，包含边界
      - 集合匹配 IN / NOT IN：判断值是否在集合内
      - 空值匹配 IS NULL / IS NOT NULL；禁止使用 = NULL
    - 常用聚集函数
      - SUM(列)：数值列求和，忽略NULL；支持DISTINCT去重后求和
      - AVG(列)：数值列求平均值，忽略NULL；NULL不参与计数
      - COUNT()、MAX()、MIN()
      - 规则：聚合函数不能放在WHERE；分组后筛选写在HAVING
    - GROUP BY 分组
      - 功能：依据字段划分数据组，配合聚合函数，一组输出一行
      - 语法规则：SELECT中非聚合字段，必须全部出现在GROUP BY后
      - 执行顺序：FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
      - WHERE：分组前过滤原始数据；HAVING：分组后过滤聚合结果
      - 支持多列分组；所有NULL值会归为同一组，GROUP BY不自带排序
  - 2. 多表连接：等值连接、自然连接、自连接、外连接、复合条件连接
    - 关系代数符号：内连接 ⋈；左外连接 ⋈ₗ；右外连接 ⋈ᵣ；全外连接 ⋈ₗᵣ
    - 内连接(INNER JOIN)：只保留两张表互相匹配成功的数据
    - 左外连接(LEFT JOIN)：保留左表所有记录；右表无匹配，字段填充NULL
    - 右外连接(RIGHT JOIN)：保留右表所有记录；左表无匹配，字段填充NULL
    - 全外连接(FULL JOIN)：左右两表全部记录保留，不匹配一侧填充NULL
    - 重要规则：外连接右表筛选条件尽量写在ON，写在WHERE容易丢失左表数据
    - ⭐核心考点：表1,表2 WHERE 等值条件 → 隐式内连接；LEFT/RIGHT/FULL JOIN属于外连接，外连接语法必须搭配ON，老式逗号写法无法实现外连接
  - 3. 嵌套子查询：IN谓词匹配、ANY/ALL量词比较、EXISTS存在性判断
  - 4. 集合查询：UNION并集、INTERSECT交集、MINUS差集
  - 【综合示例：学生选课场景查询】
- │     -- 查询：选修课程数≥2门、平均分80分以上的学生，按平均分降序排列
- │     SELECT
- │        Sno 学号,
- │        COUNT(Cno) 选课门数,
- │        AVG(Grade) 平均成绩
- │     FROM SC
- │     WHERE Grade IS NOT NULL
- │     GROUP BY Sno
- │     HAVING COUNT(Cno) &gt;= 2 AND AVG(Grade) &gt;= 80
- │     ORDER BY 平均成绩 DESC;
- │
- │     -- 关联左连接示例：查询全部学生以及选课成绩，无选课学生成绩为NULL
- │     SELECT a.Sno, a.Sname, b.Cno, b.Grade
- │     FROM Student a
- │     LEFT JOIN SC b
- │     ON a.Sno = b.Sno
- │
- 四、数据操纵语言（DML - 增删改）
  - 1. 插入 INSERT：单行常量插入、子查询批量插入
  - 2. 修改 UPDATE：按条件更新列值，省略WHERE则修改全表所有行
  - 3. 删除 DELETE：按条件删除行，省略WHERE则清空全表数据、保留表结构
  - 【综合示例：学生表数据增删改】
- │     -- 1. 插入一条完整学生记录
- │     INSERT INTO Student VALUES('95020','陈冬','男','IS',18);
- │     -- 2. 批量插入：将各系平均年龄存入新表
- │     INSERT INTO Deptage(Sdept, Avgage)
- │     SELECT Sdept, AVG(Sage) FROM Student GROUP BY Sdept;
- │     -- 3. 修改：将学号95019学生年龄改为22岁
- │     UPDATE Student SET Sage=22 WHERE Sno='95019';
- │     -- 4. 全体学生年龄+1
- │     UPDATE Student SET Sage = Sage + 1;
- │     -- 5. 删除学号95019学生记录
- │     DELETE FROM Student WHERE Sno='95019';
- │     -- 6. 删除全部选课记录，保留表结构
- │     DELETE FROM SC;
- │
- 五、核心易混区分【错题考点汇总】
  - WHERE vs HAVING：WHERE分组前筛行、不可用聚集函数；HAVING分组后筛组、可用聚集函数
  - DROP / DELETE / TRUNCATE
    - DROP TABLE：DDL，删除表结构+全部数据，无法恢复
    - DELETE：DML，删除满足条件数据，支持WHERE条件、事务回滚，逐行删除速度慢
    - TRUNCATE TABLE：DDL，清空表全部数据，保留表结构；不能带WHERE，一般不可回滚，执行速度更快
  - CHAR vs VARCHAR：CHAR定长存储、不足补空格；VARCHAR变长存储、按实际长度保存
  - ALTER TABLE考点：不能直接修改建有索引的列；教材标准语法不支持修改表名
  - 布尔型与数值区分：BOOLEAN默认值FALSE；数值型默认值0，0只是条件判断等效假，类型语义不同
  - 自增编号字段：不能选用byte类型，取值范围仅0~255，极易溢出
  - timestamp区分：rowversion(旧timestamp)自动生成、全局唯一；MySQL时间戳TIMESTAMP允许重复
  - 【GROUP BY综合示例与⚠️注意】
    - 核心原理一句话：GROUP BY要求SELECT所有非聚合内容在同一分组内必须唯一，一组只能输出一行，杜绝取值歧义，字段要么进GROUP BY、要么套聚合函数。
    - 完整SQL示例
- │    SELECT
- │        sno,
- │        COUNT(*) AS course_count,
- │        AVG(grade) AS avg_score
- │    FROM sc
- │    WHERE grade IS NOT NULL
- │    GROUP BY sno
- │    HAVING AVG(grade) &gt;= 60
- │    ORDER BY avg_score DESC;
    - 语句逻辑拆解
      - WHERE grade IS NOT NULL：分组前过滤成绩为空的原始记录
      - GROUP BY sno：按照学号分组，每位学生数据为一组
      - COUNT(*)：统计每位学生选课总行数（不忽略行内NULL）
      - AVG(grade)：分组计算平均分（忽略列内NULL值）
      - HAVING AVG(grade) &gt;= 60：分组聚合完成后筛选分组
      - ORDER BY avg_score DESC：平均分降序排序
    - ⚠️注意（分点展示）
      - 语法铁律：SELECT中非聚合字段，必须全部写在GROUP BY后
      - 执行顺序：FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
      - WHERE：分组前过滤原始行，禁止使用聚合函数；HAVING：分组后筛选，允许聚合函数
      - NULL规则：GROUP BY将所有NULL归为同一组；COUNT(*)统计行数不忽略NULL，其余聚合函数忽略列NULL
      - 多列分组 GROUP BY A,B：A、B值同时相等，才划分为同一组
      - 误区提醒：GROUP BY本身不会自动排序，排序必须手动添加ORDER BY
{% endmarkmap %}
</div>

<div id="tree-view" class="mindmap-view-content" style="display:none;">
<pre class="mindmap-tree-text">SQL语言
├─ 一、基础概述
│  ├─ SQL四大命令分类
│  │  ├─ DDL【数据定义语言/数据描述语言】
│  │  │  ├─ 操作对象：模式、基本表、索引、视图
│  │  │  ├─ 核心动词：CREATE / ALTER / DROP
│  │  │  ├─ 拓展语句：TRUNCATE TABLE（DDL）
│  │  │  └─ 典型语句：CREATE TABLE、DROP TABLE、CREATE VIEW、DROP VIEW、CREATE INDEX、DROP INDEX、TRUNCATE TABLE
│  │  ├─ DML 数据操纵语言：SELECT、INSERT、UPDATE、DELETE
│  │  ├─ DCL 数据控制语言：GRANT(授予权限)、REVOKE(回收权限)
│  │  └─ TCL 事务控制：COMMIT、ROLLBACK
│  ├─ 核心特点：高度非过程化、面向集合操作、支持交互式+嵌入式两种用法
│  └─ 对应三级模式：基本表(模式)、视图(外模式)、索引(内模式)
│
├─ 二、数据定义语言（DDL）
│  ├─ 1. 基本表操作
│  │  ├─ 创建表 CREATE TABLE：定义列名、数据类型、完整性约束
│  │  │  └─ 补充：可省略数据库名，提前用USE选定当前数据库；完整写法：库名.表名
│  │  ├─ 修改表 ALTER TABLE：ADD新增列/约束、MODIFY改列类型、DROP删约束
│  │  │  └─ 考点：建有索引的列不能直接修改；课本标准语法不支持修改表名
│  │  └─ 删除表 DROP TABLE：删除表结构与表内全部数据
│  ├─ 2. 索引操作
│  │  ├─ 创建索引：CREATE [UNIQUE][CLUSTER] INDEX，支持ASC升序/DESC降序
│  │  └─ 删除索引：DROP INDEX，仅移除索引定义，不影响表原始数据
│  ├─ 3. 视图操作
│  │  ├─ 创建视图 CREATE VIEW：基于查询语句生成虚表，不存储真实数据
│  │  └─ 删除视图 DROP VIEW：仅删除视图定义，基表不受影响
│  ├─ 4. 常用数据类型【补充疑问要点】
│  │  ├─ 数值型：INT、SMALLINT、DECIMAL(p,q)定点高精度小数、FLOAT单精度、DOUBLE双精度浮点数
│  │  │  ├─ DECIMAL(p,q)：p总有效位数，q小数位，适合金额；关键字大小写仅代码风格，语法不强制大写
│  │  │  ├─ FLOAT、DOUBLE：遵循IEEE754，商用实现分别固定4字节、8字节；属于近似浮点数，存在精度损失；标准SQL无需书写长度参数，不可用于账务存储
│  │  │  └─ 注意：FLOAT(M,D)、DOUBLE(M,D)仅为MySQL拓展语法，不属于标准SQL
│  │  ├─ 字符型：CHAR(n)定长、VARCHAR(n)变长，必须指定长度n
│  │  ├─ 时间类型区分
│  │  │  ├─ MySQL TIMESTAMP：存储时间，同一时间可重复，无法保证唯一性
│  │  │  └─ SQL Server rowversion(旧名timestamp)：非时间，数据库全局自增二进制值，自动生成，每条记录唯一
│  │  ├─ 逻辑型（BOOLEAN布尔类型）：只有TRUE/FALSE；默认值为FALSE；不要和数值0混淆
│  │  └─ 时间型：DATE日期、TIME时间、TIMESTAMP时间戳，无需填写长度
│  └─ 【综合示例：学生选课库DDL全流程（表+索引+视图）】
│     -- 1. 创建学生表，定义列类型与主键、唯一、非空约束
│     CREATE TABLE Student(
│        Sno CHAR(5) NOT NULL UNIQUE,
│        Sname CHAR(20) UNIQUE,
│        Ssex CHAR(1),
│        Sage INT,
│        Sdept CHAR(15),
│        PRIMARY KEY (Sno)
│     );
│     -- 2. 修改表：新增入学时间列
│     ALTER TABLE Student ADD Scome DATE;
│     -- 3. 修改表：调整年龄字段数据类型
│     ALTER TABLE Student MODIFY Sage SMALLINT;
│     -- 4. 修改表：删除姓名的唯一性约束
│     ALTER TABLE Student DROP UNIQUE(Sname);
│     -- 5. 创建索引：按学号建立唯一索引
│     CREATE UNIQUE INDEX Stusno ON Student(Sno ASC);
│     -- 6. 创建复合索引：选课表按学号升序、课程号降序
│     CREATE UNIQUE INDEX SCidx ON SC(Sno ASC,Cno DESC);
│     -- 7. 删除索引
│     DROP INDEX Stusno;
│     -- 8. 创建视图：计算机系学生视图
│     CREATE VIEW CS_Student AS
│        SELECT Sno,Sname,Sage FROM Student WHERE Sdept='CS';
│     -- 9. 删除视图
│     DROP VIEW CS_Student;
│     -- 10. 删除整张表
│     DROP TABLE Student;
│
├─ 三、数据查询语言（DQL - SELECT核心）
│  ├─ 完整语法框架：SELECT [DISTINCT] 目标列 FROM 表 [WHERE 行条件] [GROUP BY 分组列 [HAVING 组条件]] [ORDER BY 排序列 排序规则]
│  ├─ 标识符语法补充：[表名] 为SQL Server语法，[]用于包裹表名/列名，避免关键字冲突
│  ├─ 1. 单表查询：列筛选、条件过滤、排序、聚集统计、分组筛选
│  │  ├─ SQL条件匹配表达式
│  │  │  ├─ 等值比较：=、&lt;&gt;、&gt;、&lt;、&gt;=、&lt;=
│  │  │  ├─ 模糊匹配 LIKE：%任意多字符，_单个字符；搭配ESCAPE实现通配符转义；⚠️标准SQL不使用*，*仅用于SELECT查询所有列
│  │  │  ├─ 区间匹配 BETWEEN … AND …：闭区间，包含边界
│  │  │  ├─ 集合匹配 IN / NOT IN：判断值是否在集合内
│  │  │  └─ 空值匹配 IS NULL / IS NOT NULL；禁止使用 = NULL
│  │  ├─ 常用聚集函数
│  │  │  ├─ SUM(列)：数值列求和，忽略NULL；支持DISTINCT去重后求和
│  │  │  ├─ AVG(列)：数值列求平均值，忽略NULL；NULL不参与计数
│  │  │  ├─ COUNT()、MAX()、MIN()
│  │  │  └─ 规则：聚合函数不能放在WHERE；分组后筛选写在HAVING
│  │  └─ GROUP BY 分组
│  │     ├─ 功能：依据字段划分数据组，配合聚合函数，一组输出一行
│  │     ├─ 语法规则：SELECT中非聚合字段，必须全部出现在GROUP BY后
│  │     ├─ 执行顺序：FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
│  │     ├─ WHERE：分组前过滤原始数据；HAVING：分组后过滤聚合结果
│  │     └─ 支持多列分组；所有NULL值会归为同一组，GROUP BY不自带排序
│  ├─ 2. 多表连接：等值连接、自然连接、自连接、外连接、复合条件连接
│  │  ├─ 关系代数符号：内连接 ⋈；左外连接 ⋈ₗ；右外连接 ⋈ᵣ；全外连接 ⋈ₗᵣ
│  │  ├─ 内连接(INNER JOIN)：只保留两张表互相匹配成功的数据
│  │  ├─ 左外连接(LEFT JOIN)：保留左表所有记录；右表无匹配，字段填充NULL
│  │  ├─ 右外连接(RIGHT JOIN)：保留右表所有记录；左表无匹配，字段填充NULL
│  │  ├─ 全外连接(FULL JOIN)：左右两表全部记录保留，不匹配一侧填充NULL
│  │  ├─ 重要规则：外连接右表筛选条件尽量写在ON，写在WHERE容易丢失左表数据
│  │  └─ ⭐核心考点：表1,表2 WHERE 等值条件 → 隐式内连接；LEFT/RIGHT/FULL JOIN属于外连接，外连接语法必须搭配ON，老式逗号写法无法实现外连接
│  ├─ 3. 嵌套子查询：IN谓词匹配、ANY/ALL量词比较、EXISTS存在性判断
│  ├─ 4. 集合查询：UNION并集、INTERSECT交集、MINUS差集
│  └─ 【综合示例：学生选课场景查询】
│     -- 查询：选修课程数≥2门、平均分80分以上的学生，按平均分降序排列
│     SELECT 
│        Sno 学号, 
│        COUNT(Cno) 选课门数, 
│        AVG(Grade) 平均成绩
│     FROM SC
│     WHERE Grade IS NOT NULL
│     GROUP BY Sno
│     HAVING COUNT(Cno) &gt;= 2 AND AVG(Grade) &gt;= 80
│     ORDER BY 平均成绩 DESC;
│
│     -- 关联左连接示例：查询全部学生以及选课成绩，无选课学生成绩为NULL
│     SELECT a.Sno, a.Sname, b.Cno, b.Grade
│     FROM Student a
│     LEFT JOIN SC b
│     ON a.Sno = b.Sno
│
├─ 四、数据操纵语言（DML - 增删改）
│  ├─ 1. 插入 INSERT：单行常量插入、子查询批量插入
│  ├─ 2. 修改 UPDATE：按条件更新列值，省略WHERE则修改全表所有行
│  ├─ 3. 删除 DELETE：按条件删除行，省略WHERE则清空全表数据、保留表结构
│  └─ 【综合示例：学生表数据增删改】
│     -- 1. 插入一条完整学生记录
│     INSERT INTO Student VALUES('95020','陈冬','男','IS',18);
│     -- 2. 批量插入：将各系平均年龄存入新表
│     INSERT INTO Deptage(Sdept, Avgage)
│     SELECT Sdept, AVG(Sage) FROM Student GROUP BY Sdept;
│     -- 3. 修改：将学号95019学生年龄改为22岁
│     UPDATE Student SET Sage=22 WHERE Sno='95019';
│     -- 4. 全体学生年龄+1
│     UPDATE Student SET Sage = Sage + 1;
│     -- 5. 删除学号95019学生记录
│     DELETE FROM Student WHERE Sno='95019';
│     -- 6. 删除全部选课记录，保留表结构
│     DELETE FROM SC;
│
└─ 五、核心易混区分【错题考点汇总】
   ├─ WHERE vs HAVING：WHERE分组前筛行、不可用聚集函数；HAVING分组后筛组、可用聚集函数
   ├─ DROP / DELETE / TRUNCATE
   │  ├─ DROP TABLE：DDL，删除表结构+全部数据，无法恢复
   │  ├─ DELETE：DML，删除满足条件数据，支持WHERE条件、事务回滚，逐行删除速度慢
   │  └─ TRUNCATE TABLE：DDL，清空表全部数据，保留表结构；不能带WHERE，一般不可回滚，执行速度更快
   ├─ CHAR vs VARCHAR：CHAR定长存储、不足补空格；VARCHAR变长存储、按实际长度保存
   ├─ ALTER TABLE考点：不能直接修改建有索引的列；教材标准语法不支持修改表名
   ├─ 布尔型与数值区分：BOOLEAN默认值FALSE；数值型默认值0，0只是条件判断等效假，类型语义不同
   ├─ 自增编号字段：不能选用byte类型，取值范围仅0~255，极易溢出
   ├─ timestamp区分：rowversion(旧timestamp)自动生成、全局唯一；MySQL时间戳TIMESTAMP允许重复
   └─ 【GROUP BY综合示例与⚠️注意】
      ├─ 核心原理一句话：GROUP BY要求SELECT所有非聚合内容在同一分组内必须唯一，一组只能输出一行，杜绝取值歧义，字段要么进GROUP BY、要么套聚合函数。
      ├─ 完整SQL示例
      │    SELECT
      │        sno,
      │        COUNT(*) AS course_count,
      │        AVG(grade) AS avg_score
      │    FROM sc
      │    WHERE grade IS NOT NULL
      │    GROUP BY sno
      │    HAVING AVG(grade) &gt;= 60
      │    ORDER BY avg_score DESC;
      ├─ 语句逻辑拆解
      │  ├─ WHERE grade IS NOT NULL：分组前过滤成绩为空的原始记录
      │  ├─ GROUP BY sno：按照学号分组，每位学生数据为一组
      │  ├─ COUNT(*)：统计每位学生选课总行数（不忽略行内NULL）
      │  ├─ AVG(grade)：分组计算平均分（忽略列内NULL值）
      │  ├─ HAVING AVG(grade) &gt;= 60：分组聚合完成后筛选分组
      │  └─ ORDER BY avg_score DESC：平均分降序排序
      └─ ⚠️注意（分点展示）
         ├─ 语法铁律：SELECT中非聚合字段，必须全部写在GROUP BY后
         ├─ 执行顺序：FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
         ├─ WHERE：分组前过滤原始行，禁止使用聚合函数；HAVING：分组后筛选，允许聚合函数
         ├─ NULL规则：GROUP BY将所有NULL归为同一组；COUNT(*)统计行数不忽略NULL，其余聚合函数忽略列NULL
         ├─ 多列分组 GROUP BY A,B：A、B值同时相等，才划分为同一组
         └─ 误区提醒：GROUP BY本身不会自动排序，排序必须手动添加ORDER BY</pre>
</div>

<div id="edit-view" class="mindmap-view-content" style="display:none;">
  <div class="mindmap-editor-wrapper">
    <div class="mindmap-editor-toolbar">
      <button onclick="editorCmd('highlight')" title="高亮 == ==">🖍 高亮</button>
      <button onclick="editorCmd('strike')" title="删除线 ~~ ~~"><s>S</s> 删除线</button>
      <button onclick="editorCmd('bold')" title="粗体 ** **"><b>B</b> 粗体</button>
      <button onclick="editorCmd('code')" title="行内代码 ` `">&lt;/&gt; 代码</button>
      <span style="flex:1;"></span>
      <button onclick="editorUndo()" title="撤销 Ctrl+Z">↩ 撤销</button>
      <button onclick="editorRedo()" title="重做 Ctrl+Y">↪ 重做</button>
    </div>
    <textarea id="mindmap-textarea" class="mindmap-editor-textarea" spellcheck="false">SQL语言
├─ 一、基础概述
│  ├─ SQL四大命令分类
│  │  ├─ DDL【数据定义语言/数据描述语言】
│  │  │  ├─ 操作对象：模式、基本表、索引、视图
│  │  │  ├─ 核心动词：CREATE / ALTER / DROP
│  │  │  ├─ 拓展语句：TRUNCATE TABLE（DDL）
│  │  │  └─ 典型语句：CREATE TABLE、DROP TABLE、CREATE VIEW、DROP VIEW、CREATE INDEX、DROP INDEX、TRUNCATE TABLE
│  │  ├─ DML 数据操纵语言：SELECT、INSERT、UPDATE、DELETE
│  │  ├─ DCL 数据控制语言：GRANT(授予权限)、REVOKE(回收权限)
│  │  └─ TCL 事务控制：COMMIT、ROLLBACK
│  ├─ 核心特点：高度非过程化、面向集合操作、支持交互式+嵌入式两种用法
│  └─ 对应三级模式：基本表(模式)、视图(外模式)、索引(内模式)
│
├─ 二、数据定义语言（DDL）
│  ├─ 1. 基本表操作
│  │  ├─ 创建表 CREATE TABLE：定义列名、数据类型、完整性约束
│  │  │  └─ 补充：可省略数据库名，提前用USE选定当前数据库；完整写法：库名.表名
│  │  ├─ 修改表 ALTER TABLE：ADD新增列/约束、MODIFY改列类型、DROP删约束
│  │  │  └─ 考点：建有索引的列不能直接修改；课本标准语法不支持修改表名
│  │  └─ 删除表 DROP TABLE：删除表结构与表内全部数据
│  ├─ 2. 索引操作
│  │  ├─ 创建索引：CREATE [UNIQUE][CLUSTER] INDEX，支持ASC升序/DESC降序
│  │  └─ 删除索引：DROP INDEX，仅移除索引定义，不影响表原始数据
│  ├─ 3. 视图操作
│  │  ├─ 创建视图 CREATE VIEW：基于查询语句生成虚表，不存储真实数据
│  │  └─ 删除视图 DROP VIEW：仅删除视图定义，基表不受影响
│  ├─ 4. 常用数据类型【补充疑问要点】
│  │  ├─ 数值型：INT、SMALLINT、DECIMAL(p,q)定点高精度小数、FLOAT单精度、DOUBLE双精度浮点数
│  │  │  ├─ DECIMAL(p,q)：p总有效位数，q小数位，适合金额；关键字大小写仅代码风格，语法不强制大写
│  │  │  ├─ FLOAT、DOUBLE：遵循IEEE754，商用实现分别固定4字节、8字节；属于近似浮点数，存在精度损失；标准SQL无需书写长度参数，不可用于账务存储
│  │  │  └─ 注意：FLOAT(M,D)、DOUBLE(M,D)仅为MySQL拓展语法，不属于标准SQL
│  │  ├─ 字符型：CHAR(n)定长、VARCHAR(n)变长，必须指定长度n
│  │  ├─ 时间类型区分
│  │  │  ├─ MySQL TIMESTAMP：存储时间，同一时间可重复，无法保证唯一性
│  │  │  └─ SQL Server rowversion(旧名timestamp)：非时间，数据库全局自增二进制值，自动生成，每条记录唯一
│  │  ├─ 逻辑型（BOOLEAN布尔类型）：只有TRUE/FALSE；默认值为FALSE；不要和数值0混淆
│  │  └─ 时间型：DATE日期、TIME时间、TIMESTAMP时间戳，无需填写长度
│  └─ 【综合示例：学生选课库DDL全流程（表+索引+视图）】
│     -- 1. 创建学生表，定义列类型与主键、唯一、非空约束
│     CREATE TABLE Student(
│        Sno CHAR(5) NOT NULL UNIQUE,
│        Sname CHAR(20) UNIQUE,
│        Ssex CHAR(1),
│        Sage INT,
│        Sdept CHAR(15),
│        PRIMARY KEY (Sno)
│     );
│     -- 2. 修改表：新增入学时间列
│     ALTER TABLE Student ADD Scome DATE;
│     -- 3. 修改表：调整年龄字段数据类型
│     ALTER TABLE Student MODIFY Sage SMALLINT;
│     -- 4. 修改表：删除姓名的唯一性约束
│     ALTER TABLE Student DROP UNIQUE(Sname);
│     -- 5. 创建索引：按学号建立唯一索引
│     CREATE UNIQUE INDEX Stusno ON Student(Sno ASC);
│     -- 6. 创建复合索引：选课表按学号升序、课程号降序
│     CREATE UNIQUE INDEX SCidx ON SC(Sno ASC,Cno DESC);
│     -- 7. 删除索引
│     DROP INDEX Stusno;
│     -- 8. 创建视图：计算机系学生视图
│     CREATE VIEW CS_Student AS
│        SELECT Sno,Sname,Sage FROM Student WHERE Sdept='CS';
│     -- 9. 删除视图
│     DROP VIEW CS_Student;
│     -- 10. 删除整张表
│     DROP TABLE Student;
│
├─ 三、数据查询语言（DQL - SELECT核心）
│  ├─ 完整语法框架：SELECT [DISTINCT] 目标列 FROM 表 [WHERE 行条件] [GROUP BY 分组列 [HAVING 组条件]] [ORDER BY 排序列 排序规则]
│  ├─ 标识符语法补充：[表名] 为SQL Server语法，[]用于包裹表名/列名，避免关键字冲突
│  ├─ 1. 单表查询：列筛选、条件过滤、排序、聚集统计、分组筛选
│  │  ├─ SQL条件匹配表达式
│  │  │  ├─ 等值比较：=、<>、>、<、>=、<=
│  │  │  ├─ 模糊匹配 LIKE：%任意多字符，_单个字符；搭配ESCAPE实现通配符转义；⚠️标准SQL不使用*，*仅用于SELECT查询所有列
│  │  │  ├─ 区间匹配 BETWEEN … AND …：闭区间，包含边界
│  │  │  ├─ 集合匹配 IN / NOT IN：判断值是否在集合内
│  │  │  └─ 空值匹配 IS NULL / IS NOT NULL；禁止使用 = NULL
│  │  ├─ 常用聚集函数
│  │  │  ├─ SUM(列)：数值列求和，忽略NULL；支持DISTINCT去重后求和
│  │  │  ├─ AVG(列)：数值列求平均值，忽略NULL；NULL不参与计数
│  │  │  ├─ COUNT()、MAX()、MIN()
│  │  │  └─ 规则：聚合函数不能放在WHERE；分组后筛选写在HAVING
│  │  └─ GROUP BY 分组
│  │     ├─ 功能：依据字段划分数据组，配合聚合函数，一组输出一行
│  │     ├─ 语法规则：SELECT中非聚合字段，必须全部出现在GROUP BY后
│  │     ├─ 执行顺序：FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
│  │     ├─ WHERE：分组前过滤原始数据；HAVING：分组后过滤聚合结果
│  │     └─ 支持多列分组；所有NULL值会归为同一组，GROUP BY不自带排序
│  ├─ 2. 多表连接：等值连接、自然连接、自连接、外连接、复合条件连接
│  │  ├─ 关系代数符号：内连接 ⋈；左外连接 ⋈ₗ；右外连接 ⋈ᵣ；全外连接 ⋈ₗᵣ
│  │  ├─ 内连接(INNER JOIN)：只保留两张表互相匹配成功的数据
│  │  ├─ 左外连接(LEFT JOIN)：保留左表所有记录；右表无匹配，字段填充NULL
│  │  ├─ 右外连接(RIGHT JOIN)：保留右表所有记录；左表无匹配，字段填充NULL
│  │  ├─ 全外连接(FULL JOIN)：左右两表全部记录保留，不匹配一侧填充NULL
│  │  ├─ 重要规则：外连接右表筛选条件尽量写在ON，写在WHERE容易丢失左表数据
│  │  └─ ⭐核心考点：表1,表2 WHERE 等值条件 → 隐式内连接；LEFT/RIGHT/FULL JOIN属于外连接，外连接语法必须搭配ON，老式逗号写法无法实现外连接
│  ├─ 3. 嵌套子查询：IN谓词匹配、ANY/ALL量词比较、EXISTS存在性判断
│  ├─ 4. 集合查询：UNION并集、INTERSECT交集、MINUS差集
│  └─ 【综合示例：学生选课场景查询】
│     -- 查询：选修课程数≥2门、平均分80分以上的学生，按平均分降序排列
│     SELECT 
│        Sno 学号, 
│        COUNT(Cno) 选课门数, 
│        AVG(Grade) 平均成绩
│     FROM SC
│     WHERE Grade IS NOT NULL
│     GROUP BY Sno
│     HAVING COUNT(Cno) >= 2 AND AVG(Grade) >= 80
│     ORDER BY 平均成绩 DESC;
│
│     -- 关联左连接示例：查询全部学生以及选课成绩，无选课学生成绩为NULL
│     SELECT a.Sno, a.Sname, b.Cno, b.Grade
│     FROM Student a
│     LEFT JOIN SC b
│     ON a.Sno = b.Sno
│
├─ 四、数据操纵语言（DML - 增删改）
│  ├─ 1. 插入 INSERT：单行常量插入、子查询批量插入
│  ├─ 2. 修改 UPDATE：按条件更新列值，省略WHERE则修改全表所有行
│  ├─ 3. 删除 DELETE：按条件删除行，省略WHERE则清空全表数据、保留表结构
│  └─ 【综合示例：学生表数据增删改】
│     -- 1. 插入一条完整学生记录
│     INSERT INTO Student VALUES('95020','陈冬','男','IS',18);
│     -- 2. 批量插入：将各系平均年龄存入新表
│     INSERT INTO Deptage(Sdept, Avgage)
│     SELECT Sdept, AVG(Sage) FROM Student GROUP BY Sdept;
│     -- 3. 修改：将学号95019学生年龄改为22岁
│     UPDATE Student SET Sage=22 WHERE Sno='95019';
│     -- 4. 全体学生年龄+1
│     UPDATE Student SET Sage = Sage + 1;
│     -- 5. 删除学号95019学生记录
│     DELETE FROM Student WHERE Sno='95019';
│     -- 6. 删除全部选课记录，保留表结构
│     DELETE FROM SC;
│
└─ 五、核心易混区分【错题考点汇总】
   ├─ WHERE vs HAVING：WHERE分组前筛行、不可用聚集函数；HAVING分组后筛组、可用聚集函数
   ├─ DROP / DELETE / TRUNCATE
   │  ├─ DROP TABLE：DDL，删除表结构+全部数据，无法恢复
   │  ├─ DELETE：DML，删除满足条件数据，支持WHERE条件、事务回滚，逐行删除速度慢
   │  └─ TRUNCATE TABLE：DDL，清空表全部数据，保留表结构；不能带WHERE，一般不可回滚，执行速度更快
   ├─ CHAR vs VARCHAR：CHAR定长存储、不足补空格；VARCHAR变长存储、按实际长度保存
   ├─ ALTER TABLE考点：不能直接修改建有索引的列；教材标准语法不支持修改表名
   ├─ 布尔型与数值区分：BOOLEAN默认值FALSE；数值型默认值0，0只是条件判断等效假，类型语义不同
   ├─ 自增编号字段：不能选用byte类型，取值范围仅0~255，极易溢出
   ├─ timestamp区分：rowversion(旧timestamp)自动生成、全局唯一；MySQL时间戳TIMESTAMP允许重复
   └─ 【GROUP BY综合示例与⚠️注意】
      ├─ 核心原理一句话：GROUP BY要求SELECT所有非聚合内容在同一分组内必须唯一，一组只能输出一行，杜绝取值歧义，字段要么进GROUP BY、要么套聚合函数。
      ├─ 完整SQL示例
      │    SELECT
      │        sno,
      │        COUNT(*) AS course_count,
      │        AVG(grade) AS avg_score
      │    FROM sc
      │    WHERE grade IS NOT NULL
      │    GROUP BY sno
      │    HAVING AVG(grade) >= 60
      │    ORDER BY avg_score DESC;
      ├─ 语句逻辑拆解
      │  ├─ WHERE grade IS NOT NULL：分组前过滤成绩为空的原始记录
      │  ├─ GROUP BY sno：按照学号分组，每位学生数据为一组
      │  ├─ COUNT(*)：统计每位学生选课总行数（不忽略行内NULL）
      │  ├─ AVG(grade)：分组计算平均分（忽略列内NULL值）
      │  ├─ HAVING AVG(grade) >= 60：分组聚合完成后筛选分组
      │  └─ ORDER BY avg_score DESC：平均分降序排序
      └─ ⚠️注意（分点展示）
         ├─ 语法铁律：SELECT中非聚合字段，必须全部写在GROUP BY后
         ├─ 执行顺序：FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY
         ├─ WHERE：分组前过滤原始行，禁止使用聚合函数；HAVING：分组后筛选，允许聚合函数
         ├─ NULL规则：GROUP BY将所有NULL归为同一组；COUNT(*)统计行数不忽略NULL，其余聚合函数忽略列NULL
         ├─ 多列分组 GROUP BY A,B：A、B值同时相等，才划分为同一组
         └─ 误区提醒：GROUP BY本身不会自动排序，排序必须手动添加ORDER BY</textarea>
  </div>
  <div class="mindmap-save-row" style="display:none;">
    <button id="save-btn" class="mindmap-save-btn" onclick="saveToGitHub()">💾 保存到 GitHub</button>
    <span id="save-status" class="mindmap-save-status"></span>
  </div>
</div>

<div id="pwd-overlay" class="mindmap-token-overlay">
  <div class="mindmap-token-dialog">
    <h3>🔐 输入保存密码</h3>
    <p id="pwd-msg" style="color:#cf222e;font-size:13px;margin:0 0 8px;"></p>
    <input type="password" id="pwd-input" placeholder="请输入密码" onkeydown="if(event.key==='Enter')submitPassword()" />
    <div class="hint">
      输入密码后将自动解密 Token 并提交到 GitHub。
    </div>
    <div class="actions">
      <button onclick="hidePwdDialog()">取消</button>
      <button class="btn-primary" onclick="submitPassword()">确认提交</button>
    </div>
  </div>
</div>

<script>
(function() {
  var currentView = 'mindmap', isEditing = false;
  var sourceFilename = 'SQL操作.txt';
  var owner = '1whistlerrrr', repo = '1whistlerrrr.github.io';
  var editHistory = [], historyIdx = -1;

  window.switchMindmapView = function(view) {
    if (currentView === view && !isEditing) return;
    if (isEditing) exitEditMode(true);
    currentView = view; isEditing = false;
    var btns = document.querySelectorAll('.mindmap-toggle-btn');
    btns.forEach(function(b){b.classList.remove('active');});
    document.getElementById('mindmap-view').style.display = view==='mindmap'?'block':'none';
    document.getElementById('tree-view').style.display = view==='tree'?'block':'none';
    document.getElementById('edit-view').style.display = 'none';
    document.querySelector('.mindmap-editor-wrapper').style.display = 'none';
    document.querySelector('.mindmap-save-row').style.display = 'none';
    if(view==='mindmap'){btns[0].classList.add('active');window.dispatchEvent(new Event('resize'));}
    else{btns[1].classList.add('active');}
    document.getElementById('edit-btn').style.display='inline-flex';
    document.getElementById('cancel-edit-btn').style.display='none';
  };

  window.enterEditMode = function() {
    isEditing = true;
    var btns = document.querySelectorAll('.mindmap-toggle-btn');
    btns.forEach(function(b){b.classList.remove('active');});
    document.getElementById('mindmap-view').style.display='none';
    document.getElementById('tree-view').style.display='none';
    document.getElementById('edit-view').style.display='block';
    document.querySelector('.mindmap-editor-wrapper').style.display='block';
    document.querySelector('.mindmap-save-row').style.display='flex';
    document.getElementById('edit-btn').style.display='none';
    document.getElementById('cancel-edit-btn').style.display='inline-flex';
    document.getElementById('cancel-edit-btn').classList.add('active');
    document.getElementById('save-status').textContent='';
    document.getElementById('save-status').className='mindmap-save-status';
    var ta = document.getElementById('mindmap-textarea');
    editHistory = [ta.value]; historyIdx = 0;
    ta.focus();
  };

  window.exitEditMode = function(discard) {
    if(!discard) return;
    isEditing = false;
    document.getElementById('edit-view').style.display='none';
    document.querySelector('.mindmap-editor-wrapper').style.display='none';
    document.querySelector('.mindmap-save-row').style.display='none';
    document.getElementById('edit-btn').style.display='inline-flex';
    document.getElementById('cancel-edit-btn').style.display='none';
    document.getElementById('cancel-edit-btn').classList.remove('active');
    document.getElementById('tree-view').style.display='block';
    document.querySelectorAll('.mindmap-toggle-btn')[1].classList.add('active');
    currentView = 'tree';
  };

  window.editorCmd = function(cmd) {
    var ta=document.getElementById('mindmap-textarea');
    var s=ta.selectionStart,e=ta.selectionEnd,t=ta.value,sel=t.substring(s,e);
    var wL='',wR='';
    switch(cmd){
      case 'bold':wL='**';wR='**';break;
      case 'strike':wL='~~';wR='~~';break;
      case 'highlight':wL='==';wR='==';break;
      case 'code':wL='`';wR='`';break;
    }
    if(!sel.length){
      var ph={bold:'粗体',strike:'删除线',highlight:'高亮',code:'代码'}[cmd]||'';
      ta.value=t.substring(0,s)+wL+ph+wR+t.substring(e);
      ta.focus();ta.setSelectionRange(s+wL.length,s+wL.length+ph.length);
    }else{
      ta.value=t.substring(0,s)+wL+sel+wR+t.substring(e);
      ta.focus();ta.setSelectionRange(s,e+wL.length+wR.length);
    }
    pushHistory();
  };

  function pushHistory(){
    var ta=document.getElementById('mindmap-textarea');
    editHistory=editHistory.slice(0,historyIdx+1);
    editHistory.push(ta.value);historyIdx=editHistory.length-1;
  }

  window.editorUndo=function(){if(historyIdx>0){historyIdx--;document.getElementById('mindmap-textarea').value=editHistory[historyIdx];}};
  window.editorRedo=function(){if(historyIdx<editHistory.length-1){historyIdx++;document.getElementById('mindmap-textarea').value=editHistory[historyIdx];}};

  document.addEventListener('keydown',function(e){
    if(!isEditing)return;
    if((e.ctrlKey||e.metaKey)&&e.key==='z'&&!e.shiftKey){e.preventDefault();editorUndo();}
    if((e.ctrlKey||e.metaKey)&&(e.key==='y'||(e.key==='z'&&e.shiftKey))){e.preventDefault();editorRedo();}
  });
  document.addEventListener('input',function(e){if(e.target.id==='mindmap-textarea'&&isEditing)pushHistory();});

  var ENCRYPTED_TOKEN = 'CwsJaWEFNFQNUGZXCDISck5xKCIuQ1UGFBo/V3NvBS8YBAUCHDYRZw==';

  function decryptToken(encB64, password) {
    var binary = atob(encB64);
    var bytes = new Uint8Array(binary.length);
    for (var i=0; i<binary.length; i++) bytes[i] = binary.charCodeAt(i);
    var key = password.repeat(Math.ceil(bytes.length/password.length)).slice(0, bytes.length);
    var result = new Uint8Array(bytes.length);
    for (var i=0; i<bytes.length; i++) result[i] = bytes[i] ^ key.charCodeAt(i);
    return String.fromCharCode.apply(null, result);
  }

  function getToken(){try{return localStorage.getItem('gh_mindmap_token')||'';}catch(e){return '';}}
  function setToken(t){try{localStorage.setItem('gh_mindmap_token',t);}catch(e){}}

  window.showPwdDialog=function(msg){
    document.getElementById('pwd-overlay').style.display='flex';
    document.getElementById('pwd-msg').textContent=msg||'';
    document.getElementById('pwd-input').value='';
    document.getElementById('pwd-input').focus();
  };
  window.hidePwdDialog=function(){document.getElementById('pwd-overlay').style.display='none';};
  window.submitPassword=function(){
    var pwd=document.getElementById('pwd-input').value.trim();
    if(!pwd){showPwdDialog('请输入密码');return;}
    hidePwdDialog();
    doSave(pwd);
  };

  window.saveToGitHub=function(){
    if(ENCRYPTED_TOKEN){
      showPwdDialog('');
      return;
    }
    var token=getToken();
    if(!token){showPwdDialog('');return;}
    doSave(token);
  };

  function utf8_to_b64(str){return btoa(unescape(encodeURIComponent(str)));}

  function doSave(pwdOrToken){
    var token;
    if(ENCRYPTED_TOKEN && pwdOrToken && pwdOrToken.length < 50){
      try { token = decryptToken(ENCRYPTED_TOKEN, pwdOrToken); }
      catch(e) { showPwdDialog('密码错误，请重试'); return; }
      // Verify the decrypted token looks valid
      if(!token || !token.startsWith('ghp_')&&!token.startsWith('github_pat_')){
        showPwdDialog('密码错误，请重试'); return;
      }
    } else if(pwdOrToken && pwdOrToken.length >= 30) {
      token = pwdOrToken;
      setToken(token);
    } else {
      token = getToken();
    }
    if(!token){showPwdDialog('');return;}
    var btn=document.getElementById('save-btn');
    var status=document.getElementById('save-status');
    btn.disabled=true;status.textContent='⏳ 保存中...';status.className='mindmap-save-status';
    var content=document.getElementById('mindmap-textarea').value;
    var path='source/raw_mindmap/'+sourceFilename;

    fetch('https://api.github.com/repos/'+owner+'/'+repo+'/contents/'+path,{
      headers:{Authorization:'Bearer '+token,Accept:'application/vnd.github+json'}
    }).then(function(r){
      if(!r.ok)throw new Error('获取文件信息失败 ('+r.status+')');
      return r.json();
    }).then(function(data){
      return fetch('https://api.github.com/repos/'+owner+'/'+repo+'/contents/'+path,{
        method:'PUT',
        headers:{Authorization:'Bearer '+token,'Content-Type':'application/json',Accept:'application/vnd.github+json'},
        body:JSON.stringify({message:'✏️ 更新 '+sourceFilename+' (via web editor)',content:utf8_to_b64(content),sha:data.sha})
      });
    }).then(function(r){
      if(!r.ok)throw new Error('提交失败 ('+r.status+')');
      status.textContent='✅ 已保存！GitHub Actions 正在重新部署，约1分钟后生效。';
      status.className='mindmap-save-status success';
      document.querySelector('#tree-view .mindmap-tree-text').textContent=content;
      btn.disabled=false;
    }).catch(function(err){
      status.textContent='❌ '+err.message;
      status.className='mindmap-save-status error';
      btn.disabled=false;
    });
  }
})();
</script>
