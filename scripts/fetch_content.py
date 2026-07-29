#!/usr/bin/env python3
"""
工作台每日内容抓取器
为5个栏目各生成5条每日推荐内容，输出 daily-data.json
纯标准库实现，无需安装依赖
"""

import json
import os
import time
import datetime
import urllib.request
import urllib.error
import ssl

# 兼容性设置
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

TODAY = datetime.date.today().isoformat()
TS = int(time.time() * 1000)


def fetch_json(url, timeout=8):
    """带错误处理的JSON获取"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (WorkbenchBot/1.0)'
        })
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception as e:
        print(f"  [WARN] Fetch failed: {url} - {e}")
        return None


# ==================== 1. 英语学习 ====================

WORD_BANK = [
    ("serendipity", "n. 意外的发现；机缘巧合"),
    ("resilience", "n. 韧性；恢复力；适应力"),
    ("ephemeral", "adj. 短暂的；瞬息的"),
    ("ubiquitous", "adj. 无处不在的；普遍存在的"),
    ("paradigm", "n. 范例；范式；思维模式"),
    ("eloquent", "adj. 雄辩的；有说服力的"),
    ("meticulous", "adj. 一丝不苟的；细心的"),
    ("pragmatic", "adj. 务实的；实用主义的"),
    ("nostalgia", "n. 怀旧；乡愁"),
    ("inevitable", "adj. 不可避免的；必然的"),
    ("ambivalent", "adj. 矛盾的；犹豫不决的"),
    ("candid", "adj. 坦率的；直言不讳的"),
    ("diligent", "adj. 勤奋的；用功的"),
    ("exquisite", "adj. 精致的；优美的"),
    ("formidable", "adj. 强大的；令人敬畏的"),
    ("gregarious", "adj. 爱交际的；合群的"),
    ("impeccable", "adj. 无懈可击的；完美的"),
    ("lucid", "adj. 清晰的；明白的"),
    ("mundane", "adj. 平凡的；世俗的"),
    ("novice", "n. 新手；初学者"),
    ("obsolete", "adj. 废弃的；过时的"),
    ("placid", "adj. 平静的；温和的"),
    ("quaint", "adj. 古雅的；别致的"),
    ("resolute", "adj. 坚决的；果断的"),
    ("scrutiny", "n. 仔细审查；细看"),
    ("tenacious", "adj. 坚韧的；顽强的"),
    ("unprecedented", "adj. 史无前例的；空前的"),
    ("vibrant", "adj. 充满活力的；鲜艳的"),
    ("whimsical", "adj. 异想天开的；古怪的"),
    ("zealous", "adj. 热情的；狂热的"),
]


def fetch_english():
    print("[1/5] Generating English words...")
    words = []
    day_of_year = datetime.date.today().timetuple().tm_yday
    for i in range(5):
        idx = (day_of_year + i * 7) % len(WORD_BANK)
        word, trans = WORD_BANK[idx]

        # 尝试从 Free Dictionary API 获取英文释义
        dict_data = fetch_json(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        if dict_data and isinstance(dict_data, list) and len(dict_data) > 0:
            try:
                meanings = dict_data[0].get("meanings", [])
                if meanings:
                    defs = meanings[0].get("definitions", [])
                    if defs:
                        en_def = defs[0].get("definition", "")[:100]
                        trans = f"{trans} | EN: {en_def}"
            except Exception:
                pass

        words.append({
            "word": word,
            "trans": trans,
            "date": TODAY,
            "ts": TS + i
        })
    return words


# ==================== 2. 每日阅读 ====================

BOOK_BANK = [
    ("《小王子》- 圣埃克苏佩里", "所有的大人都曾经是小孩，虽然，只有少数的人记得。"),
    ("《活着》- 余华", "人是为活着本身而活着，而不是为了活着之外的任何事物而活着。"),
    ("《百年孤独》- 马尔克斯", "过去都是假的，回忆是一条没有归途的路。"),
    ("《追风筝的人》- 卡勒德·胡赛尼", "为你，千千万万遍。"),
    ("《人间失格》- 太宰治", "生而为人，我很抱歉。"),
    ("《围城》- 钱钟书", "婚姻是一座围城，城外的人想进去，城里的人想出来。"),
    ("《三体》- 刘慈欣", "弱小和无知不是生存的障碍，傲慢才是。"),
    ("《月亮与六便士》- 毛姆", "满地都是六便士，他却抬头看见了月亮。"),
    ("《挪威的森林》- 村上春树", "每个人都有属于自己的一片森林，也许我们从来不曾走过，但它一直在那里。"),
    ("《平凡的世界》- 路遥", "生活不能等待别人来安排，要自己去争取和奋斗。"),
    ("《解忧杂货店》- 东野圭吾", "你的地图是一张白纸，所以即使想决定目的地，也不知道路在哪里。"),
    ("《时间简史》- 霍金", "我们是如此渺小，但我们的思想却能触及宇宙。"),
    ("《非暴力沟通》- 马歇尔·卢森堡", "不带评论的观察是人类智力的最高形式。"),
    ("《被讨厌的勇气》- 岸见一郎", "一切烦恼都来自人际关系。"),
    ("《原子习惯》- 詹姆斯·克利尔", "你不需要成为你试图达到的目标的1%版本，你只需要每天进步一点点。"),
    ("《思考，快与慢》- 丹尼尔·卡尼曼", "我们对自己认为熟知的事物，确信度常常过高。"),
    ("《人类简史》- 尤瓦尔·赫拉利", "智人之所以能主宰世界，是因为能创造并相信虚构故事。"),
    ("《穷查理宝典》- 查理·芒格", "反过来想，总是反过来想。"),
    ("《亲密关系》- 罗兰·米勒", "沟通是亲密关系的血液。"),
    ("《刻意练习》- 安德斯·艾利克森", "天才不是天生的，是刻意练习的结果。"),
    ("《少有人走的路》- 斯科特·派克", "人生苦难重重，这是世界上最伟大的真理之一。"),
    ("《自卑与超越》- 阿德勒", "人的一生就是不断超越自卑的过程。"),
    ("《社会心理学》- 戴维·迈尔斯", "我们高估了自己的与众不同，低估了环境的力量。"),
    ("《心流》- 米哈里", "最优体验是在我们全力以赴做某事时产生的。"),
    ("《原则》- 瑞·达利欧", "痛苦+反思=进步。"),
]


def fetch_readings():
    print("[2/5] Generating reading recommendations...")
    readings = []
    day_of_year = datetime.date.today().timetuple().tm_yday
    for i in range(5):
        idx = (day_of_year + i * 3) % len(BOOK_BANK)
        book, note = BOOK_BANK[idx]
        readings.append({
            "book": book,
            "pages": 30 + (idx * 7) % 50,
            "note": note,
            "date": TODAY,
            "ts": TS + i
        })
    return readings


# ==================== 3. 理财学习 ====================

FINANCE_BANK = [
    ("基金定投策略", "📈 基金", "定期定额投资（DCA）是在固定时间以固定金额投资同一基金。优点：摊平成本、克服人性弱点、适合长期投资。核心原则：止盈不止损。"),
    ("复利的魔力", "💡 心得", "爱因斯坦说复利是世界第八大奇迹。每月投资1000元，年化8%，30年后将变成约150万元。关键是：越早开始越好。"),
    ("紧急备用金", "🏦 存款", "建议储备3-6个月生活开支作为紧急备用金，放在货币基金或活期存款中。这笔钱是应对失业、疾病等突发情况的安全垫。"),
    ("资产配置原则", "📊 其他", "不要把鸡蛋放在一个篮子里。经典配置：股票60%+债券30%+现金10%。年龄越大，债券比例越高。"),
    ("指数基金入门", "📈 基金", "巴菲特多次推荐指数基金。沪深300、标普500等宽基指数基金费率低、分散风险，适合新手。长期持有年化约7-10%。"),
    ("消费与投资", "💡 心得", "收入-储蓄=支出，而不是收入-支出=储蓄。先存后花，才能积累财富。建议储蓄率不低于收入的20%。"),
    ("保险规划", "📊 其他", "保险是风险管理工具。配置顺序：医疗险>重疾险>意外险>寿险。保费支出不超过年收入10%。"),
    ("基金止盈策略", "📈 基金", "常见止盈方法：1)目标收益率法（达20%止盈）；2)估值止盈法（PE高分位减仓）；3)最大回撤法（从最高点回撤5%止盈）。"),
    ("通货膨胀影响", "💡 心得", "通胀率3%意味着购买力每24年减半。现金存银行实际在贬值。必须通过投资跑赢通胀。"),
    ("定投微笑曲线", "📈 基金", "市场下跌时坚持定投，可以用相同金额买入更多份额。当市场回升时获利更多。这就是定投的'微笑曲线'。"),
    ("4%法则", "💡 心得", "退休储蓄4%法则：每年提取储蓄的4%可永续。即年支出25倍=退休金目标。年支出12万则需300万退休金。"),
    ("经济周期认知", "📘 读书", "经济有四阶段：繁荣、衰退、萧条、复苏。繁荣持股、衰退持债、萧条持现金、复苏持商品。"),
    ("记账的重要性", "💡 心得", "记账是理财第一步。了解钱花在哪里，才能找到节省空间。推荐记账APP，坚持3个月就能发现消费模式。"),
    ("可转债打新", "📈 基金", "可转债打新门槛低、风险小。上市首日通常有10-30%收益。坚持打新，一年收益可观。"),
    ("消费降级与投资", "💡 心得", "减少不必要消费：取消不用的订阅、自己做饭、理性购物。每月省下的钱用于投资，长期复利效应惊人。"),
    ("年化收益率理解", "💡 心得", "年化收益率是把当前收益率换算成一年的收益率。不要被短期高收益迷惑，要看长期年化。"),
    ("定投适合的场景", "📈 基金", "定投适合：1)有稳定现金流；2)投资期限3年以上；3)选择波动性大的标的。不适合短期需求和低波动产品。"),
    ("ROE指标", "📊 其他", "ROE（净资产收益率）=净利润/净资产。巴菲特最看重的指标，ROE>15%通常是好公司。连续多年高ROE更佳。"),
    ("PE估值法", "📊 其他", "PE（市盈率）=股价/每股收益。PE低不代表便宜，要看行业平均和历史分位。PE分位<30%相对低估。"),
    ("财务自由门槛", "💡 心得", "财务自由=被动收入>日常支出。不是要很多钱，而是降低欲望+增加被动收入。FIRE运动提倡极简+投资。"),
]


def fetch_finances():
    print("[3/5] Generating finance tips...")
    finances = []
    day_of_year = datetime.date.today().timetuple().tm_yday
    for i in range(5):
        idx = (day_of_year + i * 5) % len(FINANCE_BANK)
        title, category, content = FINANCE_BANK[idx]
        finances.append({
            "title": title,
            "category": category,
            "content": content,
            "date": TODAY,
            "ts": TS + i
        })
    return finances


# ==================== 4. 自媒体计划 ====================

MEDIA_BANK = [
    "一人居的100个生活技巧",
    "30天英语挑战打卡",
    "程序员副业指南",
    "理财小白入门系列",
    "手机拍出电影感",
    "一周穿搭不重样",
    "10分钟搞懂一个经济概念",
    "打工人的一天vlog",
    "读书笔记分享",
    "在家也能做的健身餐",
    "用AI提升效率10倍",
    "周末城市微旅行攻略",
    "零基础学理财",
    "今日热点速评",
    "好物推荐合集",
    "英语口语练习日常",
    "手账排版灵感",
    "效率工具盘点",
    "情绪管理笔记",
    "复古胶片风调色教程",
    "独居女孩安全指南",
    "低成本护肤方案",
    "职场新人沟通技巧",
    "周末一人食食谱",
    "极简生活实践",
]

PLATFORMS = ["📕 小红书", "🎵 抖音", "📺 B站", "📮 公众号", "🎬 视频号"]


def fetch_medias():
    print("[4/5] Generating media topics...")
    medias = []
    day_of_year = datetime.date.today().timetuple().tm_yday
    for i in range(5):
        idx = (day_of_year + i * 4) % len(MEDIA_BANK)
        title = MEDIA_BANK[idx]
        medias.append({
            "title": title,
            "platform": PLATFORMS[i],
            "status": "📝 待创作",
            "date": TODAY,
            "ts": TS + i
        })
    return medias


# ==================== 5. 爆款视频 ====================

VIDEO_BANK = [
    ("一个普通人的早起30天改变", "生活记录类", "🎵 抖音", 520000, 8500000, 43000,
     "选题切中'自律改变人生'共鸣点。前3秒展示对比，3-15秒展示过程，15-30秒展示结果。用数字量化结果（30天），制造期待感。", 5),
    ("5分钟学会做红烧肉", "美食教程类", "📕 小红书", 380000, 6200000, 89000,
     "高搜索量家常菜+时间承诺（5分钟）。俯拍+特写交替，展示食材变化。每步3-5秒不拖沓，步骤编号+一句话总结。", 4),
    ("我用100天学会了画画", "成长挑战类", "📺 B站", 280000, 4500000, 56000,
     "长期挑战+可见进步。从零基础到完成作品的完整弧线。Day1笨拙→Day50进步→Day100成果，渐强式BGM配合成长感。", 5),
    ("为什么你总是存不下钱", "知识科普类", "🎬 视频号", 420000, 7100000, 67000,
     "痛点直击（存不下钱）。结构：提出问题→分析原因→给出方案。用'你'拉近距离，用反问引发思考。", 4),
    ("独居女生的安全感好物", "好物推荐类", "📕 小红书", 610000, 9300000, 120000,
     "精准人群（独居女生）+情绪需求（安全感）。场景化使用演示。痛点+解决方案+使用感受，每个好物15秒。", 5),
    ("周末一个人可以做什么", "生活方式类", "🎵 抖音", 350000, 5800000, 52000,
     "解决'无聊'痛点+提供灵感。清单式+画面切换，快速剪辑每个建议5秒。编号+一句话+画面示范。", 4),
    ("3个习惯让你越来越自信", "个人成长类", "🎬 视频号", 470000, 6800000, 78000,
     "普适性需求+可执行建议。3个具体习惯+每个搭配案例。黄金3秒hook+3段式结构+总结升华。", 5),
    ("100元挑战做一周饭", "挑战类", "🎵 抖音", 590000, 9100000, 95000,
     "低门槛+强冲突（100元vs一周）。记录式+花费明细。每天快速回顾+总计对比。收据特写增加真实感。", 5),
    ("毕业三年我赚了第一个100万", "励志故事类", "📺 B站", 330000, 5200000, 61000,
     "数字冲击力+故事性。前3秒抛出数字，中间讲方法论，结尾给建议。真实感+数据支撑是关键。", 4),
    ("这5个App让你效率翻倍", "工具推荐类", "📕 小红书", 450000, 7000000, 130000,
     "实用型选题+合集形式。每个App15秒，展示核心功能+使用场景。封面用数字吸引点击。", 5),
    ("一个人住有多爽", "生活记录类", "🎵 抖音", 680000, 12000000, 89000,
     "共鸣型选题+碎片化展示。10个'爽'瞬间各5秒。配轻松BGM，文案用反问句开头。", 5),
    ("我每天5点起床后的变化", "自律挑战类", "🎬 视频号", 390000, 6300000, 71000,
     "时间点+变化对比。展示5点起床后的1小时做什么，以及坚持30天后的身体和精神变化。", 4),
]


def fetch_videos():
    print("[5/5] Generating video case studies...")
    videos = []
    day_of_year = datetime.date.today().timetuple().tm_yday
    for i in range(5):
        idx = (day_of_year + i * 3) % len(VIDEO_BANK)
        title, category, platform, likes, views, collects, analysis, stars = VIDEO_BANK[idx]
        videos.append({
            "title": title,
            "creator": category,
            "platform": platform,
            "likes": likes,
            "views": views,
            "collects": collects,
            "analysis": analysis,
            "stars": stars,
            "date": TODAY,
            "ts": TS + i
        })
    return videos


# ==================== 主函数 ====================

def main():
    print("=" * 50)
    print(f"工作台每日内容生成器 - {TODAY}")
    print("=" * 50)

    data = {
        "date": TODAY,
        "generated_at": datetime.datetime.now().isoformat(),
        "words": fetch_english(),
        "readings": fetch_readings(),
        "finances": fetch_finances(),
        "medias": fetch_medias(),
        "videos": fetch_videos()
    }

    print("\n" + "=" * 50)
    print("内容统计:")
    print(f"  英语单词:  {len(data['words'])} 条")
    print(f"  阅读推荐:  {len(data['readings'])} 条")
    print(f"  理财知识:  {len(data['finances'])} 条")
    print(f"  自媒体选题: {len(data['medias'])} 条")
    print(f"  爆款案例:  {len(data['videos'])} 条")
    print("=" * 50)

    # 输出到仓库根目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.dirname(script_dir)
    output_path = os.path.join(repo_root, "daily-data.json")

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n已生成: {output_path}")


if __name__ == "__main__":
    main()
