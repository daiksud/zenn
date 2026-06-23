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


def chip(x, y, w, h, label, icon, pal, size=20, lines=None, lh=26):
    """left-aligned info row: icon + text within a soft box."""
    out = plain_card(x, y, w, h, fill="#FFFFFFEE", stroke=PAL[pal]['g2'], rx=12, sw=1.5)
    out += emoji(x + 32, y + h/2 + 9, icon, 29)
    tx = x + 64
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


# Figures are authored at a narrow width on purpose: Zenn renders images at
# ~700px wide, so display font ≈ svg_font × 700 / W. Keeping W small (~820-940)
# lets normal font sizes (~19-23) read at ~16px, matching the article body.

# ───────────────────────── Diagram 1 ─────────────────────────
def d1():
    W, H = 940, 900
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "🤖", "1人1AI時代がやってくる",
                     "ほとんどの人が、スマホで動く“自分専用のAIエージェント”を持つ",
                     y=64, tsize=31, ssize=19)

    cols = [
        (190, "🧑", "Aさん", '「沖縄に行きたいから', ['ホテルと飛行機を', '予約しといて」']),
        (470, "🧑‍🦰", "Bさん", '「あの人のライブの', ['チケットを', '買っといて」']),
        (750, "🧑‍🦱", "Cさん", '「あれやって」', ['「これやって」', 'と頼むだけ']),
    ]
    for cx, ava, name, l0, rest in cols:
        s += f'<circle cx="{cx}" cy="220" r="46" fill="#FFFFFF" stroke="{PAL["blue"]["accent"]}" stroke-width="2.5" filter="url(#sh2)"/>'
        s += emoji(cx, 236, ava, 48)
        s += pill(cx, 292, 118, 38, name, PAL['blue']['accent'], "#FFFFFF", 20, 700)
        s += arrow(cx, 313, cx, 340, 'blue', 2.6)
        # phone with AI
        s += card(cx-88, 344, 176, 178, 'blue', rx=22)
        s += plain_card(cx-66, 368, 132, 100, fill="#FFFFFF", stroke="#BFDBFE", rx=10, sh=False)
        s += emoji(cx, 436, "🤖", 54)
        s += text(cx, 500, "自分のAIエージェント", 19, PAL['blue']['text'], 700)
        # request bubble
        by = 560
        s += card(cx-134, by, 268, 168, 'violet', rx=18)
        s += f'<path d="M{cx-13},{by+1} L{cx+13},{by+1} L{cx},{by-16} z" fill="url(#g-violet)" stroke="{PAL["violet"]["stroke"]}" stroke-width="2"/>'
        s += f'<rect x="{cx-13}" y="{by-2}" width="26" height="6" fill="url(#g-violet)"/>'
        s += mtext(cx, by+54, [l0]+rest, 22, PAL['violet']['text'], 600, "middle", lh=36)

    s += pill(W/2, 848, 720, 56, "まるで、全員に専属の秘書がついたかのよう", PAL['teal']['stroke'], "#FFFFFF", 24, 800, emoji_ch="💁")
    save("01-one-ai-per-person.svg", s)


# ───────────────────────── Diagram 2 ─────────────────────────
def d2():
    W, H = 860, 1180
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "🆚", "「コンシェルジュ」と「専属秘書」は何が違うのか",
                     "知っている“コンテキスト”が、応対の質を分ける",
                     y=60, tsize=28, ssize=18)

    # user request card
    s += plain_card(W/2-318, 124, 636, 64, fill="#EFF6FF", stroke=PAL['blue']['stroke'], rx=16)
    s += emoji(W/2-292, 165, "🧑", 28, "start")
    s += text(W/2+16, 165, "ユーザー：「沖縄に行きたいからホテルと飛行機を予約して」", 19, PAL['blue']['text'], 700)
    s += arrow(W/2, 192, W/2, 216, 'gray', 2.6)

    def panel(y, pal, emj, title, sub, chips, think_icon, think, bullets):
        cx0, cw = 40, W-80
        out = card(cx0, y, cw, 428, pal, rx=20)
        out += emoji(cx0+44, y+52, emj, 36)
        out += text(cx0+88, y+46, title, 24, PAL[pal]['text'], 800, "start")
        out += text(cx0+88, y+74, sub, 17, MUTED, 500, "start")
        bx, bw = cx0+28, cw-56
        cy0 = y+100
        for (ic, tx, tp) in chips:
            out += chip(bx, cy0, bw, 56, tx, ic, tp, size=20)
            cy0 += 70
        tb = cy0 + 8
        out += plain_card(bx, tb, bw, 178, fill="#FFFFFFEE", stroke=PAL[pal]['g2'], rx=12)
        out += emoji(bx+28, tb+44, think_icon, 28, "start")
        out += text(bx+64, tb+42, think, 20, PAL[pal]['text'], 700, "start")
        out += mtext(bx+38, tb+86, bullets, 19, TXT2, 500, "start", lh=34)
        return out

    s += panel(226, 'amber', "🛎️", "AIコンシェルジュ", "サービス側に常駐している",
               [("✅", "知っている：サービスのコンテキスト", 'teal'),
                ("🚫", "知らない：あなた個人のコンテキスト", 'rose')],
               "🤔", "無難な質問しかできない",
               ["・「行き先は本島？ 石垣島？」",
                "・「どんなホテルがお好みで？」",
                "・「航空会社は JAL？ ANA？」"])

    s += emoji(W/2, 678, "🆚", 30)

    s += panel(694, 'violet', "🤝", "専属の秘書（あなたのAI）", "あなた側に常駐している",
               [("✅", "知っている：あなた個人のコンテキスト", 'teal'),
                ("✅", "過去の旅行や好みもすべて把握している", 'teal')],
               "💡", "先回りして提案できる",
               ["・「本島と石垣は訪問済みなので宮古島は？」",
                "・「いつもの星野リゾート系列で？」",
                "・「いつもの JAL ファーストクラスで？」"])

    s += text(W/2, 1156, "同じ依頼でも、“知っているコンテキスト”の差で応対の質はこれだけ変わる", 18.5, TXT2, 600)
    save("02-concierge-vs-secretary.svg", s)


# ───────────────────────── Diagram 3 ─────────────────────────
def d3():
    W, H = 900, 640
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "🚪", "人間は、あなたのサービスに“来なくなる”",
                     "アクセスするのは本人ではなく、その人のAIエージェント",
                     y=62, tsize=28, ssize=18)

    def node(cx, cy, w, h, pal, emj, lines):
        out = card(cx-w/2, cy-h/2, w, h, pal, rx=18)
        out += emoji(cx, cy-8, emj, 46)
        out += mtext(cx, cy+32, lines, 20, PAL[pal]['text'], 700, "middle", lh=24)
        return out

    # Band 1: 従来
    y1 = 232
    s += pill(106, y1, 132, 44, "従来", PAL['slate']['accent'], "#FFFFFF", 21, 800)
    s += node(326, y1, 196, 124, 'blue', "🧑", ["人間"])
    s += node(712, y1, 232, 124, 'amber', "🖥️", ["Webサイト", "サービス"])
    s += arrow(426, y1, 594, y1, 'blue', 3)
    s += text(510, y1-22, "自分で訪問・操作", 18, TXT2, 600)

    s += f'<line x1="70" y1="346" x2="{W-70}" y2="346" stroke="#E2E8F0" stroke-width="1.5" stroke-dasharray="3 6"/>'

    # Band 2: 1人1AI時代
    y2 = 462
    s += pill(118, y2, 168, 44, "1人1AI時代", PAL['teal']['stroke'], "#FFFFFF", 20, 800)
    s += node(312, y2, 168, 124, 'blue', "🧑", ["人間"])
    s += node(540, y2, 204, 124, 'violet', "🤖", ["AIエージェント"])
    s += node(770, y2, 160, 124, 'amber', "🖥️", ["サービス"])
    s += arrow(398, y2, 436, y2, 'blue', 3)
    s += text(417, y2-22, "依頼", 18, TXT2, 600)
    s += arrow(644, y2, 688, y2, 'violet', 3)
    s += text(666, y2-22, "代わりに", 17, TXT2, 600)
    s += text(666, y2-2, "アクセス", 17, TXT2, 600)
    s += f'<path d="M312,{y2+62} C312,586 770,586 770,{y2+62}" fill="none" stroke="{PAL["rose"]["accent"]}" stroke-width="2.4" stroke-dasharray="3 7" stroke-linecap="round"/>'
    s += pill(541, 588, 280, 42, "人間はもう直接は来ない", PAL['rose']['stroke'], "#FFFFFF", 19, 700, emoji_ch="🚫")
    save("03-human-does-not-visit.svg", s)


# ───────────────────────── Diagram 4 ─────────────────────────
def d4():
    W, H = 900, 760
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "🔌", "エージェント時代に、サービスが用意すべきもの",
                     "対人間のコンシェルジュではなく、AIが“使える・分かる”入口を",
                     y=60, tsize=27, ssize=18)

    # agent (left)
    s += card(48, 356, 208, 150, 'violet', rx=20)
    s += emoji(152, 414, "🤖", 50)
    s += mtext(152, 458, ["ユーザーの", "AIエージェント"], 19, PAL['violet']['text'], 700, "middle", lh=24)

    # service container (right)
    sx, sy, sw2, sh2 = 296, 152, 560, 560
    s += card(sx, sy, sw2, sh2, 'slate', rx=22, sw=2)
    s += emoji(sx+42, sy+48, "🏢", 32)
    s += text(sx+82, sy+42, "サービス", 24, TXT, 800, "start")
    s += text(sx+82, sy+70, "AIエージェントを“顧客”として迎える", 16.5, MUTED, 500, "start")

    ix = sx + 28
    iw = sw2 - 56
    # bad item (rose, strike)
    s += plain_card(ix, sy+92, iw, 64, fill="#FFF1F2", stroke=PAL['rose']['g2'], rx=12)
    s += emoji(ix+30, sy+92+40, "🚫", 27, "start")
    s += (f'<text x="{ix+66}" y="{sy+92+33}" font-size="20" fill="{PAL["rose"]["text"]}" '
          f'font-weight="700" text-anchor="start" text-decoration="line-through">'
          f'対“人間”のAIコンシェルジュ</text>')
    s += text(ix+66, sy+92+55, "AIエージェント相手では効果が薄い", 16, MUTED, 500, "start")

    # good items: single column, full width
    gy = sy + 172
    row_h, gap = 78, 14
    items = [
        ("✅", "エージェントが使える API", 'teal', None),
        ("✅", "AI が理解できる API ドキュメント", 'teal', None),
        ("✅", "MCP サーバー", 'teal', None),
        ("✅", "対エージェントの AIコンシェルジュ", 'amber', "📚 サービスのコンテキストを提供する"),
    ]
    for i, (icon, label, pal, sub) in enumerate(items):
        py = gy + i*(row_h+gap)
        s += plain_card(ix, py, iw, row_h, fill="#FFFFFF", stroke=PAL[pal]['g2'], rx=14)
        s += emoji(ix+32, py + (row_h/2) + 10, icon, 27, "start")
        if sub:
            s += text(ix+68, py+34, label, 20, PAL[pal]['text'], 700, "start")
            s += text(ix+68, py+60, sub, 15.5, MUTED, 600, "start")
        else:
            s += text(ix+68, py + (row_h/2) + 8, label, 20, PAL[pal]['text'], 700, "start")

    # arrows agent <-> service
    s += arrow(256, 404, sx-4, gy+row_h/2, 'violet', 3)
    s += mtext((256+sx)/2-2, 372, ["API / MCP", "でアクセス"], 16, TXT2, 700, "middle", lh=20)
    r4c = gy + 3*(row_h+gap) + row_h/2
    s += (f'<path d="M{sx-4},{r4c} C250,600 210,500 256,452" fill="none" '
          f'stroke="{PAL["amber"]["accent"]}" stroke-width="2.4" stroke-dasharray="2 7" '
          f'stroke-linecap="round" marker-end="url(#arr-amber)"/>')
    s += mtext(150, 568, ["知り得ない", "情報を補完"], 16, PAL['amber']['text'], 700, "middle", lh=20)
    save("04-service-needs-api.svg", s)


# ───────────────────────── Diagram 5 ─────────────────────────
def d5():
    W, H = 900, 600
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "✨", "UX から AX へ",
                     "これから重要になるのは「AIエージェント体験（AX）」",
                     y=62, tsize=30, ssize=18)

    cy, cw, ch = 168, 346, 362
    L, R = 44, 510

    # past
    s += card(L, cy, cw, ch, 'slate', rx=22)
    s += pill(L+cw/2, cy+46, 190, 46, "これまで", PAL['slate']['accent'], "#FFFFFF", 21, 800)
    s += chip(L+26, cy+90, cw-52, 72, "", "🖥️", 'amber', size=19,
              lines=["各サービスが", "AIコンシェルジュを用意"], lh=27)
    s += chip(L+26, cy+176, cw-52, 72, "", "🧑", 'blue', size=19,
              lines=["人間が自ら", "サービスを使う"], lh=27)
    s += plain_card(L+26, cy+260, cw-52, 72, fill="#FFF7ED", stroke=PAL['amber']['stroke'], rx=14, sw=1.5)
    s += mtext(L+cw/2, cy+288, ["👀 UX（ユーザー体験）", "が競争力"], 19, PAL['amber']['text'], 800, "middle", lh=26)

    # center
    midx = L+cw + (R-(L+cw))/2
    s += emoji(midx, cy+ch/2-12, "➡️", 46)
    s += text(midx, cy+ch/2+34, "パラダイムシフト", 14.5, PAL['teal']['stroke'], 800)

    # future
    s += card(R, cy, cw, ch, 'teal', rx=22, sw=2.4)
    s += pill(R+cw/2, cy+46, 190, 46, "これから", PAL['teal']['stroke'], "#FFFFFF", 21, 800)
    s += chip(R+26, cy+90, cw-52, 72, "", "🔌", 'teal', size=19,
              lines=["各サービスが", "API / MCP サーバーを用意"], lh=27)
    s += chip(R+26, cy+176, cw-52, 72, "", "🤖", 'violet', size=19,
              lines=["人間は自分の", "AIエージェントに依頼"], lh=27)
    s += plain_card(R+26, cy+260, cw-52, 72, fill="#ECFEFF", stroke=PAL['teal']['stroke'], rx=14, sw=1.8)
    s += mtext(R+cw/2, cy+288, ["✨ AX（AIエージェント体験）", "が競争力"], 18, PAL['teal']['text'], 800, "middle", lh=26)
    save("05-ux-to-ax.svg", s)


d1(); d2(); d3(); d4(); d5()
print("done")
