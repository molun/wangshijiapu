# 临县堡则峪王氏宗谱

> 临县堡则峪王氏宗谱 · 合族珍藏 · 二零二五年续修

一个可本地运行、支持 GitHub Pages 托管的家谱编辑与展示网站。

## 功能特性

- **概览统计** — 家族总人数、传承世代、各支系分布、世代人数分布图
- **人名检索** — 按姓名、配偶、支系、世代多条件搜索，支持模糊匹配
- **世系图** — 树形结构展示上下世系关系，点击可展开查看详情
- **编辑管理** — 增删改查家族成员信息，支持导入/导出 JSON 数据
- **本地存储** — 所有修改自动保存在浏览器本地（LocalStorage），刷新不丢失
- **GitHub Pages** — 可一键部署为静态网站，全球可访问

## 文件结构

```
jiapu/
├── index.html      # 网站主文件（包含全部前端代码）
├── data.json       # 从 PDF 提取的家谱数据（2195人，30世）
├── parse_pdf.py    # PDF 文本提取脚本
└── README.md       # 本文件
```

## 🌐 在线访问

本仓库已部署至 GitHub Pages，可直接访问：

**👉 https://molun.github.io/wangshijiapu**

## 部署到 GitHub Pages（免费）

1. **创建 GitHub 仓库**
   - 登录 [GitHub](https://github.com) → New repository → 命名为 `wangshijiapu`
   - 将 `index.html` 和 `data.json` 上传至仓库

2. **启用 GitHub Pages**
   - 进入仓库 → Settings → Pages
   - Source 选择 `main` branch，Save
   - 等待 1-2 分钟

3. **访问网站**
   - 通过 `https://你的用户名.github.io/wangshijiapu` 访问

## 本地运行

双击 `index.html` 即可在浏览器中打开，无需服务器。

## 导入自己的数据

1. 进入「编辑管理」页面
2. 点击「导入 JSON」按钮
3. 选择格式正确的 JSON 文件

数据格式示例：
```json
{
  "family": "王氏家谱",
  "persons": [
    {"id": 1, "name": "王一世", "gen": 1, "branch": "长支", "wife": "张氏", "sons": 2, "notes": ""},
    {"id": 2, "name": "王二世", "gen": 2, "branch": "长支", "wife": "李氏", "sons": 1, "parent": 1, "notes": ""}
  ]
}
```

## 技术说明

- 纯前端实现，无需后端服务器
- 数据存储于浏览器 LocalStorage，支持离线使用
- 响应式设计，支持手机和电脑访问
- 使用原生 JavaScript，无外部依赖

## 数据来源

本数据来自 PDF 文件 `家谱2025年9月10日利支06.pdf` 及 Excel 文件 `王氏宗谱 - 之纲 - 在雍.xlsx`，经 OCR + 文本提取处理后导入。

## 数据更新记录

- **2026-06-10**: 替换"王在雍"支系数据（从 Excel 导入 868 人），总人数 1998 → 2195，世代 29 → 30

## License

仅供家族内部使用，请勿用于商业目的。
