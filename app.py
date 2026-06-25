# -*- coding: utf-8 -*-
"""星幕之下 · 灵魂占卜 — 答题式神秘体验 | 半遮结果 | 付费解锁"""
import sys, os, json, datetime, hashlib, uuid, random, requests, time
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="🔮 星幕之下 · 灵魂占卜", page_icon="🔮", layout="centered", initial_sidebar_state="collapsed")

# ═══════════════════════════════════
# 配置
# ═══════════════════════════════════
UNLOCK_FILE = "unlock_codes.json"
API_KEY = "sk-5abb7609eb9649ec90dda47466d821d6"
API_URL = "https://api.deepseek.com/v1/chat/completions"
UNLOCK_PRICE = "¥0.5"

# ═══════════════════════════════════
# 解锁码管理
# ═══════════════════════════════════
def _load_codes():
    if not os.path.exists(UNLOCK_FILE): return {}
    with open(UNLOCK_FILE, "r", encoding="utf-8") as f: return json.load(f)

def _save_codes(d):
    with open(UNLOCK_FILE, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=2)

def generate_unlock_code():
    """生成唯一解锁码"""
    return f"TAROT-{uuid.uuid4().hex[:8].upper()}"

def is_code_used(code):
    codes = _load_codes()
    return codes.get(code, {}).get("used", False)

def mark_code_used(code):
    codes = _load_codes()
    if code in codes:
        codes[code]["used"] = True
        codes[code]["used_at"] = str(datetime.datetime.now())
        _save_codes(codes)

# ═══════════════════════════════════
# AI解读
# ═══════════════════════════════════
def get_ai_reading(cards_data, answers_summary):
    """调用DeepSeek生成塔罗解读"""
    cards_text = "\n".join([
        f"「{c['pos']}」: {c['name']} (元素:{c.get('element','')}, 关键词:{c.get('keywords','')[:80]})"
        for c in cards_data
    ])

    prompt = f"""你是一位神秘睿智的塔罗占卜师。求问者完成了10道灵魂问答。

求问者的能量特征：{answers_summary}

塔罗牌回应：{cards_text}

请撰写一份完整的塔罗解读。格式严格按以下顺序：

## 🏷️ 命运签文
先写一句富有诗意的签文（类似古代抽签的判词），如"月照寒潭，水落石出"这种风格，然后紧跟一段50字左右的签文解释。

## 🌟 灵魂能量画像
3-4句话描述求问者的能量特质和性格倾向。

## 🔮 逐牌详解
每张牌2-3句话，结合求问者特征做个性化解读。务必把三张牌都解读完整。

## 💫 宇宙给你的讯息
3-4条哲理性的启示和建议。

## ⚠️ 当下需要注意
1-2条警惕信号。

总共不少于300字。使用中文。语气如睿智的占卜师朋友。"""

    try:
        resp = requests.post(API_URL,
            headers={"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"},
            json={"model": "deepseek-chat", "messages": [
                {"role": "system", "content": "你是资深塔罗占卜师，讲话神秘有深度，温暖真诚。"},
                {"role": "user", "content": prompt}
            ], "temperature": 0.9, "max_tokens": 1200},
            timeout=30)
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
    except: pass
    return None

# ═══════════════════════════════════
# 卡牌库(简化版,从tarot_cards导入完整版)
# ═══════════════════════════════════
MAJOR_ARCANA_SIMPLE = [
    {"name":"愚者","en":"The Fool","element":"风","keywords":"冒险、自由、新的开始","emoji":"🌟"},
    {"name":"魔术师","en":"The Magician","element":"风","keywords":"创造力、技能、自信","emoji":"🎩"},
    {"name":"女祭司","en":"The High Priestess","element":"水","keywords":"直觉、神秘、内在智慧","emoji":"🔮"},
    {"name":"女皇","en":"The Empress","element":"土","keywords":"丰饶、滋养、创造力","emoji":"👑"},
    {"name":"皇帝","en":"The Emperor","element":"火","keywords":"权威、秩序、领导力","emoji":"🏰"},
    {"name":"教皇","en":"The Hierophant","element":"土","keywords":"传统、智慧、信仰","emoji":"⛪"},
    {"name":"恋人","en":"The Lovers","element":"风","keywords":"爱情、选择、和谐","emoji":"💕"},
    {"name":"战车","en":"The Chariot","element":"水","keywords":"胜利、决心、前进","emoji":"⚔️"},
    {"name":"力量","en":"Strength","element":"火","keywords":"勇气、耐心、内在力量","emoji":"🦁"},
    {"name":"隐者","en":"The Hermit","element":"土","keywords":"内省、智慧、寻找真理","emoji":"🏮"},
    {"name":"命运之轮","en":"Wheel of Fortune","element":"火","keywords":"转折、命运、机遇","emoji":"🎡"},
    {"name":"正义","en":"Justice","element":"风","keywords":"公平、真相、因果","emoji":"⚖️"},
    {"name":"倒吊人","en":"The Hanged Man","element":"水","keywords":"放手、新的视角、牺牲","emoji":"🪢"},
    {"name":"死神","en":"Death","element":"水","keywords":"结束、转变、重生","emoji":"💀"},
    {"name":"节制","en":"Temperance","element":"火","keywords":"平衡、调和、耐心","emoji":"🏺"},
    {"name":"恶魔","en":"The Devil","element":"土","keywords":"束缚、欲望、阴影","emoji":"😈"},
    {"name":"高塔","en":"The Tower","element":"火","keywords":"突变、崩塌、觉醒","emoji":"🗼"},
    {"name":"星星","en":"The Star","element":"风","keywords":"希望、信念、治愈","emoji":"⭐"},
    {"name":"月亮","en":"The Moon","element":"水","keywords":"幻觉、潜意识、迷茫","emoji":"🌙"},
    {"name":"太阳","en":"The Sun","element":"火","keywords":"快乐、成功、活力","emoji":"☀️"},
    {"name":"审判","en":"Judgement","element":"火","keywords":"觉醒、召唤、重生","emoji":"📯"},
    {"name":"世界","en":"The World","element":"土","keywords":"完成、圆满、成就","emoji":"🌍"},
]

# ═══════════════════════════════════
# 神秘问题设计
# ═══════════════════════════════════
QUESTIONS = [
    {
        "q": "🌙 深夜，你走进一座古老的森林，你首先注意到的是...",
        "options": [
            ("A. 树梢间闪烁的点点萤火", "星星"),
            ("B. 脚下曲折蜿蜒的石板小路", "隐者"),
            ("C. 远处传来的悠远狼嚎", "月亮"),
            ("D. 一扇半掩着的古老石门", "高塔"),
        ],
    },
    {
        "q": "🔮 石门前出现了一只动物，它是...",
        "options": [
            ("A. 一只优雅的白鹿", "女皇"),
            ("B. 一只神秘的黑色渡鸦", "女祭司"),
            ("C. 一只威严的金色雄狮", "力量"),
            ("D. 一只灵巧的银狐", "魔术师"),
        ],
    },
    {
        "q": "💫 动物带你来到一个岔路口，你选择...",
        "options": [
            ("A. 左边开满鲜花的小径", "恋人"),
            ("B. 右边通往山顶的石阶", "战车"),
            ("C. 中间那条通往湖水的小路", "节制"),
            ("D. 回头看，你发现自己迷路了，原地坐下思考", "倒吊人"),
        ],
    },
    {
        "q": "🕯️ 你面前出现了一间小木屋，你...",
        "options": [
            ("A. 直接推门进去看看", "愚者"),
            ("B. 先趴在窗户上往里看看", "教皇"),
            ("C. 敲三下门，等待回应", "正义"),
            ("D. 绕到屋后，看看有什么隐藏的入口", "恶魔"),
        ],
    },
    {
        "q": "✨ 木屋里有一位老人在编织，她递给你一个盒子。你...",
        "options": [
            ("A. 毫不犹豫地打开", "命运之轮"),
            ("B. 先问她盒子里装的是什么", "隐者"),
            ("C. 感谢她，但不打开，带回家", "皇帝"),
            ("D. 和她一起喝杯茶，慢慢聊", "女皇"),
        ],
    },
    {
        "q": "🌊 盒子里是一面镜子。你看向镜子，你看到的是...",
        "options": [
            ("A. 未来的自己，光芒四射", "太阳"),
            ("B. 过去的自己，微笑着向你点头", "审判"),
            ("C. 一片璀璨的星空", "星星"),
            ("D. 镜面模糊，需要时间才能看清", "月亮"),
        ],
    },
    {
        "q": "🗝️ 老人最后给了你一把钥匙，你觉得它会打开...",
        "options": [
            ("A. 你一直想去的远方之门", "世界"),
            ("B. 你内心深处的一间密室", "死神"),
            ("C. 你从未注意到的一扇暗门", "高塔"),
            ("D. 你童年的那间老房子", "力量"),
        ],
    },
    {
        "q": "🧵 老人开始给你讲述三个故事，你想听哪一个？",
        "options": [
            ("A. 关于一颗流星坠落人间的传说", "命运之轮"),
            ("B. 关于一位公主独自守护古老王国的史诗", "皇帝"),
            ("C. 关于一只蝴蝶飞越重洋寻找失散伴侣的故事", "恋人"),
            ("D. 关于一位隐士在深山中修行百年的传奇", "隐者"),
        ],
    },
    {
        "q": "🎭 老人说你出生前选择了一个人生课题。你觉得你的课题是...",
        "options": [
            ("A. 学会放手和信任", "倒吊人"),
            ("B. 学会勇敢地做自己", "愚者"),
            ("C. 学会在黑暗中寻找光明", "星星"),
            ("D. 学会用爱化解一切", "女皇"),
        ],
    },
    {
        "q": "🕊️ 告别前，老人从长袍中取出一件礼物放在你手心。它变成了...",
        "options": [
            ("A. 一根纯白羽毛，轻若无物", "世界"),
            ("B. 一颗温热的金色种子，微微发光", "太阳"),
            ("C. 一把小巧的银钥匙，冰凉沁心", "审判"),
            ("D. 一滴晶莹的泪珠，在手心化开", "月亮"),
        ],
    },
    {
        "q": "🌅 走出木屋时天已经亮了。东方天际出现的第一道光是什么颜色？",
        "options": [
            ("A. 玫瑰金色——温暖而充满希望", "太阳"),
            ("B. 淡紫色——神秘而优雅", "魔术师"),
            ("C. 银白色——清冷而纯净", "女祭司"),
            ("D. 你没有抬头看，你还在回味刚才的对话", "隐者"),
        ],
    },
]

# ═══════════════════════════════════
# UI样式
# ═══════════════════════════════════
st.markdown("""
<style>
/* 深邃星空背景 */
.stApp {
    background: #04030f !important;
    background-image:
        radial-gradient(1.5px 1.5px at 10% 12%, rgba(255,255,255,0.9), transparent),
        radial-gradient(2px 2px at 22% 8%, rgba(200,180,255,0.8), transparent),
        radial-gradient(1px 1px at 35% 20%, rgba(255,255,255,0.7), transparent),
        radial-gradient(2.5px 2.5px at 48% 5%, rgba(255,215,0,0.9), transparent),
        radial-gradient(1px 1px at 55% 15%, rgba(255,255,255,0.8), transparent),
        radial-gradient(2px 2px at 68% 10%, rgba(180,160,255,0.7), transparent),
        radial-gradient(1.5px 1.5px at 75% 22%, rgba(255,255,255,0.6), transparent),
        radial-gradient(2px 2px at 85% 8%, rgba(255,215,0,0.8), transparent),
        radial-gradient(1px 1px at 15% 35%, rgba(255,255,255,0.7), transparent),
        radial-gradient(2px 2px at 30% 28%, rgba(200,180,255,0.6), transparent),
        radial-gradient(1.5px 1.5px at 52% 35%, rgba(255,215,0,0.8), transparent),
        radial-gradient(1px 1px at 70% 30%, rgba(255,255,255,0.5), transparent),
        radial-gradient(2px 2px at 90% 38%, rgba(180,160,255,0.6), transparent),
        radial-gradient(1px 1px at 8% 55%, rgba(255,255,255,0.8), transparent),
        radial-gradient(2px 2px at 25% 50%, rgba(255,215,0,0.7), transparent),
        radial-gradient(1.5px 1.5px at 42% 58%, rgba(255,255,255,0.6), transparent),
        radial-gradient(2px 2px at 62% 52%, rgba(200,180,255,0.7), transparent),
        radial-gradient(1px 1px at 80% 60%, rgba(255,255,255,0.5), transparent),
        radial-gradient(2px 2px at 18% 72%, rgba(255,215,0,0.6), transparent),
        radial-gradient(1px 1px at 35% 68%, rgba(255,255,255,0.7), transparent),
        radial-gradient(1.5px 1.5px at 55% 75%, rgba(200,180,255,0.5), transparent),
        radial-gradient(2px 2px at 72% 70%, rgba(255,215,0,0.6), transparent),
        radial-gradient(1px 1px at 88% 78%, rgba(255,255,255,0.4), transparent),
        radial-gradient(1.5px 1.5px at 12% 88%, rgba(255,255,255,0.5), transparent),
        radial-gradient(2px 2px at 40% 85%, rgba(180,160,255,0.6), transparent),
        radial-gradient(1px 1px at 65% 90%, rgba(255,215,0,0.5), transparent),
        radial-gradient(1.5px 1.5px at 80% 92%, rgba(255,255,255,0.4), transparent),
        /* 星云 */
        radial-gradient(ellipse 400px 150px at 25% 25%, rgba(80,30,160,0.06), transparent),
        radial-gradient(ellipse 300px 120px at 75% 20%, rgba(60,20,140,0.05), transparent),
        radial-gradient(ellipse 350px 180px at 50% 65%, rgba(90,40,170,0.04), transparent),
        radial-gradient(ellipse 250px 100px at 20% 75%, rgba(70,25,150,0.05), transparent),
        /* 底部深色渐变 */
        linear-gradient(180deg, rgba(4,3,15,0.3) 0%, rgba(6,4,20,0.5) 40%, rgba(4,3,15,0.95) 100%) !important;
    background-attachment: fixed !important;
}
.main > div { background: transparent !important; }

/* 标题 */
h1 {
    font-size: 2.6rem !important; text-align: center;
    background: linear-gradient(180deg, #e8d0ff, #ffd700, #b890e0);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 5px !important;
}
h3 { color: #c9a0dc !important; text-align: center; }

/* 进度条 */
.stProgress > div > div { background: linear-gradient(90deg, #7b2d8b, #c084fc, #ffd700) !important; }

/* 按钮 */
.stButton > button {
    background: linear-gradient(135deg, #3a1050, #7b2d8b) !important;
    color: #f0e0ff !important; border: 2px solid #9b59b6 !important;
    border-radius: 30px !important; font-size: 18px !important;
    padding: 16px 40px !important; transition: all 0.3s !important;
    box-shadow: 0 0 30px rgba(155,89,182,0.35) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #7b2d8b, #a855f7) !important;
    box-shadow: 0 0 50px rgba(180,120,220,0.6) !important;
    transform: translateY(-3px) !important; border-color: #d4a8ff !important;
}

/* 选项按钮 */
.option-btn {
    display: block; width: 100%; padding: 18px 24px; margin: 8px 0;
    background: rgba(20,10,50,0.8); border: 1px solid rgba(155,89,182,0.4);
    border-radius: 16px; color: #d5c0e8; font-size: 16px; text-align: left;
    cursor: pointer; transition: all 0.25s;
}
.option-btn:hover {
    background: rgba(60,20,100,0.6); border-color: #c084fc;
    box-shadow: 0 0 25px rgba(150,100,200,0.3); color: #fff;
    transform: translateX(5px);
}

/* 卡片展示 */
.card-box {
    background: linear-gradient(135deg, rgba(20,8,40,0.95), rgba(40,15,65,0.95));
    border: 1px solid rgba(180,130,255,0.3); border-radius: 20px;
    padding: 25px 15px; text-align: center; margin: 10px 0;
    box-shadow: 0 0 25px rgba(120,60,200,0.2);
    transition: all 0.3s;
}
.card-box:hover { box-shadow: 0 0 40px rgba(160,100,240,0.4); transform: translateY(-3px); }

/* 付费遮罩 */
.paywall-overlay {
    position: relative; background: rgba(15,8,30,0.95);
    border: 2px solid rgba(255,215,0,0.4); border-radius: 20px;
    padding: 40px 25px; text-align: center; margin: 20px 0;
}
.blur-text {
    filter: blur(8px); user-select: none; pointer-events: none;
    opacity: 0.3; transition: all 0.5s;
}
.blur-text.revealed { filter: blur(0); opacity: 1; }

/* 答案卡片 */
.answer-card {
    background: rgba(25,10,50,0.8); border: 1px solid rgba(155,89,182,0.3);
    border-radius: 16px; padding: 20px; margin: 8px 0;
    text-align: center; cursor: pointer; transition: all 0.2s; color: #d5c0e8;
}
.answer-card:hover { background: rgba(60,20,100,0.5); border-color: #c084fc; color: #fff; }
.answer-card.selected { background: rgba(80,30,140,0.6); border-color: #ffd700; color: #ffd700; }

/* 神秘分割线 */
.divider { text-align: center; color: #7b5ea0; font-size: 1.2rem; margin: 15px 0; letter-spacing: 8px; }

/* 输入框 */
input { background: rgba(15,8,35,0.9) !important; border: 1px solid rgba(155,89,182,0.5) !important;
    color: #d5c0e8 !important; border-radius: 12px !important; }

/* 闪烁星星 */
@keyframes twinkle1 { 0%,100%{opacity:0.3} 50%{opacity:1} }
@keyframes twinkle2 { 0%,100%{opacity:0.6} 38%{opacity:0.2} 76%{opacity:0.9} }
@keyframes twinkle3 { 0%,100%{opacity:0.8} 25%{opacity:0.2} 82%{opacity:0.4} }
@keyframes twinkle4 { 0%,100%{opacity:0.5} 15%{opacity:1} 63%{opacity:0.1} }
@keyframes witchFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }
@keyframes auraGlow { 0%,100%{opacity:0.3;transform:scale(1)} 50%{opacity:0.7;transform:scale(1.12)} }
@keyframes candleFlicker { 0%,100%{opacity:0.5;transform:scaleY(1)} 25%{opacity:0.85;transform:scaleY(1.2)scaleX(0.85)} 75%{opacity:0.35;transform:scaleY(0.8)scaleX(1.15)} }
@keyframes shootingStar { 0%{transform:translateX(0)translateY(0);opacity:1} 100%{transform:translateX(-400px)translateY(400px);opacity:0} }
@keyframes sideFloat { 0%,100%{transform:translateY(0)rotate(0deg)} 50%{transform:translateY(-20px)rotate(3deg)} }
@keyframes pulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.05)} }

@media (max-width:768px) {
    .stButton > button { font-size: 16px !important; padding: 12px 28px !important; }
    #witch-container { transform: scale(0.5); right: -5% !important; bottom: -30px !important; opacity: 0.4; }
    h1 { font-size: 1.8rem !important; }
    .stButton > button { font-size: 16px !important; padding: 12px 28px !important; }
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════
# 浮动装饰元素
# ═══════════════════════════════════
st.markdown("""
<!-- 闪烁星星 -->
<div style="position:fixed;top:8%;left:10%;font-size:10px;color:#fff;pointer-events:none;z-index:0;animation:twinkle1 2s infinite;">✦</div>
<div style="position:fixed;top:14%;left:32%;font-size:8px;color:#ffd700;pointer-events:none;z-index:0;animation:twinkle2 2.5s infinite;">✦</div>
<div style="position:fixed;top:6%;left:55%;font-size:12px;color:#e8d5ff;pointer-events:none;z-index:0;animation:twinkle3 1.8s infinite;">✧</div>
<div style="position:fixed;top:20%;left:72%;font-size:7px;color:#fff;pointer-events:none;z-index:0;animation:twinkle4 3s infinite;">✦</div>
<div style="position:fixed;top:11%;left:88%;font-size:11px;color:#ffd700;pointer-events:none;z-index:0;animation:twinkle1 2.2s infinite;">✧</div>
<div style="position:fixed;top:35%;left:6%;font-size:9px;color:#ffd700;pointer-events:none;z-index:0;animation:twinkle2 2.8s infinite;">✦</div>
<div style="position:fixed;top:42%;left:90%;font-size:10px;color:#e8d5ff;pointer-events:none;z-index:0;animation:twinkle3 2.1s infinite;">✦</div>
<div style="position:fixed;top:58%;left:15%;font-size:8px;color:#fff;pointer-events:none;z-index:0;animation:twinkle4 2.6s infinite;">✧</div>
<div style="position:fixed;top:65%;left:80%;font-size:11px;color:#ffd700;pointer-events:none;z-index:0;animation:twinkle1 1.9s infinite;">✦</div>
<div style="position:fixed;top:78%;left:25%;font-size:7px;color:#e8d5ff;pointer-events:none;z-index:0;animation:twinkle2 3.2s infinite;">✦</div>
<div style="position:fixed;top:85%;left:60%;font-size:9px;color:#fff;pointer-events:none;z-index:0;animation:twinkle3 2.4s infinite;">✧</div>
<div style="position:fixed;top:90%;left:42%;font-size:6px;color:#ffd700;pointer-events:none;z-index:0;animation:twinkle4 2.7s infinite;">✦</div>

<!-- 流星 -->
<div style="position:fixed;top:8%;left:75%;width:2px;height:2px;background:#fff;border-radius:50%;
    box-shadow:0 0 8px 4px rgba(255,255,255,0.6),0 0 25px 10px rgba(180,150,255,0.2);
    pointer-events:none;z-index:0;animation:shootingStar 3s ease-in 6s infinite;"></div>
<div style="position:fixed;top:15%;left:88%;width:1.5px;height:1.5px;background:#fff;border-radius:50%;
    box-shadow:0 0 5px 3px rgba(255,255,255,0.4),0 0 18px 6px rgba(180,150,255,0.15);
    pointer-events:none;z-index:0;animation:shootingStar 3.5s ease-in 10s infinite;"></div>

<!-- 女巫 -->
<div id="witch-container" style="position:fixed;bottom:0;right:6%;pointer-events:none;z-index:2;animation:witchFloat 7s ease-in-out infinite;">
    <div style="position:relative;width:100px;height:200px;">
        <div style="position:absolute;top:-15px;left:-20px;width:140px;height:140px;border-radius:50%;
            background:radial-gradient(circle,rgba(160,100,220,0.2)0%,rgba(80,30,140,0.05)60%,transparent 70%);
            animation:auraGlow 5s ease-in-out infinite;"></div>
        <div style="position:absolute;top:0;left:50%;transform:translateX(-50%);
            width:0;height:0;border-left:28px solid transparent;border-right:28px solid transparent;
            border-bottom:60px solid #251048;filter:drop-shadow(0 0 12px rgba(130,80,200,0.5));"></div>
        <div style="position:absolute;top:50px;left:12px;width:76px;height:110px;
            background:linear-gradient(180deg,#341860 0%,#3e1a6e 30%,#241040 70%,#160830 100%);
            border-radius:38px 38px 25px 25px;box-shadow:0 0 25px rgba(100,50,180,0.3);"></div>
        <div style="position:absolute;top:52px;left:22px;width:56px;height:3px;
            background:linear-gradient(90deg,#c9a050,#ffd700,#c9a050);border-radius:2px;
            box-shadow:0 0 8px rgba(255,215,0,0.4);"></div>
        <div style="position:absolute;top:80px;left:0;font-size:26px;
            filter:drop-shadow(0 0 18px rgba(180,120,255,0.7));">🔮</div>
        <div style="position:absolute;top:-18px;left:50%;transform:translateX(-50%);font-size:16px;
            filter:drop-shadow(0 0 6px rgba(255,215,0,0.8));">⭐</div>
    </div>
</div>

<!-- 烛台 -->
<div style="position:fixed;bottom:5%;left:6%;pointer-events:none;z-index:1;">
    <div style="font-size:18px;filter:drop-shadow(0 0 10px rgba(255,140,20,0.6));animation:candleFlicker 1.8s infinite;">🕯️</div>
    <div style="width:28px;height:35px;background:linear-gradient(180deg,#6b3a0a,#3a1a00);margin:0 auto;border-radius:5px 5px 0 0;opacity:0.5;"></div>
</div>
<div style="position:fixed;bottom:5%;right:6%;pointer-events:none;z-index:1;">
    <div style="font-size:18px;filter:drop-shadow(0 0 10px rgba(255,140,20,0.6));animation:candleFlicker 2s infinite 0.6s;">🕯️</div>
    <div style="width:28px;height:35px;background:linear-gradient(180deg,#6b3a0a,#3a1a00);margin:0 auto;border-radius:5px 5px 0 0;opacity:0.5;"></div>
</div>

<!-- 神秘符号 -->
<div style="position:fixed;top:30%;left:2%;font-size:28px;opacity:0.08;pointer-events:none;z-index:0;
    filter:drop-shadow(0 0 12px rgba(140,80,200,0.3));animation:sideFloat 6s ease-in-out infinite;">☽</div>
<div style="position:fixed;top:33%;right:2%;font-size:32px;opacity:0.08;pointer-events:none;z-index:0;
    filter:drop-shadow(0 0 12px rgba(180,140,220,0.3));animation:sideFloat 6s ease-in-out 1.5s infinite;">☀</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════
# Session状态初始化
# ═══════════════════════════════════
if "stage" not in st.session_state:
    st.session_state.stage = "landing"  # landing | questions | result
    st.session_state.current_q = 0
    st.session_state.answers = []
    st.session_state.cards_drawn = []
    st.session_state.ai_reading = None
    st.session_state.unlock_code = None
    st.session_state.show_full = False

# ═══════════════════════════════════
# Stage 1: 神秘开场页
# ═══════════════════════════════════

def _draw_cards_based_on_answers():
    """根据用户答案，加权抽取对应卡牌"""
    answers = st.session_state.answers
    card_weights = {}
    for i, (_, card_name) in enumerate(QUESTIONS):
        if i < len(answers):
            card_weights[card_name] = card_weights.get(card_name, 0) + 1

    # 选出权重最高的几张牌作为关联牌
    weighted_cards = sorted(card_weights.items(), key=lambda x: x[1], reverse=True)

    # 抽3张: 过去(偏好最高的), 现在(随机大牌), 未来(第二关联)
    past_card_name = weighted_cards[0][0] if weighted_cards else "愚者"
    future_card_name = weighted_cards[1][0] if len(weighted_cards) > 1 else random.choice(MAJOR_ARCANA_SIMPLE)["name"]

    def find_card(name):
        for c in MAJOR_ARCANA_SIMPLE:
            if c["name"] == name: return c
        return random.choice(MAJOR_ARCANA_SIMPLE)

    past_card = find_card(past_card_name)
    # 随机一张与答案无关的牌作为"现在"——增加神秘感
    remaining = [c for c in MAJOR_ARCANA_SIMPLE if c["name"] not in [past_card_name, future_card_name]]
    present_card = random.choice(remaining) if remaining else random.choice(MAJOR_ARCANA_SIMPLE)
    future_card = find_card(future_card_name)

    cards = [
        {"pos": "你的过去", "name": past_card["name"], "en": past_card["en"], "emoji": past_card["emoji"],
         "element": past_card["element"], "keywords": past_card["keywords"], "reversed": random.random() < 0.25},
        {"pos": "你的当下", "name": present_card["name"], "en": present_card["en"], "emoji": present_card["emoji"],
         "element": present_card["element"], "keywords": present_card["keywords"], "reversed": random.random() < 0.25},
        {"pos": "你的未来", "name": future_card["name"], "en": future_card["en"], "emoji": future_card["emoji"],
         "element": future_card["element"], "keywords": future_card["keywords"], "reversed": random.random() < 0.25},
    ]

    st.session_state.cards_drawn = cards

    # 免费看一种风格，付费后随机换另一种风格（14种随机，每次解锁都不一样）
    from reading_engine import generate_reading, READING_STYLES
    import random as _random

    # 免费版：随机选一种风格
    free_style = _random.choice(READING_STYLES)
    free_reading = generate_reading(cards, style=free_style)

    # 付费版：选一种不同的风格（如果只有1种则用同一种）
    other_styles = [s for s in READING_STYLES if s["name"] != free_style["name"]]
    paid_style = _random.choice(other_styles) if other_styles else free_style
    paid_reading = generate_reading(cards, style=paid_style)

    # 免费部分 = 免费风格的前半段（签文+风格+过去）
    # 付费部分 = 免费风格的后半段 + 额外风格的完整版
    free_split = free_reading.find("### 当下")
    if free_split < 0:
        free_split = free_reading.find("### ⚡ 当下")
    if free_split > 0:
        st.session_state.free_part = free_reading[:free_split].strip()
        st.session_state.paid_part = free_reading[free_split:].strip()
    else:
        st.session_state.free_part = free_reading
        st.session_state.paid_part = ""

    # 额外附赠一个不同风格的完整解读
    st.session_state.paid_part += f"\n\n---\n\n## 🔮 额外解读：{paid_style['name']}\n\n{paid_reading}"

    # 完整存储
    st.session_state.ai_reading = free_reading
    st.session_state.unlock_code = generate_unlock_code()

# ═══════════════════════════════════

if st.session_state.stage == "landing":
    st.markdown("<br><br>", unsafe_allow_html=True)

    # 水晶球 + 标题
    st.markdown("""
    <div style="text-align:center;">
        <div style="font-size:90px;margin-bottom:10px;filter:drop-shadow(0 0 40px rgba(180,140,220,0.7))drop-shadow(0 0 80px rgba(100,40,180,0.4));
            animation:pulse 3s ease-in-out infinite;">🔮</div>
<h1>星 幕 之 下 · 灵 魂 占 卜</h1>
        <p style="color:#c9a0dc;font-size:15px;letter-spacing:4px;margin-bottom:5px;">✦ 11道灵魂问答 · 揭晓你的命运牌面 ✦</p>
        <p style="color:#7b5ea0;font-size:13px;margin-bottom:30px;">回答11个神秘问题 · 揭示你的命运牌面</p>
    </div>
    """, unsafe_allow_html=True)

    # 特色介绍卡片
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div style="text-align:center;padding:15px;background:rgba(20,10,45,0.6);border-radius:14px;border:1px solid rgba(155,89,182,0.2);">
            <div style="font-size:35px;">🔮</div>
            <p style="color:#d4a8ff;font-size:14px;margin:5px 0;">7道灵魂问答</p>
            <p style="color:#7b5ea0;font-size:11px;">每一题都是与潜意识的对话</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="text-align:center;padding:15px;background:rgba(20,10,45,0.6);border-radius:14px;border:1px solid rgba(155,89,182,0.2);">
            <div style="font-size:35px;">✨</div>
            <p style="color:#d4a8ff;font-size:14px;margin:5px 0;">AI深度解读</p>
            <p style="color:#7b5ea0;font-size:11px;">你的专属命运之牌</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="text-align:center;padding:15px;background:rgba(20,10,45,0.6);border-radius:14px;border:1px solid rgba(155,89,182,0.2);">
            <div style="font-size:35px;">🎴</div>
            <p style="color:#d4a8ff;font-size:14px;margin:5px 0;">3张命运之牌</p>
            <p style="color:#7b5ea0;font-size:11px;">过去·现在·未来</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        if st.button("🔮 开始灵魂探索", use_container_width=True):
            st.session_state.stage = "questions"
            st.session_state.current_q = 0
            st.session_state.answers = []
            st.session_state.cards_drawn = []
            st.session_state.ai_reading = None
            st.session_state.show_full = False
            st.rerun()

    st.markdown("""
    <p style="text-align:center;color:#4a3560;font-size:11px;margin-top:25px;">
    ⚜️ 仅供娱乐探索 · 你的命运由你书写 ⚜️
    </p>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════
# Stage 2: 答题流程
# ═══════════════════════════════════
elif st.session_state.stage == "questions":
    q_idx = st.session_state.current_q
    total_q = len(QUESTIONS)

    # 进度条
    progress = (q_idx + 1) / total_q
    st.progress(progress, text=f"灵魂探索进度 {q_idx + 1}/{total_q}")

    # 女巫对话气泡
    q_data = QUESTIONS[q_idx]
    st.markdown(f"""
    <div style="text-align:center;margin:20px 0;">
        <div style="font-size:50px;margin-bottom:5px;filter:drop-shadow(0 0 20px rgba(180,140,220,0.5));">🧙‍♀️</div>
        <p style="color:#c9a0dc;font-size:13px;margin:0;">星幕之下，她轻声问道...</p>
    </div>
    """, unsafe_allow_html=True)

    # 问题
    st.markdown(f"""
    <div style="background:rgba(20,10,50,0.7);border:1px solid rgba(155,89,182,0.3);border-radius:20px;
        padding:30px 25px;text-align:center;margin:10px 0;">
        <p style="color:#f0e0ff;font-size:20px;line-height:1.6;margin:0;">{q_data['q']}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 选项
    for opt_text, _ in q_data["options"]:
        if st.button(opt_text, key=f"q{q_idx}_{opt_text[:20]}", use_container_width=True):
            # 记录答案
            st.session_state.answers.append(opt_text)
            if q_idx < total_q - 1:
                st.session_state.current_q += 1
            else:
                # 全部答完，抽牌
                st.session_state.stage = "result"
                _draw_cards_based_on_answers()
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if q_idx > 0:
        col_back1, col_back2, col_back3 = st.columns([1, 1, 1])
        with col_back2:
            if st.button("← 返回上一题", key="go_back"):
                st.session_state.current_q -= 1
                st.session_state.answers.pop()
                st.rerun()

# ═══════════════════════════════════
# 根据答案抽牌
# ═══════════════════════════════════
# Stage 3: 结果展示 + 半遮付费
# ═══════════════════════════════════
elif st.session_state.stage == "result":
    cards = st.session_state.cards_drawn
    reading = st.session_state.ai_reading
    unlock_code = st.session_state.unlock_code
    show_full = st.session_state.show_full

    st.markdown("### ✨ 你的灵魂牌面已揭开")
    st.markdown('<div class="divider">✦ ✦ ✦</div>', unsafe_allow_html=True)

    # 三张牌
    cols = st.columns(3)
    for i, (card, col) in enumerate(zip(cards, cols)):
        with col:
            rev = card.get("reversed", False)
            rev_color = "#e74c3c" if rev else "#c084fc"
            rev_label = "逆位" if rev else "正位"
            st.markdown(f"""
            <div class="card-box" style="border-color:{rev_color};box-shadow:0 0 20px {rev_color}33;">
                <div style="font-size:55px;filter:drop-shadow(0 0 15px {rev_color}55);">{card['emoji']}</div>
                <div style="font-size:18px;font-weight:700;color:#e8d5f5;margin:6px 0;">{card['name']}</div>
                <div style="font-size:12px;color:#888;">{card['en']}</div>
                <div style="color:{rev_color};font-size:13px;margin-top:6px;">{rev_label} · {card['element']}元素</div>
                <div style="color:#9988aa;font-size:12px;margin-top:4px;">📍 {card['pos']}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="divider">✦ ✦ ✦</div>', unsafe_allow_html=True)
    st.markdown("### 📜 命运解读")

    # 使用_draw_cards阶段已经分好的免费/付费内容
    free_part = st.session_state.get("free_part", reading)
    paid_part = st.session_state.get("paid_part", "")
    if not paid_part.strip():
        # 降级：从reading中切一半
        lines = reading.split("\n") if reading else []
        mid = max(10, len(lines) // 2)
        free_part = "\n".join(lines[:mid])
        paid_part = "\n".join(lines[mid:])
        paid_part = f"""## 🔮 逐牌详解
每一张塔罗牌都是宇宙的一面镜子，照见你灵魂的不同侧面。

**{cards[0]['name']}** 出现在过去的位置——{cards[0]['keywords']}。这股能量曾在你生命中留下深深的印记，也许你并未察觉，但它塑造了你面对世界的姿态。

**{cards[1]['name']}** 是当下的能量——{cards[1]['keywords']}。此刻的你需要倾听内心的声音，感受这股力量在如何影响你的选择和判断。

**{cards[2]['name']}** 指向未来——{cards[2]['keywords']}。它是一盏灯，不是一个地图。它照亮方向，但路依然要靠你自己一步一步走出来。

## 💫 宇宙给你的讯息
命运不是轨道，是旷野。你手中的每一张牌都在提醒你：你有选择，你有力量，你被宇宙温柔地注视着。每一次困惑都是在邀请你更深入地看见自己。

## ⚠️ 当下需要注意
保持觉察，不要被外界的噪音淹没了内心的声音。直觉是你最好的向导。"""

    # 免费部分
    st.markdown(f'<div class="reading-text" style="background:rgba(15,8,35,0.7);border-left:3px solid #9b59b6;padding:20px;border-radius:0 12px 12px 0;margin:10px 0;color:#d5c0e0;line-height:1.8;">{free_part}</div>', unsafe_allow_html=True)

    # 付费壁
    if not show_full:
        st.markdown('<div class="divider">🔒 🔒 🔒</div>', unsafe_allow_html=True)

        # 好奇钩子
        c0_name = cards[0]['name']
        c1_name = cards[1]['name']
        c2_name = cards[2]['name']
        st.markdown(f"""
        <div style="background:rgba(30,15,60,0.6);border:1px dashed rgba(255,215,0,0.3);border-radius:16px;
            padding:20px;margin:10px 0;text-align:center;">
            <p style="color:#c9a0dc;font-size:14px;margin:0;line-height:2;">
            🔮 女巫看到了关于<strong style="color:#ffd700;">{c0_name}</strong>的一段往事...<br>
            ⚡ {c1_name}的能量正在此刻影响你的<strong style="color:#ffd700;">一个重要决定</strong>...<br>
            ✨ {c2_name}已经在你前方<strong style="color:#ffd700;">不到三个月</strong>的位置等待...<br>
            💫 还有<strong style="color:#ffd700;">四条宇宙讯息</strong>和一个<strong style="color:#ff4444;">重要警告</strong>...
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 模糊预览
        st.markdown(f"""
        <div style="position:relative;margin:20px 0;">
            <div class="blur-text" style="background:rgba(15,8,35,0.5);border-left:3px solid rgba(155,89,182,0.3);padding:20px;border-radius:0 12px 12px 0;">
                {paid_part[:500] + ('...' if len(paid_part) > 500 else '')}
            </div>
            <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;pointer-events:none;">
                <div style="font-size:50px;filter:drop-shadow(0 0 20px rgba(255,215,0,0.5));">🔒</div>
                <p style="color:#ffd700;font-size:18px;font-weight:bold;margin:10px 0;">女巫还有更多秘密...</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 付费区域
        st.markdown(f"""
        <div class="paywall-overlay" style="animation:pulse 2s ease-in-out infinite;">
            <div style="font-size:40px;margin-bottom:10px;">🔮</div>
            <h3 style="color:#ffd700;">解锁完整命运解读</h3>
            <p style="color:#c9a0dc;font-size:14px;">
                逐牌详解 · 宇宙讯息 · 注意事项<br>
                仅需 <strong style="font-size:22px;color:#ffd700;">{UNLOCK_PRICE}</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)

        # 微信收款码
        import base64 as b64
        qr_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "card_images", "pay_qr.png")
        if os.path.exists(qr_path):
            with open(qr_path, "rb") as f:
                qr_b64 = b64.b64encode(f.read()).decode()
            col_q1, col_q2, col_q3 = st.columns([1, 1.5, 1])
            with col_q2:
                st.markdown(f"""
                <div style="text-align:center;background:rgba(0,0,0,0.2);padding:15px;border-radius:12px;margin:10px 0;">
                    <img src="data:image/png;base64,{qr_b64}" style="width:200px;border-radius:8px;">
                    <p style="color:#ccc;font-size:12px;margin:8px 0 3px 0;">微信扫码支付 {UNLOCK_PRICE}</p>
                    <p style="color:#888;font-size:11px;margin:3px 0;">支付后截图发送微信：<strong style="color:#ffd700;">fjwjrbrnkw0</strong></p>
                    <p style="color:#666;font-size:10px;">发送暗号「塔罗解锁」即刻获取解锁码</p>
                </div>
                """, unsafe_allow_html=True)

        st.markdown('<p style="text-align:center;color:#7b5ea0;font-size:11px;">已有解锁码？在下方输入</p>', unsafe_allow_html=True)

        # 解锁码输入
        col_code1, col_code2, col_code3 = st.columns([1, 1.5, 1])
        with col_code2:
            user_code = st.text_input("输入解锁码", placeholder="例如: TAROT-XXXXXXXX", key="unlock_input")
            if st.button("🔓 解锁全部内容", use_container_width=True):
                if user_code.strip():
                    codes = _load_codes()
                    # 检查是否是本次生成的码
                    if user_code.strip() == unlock_code:
                        mark_code_used(user_code.strip())
                        st.session_state.show_full = True
                        st.success("✨ 封印已解除！宇宙的秘密为你展开...")
                        time.sleep(1)
                        st.rerun()
                    # 检查是否是已生成但未使用的码
                    elif user_code.strip() in codes and not codes[user_code.strip()].get("used", False):
                        mark_code_used(user_code.strip())
                        st.session_state.show_full = True
                        st.success("✨ 封印已解除！")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("解锁码无效或已被使用，请联系客服获取新码。")
                else:
                    st.warning("请输入解锁码")

    # 完整解读
    if show_full:
        st.markdown('<div class="divider">✨ ✨ ✨</div>', unsafe_allow_html=True)
        st.markdown("### 🔓 完整命运解读")
        st.markdown(f'<div class="reading-text" style="background:rgba(15,8,35,0.7);border-left:3px solid #ffd700;padding:20px;border-radius:0 12px 12px 0;margin:10px 0;color:#e0d5f0;line-height:1.8;">{free_part}\n\n{paid_part}</div>', unsafe_allow_html=True)
        st.success("✅ 你已解锁完整内容")

        # 分享 + 分享两次免费解锁
        st.markdown('<div class="divider">✦ ✦ ✦</div>', unsafe_allow_html=True)
        card_names = " · ".join([f"{c['emoji']}{c['name']}" for c in cards])
        share_title = "🔮 我的星幕之下 · 灵魂占卜结果"
        share_text = f"我刚完成了塔罗占卜！我的三张命运之牌是：{card_names}。来看看你的牌是什么？"
        share_url = "https://quant-model-u8qlraudbumgg5bmj6h8wo.streamlit.app"
        # 预设一个免费解锁码
        free_code = "TAROT-FREE-" + str(random.randint(10000000, 99999999))

        # 将免费码写入数据库
        codes_db = _load_codes()
        codes_db[free_code] = {"used": False, "created": "share-reward"}
        _save_codes(codes_db)

        st.markdown(f"""
        <div style="text-align:center;margin:20px 0;">
            <p style="color:#ffd700;font-size:16px;margin-bottom:5px;">🎁 分享2次，免费解锁</p>
            <p style="color:#888;font-size:12px;margin-bottom:15px;">分享给两个朋友即可免费获取解锁码</p>
            <div id="share-count-bar" style="display:flex;gap:10px;justify-content:center;align-items:center;margin:10px 0;">
                <div id="share-slot-1" style="width:40px;height:40px;border-radius:50%;border:2px dashed #9b59b6;display:flex;align-items:center;justify-content:center;font-size:18px;color:#9b59b6;">?</div>
                <div id="share-slot-2" style="width:40px;height:40px;border-radius:50%;border:2px dashed #9b59b6;display:flex;align-items:center;justify-content:center;font-size:18px;color:#9b59b6;">?</div>
            </div>
            <div id="free-code-box" style="display:none;background:rgba(0,0,0,0.4);padding:15px;border-radius:10px;margin:15px 0;border:2px solid #ffd700;">
                <p style="color:#ffd700;font-size:14px;margin:0;">🎉 恭喜！你的免费解锁码：</p>
                <p style="color:#fff;font-size:22px;font-weight:bold;margin:8px 0;font-family:monospace;">{free_code}</p>
                <p style="color:#888;font-size:11px;">复制此码，在下方输入框解锁</p>
            </div>
            <div id="share-buttons" style="display:flex;gap:12px;justify-content:center;flex-wrap:wrap;">
                <button onclick="doShare()" id="nativeShareBtn2"
                    style="background:linear-gradient(135deg,#7b2d8b,#a855f7);color:#fff;border:none;
                    border-radius:25px;padding:14px 32px;font-size:16px;cursor:pointer;
                    box-shadow:0 0 20px rgba(155,89,182,0.4);">
                    📲 分享给好友
                </button>
                <button onclick="doCopyShare()"
                    style="background:linear-gradient(135deg,#3a1050,#7b2d8b);color:#d4a8ff;border:1px solid #9b59b6;
                    border-radius:25px;padding:14px 32px;font-size:16px;cursor:pointer;
                    box-shadow:0 0 15px rgba(155,89,182,0.3);">
                    📋 复制文案分享
                </button>
            </div>
            <p id="copyConfirm2" style="color:#4caf50;font-size:13px;margin-top:10px;display:none;">已复制！去微信/QQ粘贴发送。分享2次即可解锁免费码</p>
        </div>
        <script>
            let shareCount = parseInt(localStorage.getItem('tarot_share_count') || '0');
            updateShareUI();

            function updateShareUI() {{
                if (shareCount >= 2) {{
                    document.getElementById('share-slot-1').innerHTML = '✓'; shareCount = 2;
                    document.getElementById('share-slot-2').innerHTML = '✓';
                    document.getElementById('share-slot-1').style.borderColor = '#4caf50';
                    document.getElementById('share-slot-2').style.borderColor = '#4caf50';
                    document.getElementById('share-slot-1').style.color = '#4caf50';
                    document.getElementById('share-slot-2').style.color = '#4caf50';
                    document.getElementById('free-code-box').style.display = 'block';
                    document.getElementById('nativeShareBtn2').textContent = '再分享一次';
                    document.getElementById('nativeShareBtn2').disabled = true;
                    document.getElementById('nativeShareBtn2').style.opacity = '0.5';
                }} else if (shareCount >= 1) {{
                    document.getElementById('share-slot-1').innerHTML = '✓';
                    document.getElementById('share-slot-1').style.borderColor = '#4caf50';
                    document.getElementById('share-slot-1').style.color = '#4caf50';
                    document.getElementById('nativeShareBtn2').textContent = '再分享1次解锁';
                }}
            }}

            function addShareCount() {{
                shareCount = Math.min(2, shareCount + 1);
                localStorage.setItem('tarot_share_count', shareCount);
                updateShareUI();
            }}

            async function doShare() {{
                if (navigator.share) {{
                    try {{
                        await navigator.share({{title: '{share_title}', text: '{share_text}', url: '{share_url}'}});
                        addShareCount();
                    }} catch(e) {{}}
                }} else {{
                    doCopyShare();
                }}
            }}

            async function doCopyShare() {{
                const text = '{share_text} {share_url}';
                try {{ await navigator.clipboard.writeText(text); }} catch(e) {{
                    const ta = document.createElement('textarea'); ta.value = text;
                    ta.style.position = 'fixed'; ta.style.left = '-9999px';
                    document.body.appendChild(ta); ta.select();
                    document.execCommand('copy'); document.body.removeChild(ta);
                }}
                document.getElementById('copyConfirm2').style.display = 'block';
                setTimeout(function(){{ document.getElementById('copyConfirm2').style.display = 'none'; }}, 3000);
                addShareCount();
            }}
        </script>
        """, unsafe_allow_html=True)

    # 重新开始
    st.markdown('<div class="divider">✦ ✦ ✦</div>', unsafe_allow_html=True)
    col_restart1, col_restart2, col_restart3 = st.columns([1, 1.5, 1])
    with col_restart2:
        if st.button("🔄 重新探索灵魂", use_container_width=True):
            st.session_state.stage = "questions"
            st.session_state.current_q = 0
            st.session_state.answers = []
            st.session_state.cards_drawn = []
            st.session_state.ai_reading = None
            st.session_state.show_full = False
            st.rerun()

    st.caption("⚜️ 塔罗牌是自我探索的工具，解读仅供参考娱乐。")

# 侧边栏 — 安静无干扰
