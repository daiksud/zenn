#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate rich, hand-crafted SVGs for the article.
The .mmd files are the source of truth for the diagram *content*;
these SVGs express that content beyond Mermaid's default look.
"""
import os, html

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "svg", "articles", "one-person-one-ai-agent-experience")
os.makedirs(OUT, exist_ok=True)

FONT = "'Hiragino Sans','Hiragino Kaku Gothic ProN','Noto Sans JP','Yu Gothic',sans-serif"

PAL = {
    'blue':   {'g1':'#EFF6FF','g2':'#DBEAFE','stroke':'#2563EB','accent':'#3B82F6','text':'#1E3A8A'},
    'violet': {'g1':'#F6F4FF','g2':'#EDE9FE','stroke':'#7C3AED','accent':'#8B5CF6','text':'#5B21B6'},
    'amber':  {'g1':'#FFFBEB','g2':'#FEF1C9','stroke':'#D97706','accent':'#F59E0B','text':'#92400E'},
    'teal':   {'g1':'#ECFDF5','g2':'#CCFBEF','stroke':'#0D9488','accent':'#10B981','text':'#065F46'},
    'rose':   {'g1':'#FFF1F2','g2':'#FFE0E4','stroke':'#E11D48','accent':'#F43F5E','text':'#9F1239'},
    'slate':  {'g1':'#F8FAFC','g2':'#EAEFF6','stroke':'#94A3B8','accent':'#64748B','text':'#334155'},
}
TXT   = '#0F172A'
TXT2  = '#475569'
MUTED = '#64748B'
GRAY  = '#94A3B8'


def esc(s):
    return html.escape(str(s), quote=True)


def defs():
    grads = []
    markers = []
    for name, p in PAL.items():
        grads.append(
            f'<linearGradient id="g-{name}" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{p["g1"]}"/>'
            f'<stop offset="1" stop-color="{p["g2"]}"/></linearGradient>')
        markers.append(
            f'<marker id="arr-{name}" viewBox="0 0 10 10" refX="8.5" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 L3,5 z" fill="{p["accent"]}"/></marker>')
    markers.append(
        f'<marker id="arr-gray" viewBox="0 0 10 10" refX="8.5" refY="5" '
        f'markerWidth="7.5" markerHeight="7.5" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 L3,5 z" fill="{GRAY}"/></marker>')
    page = ('<linearGradient id="g-page" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#FFFFFF"/>'
            '<stop offset="1" stop-color="#F3F6FB"/></linearGradient>')
    shadow = ('<filter id="sh" x="-25%" y="-25%" width="150%" height="160%">'
              '<feDropShadow dx="0" dy="3" stdDeviation="6" flood-color="#1E293B" flood-opacity="0.13"/></filter>')
    softsh = ('<filter id="sh2" x="-25%" y="-25%" width="150%" height="160%">'
              '<feDropShadow dx="0" dy="1.5" stdDeviation="3" flood-color="#1E293B" flood-opacity="0.10"/></filter>')
    return "<defs>" + page + "".join(grads) + "".join(markers) + shadow + softsh + "</defs>"


def svg_open(w, h):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" font-family="{FONT}">' + defs())


def page_bg(w, h):
    return (f'<rect x="10" y="10" width="{w-20}" height="{h-20}" rx="30" '
            f'fill="url(#g-page)" stroke="#E2E8F0" stroke-width="1.5"/>')


def card(x, y, w, h, pal, rx=18, sh=True, sw=2):
    f = ' filter="url(#sh)"' if sh else ''
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="url(#g-{pal})" stroke="{PAL[pal]["stroke"]}" stroke-width="{sw}"{f}/>')


def plain_card(x, y, w, h, fill="#FFFFFF", stroke="#E2E8F0", rx=14, sw=1.5, sh=True):
    f = ' filter="url(#sh2)"' if sh else ''
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{f}/>')


def text(x, y, s, size=18, color=TXT, weight=400, anchor="middle", spacing=None):
    ls = f' letter-spacing="{spacing}"' if spacing else ''
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}"{ls}>{esc(s)}</text>')


def mtext(x, y, lines, size=18, color=TXT, weight=400, anchor="middle", lh=26):
    spans = "".join(f'<tspan x="{x}" dy="{0 if i==0 else lh}">{esc(l)}</tspan>'
                    for i, l in enumerate(lines))
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{spans}</text>')


def emoji(x, y, ch, size=40, anchor="middle"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}">{ch}</text>')


def arrow(x1, y1, x2, y2, pal='gray', w=2.6, dashed=False):
    color = GRAY if pal == 'gray' else PAL[pal]['accent']
    d = ' stroke-dasharray="2 7" stroke-linecap="round"' if dashed else ' stroke-linecap="round"'
    mk = 'arr-gray' if pal == 'gray' else f'arr-{pal}'
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="{w}" marker-end="url(#{mk})"{d}/>')


def pill(cx, cy, w, h, label, fill, tcolor="#FFFFFF", size=19, weight=700, emoji_ch=None, stroke=None):
    x, y = cx - w/2, cy - h/2
    st = f' stroke="{stroke}" stroke-width="1.5"' if stroke else ''
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{fill}"{st} filter="url(#sh2)"/>'
    if emoji_ch:
        out += emoji(x + h*0.62, cy + size*0.08, emoji_ch, size*1.05, anchor="middle")
        out += text(cx + h*0.25, cy + size*0.36, label, size, tcolor, weight, "middle")
    else:
        out += text(cx, cy + size*0.36, label, size, tcolor, weight, "middle")
    return out


def title_block(w, emj, title, subtitle, y=56, tsize=29, ssize=18):
    out = text(w/2, y, f"{emj}　{title}", tsize, TXT, 800, "middle")
    if subtitle:
        out += text(w/2, y + tsize*1.12, subtitle, ssize, TXT2, 500, "middle")
    return out


def chip(x, y, w, h, label, icon, pal, size=16, lines=None, lh=22,
         icon_size=26, icon_off=30, txoff=58):
    """left-aligned info row: icon + text within a soft box."""
    out = plain_card(x, y, w, h, fill="#FFFFFFEE", stroke=PAL[pal]['g2'], rx=12, sw=1.5)
    out += emoji(x + icon_off, y + h/2 + icon_size*0.32, icon, icon_size)
    tx = x + txoff
    if lines:
        n = len(lines)
        start = y + h/2 - (n-1)*lh/2 + size*0.34
        out += mtext(tx, start, lines, size, PAL[pal]['text'], 600, "start", lh=lh)
    else:
        out += text(tx, y + h/2 + size*0.34, label, size, PAL[pal]['text'], 600, "start")
    return out


def save(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body + "</svg>")
    print("wrote", path)


# Diagrams are authored at the SAME width Zenn displays them (700px), so
# 1 SVG px == 1 displayed px. The body label size is 16px to match the
# article body; titles are larger, captions smaller. Height is unconstrained.
W = 700

# ───────────────────────── Diagram 1 ─────────────────────────
def d1():
    H = 690
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "🤖", "1人1AI時代がやってくる",
                     "ほとんどの人が、スマホで動く“自分専用のAIエージェント”を持つ",
                     y=48, tsize=23, ssize=14)

    cols = [
        (132, "🧑",    "Aさん", ["「沖縄に行きたいから", "ホテルと飛行機を", "予約しといて」"]),
        (350, "🧑‍🦰", "Bさん", ["「あの人のライブの", "チケットを", "買っといて」"]),
        (568, "🧑‍🦱", "Cさん", ["「あれやって」", "「これやって」", "と頼むだけ"]),
    ]
    for cx, ava, name, req in cols:
        s += (f'<circle cx="{cx}" cy="158" r="38" fill="#FFFFFF" '
              f'stroke="{PAL["blue"]["accent"]}" stroke-width="2.5" filter="url(#sh2)"/>')
        s += emoji(cx, 172, ava, 40)
        s += pill(cx, 214, 92, 32, name, PAL['blue']['accent'], "#FFFFFF", 15, 700)
        s += arrow(cx, 232, cx, 252, 'blue', 2.4)
        # phone with AI
        s += card(cx-76, 256, 152, 146, 'blue', rx=20)
        s += plain_card(cx-56, 276, 112, 80, fill="#FFFFFF", stroke="#BFDBFE", rx=10, sh=False)
        s += emoji(cx, 334, "🤖", 44)
        s += text(cx, 390, "自分のAIエージェント", 14, PAL['blue']['text'], 700)
        # request bubble
        by = 424
        s += card(cx-100, by, 200, 132, 'violet', rx=16)
        s += (f'<path d="M{cx-11},{by+1} L{cx+11},{by+1} L{cx},{by-14} z" '
              f'fill="url(#g-violet)" stroke="{PAL["violet"]["stroke"]}" stroke-width="2"/>')
        s += f'<rect x="{cx-11}" y="{by-2}" width="22" height="6" fill="url(#g-violet)"/>'
        s += mtext(cx, by+44, req, 15, PAL['violet']['text'], 600, "middle", lh=30)

    s += pill(W/2, 632, 600, 48, "まるで、全員に専属の秘書がついたかのよう",
              PAL['teal']['stroke'], "#FFFFFF", 17, 800, emoji_ch="💁")
    save("01-one-ai-per-person.svg", s)


# ───────────────────────── Diagram 2 ─────────────────────────
def d2():
    H = 1086
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "🆚", "「コンシェルジュ」と「専属秘書」は何が違うのか",
                     "知っている“コンテキスト”が、応対の質を分ける",
                     y=46, tsize=21, ssize=14)

    # user request card
    s += plain_card(50, 100, 600, 56, fill="#EFF6FF", stroke=PAL['blue']['stroke'], rx=16)
    s += emoji(80, 137, "🧑", 26, "start")
    s += text(W/2+16, 135, "ユーザー：「沖縄に行きたいからホテルと飛行機を予約して」",
              15, PAL['blue']['text'], 700)
    s += arrow(W/2, 160, W/2, 182, 'gray', 2.4)

    def panel(y, pal, emj, title, sub, chips, ticon, think, bullets):
        x, w, h = 40, 620, 380
        out = card(x, y, w, h, pal, rx=20)
        out += emoji(x+42, y+44, emj, 30)
        out += text(x+78, y+42, title, 20, PAL[pal]['text'], 800, "start")
        out += text(x+78, y+66, sub, 13.5, MUTED, 500, "start")
        bx, bw = x+26, w-52
        out += chip(bx, y+86, bw, 50, chips[0][1], chips[0][0], chips[0][2], size=16)
        out += chip(bx, y+148, bw, 50, chips[1][1], chips[1][0], chips[1][2], size=16)
        tb = y+212
        out += plain_card(bx, tb, bw, 148, fill="#FFFFFFEE", stroke=PAL[pal]['g2'], rx=12)
        out += emoji(bx+26, tb+38, ticon, 26, "start")
        out += text(bx+58, tb+36, think, 18, PAL[pal]['text'], 700, "start")
        out += mtext(bx+34, tb+74, bullets, 15, TXT2, 500, "start", lh=29)
        return out

    s += panel(196, 'amber', "🛎️", "AIコンシェルジュ", "サービス側に常駐している",
               [("✅", "知っている：サービスのコンテキスト", 'teal'),
                ("🚫", "知らない：あなた個人のコンテキスト", 'rose')],
               "🤔", "無難な質問しかできない",
               ["・「行き先は本島？ 石垣島？」",
                "・「どんなホテルがお好みで？」",
                "・「航空会社は JAL？ ANA？」"])

    s += emoji(W/2, 600, "🆚", 28)

    s += panel(616, 'violet', "🤝", "専属の秘書（あなたのAI）", "あなた側に常駐している",
               [("✅", "知っている：あなた個人のコンテキスト", 'teal'),
                ("✅", "過去の旅行や好みもすべて把握している", 'teal')],
               "💡", "先回りして提案できる",
               ["・「本島と石垣は訪問済みなので宮古島は？」",
                "・「いつもの星野リゾート系列で？」",
                "・「いつもの JAL ファーストクラスで？」"])

    s += text(W/2, 1058, "同じ依頼でも、“知っているコンテキスト”の差で応対の質はこれだけ変わる",
              15, TXT2, 600)
    save("02-concierge-vs-secretary.svg", s)


# ───────────────────────── Diagram 3 ─────────────────────────
def d3():
    H = 548
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "🚪", "人間は、あなたのサービスに“来なくなる”",
                     "アクセスするのは本人ではなく、その人のAIエージェント",
                     y=46, tsize=22, ssize=14)

    def node(cx, cy, w, h, pal, emj, lines):
        out = card(cx-w/2, cy-h/2, w, h, pal, rx=16)
        out += emoji(cx, cy-6, emj, 40)
        out += mtext(cx, cy+30, lines, 16, PAL[pal]['text'], 700, "middle", lh=20)
        return out

    # Band 1: 従来
    s += pill(82, 130, 88, 32, "従来", PAL['slate']['accent'], "#FFFFFF", 15, 800)
    y1 = 196
    s += node(168, y1, 120, 100, 'blue', "🧑", ["人間"])
    s += node(516, y1, 188, 100, 'amber', "🖥️", ["Webサイト", "サービス"])
    s += arrow(232, y1, 418, y1, 'blue', 2.8)
    s += text(325, y1-16, "自分で訪問・操作", 14, TXT2, 600)

    s += f'<line x1="40" y1="266" x2="{W-40}" y2="266" stroke="#E2E8F0" stroke-width="1.5" stroke-dasharray="3 6"/>'

    # Band 2: 1人1AI時代
    s += pill(110, 298, 146, 32, "1人1AI時代", PAL['teal']['stroke'], "#FFFFFF", 15, 800)
    y2 = 370
    s += node(90, y2, 110, 100, 'blue', "🧑", ["人間"])
    s += node(350, y2, 150, 100, 'violet', "🤖", ["AIエージェント"])
    s += node(610, y2, 116, 100, 'amber', "🖥️", ["サービス"])
    s += arrow(146, y2, 274, y2, 'blue', 2.8)
    s += text(210, y2-16, "依頼", 14, TXT2, 600)
    s += arrow(426, y2, 552, y2, 'violet', 2.8)
    s += mtext(489, y2-24, ["代わりに", "アクセス"], 13, TXT2, 600, "middle", lh=15)
    s += (f'<path d="M90,{y2+50} C90,476 610,476 610,{y2+50}" fill="none" '
          f'stroke="{PAL["rose"]["accent"]}" stroke-width="2.2" stroke-dasharray="3 7" stroke-linecap="round"/>')
    s += pill(350, 480, 252, 38, "人間はもう直接は来ない", PAL['rose']['stroke'], "#FFFFFF", 15, 700, emoji_ch="🚫")
    save("03-human-does-not-visit.svg", s)


# ───────────────────────── Diagram 4 ─────────────────────────
def d4():
    H = 760
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "🔌", "エージェント時代に、サービスが用意すべきもの",
                     "対人間のコンシェルジュではなく、AIが“使える・分かる”入口を",
                     y=46, tsize=21, ssize=14)

    # agent node (top, wide)
    ax, ay, aw, ah = 200, 92, 300, 80
    s += card(ax, ay, aw, ah, 'violet', rx=18)
    s += emoji(ax+48, ay+ah/2+6, "🤖", 40)
    s += text(ax+86, ay+ah/2+6, "ユーザーのAIエージェント", 16, PAL['violet']['text'], 700, "start")

    # connector zone (between agent and service)
    s += arrow(322, ay+ah, 322, 246, 'violet', 2.8)
    s += mtext(308, ay+ah+28, ["API / MCP", "でアクセス"], 13.5, TXT2, 700, "end", lh=17)
    s += arrow(398, 246, 398, ay+ah, 'amber', 2.4, dashed=True)
    s += mtext(412, ay+ah+28, ["知り得ない", "コンテキストを補完"], 13.5, PAL['amber']['text'], 700, "start", lh=17)

    # service container
    sx, sy, sw2, sh2 = 40, 250, 620, 484
    s += card(sx, sy, sw2, sh2, 'slate', rx=22, sw=2)
    s += emoji(sx+40, sy+44, "🏢", 30)
    s += text(sx+74, sy+38, "サービス", 20, TXT, 800, "start")
    s += text(sx+74, sy+62, "AIエージェントを“顧客”として迎える", 14, MUTED, 500, "start")

    ix, iw = sx+26, sw2-52
    # bad item
    s += plain_card(ix, sy+84, iw, 58, fill="#FFF1F2", stroke=PAL['rose']['g2'], rx=12)
    s += emoji(ix+28, sy+84+38, "🚫", 24, "start")
    s += (f'<text x="{ix+58}" y="{sy+84+30}" font-size="18" fill="{PAL["rose"]["text"]}" '
          f'font-weight="700" text-anchor="start" text-decoration="line-through">'
          f'対“人間”のAIコンシェルジュ</text>')
    s += text(ix+58, sy+84+50, "AIエージェント相手では効果が薄い", 13.5, MUTED, 500, "start")

    # good items (single full-width column)
    gy, row_h, gap = sy+150, 70, 14
    items = [
        ("✅", "エージェントが使える API", 'teal', None),
        ("✅", "AI が理解できる API ドキュメント", 'teal', None),
        ("✅", "MCP サーバー", 'teal', None),
        ("✅", "対エージェントの AIコンシェルジュ", 'amber', "📚 サービスのコンテキストを提供する"),
    ]
    for i, (icon, label, pal, sub) in enumerate(items):
        py = gy + i*(row_h+gap)
        s += plain_card(ix, py, iw, row_h, fill="#FFFFFF", stroke=PAL[pal]['g2'], rx=14)
        s += emoji(ix+30, py + row_h/2 + 8, icon, 24, "start")
        if sub:
            s += text(ix+62, py+30, label, 18, PAL[pal]['text'], 700, "start")
            s += text(ix+62, py+54, sub, 13.5, MUTED, 600, "start")
        else:
            s += text(ix+62, py + row_h/2 + 7, label, 18, PAL[pal]['text'], 700, "start")
    save("04-service-needs-api.svg", s)


# ───────────────────────── Diagram 5 ─────────────────────────
def d5():
    H = 520
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "✨", "UX から AX へ",
                     "これから重要になるのは「AIエージェント体験（AX）」",
                     y=48, tsize=24, ssize=14)

    cw, ch, cy = 290, 360, 108
    L, R = 24, 386

    # past (left)
    s += card(L, cy, cw, ch, 'slate', rx=20)
    s += pill(L+cw/2, cy+44, 150, 40, "これまで", PAL['slate']['accent'], "#FFFFFF", 17, 800)
    s += chip(L+22, cy+86, cw-44, 70, "", "🖥️", 'amber', size=14, lh=21,
              lines=["各サービスが", "AIコンシェルジュを用意"], icon_size=23, icon_off=27, txoff=50)
    s += chip(L+22, cy+168, cw-44, 70, "", "🧑", 'blue', size=14, lh=21,
              lines=["人間が自ら", "サービスを使う"], icon_size=23, icon_off=27, txoff=50)
    s += plain_card(L+22, cy+250, cw-44, 72, fill="#FFF7ED", stroke=PAL['amber']['stroke'], rx=14, sw=1.5)
    s += mtext(L+cw/2, cy+280, ["👀 UX（ユーザー体験）", "が競争力"], 15.5, PAL['amber']['text'], 800, "middle", lh=24)

    # center
    midx = 350
    s += emoji(midx, cy+ch/2-6, "➡️", 40)
    s += mtext(midx, cy+ch/2+30, ["パラダイム", "シフト"], 13, PAL['teal']['stroke'], 800, "middle", lh=16)

    # future (right)
    s += card(R, cy, cw, ch, 'teal', rx=20, sw=2.2)
    s += pill(R+cw/2, cy+44, 150, 40, "これから", PAL['teal']['stroke'], "#FFFFFF", 17, 800)
    s += chip(R+22, cy+86, cw-44, 70, "", "🔌", 'teal', size=14, lh=21,
              lines=["各サービスが", "API / MCP サーバーを用意"], icon_size=23, icon_off=27, txoff=50)
    s += chip(R+22, cy+168, cw-44, 70, "", "🤖", 'violet', size=14, lh=21,
              lines=["人間は自分の", "AIエージェントに依頼"], icon_size=23, icon_off=27, txoff=50)
    s += plain_card(R+22, cy+250, cw-44, 72, fill="#ECFEFF", stroke=PAL['teal']['stroke'], rx=14, sw=1.8)
    s += mtext(R+cw/2, cy+280, ["✨ AX（AIエージェント体験）", "が競争力"], 14, PAL['teal']['text'], 800, "middle", lh=24)
    save("05-ux-to-ax.svg", s)


d1(); d2(); d3(); d4(); d5()
print("done")
