#!/usr/bin/env python3
"""Generate README, visual style gallery and source/license documentation."""
import json
from collections import defaultdict
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
BT = chr(96)

def get(path):
    return json.loads((ROOT/path).read_text(encoding="utf-8"))

def safe(v, n=130):
    return " ".join(str(v or "").replace("|","｜").replace("\n"," ").split())[:n]

def save(path, data):
    p=ROOT/path
    p.parent.mkdir(parents=True,exist_ok=True)
    data="\n".join(data).rstrip()+"\n"
    if not p.exists() or p.read_text(encoding="utf-8")!=data:
        p.write_text(data,encoding="utf-8")

def generate():
    skills=get("catalog/skills.json")["skills"]
    presets=get("catalog/styles.json")["presets"]
    locks=get("config/upstream-lock.json")["sources"]
    sources=yaml.safe_load((ROOT/"config/sources.yaml").read_text(encoding="utf-8"))["sources"]
    groups=defaultdict(list)
    cats=defaultdict(list)
    for s in skills:
        groups[s["source_id"]].append(s)
        cats[s["category"]].append(s)
    wibi=groups["wibi-style"]
    readme=[
        "# PhotoStyle Atlas 📷", "",
        "**AI 修图、艺术风格转换、摄影海报的开源 Agent Skills 图鉴。**", "",
        "将多来源 Agent Skills **直接复制为本仓库实际文件**，不使用 Git submodule 或软链接。",
        "包含风格分类、中文说明、图片预览、上游版本 SHA、许可证、自动定时同步和人工审查 PR。", "",
        "> 本仓库不提供生成模型、API Key 或免费额度。镜像文件仍属于各原作者，",
        "> Wibi Style 视觉指令受个人非商业等独立许可限制。", "",
        "## 收录统计", "",
        "- 独立安装 Skill：" + str(len(skills)),
        "- 上游来源：" + str(len(sources)),
        "- Wibi Style Skills：" + str(len(wibi)),
        "- Image Style Transfer 内部风格预设：" + str(sum(x["skill_id"]=="image-style-transfer" for x in presets)),
        "- Anime Restyle 动漫风格 key：" + str(sum(x["skill_id"]=="anime-image-restyle" for x in presets)),
        "- Poster Generator 版式：" + str(sum(x["skill_id"]=="poster-generator" for x in presets)),
        "- Photo Editing Craft 修图配方：" + str(sum(x["skill_id"]=="photo-editing-craft" for x in presets)), "",
        "[全部风格图鉴](docs/STYLES.md) · [安装教程](docs/INSTALL.md) · "+
        "[上游来源和许可](docs/SOURCES.md) · [维护文档](docs/MAINTENANCE.md) · "+
        "[效果对照模板](docs/STYLE-COMPARISON.md) · "+
        "[人像光影与糖水片指南](docs/PORTRAIT-LIGHTING.md)", "",
        "## 风格预览 · Wibi Style", "",
        "以下缩略图从原作者仓库同步，保留署名与原始授权；不要独立拆包用于商业图库。", "",
        "| 预览 | 风格名 | Skill |", "| --- | --- | --- |",
    ]
    for x in wibi[:12]:
        preview=x.get("preview")
        visual="<img src=\""+preview+"\" width=\"145\" alt=\""+safe(x["title"],50)+"\">" if preview else "—"
        readme.append("| "+visual+" | "+safe(x["title"],70)+" | ["+x["id"]+"]("+x["path"]+"/SKILL.md) |")
    readme.extend(["","[查看全部 Wibi Style 风格](docs/STYLES.md#wibi-style-视觉风格)","",
                   "## 新增 · 人像精修与布光", "",
                   "人像原图与风景兼顾，区分普通局部补光和需要图像生成工具的重新布光。", "",
                   "| 预览 | Skill | 适用场景 |", "| --- | --- | --- |"])
    for x in skills:
        if x["source_id"] not in {"xxg-portrait-light", "ai-portrait-light", "genai-portrait"}:
            continue
        preview=x.get("preview")
        visual=("<img src=\""+preview+"\" width=\"145\" alt=\""+safe(x["title"],50)+"\">"
                if preview else "—")
        readme.append("| "+visual+" | ["+safe(x["title"],80)+"]("+x["path"]+"/SKILL.md) | "+
                      safe(" / ".join(x.get("use_cases") or x.get("tags") or []),120)+" |")
    readme.extend(["", "**授权提醒：** [x-rush/photo-retouch](https://github.com/x-rush/photo-retouch) 未附许可证，"+
                   "暂仅列入[外部候选目录](catalog/external-skills.yaml)，不复制其内容。", "",
                   "## 按用途挑选","",
                   "| 分类 | Skills 数量 | 用途 |","| --- | ---: | --- |"])
    descriptions={
        "艺术海报":"水彩、炭笔、纸雕、像素与旅行海报",
        "创意风格":"漫画、胶片、印刷和实验视觉",
        "风格迁移":"80 种艺术风格预设",
        "极简印刷":"单双色印刷、网点、留白",
        "杂志排版":"旅行画册、视觉日记与系列海报",
        "极简海报":"建筑线条与抽象图形",
        "动漫插画":"动漫、国风、数字绘画",
        "真实修图":"选片、人像、风景后期",
        "Lightroom 后期":"裁切、曝光、调色",
        "专业修图":"曲线、蒙版、PSD 与导出",
        "海报设计":"电影海报、瑞士排版、包豪斯",
        "人像光影":"闪光灯补光、逆光重建与自然肤色",
        "人像布光":"柔雾糖水片、直闪和摄影光位配方",
        "人像精修":"光线迁移、人物保真与背景融合"
    }
    for cat in sorted(cats):
        readme.append("| ["+cat+"](docs/STYLES.md) | "+str(len(cats[cat]))+
                      " | "+descriptions.get(cat,"照片艺术处理")+" |")
    readme.extend(["","## 关键目录","",
      "- "+BT+"skills/"+BT+"：原始 Skill 实体文件（含所需脚本与素材）。",
      "- "+BT+"previews/"+BT+"：风格缩略图。",
      "- "+BT+"catalog/skills.json"+BT+"：Skill 元数据。",
      "- "+BT+"catalog/styles.json"+BT+"：单 Skill 内部的子风格信息。",
      "- "+BT+"catalog/overrides.yaml"+BT+"：手动维护的中文名称与标签。",
      "- "+BT+"config/sources.yaml"+BT+"：同步 Manifest。",
      "- "+BT+"config/upstream-lock.json"+BT+"：Commit SHA 与文件 SHA-256。",
      "- "+BT+"LICENSES/"+BT+"：各上游 LICENSE 原文。",
      "- "+BT+"resources/"+BT+"：非标准 SKILL.md 的创意配方。","",
      "## 更新与安装","",
      "每日上午北京时间 10:17 左右由 GitHub Actions 检查上游；后续更新以 PR 形式供审核。"+
      "同步完成后不需要使用者再访问原仓库。完整安装步骤见 [安装教程](docs/INSTALL.md)。","",
      "本仓库自己编写的代码以根目录 LICENSE 为准；上游原样镜像的 Skills 及视觉素材"+
      "**分别遵守其自身许可证**，本仓库 MIT 许可证不覆盖这些第三方内容。",""])
    save("README.md",readme)

    gallery=["# 摄影与照片风格图鉴","",
       "自动从每个真实 Skill 的 SKILL.md、manifest.json 和来源锁文件生成。",
       "预览代表上游所示的风格示例，并不代表本项目已对每个 Skill 做实测。","",
       "## Wibi Style 视觉风格","",
       "包含全部 51 个独立 Skill，保留每个目录内的 LICENSE 与 NOTICE。","",
       "| 预览 | 风格与特征 | Skill 文件 |","| --- | --- | --- |"]
    for x in wibi:
        pic=x.get("preview")
        picture="<img src=\"../"+pic+"\" width=\"180\" alt=\""+safe(x["title"],60)+"\">" if pic else "—"
        gallery.append("| "+picture+" | **"+safe(x["title"],75)+"**<br>"+
            safe(x.get("description"),130)+" | ["+x["id"]+"](../"+x["path"]+"/SKILL.md) |")
    gallery.extend(["","## 其他风格与真实修图 Skills","",
                    "| 类别 | 预览 | 中文名 / Skill | 风格特征 | 上游 |",
                    "| --- | --- | --- | --- | --- |"])
    for x in skills:
        if x["source_id"]=="wibi-style": continue
        tags=" / ".join(x.get("tags") or [])
        preview=x.get("preview")
        pic=("<img src=\"../"+preview+"\" width=\"110\" alt=\""+safe(x["title"],45)+"\">"
             if preview else "—")
        gallery.append("| "+safe(x["category"])+" | "+pic+" | ["+safe(x["title"],70)+"](../"+
            x["path"]+"/SKILL.md) | "+safe(tags or x.get("description"),135)+" | ["+
            x["source_id"]+"](https://github.com/"+x["source_repo"]+") |")
    for skill_id, headline, intro in [
        ("image-style-transfer", "Image Style Transfer · 80 种艺术风格", "同一个 Skill 内的 80 个编号预设，不是独立安装目录。"),
        ("anime-image-restyle", "Anime Restyle · 71 种动漫风格", "使用下表中的风格 key 来指定动漫转换画风。"),
        ("poster-generator", "Poster Generator · 20 种设计版式", "海报 Skill 内的设计风格名，可用来指导版式选择。"),
        ("photo-editing-craft", "Photo Editing Craft · 14 套修图配方", "这些是实际像素处理配方，而不是生成式视觉风格。"),
    ]:
        candidates = [x for x in presets if x["skill_id"] == skill_id]
        gallery.extend(["", "## " + headline, "", intro, "",
                        "| 标识 | 名称 | Skill |", "| --- | --- | --- |"])
        for x in candidates:
            code = str(x["number"]) if "number" in x else x["key"]
            gallery.append("| " + code + " | " + safe(x["title"], 115) +
                           " | [" + skill_id + "](../skills/" + skill_id + "/SKILL.md) |")
    gallery.extend(["", "[80 种风格的完整提示词](../skills/image-style-transfer/references/style-library.md) · "
                    "[动漫风格 key 详细规则](../skills/anime-image-restyle/references/style-registry.md)", ""])
    save("docs/STYLES.md",gallery)

    provenance=["# 上游来源与许可证","",
      "本项目同步的是可安装 Skills 及必要依赖，不是整仓库 1:1 克隆所有案例图库和开发历史。",
      "各上游原始版权声明请以 LICENSES/ 与各 Skill 内的 LICENSE/NOTICE 为准。","",
      "| 源仓库 | 独立 Skills | 上游版本 Commit | 授权 |",
      "| --- | ---: | --- | --- |"]
    for s in sources:
        d=locks.get(s["id"],{})
        sha=d.get("commit","")
        version=("["+sha[:12]+"](https://github.com/"+s["repo"]+"/commit/"+sha+")") if sha else "—"
        provenance.append("| ["+s["repo"]+"](https://github.com/"+s["repo"]+") | "+
                         str(len(groups[s["id"]]))+" | "+version+" | "+safe(s["license"],100)+" |")
    provenance.extend(["","## 新增人像修图的授权与依赖","",
        "- **XXG Portrait Rebuild Light**：上游 MIT；主要是光影工作流与核对脚本，需外部实际修图后端。",
        "- **AI Portrait Light**：上游文本/图片 CC BY 4.0，代码 MIT；署名与原有 CC BY 4.0 条款必须保留；镜像仅保存其许可明确覆盖的早期示例预览。最新示例图从上游获取。",
        "- **GenAI Portrait Skill**：上游 MIT；其 Python CLI 依赖须另行安装，生成式编辑可能需要 OpenAI/Gemini 等服务凭据。",
        "- **Photo Retouch（x-rush）**：上游没有明确 LICENSE，本仓库只提供外部链接与介绍，不收录代码或 Skill 正文。", "",
        "## Wibi Style 特殊条款","",
        "上游对自动化工具使用 MIT 条款，对原创视觉规则与提示词使用个人非商业许可；"+
        "各目录保留作者署名、LICENSE 和 NOTICE。第三方图片与字体可能各有额外要求。",
        "用户表示已经获得导入许可，但公开镜像不等于项目向第三人发放商业使用权。","",
        "本项目不是上述上游项目的官方发行版。",""])
    save("docs/SOURCES.md",provenance)
    print("Generated README, gallery and license/source docs:",len(skills),"Skills,",len(presets),"presets")

if __name__=="__main__":
    generate()
