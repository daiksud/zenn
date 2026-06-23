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


def title_block(w, emj, title, subtitle, y=74):
    out = text(w/2, y, f"{emj}　{title}", 37, TXT, 800, "middle")
    if subtitle:
        out += text(w/2, y + 38, subtitle, 20.5, TXT2, 500, "middle")
    return out


def chip(x, y, w, h, label, icon, pal, size=18.5, lines=None):
    """left-aligned info row: icon + text within a soft box."""
    out = plain_card(x, y, w, h, fill="#FFFFFFEE", stroke=PAL[pal]['g2'], rx=12, sw=1.5)
    out += emoji(x + 30, y + h/2 + 8, icon, 27)
    tx = x + 58
    if lines:
        n = len(lines)
        start = y + h/2 - (n-1)*12 + 6
        out += mtext(tx, start, lines, size, PAL[pal]['text'], 600, "start", lh=24)
    else:
        out += text(tx, y + h/2 + 7, label, size, PAL[pal]['text'], 600, "start")
    return out


def save(name, body):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body + "</svg>")
    print("wrote", path)


# ───────────────────────── Diagram 1 ─────────────────────────
def d1():
    W, H = 1200, 800
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "🤖", "1人1AI時代がやってくる",
                     "ほとんどの人が、スマホで動く“自分専用のAIエージェント”を持つ", y=78)

    cols = [
        (270, "🧑", "Aさん", '「沖縄に行きたいから', ['ホテルと飛行機を', '予約しといて」']),
        (600, "🧑‍🦰", "Bさん", '「あの人のライブの', ['チケットを', '買っといて」']),
        (930, "🧑‍🦱", "Cさん", '「あれやって」', ['「これやって」', 'と頼むだけ']),
    ]
    for cx, ava, name, l0, rest in cols:
        # avatar
        s += f'<circle cx="{cx}" cy="208" r="46" fill="#FFFFFF" stroke="{PAL["blue"]["accent"]}" stroke-width="2.5" filter="url(#sh2)"/>'
        s += emoji(cx, 224, ava, 46)
        s += pill(cx, 280, 104, 32, name, PAL['blue']['accent'], "#FFFFFF", 17, 700)
        s += arrow(cx, 300, cx, 326, 'blue', 2.6)
        # phone with AI
        s += card(cx-86, 330, 172, 168, 'blue', rx=22)
        s += plain_card(cx-64, 352, 128, 96, fill="#FFFFFF", stroke="#BFDBFE", rx=10, sh=False)
        s += emoji(cx, 416, "🤖", 50)
        s += text(cx, 478, "自分のAIエージェント", 16, PAL['blue']['text'], 700)
        # request bubble
        by = 534
        s += card(cx-152, by, 304, 150, 'violet', rx=18)
        # tail
        s += f'<path d="M{cx-12},{by+1} L{cx+12},{by+1} L{cx},{by-15} z" fill="url(#g-violet)" stroke="{PAL["violet"]["stroke"]}" stroke-width="2"/>'
        s += f'<rect x="{cx-12}" y="{by-2}" width="24" height="6" fill="url(#g-violet)"/>'
        s += mtext(cx, by+52, [l0]+rest, 20, PAL['violet']['text'], 600, "middle", lh=33)

    # bottom banner
    s += pill(W/2, 742, 660, 50, "まるで、全員に専属の秘書がついたかのよう", PAL['teal']['stroke'], "#FFFFFF", 22, 800, emoji_ch="💁")
    save("01-one-ai-per-person.svg", s)


# ───────────────────────── Diagram 2 ─────────────────────────
def d2():
    W, H = 1220, 770
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "🆚", "「コンシェルジュ」と「専属秘書」は何が違うのか",
                     "知っている“コンテキスト”が、応対の質を分ける", y=74)

    # user request card
    s += plain_card(W/2-330, 128, 660, 60, fill="#EFF6FF", stroke=PAL['blue']['stroke'], rx=16)
    s += emoji(W/2-300, 165, "🧑", 26, "start")
    s += text(W/2+14, 165, "ユーザー：「沖縄に行きたいからホテルと飛行機を予約して」", 19.5, PAL['blue']['text'], 700)

    # two columns
    L, R = 322, 898
    cw, cy, ch = 540, 232, 446
    s += arrow(W/2-150, 192, L+40, cy-6, 'gray', 2.4)
    s += arrow(W/2+150, 192, R-40, cy-6, 'gray', 2.4)

    # Concierge (amber)
    s += card(L-cw/2, cy, cw, ch, 'amber', rx=20)
    s += emoji(L-cw/2+44, cy+44, "🛎️", 34)
    s += text(L-cw/2+76, cy+38, "AIコンシェルジュ", 23, PAL['amber']['text'], 800, "start")
    s += text(L-cw/2+76, cy+64, "サービス側に常駐している", 15.5, MUTED, 500, "start")
    bx = L-cw/2+26
    s += chip(bx, cy+90, cw-52, 50, "知っている：サービスのコンテキスト", "✅", 'teal', 18)
    s += chip(bx, cy+150, cw-52, 50, "知らない：あなた個人のコンテキスト", "🚫", 'rose', 18)
    s += plain_card(bx, cy+212, cw-52, 206, fill="#FFFFFFEE", stroke=PAL['amber']['g2'], rx=12)
    s += emoji(bx+24, cy+248, "🤔", 26, "start")
    s += text(bx+54, cy+247, "無難な質問しかできない", 18.5, PAL['amber']['text'], 700, "start")
    s += mtext(bx+30, cy+288, [
        "・「行き先は本島？ 石垣島？」",
        "・「どんなホテルがお好みで？」",
        "・「航空会社は JAL？ ANA？」",
    ], 17.5, TXT2, 500, "start", lh=37)

    # Secretary (violet)
    s += card(R-cw/2, cy, cw, ch, 'violet', rx=20)
    s += emoji(R-cw/2+44, cy+44, "🤝", 34)
    s += text(R-cw/2+76, cy+38, "専属の秘書（あなたのAI）", 23, PAL['violet']['text'], 800, "start")
    s += text(R-cw/2+76, cy+64, "あなた側に常駐している", 15.5, MUTED, 500, "start")
    bx2 = R-cw/2+26
    s += chip(bx2, cy+90, cw-52, 50, "知っている：あなた個人のコンテキスト", "✅", 'teal', 18)
    s += chip(bx2, cy+150, cw-52, 50, "過去の旅行や好みもすべて把握", "✅", 'teal', 18)
    s += plain_card(bx2, cy+212, cw-52, 206, fill="#FFFFFFEE", stroke=PAL['violet']['g2'], rx=12)
    s += emoji(bx2+24, cy+248, "💡", 26, "start")
    s += text(bx2+54, cy+247, "先回りして提案できる", 18.5, PAL['violet']['text'], 700, "start")
    s += mtext(bx2+30, cy+288, [
        "・「本島と石垣は訪問済→宮古島は？」",
        "・「いつもの星野リゾート系列で？」",
        "・「いつもの JAL ファーストで？」",
    ], 17, TXT2, 500, "start", lh=37)

    s += text(W/2, 712, "同じ依頼でも、“知っているコンテキスト”の差で応対の質はこれだけ変わる", 19, TXT2, 600)
    save("02-concierge-vs-secretary.svg", s)


# ───────────────────────── Diagram 3 ─────────────────────────
def d3():
    W, H = 1200, 600
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "🚪", "人間は、あなたのサービスに“来なくなる”",
                     "アクセスするのは本人ではなく、その人のAIエージェント", y=70)

    def node(cx, cy, w, h, pal, emj, lines):
        out = card(cx-w/2, cy-h/2, w, h, pal, rx=18)
        out += emoji(cx, cy-6, emj, 44)
        out += mtext(cx, cy+34, lines, 17.5, PAL[pal]['text'], 700, "middle", lh=22)
        return out

    # Band 1: 従来
    y1 = 210
    s += pill(120, y1, 150, 40, "従来", PAL['slate']['accent'], "#FFFFFF", 19, 800)
    s += node(360, y1, 200, 116, 'blue', "🧑", ["人間"])
    s += node(820, y1, 240, 116, 'amber', "🖥️", ["Webサイト", "サービス"])
    s += arrow(468, y1, 696, y1, 'blue', 3)
    s += text(582, y1-20, "自分で訪問・操作", 17, TXT2, 600)

    # divider
    s += f'<line x1="80" y1="312" x2="{W-80}" y2="312" stroke="#E2E8F0" stroke-width="1.5" stroke-dasharray="3 6"/>'

    # Band 2: 1人1AI時代
    y2 = 430
    s += pill(120, y2, 178, 40, "1人1AI時代", PAL['teal']['stroke'], "#FFFFFF", 18, 800)
    s += node(330, y2, 176, 116, 'blue', "🧑", ["人間"])
    s += node(620, y2, 210, 116, 'violet', "🤖", ["AIエージェント"])
    s += node(950, y2, 210, 116, 'amber', "🖥️", ["サービス"])
    s += arrow(420, y2, 513, y2, 'blue', 3)
    s += text(466, y2-20, "依頼", 16.5, TXT2, 600)
    s += arrow(727, y2, 843, y2, 'violet', 3)
    s += text(785, y2-20, "代わりにアクセス", 16.5, TXT2, 600)
    # crossed direct path human -> service
    s += f'<path d="M330,{y2+62} C330,548 950,548 950,{y2+62}" fill="none" stroke="{PAL["rose"]["accent"]}" stroke-width="2.4" stroke-dasharray="3 7" stroke-linecap="round"/>'
    s += pill(640, 548, 250, 38, "人間はもう直接は来ない", PAL['rose']['stroke'], "#FFFFFF", 17, 700, emoji_ch="🚫")
    save("03-human-does-not-visit.svg", s)


# ───────────────────────── Diagram 4 ─────────────────────────
def d4():
    W, H = 1220, 700
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "🔌", "エージェント時代に、サービスが用意すべきもの",
                     "対人間のコンシェルジュではなく、AIが“使える・分かる”入口を", y=72)

    # agent (left)
    ay = 360
    s += card(70, ay-66, 214, 132, 'violet', rx=20)
    s += emoji(177, ay-12, "🤖", 46)
    s += mtext(177, ay+30, ["ユーザーの", "AIエージェント"], 17.5, PAL['violet']['text'], 700, "middle", lh=22)

    # service container (right)
    sx, sy, sw2, sh2 = 360, 150, 790, 460
    s += card(sx, sy, sw2, sh2, 'slate', rx=22, sw=2)
    s += emoji(sx+44, sy+46, "🏢", 30)
    s += text(sx+76, sy+40, "サービス", 23, TXT, 800, "start")
    s += text(sx+76, sy+66, "AIエージェントを“顧客”として迎える", 15.5, MUTED, 500, "start")

    ix = sx + 30
    iw = sw2 - 60
    # bad item (rose, strike)
    s += plain_card(ix, sy+88, iw, 58, fill="#FFF1F2", stroke=PAL['rose']['g2'], rx=12)
    s += emoji(ix+30, sy+88+36, "🚫", 25, "start")
    s += (f'<text x="{ix+60}" y="{sy+88+36}" font-size="18.5" fill="{PAL["rose"]["text"]}" '
          f'font-weight="600" text-anchor="start" text-decoration="line-through">'
          f'対“人間”のAIコンシェルジュ</text>')
    s += text(ix+iw-24, sy+88+36, "エージェント相手では効果が薄い", 16, MUTED, 500, "end")

    # good items 2x2
    gy = sy + 170
    row_h, gap_y, gap_x = 108, 18, 24
    gw = (iw - gap_x) / 2
    items = [
        ("✅", ["エージェントが使えるAPI"], "teal", None),
        ("✅", ["AIが理解できる使い方", "（API ドキュメント）"], "teal", None),
        ("✅", ["MCP サーバー"], "teal", None),
        ("✅", ["対エージェントの", "AIコンシェルジュ"], "amber", "📚 サービスのコンテキストを提供"),
    ]
    pos = [(ix, gy), (ix+gw+gap_x, gy),
           (ix, gy+row_h+gap_y), (ix+gw+gap_x, gy+row_h+gap_y)]
    lh = 26
    for (icon, lines, pal, sub), (px, py) in zip(items, pos):
        s += plain_card(px, py, gw, row_h, fill="#FFFFFF", stroke=PAL[pal]['g2'], rx=14)
        mid = py + row_h/2
        s += emoji(px+30, mid+9, icon, 25, "start")
        n = len(lines)
        size = 18 if n == 1 else 17.5
        if sub:
            first = mid - (n-1)*lh/2 - 8
            s += mtext(px+62, first, lines, size, PAL[pal]['text'], 700, "start", lh=lh)
            s += text(px+62, first + (n-1)*lh + 27, sub, 14.5, MUTED, 600, "start")
        else:
            first = mid - (n-1)*lh/2 + 6
            s += mtext(px+62, first, lines, size, PAL[pal]['text'], 700, "start", lh=lh)

    # arrows agent <-> service
    s += arrow(284, 354, sx-6, gy+row_h/2, 'violet', 3)
    s += mtext((284+sx)/2, 322, ["API / MCP", "経由でアクセス"], 15.5, TXT2, 700, "middle", lh=20)
    r2c = gy + row_h + gap_y + row_h/2
    s += (f'<path d="M{sx-6},{r2c} C300,560 250,470 286,392" fill="none" '
          f'stroke="{PAL["amber"]["accent"]}" stroke-width="2.4" stroke-dasharray="2 7" '
          f'stroke-linecap="round" marker-end="url(#arr-amber)"/>')
    s += text(232, 556, "知り得ない情報を補完", 15, PAL['amber']['text'], 700)
    save("04-service-needs-api.svg", s)


# ───────────────────────── Diagram 5 ─────────────────────────
def d5():
    W, H = 1200, 600
    s = svg_open(W, H) + page_bg(W, H)
    s += title_block(W, "✨", "UX から AX へ",
                     "これから重要になるのは「AIエージェント体験（AX）」", y=72)

    cy, cw, ch = 180, 446, 320
    L, R = 70, 684

    # past
    s += card(L, cy, cw, ch, 'slate', rx=22)
    s += pill(L+cw/2, cy+44, 200, 44, "これまで", PAL['slate']['accent'], "#FFFFFF", 20, 800)
    s += chip(L+30, cy+86, cw-60, 64, "各サービスがAIコンシェルジュを用意", "🖥️", 'amber', 18, lines=["各サービスが", "AIコンシェルジュを用意"])
    s += chip(L+30, cy+160, cw-60, 64, "人間が自らサービスを使う", "🧑", 'blue', 18)
    s += plain_card(L+30, cy+234, cw-60, 62, fill="#FFF7ED", stroke=PAL['amber']['stroke'], rx=14, sw=1.5)
    s += text(L+cw/2, cy+272, "👀 UX（ユーザー体験）が競争力", 19.5, PAL['amber']['text'], 800)

    # arrow
    midx = L+cw+ (R-(L+cw))/2
    s += emoji(midx, cy+ch/2-18, "➡️", 50)
    s += pill(midx, cy+ch/2+34, 168, 38, "パラダイムシフト", PAL['teal']['stroke'], "#FFFFFF", 16.5, 800)

    # future
    s += card(R, cy, cw, ch, 'teal', rx=22, sw=2.4)
    s += pill(R+cw/2, cy+44, 200, 44, "これから", PAL['teal']['stroke'], "#FFFFFF", 20, 800)
    s += chip(R+30, cy+86, cw-60, 64, "各サービスがAPI / MCPを用意", "🔌", 'teal', 18, lines=["各サービスが", "API / MCPサーバーを用意"])
    s += chip(R+30, cy+160, cw-60, 64, "人間は自分のAIエージェントに依頼", "🤖", 'violet', 18, lines=["人間は自分の", "AIエージェントに依頼"])
    s += plain_card(R+30, cy+234, cw-60, 62, fill="#ECFEFF", stroke=PAL['teal']['stroke'], rx=14, sw=1.8)
    s += text(R+cw/2, cy+272, "✨ AX（AIエージェント体験）が競争力", 18.5, PAL['teal']['text'], 800)
    save("05-ux-to-ax.svg", s)


d1(); d2(); d3(); d4(); d5()
print("done")
