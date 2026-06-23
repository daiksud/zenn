---
emoji: 🗝️
published: true
title: 「1人1AI」時代は必ず訪れる。その時代では「AI-UX」が鍵となる
topics: ['ai', 'aiエージェント', 'mcp', 'ux', 'design']
type: tech
---

## 🤖 もうすぐ、全員が「自分のAI」を持つ

2026 年現在、ほとんどの人がスマートフォンを持っています。よって近い将来、ほとんどの人が持つそのスマートフォンの上で、AIエージェントが動いている時代が来るでしょう。

その時代になったら、たぶんみんな自分で作業することはなくなり、「あれやって」「これやって」と手元の自分のAIエージェントにお願いするのが当たり前になるでしょう。「沖縄行きたいからホテルと飛行機予約しといて」「あの人のライブを見たいからチケット買っといて」など。**全員に専属の秘書がいるのと同じ** です。

![1人1AI時代のイメージ。3人それぞれがスマホの中に自分のAIエージェントを持ち、依頼している図](/images/articles/one-person-one-ai-agent-experience/01-one-ai-per-person.webp)
_誰もが、スマホの中に“自分専用のAIエージェント”を持つようになる_

<!-- 図のソース: mermaid/articles/one-person-one-ai-agent-experience/01-one-ai-per-person.mmd（Mermaid＝図の論理）→ svg/articles/one-person-one-ai-agent-experience/01-one-ai-per-person.svg（手書きSVGでリッチ化）→ images/.../01-one-ai-per-person.webp。変更時は .mmd を直し SVG を更新して scripts/svg2webp.mjs で再生成する -->

## 🛎️ 今の「AI対応」の多くは “AIコンシェルジュ” である

2026 年 6 月時点では、私の見る限り、世の中のサービスの「AI 対応しました！」のほとんどが、「**サービスに AI を活用した、チャットボットなどの人間向けのサービスが組み込まれた**」というものが多いように見えます。

![現状のAI対応のイメージ。ホテル・航空券・ECなど各サービスがそれぞれ自社のAIコンシェルジュを持ち、個人を知らないまま無難な質問をする図](/images/articles/one-person-one-ai-agent-experience/02-services-have-concierge.webp)
_前章の「1人1AI」とは対照的に、いまは“各サービス”がそれぞれAIコンシェルジュを抱えている_

<!-- 図のソース: mermaid/articles/one-person-one-ai-agent-experience/02-services-have-concierge.mmd（Mermaid＝図の論理）→ svg/articles/one-person-one-ai-agent-experience/02-services-have-concierge.svg（手書きSVGでリッチ化）→ images/.../02-services-have-concierge.webp -->

これは従来のものに例えると、**各サービスに設置された問い合わせ窓口** のようなものです。それぞれの会社・サービスに専属の対応要員が配置されていて、そこで顧客の要望を聞いて対応してくれます。

ただ、AIコンシェルジュはあくまでも **会社・サービス側のコンテキスト** で配置されているので、一人ひとりの顧客のコンテキストは知りませんし、知り得ません。なので、「俺が好きなアレ買っといて」と言ってもAIコンシェルジュは対応できません。

そこまで極端なケースでなくとも、例えば「沖縄行きたいからホテルと飛行機予約して」という依頼に対し、AIコンシェルジュはそれぞれの担当範囲で無難な対応しかできません。

- ホテルAIコンシェルジュ「どのようなホテルがお好みでしょうか？」
- 航空会社AIコンシェルジュ「飛行機は JAL と ANA のどちらにしますか？」

このように、人間はいろいろとAIコンシェルジュから尋ねられることでしょう。

## 🧭 もう1つの決定的な差は「連携範囲」

そしてAIコンシェルジュとAIエージェントには、**どこまで横断して連携できるか** という差があります。

たとえば先ほどの「沖縄に行きたいからホテルと飛行機予約して」という依頼でも、サービス側のAIコンシェルジュは基本的に自サービスの範囲しか扱えません。ホテル予約サービスならホテル予約まで、航空券予約サービスなら航空券予約までです。ホテル側AIコンシェルジュに「航空券も取って」と言っても、原則そこは越えられません。

一方、個人側のAIエージェントは、目的（この場合は沖縄旅行）を起点に複数サービスを横断できます。

- ホテル予約
- 航空券予約
- レンタカー予約
- 現地アクティビティ予約
- 旅程の立案
- 現地での道案内

![AIコンシェルジュはサービス内に閉じ、AIエージェントは旅行目的で複数サービスを横断できる違いを示す図](/images/articles/one-person-one-ai-agent-experience/07-cross-service-orchestration.webp)
_AIコンシェルジュは「縦に深い」、AIエージェントは「横に広い」_

<!-- 図のソース: mermaid/articles/one-person-one-ai-agent-experience/07-cross-service-orchestration.mmd（Mermaid＝図の論理）→ svg/articles/one-person-one-ai-agent-experience/07-cross-service-orchestration.svg（手書きSVGでリッチ化）→ images/.../07-cross-service-orchestration.webp -->

## 📒 “専属秘書” は、あなたのコンテキストで動く

このように、個人の専属秘書は「**個人のコンテキスト**」で動けます。さらに、過去のことも知っているので、同じ依頼でもこう返してくれるはずです。

- 「すでに本島と石垣島には訪れていますので、今回は宮古島はいかがでしょうか？」
- 「ホテルはいつも泊まっておられる星野リゾート系列でよろしいでしょうか？」
- 「飛行機はいつもの JAL のファーストクラスでよいでしょうか？」

誰もが持つスマートフォンにAIエージェントが搭載され、AIにお願いすることが当たり前になった場合、**全員が上記の体験を得られるようになります**。

![AIコンシェルジュと専属秘書の比較図。知っているコンテキストの違いで応対の質が変わることを示す](/images/articles/one-person-one-ai-agent-experience/03-concierge-vs-secretary.webp)
_「知っているコンテキスト」の差が、そのまま応対の質の差になる_

<!-- 図のソース: mermaid/articles/one-person-one-ai-agent-experience/03-concierge-vs-secretary.mmd（Mermaid＝図の論理）→ svg/articles/one-person-one-ai-agent-experience/03-concierge-vs-secretary.svg（手書きSVGでリッチ化）→ images/.../03-concierge-vs-secretary.webp -->

同じ「沖縄に行きたい」という依頼でも、応対はこれだけ変わります。

| 確認したいこと | 🛎️ AIコンシェルジュ（サービス側） | 🤝 専属秘書（あなた側） |
| --- | --- | --- |
| ホテル | 「どのようなホテルがお好みで？」と確認 | 「いつもの星野リゾート系列でよろしいですか？」 |
| 航空券 | 「JAL と ANA、どちらにしますか？」と確認 | 「いつもの JAL のファーストクラスでよいですか？」 |
| 前提 | あなた個人のことを **知らない** | あなたの履歴・好みを **知っている** |

AIコンシェルジュが悪いわけではありません。立っている場所が「サービス側」である以上、あなた個人のコンテキストは構造的に持ちようがない、というだけの話です。

## 🚪 1人1AI時代、人間はあなたのサービスに「来ない」

そのような「1 人 1 AI」時代において、サービスに必要なAI機能は、AIコンシェルジュのような機能でしょうか？

恐らく異なるでしょう。なぜなら、

:::message
そもそも、**人間があなたのサービスの Web サイトに訪れない**
:::

からです。

アクセスしてくるのは、個人個人のスマートフォンで動作する **AIエージェント** です。

![従来は人間が自らWebサイトに訪れていたが、1人1AI時代はAIエージェントが代わりにアクセスし、人間は直接来なくなることを示す図](/images/articles/one-person-one-ai-agent-experience/04-human-does-not-visit.webp)
_アクセスの主体が「人間」から「その人のAIエージェント」へと変わる_

<!-- 図のソース: mermaid/articles/one-person-one-ai-agent-experience/04-human-does-not-visit.mmd（Mermaid＝図の論理）→ svg/articles/one-person-one-ai-agent-experience/04-human-does-not-visit.svg（手書きSVGでリッチ化）→ images/.../04-human-does-not-visit.webp -->

これは、サービス提供側にとっては大きな前提の変化です。これまで一生懸命に磨いてきた「人間にとって使いやすい画面」を、肝心の人間が見にこなくなるのですから。

## 🔌 必要なのは「AIが使えるAPI」と「AIが分かる使い方」

そのようなAIエージェントに対して、人間向けのAIコンシェルジュを用意してあげても、効果は薄いでしょう。

必要なのは、以下のようなものです。

- AIエージェントが **アクセス・使用できる API**
- AIエージェントが **アクセス・理解できる API の使い方**（ドキュメント）

もしAIコンシェルジュを用意するなら、**対AIエージェント用に** 準備すべきです。つまり、MCP サーバーや API 経由で、AIエージェントとAIコンシェルジュが対話できるようにしてあげます。

:::details 🧩 MCP（Model Context Protocol）とは？
MCP は、AIエージェントと外部のツール・データソースを接続するための **オープンな標準仕様** です。2024 年に Anthropic が提唱しました。

サービス側が「MCP サーバー」を用意しておくと、さまざまなAIエージェントが共通のプロトコルでそのサービスの機能を呼び出せるようになります。AIエージェントにとっての“共通の差込口”だと考えると分かりやすいでしょう。

ここでは「AIエージェントがサービスを利用するための標準的な入口」くらいの理解で読み進めて問題ありません。
:::

ただし、そのAIコンシェルジュは「**そのサービスを熟知している**」必要があります。AIコンシェルジュが一人ひとりのユーザーのコンテキストを知らないのと同じように、AIエージェントは「**サービスのコンテキスト**」を知りません。

![サービスが用意すべきもの。対人間のAIコンシェルジュではなく、API・APIドキュメント・MCPサーバー・対AIエージェントのAIコンシェルジュを用意する図](/images/articles/one-person-one-ai-agent-experience/05-service-needs-api.webp)
_対人間のAIコンシェルジュではなく、AIが「使える・分かる」入口を用意する_

<!-- 図のソース: mermaid/articles/one-person-one-ai-agent-experience/05-service-needs-api.mmd（Mermaid＝図の論理）→ svg/articles/one-person-one-ai-agent-experience/05-service-needs-api.svg（手書きSVGでリッチ化）→ images/.../05-service-needs-api.webp -->

:::message
AIコンシェルジュをサービスに用意するなら、**AIエージェントが知り得ないコンテキストを提供できなければ意味がありません**。「サービスを熟知した案内役」を、人間ではなくAIエージェント向けに開くイメージです。
:::

## ✨ まとめ：UX から AI-UX へ

要するに、これからは以下のような変化が起こるのではないか、と思っています。

| | これまで | これから（1人1AI時代） |
| --- | --- | --- |
| サービスが用意するもの | 🖥️ Web サイト・AIコンシェルジュ | 🔌 AIエージェント向けの API・MCP サーバー |
| 人間の行動 | 自ら Web サイト・サービスを使う | 自分のAIエージェントに依頼する |
| 連携範囲 | 1 サービス内で完結しがち | 複数サービスを目的単位で横断 |
| 重要な体験 | 👀 ユーザー体験（UX） | ✨ AI-UX（AIエージェント向けUX）[^aiux] |

![UXからAI-UXへのパラダイムシフトを示すまとめ図](/images/articles/one-person-one-ai-agent-experience/06-ux-to-ax.webp)
_重要な体験の主役が、人間向けUXからAIエージェント向けのAI-UXへ移っていく_

<!-- 図のソース: mermaid/articles/one-person-one-ai-agent-experience/06-ux-to-ax.mmd（Mermaid＝図の論理）→ svg/articles/one-person-one-ai-agent-experience/06-ux-to-ax.svg（手書きSVGでリッチ化）→ images/.../06-ux-to-ax.webp -->

これまでは「ユーザー体験（UX）」が重要でしたが、これからは「**AI-UX（AIエージェント向けUX）**」が重要になるでしょう。あなたのサービスは、AIエージェントにとって使いやすく、理解しやすい存在になっているでしょうか。

1 人 1 AI 時代に向けて、いまから少しずつ「AIエージェントという新しい顧客」を意識してみてはいかがでしょうか。

[^aiux]: 2026 年 6 月現在、AIエージェント向けのユーザーエクスペリエンスを指すデファクトスタンダードな用語は、まだ定まっていないように見えます。この記事では便宜的に「AI-UX」という呼び方を使います。
