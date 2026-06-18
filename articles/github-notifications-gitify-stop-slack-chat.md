---
emoji: 🔔
published: false
title: GitHub Notifications を使い倒したら、Slack でチャットしなくなった
topics: ['github', 'slack', 'gitify', 'コミュニケーション', 'チーム開発']
type: tech
---

## 🔔 はじめに

**GitHub の [Notifications](https://github.com/notifications) を使いこなしたら、Slack でチャットしなくなりました。**

みなさん GitHub の [Notifications](https://github.com/notifications) は活用しているでしょうか。意外と使っていない人も多いかもしれません。ちなみに私自身と、私の周りの方々はこの GitHub Notifications をかなり使っています。

この記事で言いたいことを先に図にすると、こういうことです。

![Gitify を境に、散らばった情報が GitHub へ集約される図](/images/articles/github-notifications-gitify-stop-slack-chat/01-overview.webp)

<!-- 図のソース: mermaid/articles/github-notifications-gitify-stop-slack-chat/01-overview.mmd（Mermaid）→ 01-overview.drawio（draw.io でリッチ化）→ 01-overview.webp。図を変更するときは .mmd を直してから .drawio を更新し scripts/convert.sh で再生成する -->

「業務の会話を全部 GitHub に集約できたら最高だよね」という話を、実体験ベースで書いていきます。

## 📭 GitHub Notifications の弱点：デスクトップ通知がない

便利な GitHub Notifications ですが、後述する Gitify というアプリなしではいまいち使い勝手が悪いと思っています。なぜなら、**デスクトップ通知してくれない** からです。

デスクトップ通知がないので、右上にあるメールボックスのようなアイコンで未読があるかどうかを **能動的に** 気にしなければなりません。未読があるなと思ったら、これまた能動的にクリックして見に行く必要があります。

![GitHub Notifications は「能動的な確認」に依存していることを示す図](/images/articles/github-notifications-gitify-stop-slack-chat/02-notification-miss.webp)

<!-- 図のソース: mermaid/articles/github-notifications-gitify-stop-slack-chat/02-notification-miss.mmd（Mermaid）→ 02-notification-miss.drawio（draw.io でリッチ化）→ 02-notification-miss.webp。図を変更するときは .mmd を直してから .drawio を更新し scripts/convert.sh で再生成する -->

これを全員に意識させ、徹底することは到底無理です。人間は忘れる生き物なので、「通知を見に行く」という能動的な行動に依存した運用は必ずどこかで破綻します。

## 🚀 Gitify でデスクトップ通知を実現する

デスクトップ通知してくれればいいのになぁと思い探してみたところ、そのままズバリな [Gitify](https://gitify.io/) というデスクトップアプリを見つけました。

Gitify はこういうアプリです。

- **メニューバー（タスクトレイ）常駐型** で、GitHub の通知をリアルタイムにデスクトップ通知してくれる
- **macOS / Windows / Linux** に対応
- **GitHub Cloud / GitHub Enterprise** はもちろん、Gitea（Forgejo・Codeberg）にも対応
- **MIT ライセンスの OSS**[^oss] で無料

[^oss]: ソースコードは [gitify-app/gitify](https://github.com/gitify-app/gitify) で公開されています。OSS なので中身を確認できる安心感もあります。

導入はとても簡単で、アプリをインストールして GitHub アカウントで認証するだけです。あとはメニューバーに通知が溜まり、新着があればデスクトップ通知が飛んできます。

![Gitify の通知一覧画面](/images/articles/github-notifications-gitify-stop-slack-chat/gitify-notifications.webp)

これを導入してみたところかなり良かったので、周りの仲間にも Gitify を入れるようお願いし入れてもらいました。すると、いまでは全員が Gitify なしでは生きられない体になってしまいました。

:::message
Gitify を入れると通知が可視化されるぶん、**通知疲れ** が気になるかもしれません。GitHub 側で [通知の購読範囲を調整](https://docs.github.com/ja/account-and-profile/managing-subscriptions-and-notifications-on-github) したり、Gitify 側で通知をフィルタリングしたりして、「自分宛て（Participating）」を中心に絞るのがおすすめです。
:::

## 🤔 ある日気付いた「あれ？ Slack で会話してないぞ？」

Gitify をみんなで導入してしばらく経ったある日、あることに気付きました。

> **「あれ？ Slack で全然会話してないぞ？」**

いつの間にか、**業務の会話はすべて GitHub Issue / PR で完結** するようになっていて、Slack ではちょっとした雑談とか勤怠連絡ぐらいしかしなくなっていたのです。

なぜこんなことが起きたのか。それを理解するために、Gitify 導入の **Before / After** を見ていきましょう。

## 📉 Before：Gitify 導入前の「コンテキスト分断」地獄

Gitify を導入する前は、以下のようなことがよく起こっていました。

![メンションに気付かず会話が Slack に逃げてコンテキストが分断する流れの図](/images/articles/github-notifications-gitify-stop-slack-chat/03-context-fragmentation.webp)

<!-- 図のソース: mermaid/articles/github-notifications-gitify-stop-slack-chat/03-context-fragmentation.mmd（Mermaid）→ 03-context-fragmentation.drawio（draw.io でリッチ化）→ 03-context-fragmentation.webp。図を変更するときは .mmd を直してから .drawio を更新し scripts/convert.sh で再生成する -->

文章にするとこうです。

1. A さんが GitHub Issue や PR で B さんにメンション
2. B さんはメンションに気付かず
3. 仕方なく A さんは Slack で「B さん、すみません `#123` の件いかがでしょうか？」とチャット
4. B さんはそのまま **Slack で** 返事をしてしまう
5. A さんもそのまま Slack で会話を続けてしまう
6. **コンテキストが分断** し、GitHub のメンションは宙に浮いたまま、Slack での会話が **唐突に PR に反映** される
7. 数ヶ月後、C さんが引き継ぐ
8. C さんは PR を見ても **会話が途切れていて** 経緯が辿れない
9. 知ってそうな人（A さんか B さん）に **また Slack で** 話しかける（GitHub でメンションすらしない）
10. つづく…

このように、**GitHub でメンションしても気付いてもらえないので、最初から Slack で話しかけてそこで議論が進んでしまう** というのが普通でした。この状態は以下のような事態を引き起こします。

- どういう議論の結果この仕様になったのか分からない
- ADR はあるけどいまいち理解できない
- ある議論をどのチャネル・スレッドで話したか分からず探すのに手間がかかる
- チャネル・スレッド内で複数のトピックが入り乱れている

### 💧 チャットは「フロー情報」なので流れて消える

チャットは **フロー情報** なので、後から掘り起こすのに手間がかかります。なので、Slack で話して決まったことはきちんと **ストック情報** にしましょうと啓蒙しているチームも多いと思います。

しかし、徹底するのはやはり難しく、どうしても **ストック情報への変換を忘れた** り、**ストックになってるけど情報が足りてない** ので分からない、という状態になりがちです。

![フロー情報は変換が要るが、GitHub なら会話がそのままストックになることを示す図](/images/articles/github-notifications-gitify-stop-slack-chat/04-flow-vs-stock.webp)

<!-- 図のソース: mermaid/articles/github-notifications-gitify-stop-slack-chat/04-flow-vs-stock.mmd（Mermaid）→ 04-flow-vs-stock.drawio（draw.io でリッチ化）→ 04-flow-vs-stock.webp。図を変更するときは .mmd を直してから .drawio を更新し scripts/convert.sh で再生成する -->

フロー情報を後からストック情報に「変換する」という作業そのものが、抜け漏れの温床になっているわけです。

## 🧲 考察：なぜ人は Slack で会話を始めたがるのか

そもそも、なぜ人は GitHub でメンションせずに、わざわざ Slack で話しかけてしまうのでしょうか。私は **「Slack の通知がしっかりしているから」** だと考えています。

Slack はデスクトップ通知もモバイル通知も手厚く、話しかけられた側も **気付きやすい**。人は無意識のうちに、**気付いてもらえて、会話が続きやすい場所** を選んで話しかけます。だから、つい Slack で話し始めてしまうのです。

一方、GitHub Issue / PR は、従来 **「メンションしても気付いてもらえない」** という弱点を抱えていました。気付いてもらえないと分かっているから、最初から Slack で「すみません、こちらの件ですが……」と話しかけてしまう。つまり、**会話は「気付いてもらえる場所」に流れていく** のです。

![会話は「気付いてもらえる場所」に流れる、という比較図](/images/articles/github-notifications-gitify-stop-slack-chat/05-why-slack-conversation.webp)

<!-- 図のソース: mermaid/articles/github-notifications-gitify-stop-slack-chat/05-why-slack-conversation.mmd（Mermaid）→ 05-why-slack-conversation.drawio（draw.io でリッチ化）→ 05-why-slack-conversation.webp。図を変更するときは .mmd を直してから .drawio を更新し scripts/convert.sh で再生成する -->

ここで [Gitify](https://gitify.io/) が効いてきます。Gitify を導入すると、GitHub の通知を **Slack に匹敵するレベル** まで引き上げられ、Slack と **同じくらいの「気付きやすさ」** を実現できます。

**この「気付きやすさを揃える」ことこそが最大のポイント** です。気付いてもらえる場所が GitHub になれば、わざわざ Slack に逃げる理由がなくなり、会話は自然と GitHub で始まり、GitHub で続くようになります。

## 📈 After：会話が GitHub に集約される

Gitify を導入したら、**みんなメンションに気付くし、気付くので Issue / PR で会話がちゃんと進む** ようになりました。

その結果、最初に書いたように「あれ？ Slack で全然会話してないぞ？」という状態になりました。

「全く会話がない」はちょっと盛りましたが[^moru]、少なくとも Slack で話していることは、最近やったゲームがどうとか、ネコがどうとか、他愛もないまさしくフローな情報だけになりました。

[^moru]: 雑談はチームの潤滑油なので、むしろ Slack に残ってよかったと思っています。消したいのは「業務上の意思決定」が流れて消えてしまうことであって、雑談ではありません。

GitHub Issue / PR ですべて会話が進むようになったので、以下のようなメリットが生まれました。

- **探しやすい:** ある PR の話は必ずその PR で会話されている
- **検証しやすい:** ADR で理解できない部分があっても生の会話ログを簡単に見られる
- **ストックしやすい:** 1 つの Issue での会話が 1 つのトピックになっている

### 🧠 「すべて GitHub にある」という信頼感

また、「すべて GitHub にある」という信頼感が思ったよりも大きいです。

万が一ドキュメントに書くことを忘れていても、「必ずこのリポジトリの Issue か PR を探せばあるだろう」というのは、心理的な負担が意外と軽くなります。「GitHub だっけ？ Slack だっけ？ メールだっけ？」とあちこち探さなくてもいいだけで、かなり楽です。

情報の置き場所が **1 か所に決まっている** ということ自体が、想像以上に効いてくるのです。

## 🔗 「GitHub の通知を Slack に流せばいいのでは？」への回答

ここで「[GitHub for Slack](https://github.com/integrations/slack) 連携を入れれば、GitHub の通知は Slack に飛んでくる。わざわざ Gitify を入れなくてもいいのでは？」と思った方もいるかもしれません。

確かに通知を Slack に流すことはできます。しかし、これは今回やりたいこととは **向きが真逆** です。

通知が Slack に届くと、人はつい **その場（Slack）で返信** してしまいます。すると、また Slack で会話が始まり、Before で見た「コンテキスト分断」の地獄に逆戻りです。

![通知を Slack に流す vs GitHub に引き戻す、向きの対比図](/images/articles/github-notifications-gitify-stop-slack-chat/06-notification-direction.webp)

<!-- 図のソース: mermaid/articles/github-notifications-gitify-stop-slack-chat/06-notification-direction.mmd（Mermaid）→ 06-notification-direction.drawio（draw.io でリッチ化）→ 06-notification-direction.webp。図を変更するときは .mmd を直してから .drawio を更新し scripts/convert.sh で再生成する -->

大事なのは「通知を **どこで受け取るか**」ではなく、「会話を **どこに引き戻すか**」です。Slack 連携は会話を Slack に引き込んでしまいますが、Gitify はデスクトップ通知から **GitHub に引き戻して** くれます。ここが決定的な違いです。

## 🚨 応用：エラー通知も Slack ではなく GitHub Issue に

この「全部 GitHub に寄せる」という発想は、人同士の会話以外にも応用できます。私たちのチームでは、**エラー発生時は Slack に通知するのではなく、GitHub Issue を作る** というフローにしました。

よくあるのは、Slack にエラー通知用チャネルがあって、そこにエラー通知が来て、そこで会話が始まってしまう……という状態です。これもやはり後でストックにするのを忘れてしまったり、ストックにしても情報が足りなかったりということが起きます。

![エラー通知も Slack ではなく GitHub Issue に寄せる流れの図](/images/articles/github-notifications-gitify-stop-slack-chat/07-error-to-issue.webp)

<!-- 図のソース: mermaid/articles/github-notifications-gitify-stop-slack-chat/07-error-to-issue.mmd（Mermaid）→ 07-error-to-issue.drawio（draw.io でリッチ化）→ 07-error-to-issue.webp。図を変更するときは .mmd を直してから .drawio を更新し scripts/convert.sh で再生成する -->

エラー通知を Slack にするのではなく GitHub Issue を作ることにしたことで、その負担もなくなりました。むしろ、そのエラーを修正するための Pull Request と Issue をきちんと紐付けられるので、**透明性が上がりました**。

## 📱 外出先は GitHub Mobile で取りこぼさない

Gitify はデスクトップアプリなので、PC の前を離れているときは通知に気付けません。そこを補完するのが [GitHub Mobile](https://github.com/mobile) です。

スマホアプリのプッシュ通知を有効にしておけば、離席中や外出先でもメンションに気付けます。「**デスクは Gitify、外出先は GitHub Mobile**」と二段構えにしておくと、通知の取りこぼしがほぼなくなります。

そして GitHub Mobile からも Issue / PR に直接返信できるので、**外出先で返信しても会話はちゃんと GitHub に残ります**。「気付いたその場で GitHub に返す」を、デスクでも外出先でも徹底できるわけです。

## 🧭 それでも Slack を使う場面：使い分けの指針

ここまで読んで「じゃあ Slack は要らないの？」と思うかもしれませんが、そうではありません。**リアルタイム性・即時性が必要なものは Slack**、**記録に残すべき意思決定や議論は GitHub** という使い分けが軸になります。

| 種類 | 置き場所 | 例 |
| --- | --- | --- |
| 🌊 フロー情報（流れてよい） | **Slack** | 雑談・勤怠連絡・軽い声かけ |
| 🚑 即時性が必要 | **Slack**（huddle 等） | 障害発生時のリアルタイム招集 |
| 📚 ストック情報（残すべき） | **GitHub** | 仕様の議論・設計判断・レビュー |
| 🔗 作業に紐づく記録 | **GitHub** | エラー対応・タスク・意思決定 |

ポイントは「Slack を捨てる」ことではなく、**後から掘り起こしたくなる情報を Slack の中で迷子にさせない** ことです。障害対応のように Slack でリアルタイムにやり取りした場合でも、決まったこと・分かったことは最終的に Issue / PR に残す、という運用にしておくと安心です。

## 🏁 まとめ

- GitHub Notifications は便利だが、**デスクトップ通知がない** のが弱点
- [Gitify](https://gitify.io/) を入れると通知に気付けるようになり、**メンションが機能する**
- メンションが機能すると、会話が Slack に逃げず **Issue / PR に集約** される
- 結果として「探しやすい・検証しやすい・ストックしやすい」が手に入り、**「すべて GitHub にある」という信頼感** が生まれる
- エラー通知も Issue 化するなど、**全部 GitHub に寄せる** ほど効果は大きくなる
- 通知は **Slack に流すより GitHub に引き戻す** のが肝。デスクは Gitify、外出先は **GitHub Mobile** で取りこぼさない
- とはいえ Slack を捨てる必要はなく、**フロー情報・即時性は Slack、ストック情報は GitHub** と使い分けるのが現実的

**全部 GitHub で会話する** のはかなりおすすめです。ぜひ皆さんも [Gitify](https://gitify.io/) を導入し、全部 GitHub で会話するというストロングスタイルを実践してみてはいかがでしょうか。
