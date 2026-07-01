---
emoji: 🤖
published: true
published_at: 2025-07-07
title: Dependabot のバージョンアップデートとセキュリティアップデートを使い分ける
topics: ['github', 'dependabot', 'cicd', 'devops']
type: tech
---

## はじめに

以前 [Dependabot バージョンアップデート](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates) を使ってみたので、その備忘録です。

まず、Dependabot には、バージョンアップデートとセキュリティアップデートの 2 種類があります。これらは似ているようで、設定できる項目や挙動が微妙に異なります。

とくに `.github/dependabot.yml` の扱いがややこしく、セキュリティアップデートだけを使いたい場合にもハマりやすいポイントがあります。この記事では、バージョンアップデートの有効化手順と、セキュリティアップデートだけを使いたい場合の注意点をまとめます。

## Dependabot とは

Dependabot は、依存関係のアップデートをチェックし、もし新バージョンがあればそれに更新する Pull Request を作ってくれるボットです。似たようなツールとしては [Renovate](https://github.com/renovatebot/renovate) をよく見ますね。

ちなみに Dependabot は、GitHub が買収したとか何かで、GitHub の一部として組み込まれたようです。つまり GitHub の純正ツールと言えるでしょう。ドキュメントも [GitHub Docs](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/dependabot-quickstart) にあります。

## Dependabot の 2 つの機能

Dependabot には [バージョンアップデート](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-version-updates) と [セキュリティアップデート](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-security-updates) の 2 種類があります。また、セキュリティアップデートの方はその前段として [Dependabot alerts](https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts) という警告だけを出すものがあり、セキュリティアップデートはそのアラート解消のための仕組みです。

バージョンアップデートもセキュリティアップデートも、どちらも「依存関係を更新する」という点は同じなのですが、依存関係のタイプや Pull Request の作られ方、設定の適用範囲が微妙に異なります。

セキュリティアップデートは、セキュリティリスクのあるパッケージなどを見つけると、それを「問題のないバージョンまで」アップデートする Pull Request を作ります。ポイントは、最新バージョンではなく、脆弱性が解消されているバージョンまでのアップデートであることです。

一方、バージョンアップデートは、セキュリティリスクの有無に関係なく、依存関係の新しいバージョンをチェックして Pull Request を作ります。

実はこの 2 つが同じようで違う感じになっていて、地味にややこしい仕組みになっています。ややこしい設定の違いについては、後述の「`dependabot.yml` は「基本」バージョンアップデート用」以降で説明します。

## バージョンアップデートを有効にする

とは言っても、何も別に難しいことはありません。リポジトリに `/.github/dependabot.yml` というファイルを作り、アップデート対象にしたいパッケージエコシステムを指定するだけです。

```yaml
# https://docs.github.com/en/code-security/concepts/supply-chain-security/about-the-dependabot-yml-file
version: 2
updates:
  - package-ecosystem: npm # アップデート対象のパッケージエコシステム
    directory: / # パッケージエコシステムのファイルが存在するディレクトリ
    schedule:
      interval: daily # 更新チェックを行う間隔
```

例えば上記のような内容で `.github/dependabot.yml` を作ると、リポジトリルートの `package.json` に書かれている npm パッケージのバージョンアップをやってくれます。

## バージョンアップデートの設定

色々と設定項目があります。
[Dependabot オプション リファレンス](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) を見ればすべて載っています。

また、やりたくなりそうなことはガイドもいくつかあります。

- [より細かいスケジュール設定（毎週日曜日の午前 3 時にするなど）](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/optimizing-pr-creation-version-updates#controlling-the-frequency-and-timings-of-dependency-updates)
- [Pull Request のグループ化](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/optimizing-pr-creation-version-updates#grouping-related-dependencies-together)
- [レビュアーとアサインを自動的に設定する](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/customizing-dependabot-prs#automatically-adding-reviewers)
- [Pull Request に付けるラベルの設定](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/customizing-dependabot-prs#labeling-pull-requests-with-custom-labels)
- [コミットメッセージにプレフィックスを付ける](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/customizing-dependabot-prs#adding-a-prefix-to-commit-messages)
- [マイルストーンを紐づける](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/customizing-dependabot-prs#associating-pull-requests-with-a-milestone)
- [ブランチ名の区切り文字を変える](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/customizing-dependabot-prs#changing-the-separator-in-the-pull-request-branch-name)
- [デフォルトブランチ以外をターゲットにする](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/customizing-dependabot-prs#targeting-pull-requests-against-a-non-default-branch)

ほとんどのやりたいことは上記でカバーできていると思います。

バージョンアップのチェックが可能なパッケージエコシステムは意外と多く、**Docker** や **Dev Containers**, **GitHub Actions** なんかもチェックできます。
参考: [サポートされているエコシステムとリポジトリ](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-repositories)

## `dependabot.yml` は「基本」バージョンアップデート用

Dependabot セキュリティアップデートは、リポジトリの Settings > Advanced Security の中に「Dependabot security updates」という項目で Enable すると有効になります。これだけで、Dependabot はセキュリティリスクのあるパッケージなどを見つけると、それを問題のないバージョンまでアップデートする Pull Request を作り始めます。

一方で、バージョンアップデートは同じページに「Dependabot version updates」という項目があります。しかし、こちらは Enable/Disable ではなく「Configure」というボタンになっており、押すと `.github/dependabot.yml` の編集画面が開かれます。

ここから分かる通り `dependabot.yml` は _基本的に_ バージョンアップデートのためのファイルなのです。

ところがどっこい、`dependabot.yml` は **セキュリティアップデートにも** 作用します。

つまり、セキュリティアップデートの Pull Request の作らせ方を制御するには `dependabot.yml` を作って設定するしかありません。
これが非常に厄介な仕様です。

「バージョンアップデートをしたいわけではない」のに、`dependabot.yml` を作る必要があるので、勝手にバージョンアップデートが動き始めてしまうのです。

## バージョンアップデートを止めてセキュリティアップデートだけ使う

[`open-pull-requests-limit`](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#open-pull-requests-limit-) を `0` にするとバージョンアップデートの Pull Request が作られず、セキュリティアップデートの Pull Request だけになります。

非常にわかりにくい。。

最悪です。明らかに直感的ではないですよね。

Pull Request 数をゼロに制限しているという「ように見える」のに、セキュリティアップデートはこれを無視して作るのですから。

これが、「`dependabot.yml` は _基本的に_ バージョンアップデートのためのファイル」と説明した理由です。セキュリティアップデートは、一部の設定は考慮するけど、一部の設定は無視するのです。

皆さんはこんなクソ仕様のシステムを作らないように気をつけましょう。

## 設定の適用範囲が違う罠

Dependabot が作る Pull Request をあれこれとカスタマイズしたくなるでしょう。なので当然 [Dependabot オプション リファレンス](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference) を見るわけですが、ここで注意点があります。

:::message
セキュリティアップデートで使える設定、バージョンアップデートで使える設定、それぞれが微妙に異なります。
:::

これがめちゃめちゃハマりやすいです。

1 つ紹介すると、[デフォルトブランチ以外をターゲットにする設定](https://docs.github.com/en/code-security/tutorials/secure-your-dependencies/customizing-dependabot-prs#targeting-pull-requests-against-a-non-default-branch) が使えるのはバージョンアップデートだけ、というものです。

注意書きもあります。

> Dependabot により、**既定のブランチのみ**に対してセキュリティ更新プログラム用の pull request が生成されます。
> `target-branch` を使うと、結果として、そのパッケージ マネージャーのすべての構成設定は、セキュリティ更新プログラムではなくバージョン更新プログラムに "のみ" 適用されます。

言い回しが分かりにくいですね。おそらく以下の意味です。

「Dependabot が作成する「セキュリティアップデート」の Pull Request は、**既定のブランチにのみ**生成されます。`target-branch` を設定すると、この設定を含む一連の設定は「バージョンアップデート」に**のみ**適用されるようになり、セキュリティアップデートでは無視されます。」

こんな感じでわっかりにくい設定などが結構あります。セキュリティアップデートとバージョンアップデートでは設定の適用範囲が異なるので、`dependabot.yml` を書くときはどちらに効く設定なのかを確認した方がよさそうです。

## まとめ

Dependabot を有効にしてしばらく使ったときに分かったことを書きました。Dependabot バージョンアップデートは `/.github/dependabot.yml` を作るだけで簡単に有効化できます。

バージョンアップをサボると、後々苦労します。Dependabot バージョンアップデートを活用して、小さな変更で済むうちに、こまめにアップデートするのが吉です。

一方で、Dependabot にはバージョンアップデートとセキュリティアップデートの 2 種類があり、設定できる項目や適用範囲が微妙に異なります。セキュリティアップデートだけを使いたい場合は、`dependabot.yml` に [`open-pull-requests-limit`](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#open-pull-requests-limit-) を `0` と設定する必要があります。

簡単に有効化できる一方で、設定の効き方は分かりにくいところがあります。セキュリティアップデートとバージョンアップデートの違いに注意しつつ、Dependabot を活用していきましょう。
