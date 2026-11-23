# COMP3211 Final 溫習包 — STATUS

> 新對話開工時：先讀呢個檔，跟「下一步」繼續。每完成一個 html 就更新。
> 做法同 DSAI4205 final 溫習包一樣（樣板：DSAI4205-quiz1/final/P4-L7.html），淺色版（Quiz 2 配色），唔要深色模式。

## 考試資料
- 日期：**2026-12-05**（Kelvin 講）
- 形式（參考 2025/26 真卷，Prof. PEI Yu Max；L0 寫明今年都係 3 小時 closed book，佔 70%）：
  - 3 小時，closed book，**冇 formula sheet**，總分 100
  - **Section A**：Q1–20，**True/False，每題 1 分 = 20 分**（2023 答題紙寫明；4 份真卷嘅 Section A 頁全部被抽走，冇原題）
  - **Section B**：Q21–27，短答 + 畫圖 = 80 分；每小題有字數上限（<50／<100／<150 words），超字會扣分
- 老師冇講額外考試資料；Kelvin 話「同之前出嘅差唔多」
- 教材：lecture L0–L12、4 份真卷（2022–2025）、Asm1（有官方 solution）、Asm2（冇 solution）、L5 Exercise
- tutorial／lab 資料夾係空嘅
- 真卷冇官方答案：溫習包答案按 lecture 寫，標明出處

## 缺頁／讀唔到（唔好估）
- 4 份真卷 Section A（T/F）全部冇
- 2025 Q21(4)：「which of the following two」嘅兩個選項唔喺卷上（頁被抽走），按 Scrum 原則答並註明
- 2025 份卷 6 頁得 5 頁

## 出題習慣（總結）
1. 重用：Asm1 Q4 = 2022 Q22；Asm2 Q1 = 2022 Q24；Asm2 Q3 = 2022 Q26；Asm1 Q1 ≈ 2022 Q21；「Tom」情境 3 次；圖書館情境 3 次
2. 大題次序固定：Process → RE → Architecture → Class diagram →（Sequence）→ Testing → Evolution／Reuse
3. Partition testing 表（same branch coverage 定義）：2022、2024、2025、Asm2
4. 填圖題：MVC 12 格（2023）、CCB change management 6 格（2024）、reuse RE 4 格（2023）
5. 排序／配對：CMMI 等級、layer 上下、elicitation 4 stage；XP ↔ agile principle；activity ↔ elicitation/spec/validation
6. 情境判斷 + X vs Y 比較；字數上限

## 檔案分組（Kelvin 已確認 2026-11-22）
| 檔案 | 內容 | 對應題 | 狀態 |
|---|---|---|---|
| final/index.html | 點用、進度、考試格式圖、逐份卷比較表（有連結）、出題習慣、預測表、Asm 對應表、模擬卷 Section A（20 T/F）、跨課 MC（10 題，含多選）、模擬卷 Section B（Q21–27 全答，cinema class diagram、ATM sequence diagram、grade() partition 互動表，Java 跑過）、必背清單、易錯總表 | 全部 | ✅ 2026-11-22 |
| final/P1-UML.html | 12 張概念卡（modelling 4 角度、class box、6 種關係、multiplicity、inheritance、noun hunt、Information Expert、use case、sequence 元素、frames、state、一致性）；2025 Q24 完整示範；2022／2023／2024 Q24 + 2022／2025 Q25 + L5 Exercise 全答（全部 SVG）；4 drill；關係填表；20 T/F + 8 MC | Q24、Q25（18–27 分） | ✅ 2026-11-22 |
| final/P2-Testing.html | 14 張概念卡（validation vs defect、V&V、3 stages、black/white box、coverage、EP+BVA、branch-coverage partition、oracle + V-model、interface、regression/CI、TDD、release、alpha/beta/acceptance、static + stop criteria）；2025 Q26(3) 決策樹示範；2025／2024／2023／2022 testing 題全答（nextDate 14 行、removeLDLetters 5 行、calculateDiscount 8 行，全部 Java 窮舉驗證）；4 drill；2 個互動 partition 表；22 T/F + 8 MC | Q25／26（11–15） | ✅ 2026-11-22 |
| final/P3-Process-Agile.html | 13 張概念卡（SE 定義 + good software、ethics/ETHICS-PLUS、4 activities、waterfall、incremental、reuse、coping with change、prototyping vs incremental delivery、CMMI、agile manifesto、XP、Scrum、agile 問題 + 決策圖）；2025 Q21 完整示範（Q21(4) 選項缺頁已註明）；2024／2023／2022 Q21 + Asm1 Q1 全答；4 drill；2 組填充；24 T/F + 8 MC | Q21（15） | ✅ 2026-11-22 |
| final/P4-Requirements.html | 12 張概念卡（RE 定義、user vs system、F vs NF、verifiable NFR + metrics、F/NF 界線 + 衝突、spiral 3 activities、elicitation 持份者 + 4 stage、interview/observation、NL spec 指引、SRS 結構、5 validation checks、traceability + moving target）；2022 Q22 = Asm1 Q4 完整示範；2025／2024／2023 Q22 + Asm1 Q3 全答；3 drill；2 組填充；22 T/F + 8 MC | Q22（10–12） | ✅ 2026-11-22 |
| final/P5-Architecture.html | 12 張概念卡（architectural design、NFR 對 architecture、MVC（Sommerville 6.3 圖）、layered（iLearn 對 HappyProgramming）、repository vs blackboard、client-server、pipe & filter、EDA、揀／組合 pattern 決策表、application architectures、distributed + thin/fat + CAP、master-slave／multi-tier／DCA／P2P／SaaS）；2025 Q23 完整示範；2024／2023／2022 Q23 + Asm2 Q2 全答；3 drill；MVC 12 格 + module 分層互動填；24 T/F + 8 MC | Q23（10–14） | ✅ 2026-11-22 |
| final/P6-Evolution-Reuse.html | 14 張概念卡（evolution process、CCB 流程（2024 圖）、agile evolution + maintenance 成本、technical debt quadrant、legacy、value×quality 四格、refactoring vs re-engineering、codeline/baseline、centralized vs distributed、fork+PR + VC key features、reuse 層次 + L2 reuse 流程（2023 圖）、framework vs product line、CBSE + container、SOA + MDE）；2024 Q26 完整示範；2025 Q27、2022 Q27、Asm2 Q4、2023 Q26 全答；3 drill；CCB + reuse 互動填圖；24 T/F + 8 MC | Q26／27（10–14） | ✅ 2026-11-22 |
| final/P7-Design-OO.html | 13 張概念卡（analysis vs design、structured development、DFD leveling/balancing、ER、structure chart、cohesion/coupling、info hiding KWIC、Java OOP、inheritance/polymorphism/composite、OO vs PO + CRC、GRASP 9、SOLID 5（Java 跑過 LSP／OCP）、pitfalls）；SOLID 改 code 示範；2022 Q23(3) + 3 條預測題；3 drill；2 組填充；28 T/F + 8 MC | T/F + 小題 | ✅ 2026-11-22 |

次序：index → P1 → P2 → P3 → P4 → P5 → P6 → P7

## 每頁格式（新格式規則）
- 九部分：一、點考 二、筆記（概念卡）三、完整示範 四、Past paper 全答 五、Drill 六、互動填充 七、T/F + MC 八、短答 九、常見疑問
- 每 section 開頭 `.key`「一分鐘重點」
- 每個概念一張 `.concept` 卡，`.lab` 標籤五部分：一句講完 → 點解要咁做（.why）→ 圖解（.pic）→ 例子（.eg，逐步）→ 易錯（.trap）
- 每個概念最少一幅 SVG；同類嘢同色：白 = 普通 class／component、藍 = superclass／abstract、青 = subclass／處理步驟、橙 = 重點／actor、黃 = 外部系統／database／frame
- 步驟用 `ol.steps`；數學用 `$$...$$`、`\( \)`（KaTeX CDN）
- 字多嘅表加 `class="stack"`（手機變卡片）；partition 表用 `class="pt"`
- **T/F + MC**（Kelvin 2026-11-22 加要求）：每頁 T/F 15–25 題（同真卷 Section A），另加 MC 同少量多選題；每題逐個講其他選項點解錯
- 互動 fill-in：partition testing 表、填圖題（MVC／CCB／reuse），用 `.practice.fill` + `input.blank`
- 參考答案控制喺題目字數上限之內

## 點樣改／build
- 原始內容：`final/_src/parts/*.html`；CSS/JS 模板：`final/_src/build.py`
- UML 圖：`final/_src/diagrams.py` 寫 spec，`_src/uml.py` 自動畫 SVG；parts 入面用 `{{UML:key}}`
- MCQ JSON：`{"t":"課","s":"題目","a":答案}`（冇 `o` = T/F，a=0 係 True、1 係 False）；有 `o` = MC；`a` 係 array = 多選
- Build：`cd final/_src && python3 build.py <檔名>.html`，輸出喺 `_src/out/`，再 copy 去 `final/`
- 檢查：`node shot.js <檔名>.html`（390px 冇溢出）
- Testing 答案用 Java 實際跑過核對（container 嘅 /home/claude/w/java/PT.java 窮舉；新 session 要重寫）
- 手畫 SVG 規則：字多嘅圖 viewBox 闊 ≤ 380（手機 1:1 睇得清）；闊圖（UML）放 `.uml` 框，手機左右捲
- 預覽單幅 UML：`python3 preview.py <key>`；截某個元素：`node snap.js <檔名> "<selector>" 390`

## 下一步
- 8 頁全部完成（2026-11-22）。全部 390px／820px 檢查冇溢出、冇 JS error；所有填充題「顯示答案 → 對答案」全對；共 184 T/F + 66 MC
- 等 Kelvin push 上 GitHub（repo：COMP3211-revision，Pages 由 main branch 根目錄出；網址 https://kelvin0611.github.io/COMP3211-revision/final/）
- KaTeX 經 CDN 喺瀏覽器 render（container 預覽唔到），要喺手機確認公式顯示正常
- 之後按 Kelvin 溫書時嘅問題補 FAQ／drill；可以加第二套模擬卷（mock2.html）

## Kelvin 唔熟／想補嘅位
- （未有）

## Repo 結構
- COMP3211-revision/index.html：自動跳去 final/
- COMP3211-revision/.gitignore：.DS_Store、final/_src/out/
- COMP3211-revision/README.md
