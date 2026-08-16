# AI Jobs Market Intelligence · 懶人工具駅

公開嘅 AI／自動化職位市場分析頁（Hong Kong + Global Remote）。

## 原則
- 爬蟲只收集，零改動、零 hardcode
- 四隻獨立 AI 分工：審計 → 清洗 → 分析 → 出 JSON（職責分離、可交叉驗證）
- 人類做最終審批，先至發布

## 本地啟動
python -m http.server 8000
- 工作台：http://localhost:8000/panel.html
- 公眾頁：http://localhost:8000/index.html

## 更新流程
1. GitHub → Actions → crawl → Run workflow（網頁／手機 App 都撳得）
2. 跑完自動 commit output/jobs_latest.csv + errors_latest.csv
3. 開 panel.html 行 4 步 AI pipeline（每步一掣複製）
4. 驗證通過後下載 jobs_data.json，upload 返去 repo 根目錄 → dashboard 更新

## 免責
數據源自公開平台，僅供參考；職位詳情以原平台為準。
