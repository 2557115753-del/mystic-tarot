# -*- coding: utf-8 -*-
"""塔罗解读引擎 — 14种趣味风格 · 300+字/条"""
import random, hashlib, json, os

_DIR = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(_DIR, "styles_data.json"), "r", encoding="utf-8") as f:
    READING_STYLES = json.load(f)

FORTUNE_SLIPS = [
    "「云开见月，水落石出」——你一直在等的那件事，最近终于要有个像样的结果了。",
    "「潜龙在渊，待时而动」——现在的你不是在躺平，是在以肉眼不可见的方式蓄大招。",
    "「暗香浮动，月影西斜」——有什么好事正在悄悄地靠近你的生活。别急，让它自然发生。",
    "「大鹏乘风，九万里程」——格局打开！接下来的你要切换到起飞模式了，请系好安全带。",
    "「柳暗花明，峰回路转」——那个你以为无解的问题，即将出现意想不到的优雅解法。",
    "「星垂平野，月涌大江」——你比自己想象中的要辽阔得多。深呼吸。",
    "「松风煮茗，竹雨谈诗」——宇宙建议你调低速度。不是放弃，是换个频率。",
    "「破茧成蝶，凤凰涅槃」——见证奇迹的时刻快到了。现在的难受是蜕变的副作用。再忍一下。",
    "「春江水暖，鸭先知之」——你比你自以为的更早知道答案。别再到处找人求确认了。",
    "「海上生明月，天涯共此时」——在某个你看不见的地方，有人在想着你。你不是孤岛。",
    "「不经一番寒彻骨，怎得梅花扑鼻香」——之前吃的苦没有一粒是白吃的。大礼包在配送中。",
    "「试玉要烧三日满，辨材须待七年期」——别急，你还在窑里烧。你已经很棒了，真的。",
    "「春风得意马蹄疾，一日看尽长安花」——接下来两周运势UP！尽情享受，别不好意思。",
    "「行到水穷处，坐看云起时」——换个方向面对。站起来，风景刚好。",
]

def generate_reading(cards, area="综合", style=None):
    if style is None:
        style = random.choice(READING_STYLES)
    rng = random.Random(hashlib.md5(
        "|".join(f"{c.get('name','')}{c.get('is_reversed',False)}" for c in cards).encode()
    ).hexdigest())
    fortune = random.choice(FORTUNE_SLIPS)
    c1 = cards[0] if len(cards) > 0 else {"name": "命运", "keywords": "未知的力量"}
    c2 = cards[1] if len(cards) > 1 else {"name": "命运", "keywords": "当下的能量"}
    c3 = cards[2] if len(cards) > 2 else {"name": "命运", "keywords": "未来的召唤"}

    parts = []
    parts.append("## 命运签文")
    parts.append(f"**{fortune}**")
    parts.append("")
    parts.append(f"## 今日解读风格：{style['name']}")
    parts.append(f"*{style['intro']}*")
    parts.append("")

    for i, para in enumerate(style["paragraphs"]):
        filled = para.format(
            card1_name=c1.get("name", "命运"), card1_keywords=c1.get("keywords", "指引"),
            card2_name=c2.get("name", "命运"), card2_keywords=c2.get("keywords", "能量"),
            card3_name=c3.get("name", "命运"), card3_keywords=c3.get("keywords", "方向"),
        )
        labels = ["### 过去", "### 当下", "### 未来"]
        parts.append(labels[i])
        parts.append(filled)
        parts.append("")

    parts.append("## 命运小结")
    tips = [
        f"幸运数字：**{rng.randint(1, 99)}**",
        f"今日能量色：**{rng.choice(['深邃紫','月光银','午夜蓝','玫瑰金','翡翠绿','琥珀黄'])}**",
        f"能量窗口：**{rng.choice(['3天内注意','本周五前后','下一个满月','接下来两周','未来一个月内'])}**",
        f"幸运物：**{rng.choice(['紫水晶','白水晶','月光石','黄水晶','黑曜石','粉晶'])}**",
    ]
    parts.extend(tips)
    parts.append("")
    parts.append("---")
    parts.append("*塔罗是自我探索的工具。你相信什么，什么就是你的力量。*")
    return "\n".join(parts)

def generate_share_text(cards, area="综合"):
    if not cards: return "我刚完成了AI塔罗占卜，来看看你的命运之牌！"
    primary = cards[0]
    return "\n".join([
        f"我的塔罗占卜结果！",
        f"命运之牌：{primary.get('emoji','')}{primary.get('name','命运')}",
        f"解读风格超有趣，你也来测测！",
    ])
