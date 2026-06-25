"""塔罗牌库 — 78张完整牌面数据"""
import random

MAJOR_ARCANA = [
    {"name": "愚者", "en": "The Fool", "num": 0,
     "upright": "新的开始、冒险、天真、无限可能",
     "reversed": "鲁莽、冒险过头、缺乏方向、愚蠢的决定",
     "symbol": "🃏", "element": "风"},
    {"name": "魔术师", "en": "The Magician", "num": 1,
     "upright": "创造力、技能、意志力、掌控局面",
     "reversed": "欺骗、能力不足、滥用权力、计划受阻",
     "symbol": "🎩", "element": "风"},
    {"name": "女祭司", "en": "The High Priestess", "num": 2,
     "upright": "直觉、神秘、潜意识、内在智慧",
     "reversed": "忽视直觉、秘密被揭露、情感封闭",
     "symbol": "🔮", "element": "水"},
    {"name": "女皇", "en": "The Empress", "num": 3,
     "upright": "丰饶、母性、创造力、感官享受",
     "reversed": "依赖、缺乏创造力、情感贫瘠",
     "symbol": "👑", "element": "土"},
    {"name": "皇帝", "en": "The Emperor", "num": 4,
     "upright": "权威、秩序、领导力、稳定",
     "reversed": "专制、失控、缺乏纪律、滥用职权",
     "symbol": "🏰", "element": "火"},
    {"name": "教皇", "en": "The Hierophant", "num": 5,
     "upright": "传统、信仰、导师、精神指引",
     "reversed": "打破传统、反叛、质疑权威",
     "symbol": "⛪", "element": "土"},
    {"name": "恋人", "en": "The Lovers", "num": 6,
     "upright": "爱情、和谐、选择、灵魂伴侣",
     "reversed": "分手、不和谐、错误选择、价值观冲突",
     "symbol": "💕", "element": "风"},
    {"name": "战车", "en": "The Chariot", "num": 7,
     "upright": "胜利、决心、意志力、克服困难",
     "reversed": "失控、失败、方向错误、过度竞争",
     "symbol": "⚔️", "element": "水"},
    {"name": "力量", "en": "Strength", "num": 8,
     "upright": "勇气、内在力量、耐心、温柔的力量",
     "reversed": "软弱、自我怀疑、失控、缺乏勇气",
     "symbol": "🦁", "element": "火"},
    {"name": "隐者", "en": "The Hermit", "num": 9,
     "upright": "内省、寻求真理、独处、智慧",
     "reversed": "孤独、逃避、恐惧独处、拒绝建议",
     "symbol": "🏮", "element": "土"},
    {"name": "命运之轮", "en": "Wheel of Fortune", "num": 10,
     "upright": "命运转折、好运来临、周期变化、机遇",
     "reversed": "厄运、抵抗变化、坏循环、错失良机",
     "symbol": "🎡", "element": "火"},
    {"name": "正义", "en": "Justice", "num": 11,
     "upright": "公正、真相、因果报应、平衡",
     "reversed": "不公、偏见、逃避责任、法律纠纷",
     "symbol": "⚖️", "element": "风"},
    {"name": "倒吊人", "en": "The Hanged Man", "num": 12,
     "upright": "牺牲、换个角度看问题、等待、顿悟",
     "reversed": "无谓牺牲、固执、停滞不前",
     "symbol": "🪢", "element": "水"},
    {"name": "死神", "en": "Death", "num": 13,
     "upright": "结束、转变、放下、新生的前奏",
     "reversed": "抗拒改变、停滞、恐惧结束",
     "symbol": "💀", "element": "水"},
    {"name": "节制", "en": "Temperance", "num": 14,
     "upright": "平衡、调和、耐心、中庸之道",
     "reversed": "失衡、过度、缺乏节制、冲突",
     "symbol": "🕊️", "element": "火"},
    {"name": "恶魔", "en": "The Devil", "num": 15,
     "upright": "束缚、欲望、物质主义、执念",
     "reversed": "摆脱束缚、觉醒、重获自由",
     "symbol": "😈", "element": "土"},
    {"name": "高塔", "en": "The Tower", "num": 16,
     "upright": "突变、崩塌、真相揭露、推倒重来",
     "reversed": "逃避灾难、勉强维持、恐惧改变",
     "symbol": "🗼", "element": "火"},
    {"name": "星星", "en": "The Star", "num": 17,
     "upright": "希望、灵感、治愈、信念",
     "reversed": "绝望、失去信心、疲惫、幻灭",
     "symbol": "⭐", "element": "风"},
    {"name": "月亮", "en": "The Moon", "num": 18,
     "upright": "潜意识、幻觉、恐惧、梦境",
     "reversed": "真相浮现、恐惧消散、解开心结",
     "symbol": "🌙", "element": "水"},
    {"name": "太阳", "en": "The Sun", "num": 19,
     "upright": "快乐、成功、活力、光明",
     "reversed": "暂时的挫折、阴霾、缺乏活力",
     "symbol": "☀️", "element": "火"},
    {"name": "审判", "en": "Judgement", "num": 20,
     "upright": "觉醒、重生、召唤、清算",
     "reversed": "逃避审判、后悔、拒绝觉醒",
     "symbol": "📯", "element": "火"},
    {"name": "世界", "en": "The World", "num": 21,
     "upright": "完成、圆满、成就、旅程终点",
     "reversed": "未完成、延迟、空虚、缺少闭环",
     "symbol": "🌍", "element": "土"},
]

MINOR_SUITS = {
    "圣杯": {"element": "水", "realm": "情感/关系", "symbol": "🏆"},
    "宝剑": {"element": "风", "realm": "思想/沟通", "symbol": "🗡️"},
    "权杖": {"element": "火", "realm": "行动/事业", "symbol": "🪄"},
    "星币": {"element": "土", "realm": "物质/财富", "symbol": "🪙"},
}

MINOR_RANKS = [
    ("首牌", "Ace"), ("二", "Two"), ("三", "Three"), ("四", "Four"),
    ("五", "Five"), ("六", "Six"), ("七", "Seven"), ("八", "Eight"),
    ("九", "Nine"), ("十", "Ten"), ("侍从", "Page"),
    ("骑士", "Knight"), ("皇后", "Queen"), ("国王", "King"),
]

MINOR_MEANINGS = {
    "首牌": {"up": "新的开始、潜力、契机、萌芽", "rev": "错失机会、虚假开始、潜力未发挥"},
    "二": {"up": "平衡、选择、二元性、合作关系", "rev": "失衡、犹豫不决、分裂"},
    "三": {"up": "成长、协作、初步成果、庆祝", "rev": "停滞、团队分裂、成果延迟"},
    "四": {"up": "稳固、休息、安全、保守", "rev": "不安、动荡、过度保守"},
    "五": {"up": "冲突、挑战、竞争、失去", "rev": "和解、妥协、冲突化解"},
    "六": {"up": "和谐、回忆、礼物、善意", "rev": "失去平衡、贪婪、被利用"},
    "七": {"up": "反思、评估、坚持、考验", "rev": "放弃、焦虑、过度担忧"},
    "八": {"up": "行动、前进、突破、放下", "rev": "退缩、无法前进、被困"},
    "九": {"up": "接近完成、满足、独立、收获", "rev": "不满足、依赖、功亏一篑"},
    "十": {"up": "完成、圆满、结果、终点", "rev": "未完成、持续、不愿结束"},
    "侍从": {"up": "学习、好奇、新消息、少年", "rev": "不成熟、坏消息、懒惰"},
    "骑士": {"up": "行动、追求、冒险、激情", "rev": "鲁莽、急躁、半途而废"},
    "皇后": {"up": "成熟、滋养、务实、温柔", "rev": "依赖、情绪化、不切实际"},
    "国王": {"up": "掌控、权威、成就、稳健", "rev": "专制、固执、滥用权力"},
}

def build_deck():
    deck = []
    for card in MAJOR_ARCANA:
        deck.append({**card, "type": "major", "suit": None})
    for suit_name, suit_info in MINOR_SUITS.items():
        for rank_cn, rank_en in MINOR_RANKS:
            meaning = MINOR_MEANINGS[rank_cn]
            deck.append({
                "name": f"{suit_name}{rank_cn}",
                "en": f"{rank_en} of {suit_name}",
                "num": None, "type": "minor",
                "suit": suit_name, "rank": rank_cn,
                "symbol": suit_info["symbol"],
                "element": suit_info["element"],
                "realm": suit_info["realm"],
                "upright": f"{suit_info['realm']} — {meaning['up']}",
                "reversed": f"{suit_info['realm']} — {meaning['rev']}",
            })
    return deck

DECK = build_deck()

def draw_cards(n=1, with_reverse=True):
    """抽n张牌，返回每张牌+正逆位"""
    cards = random.sample(DECK, n)
    results = []
    for c in cards:
        is_reversed = random.random() < 0.3 if with_reverse else False
        results.append({**c, "is_reversed": is_reversed})
    return results
