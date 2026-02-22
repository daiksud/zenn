---
title: GitHub CodespacesでDevEnv as Codeしよう
emoji: 🧑‍💻
type: idea
topics:
  ['github', 'githubcodespaces', 'devcontainer', 'everythingascode', 'gitops']
published: true
published_at: 2025-07-16
---

みなさん、[GitHub Codespaces](https://github.co.jp/features/codespaces) は使っていますか？

えっ？まだローカルPCに `git clone` なんかしてるんですか？

`Infrastructure as Code` なんて古いです。「インフラしか」コード化してないなんて。

今や `Everything as Code` の時代です。GitOps です。すべてをコード化しましょう。

もちろん **「開発環境も」** コード化しましょう。

## 🚀 GitHub Codespaces のメリデメまとめ

### 👍 いいところ

- 開発環境のコード化（DevEnv as Code）
- 開発環境のセットアップが要らなくなる
- チームメンバー全員に同じ環境を簡単に展開できる
- リポジトリごとに環境を用意できる
- どこでもどんなデバイスでも開発できる

### 👎 わるいところ

- たまにモタつくことがある
- たまに落ちることがある
- 複数リポジトリ間（Codespaces 間）のファイルコピーが面倒くさい

## 📓 開発環境のコード化（DevEnv as Code）

**あなたの開発環境、すぐに再現できますか？**

おそらく難しいんじゃないかなと思います。エンジニアならまぁ `dotfiles` ぐらいは GitHub に置いてるよという人も多いんじゃないかなと思います。でも `dotfiles` リポジトリで再現できるのは、所詮 `dotfiles` だけです。

新しい MacBook を買ってきました。`dotfiles` を `git clone` しました。それで以前の MacBook の開発環境を再現できてますか？

一部の猛者を除いて、恐らくできていないです。だって、そこから [Homebrew](https://brew.sh/) を入れなきゃ、Google Chrome を入れなきゃ、あれの設定しなきゃ、といったことを思う人がほとんどじゃないでしょうか。

さらに、`dotfiles` はスタンダードな書き方がないため、エンジニアの数だけ `dotfiles` のスタイルが存在します。 秘伝オブ秘伝のタレです。ポータビリティがありません。

一方 Codespaces は、[Development Container (Dev Container)](https://containers.dev/) というスタンダードがあります。他人が書いた Dev Container の設定でも、全員同じ書き方なので理解しやすいですし、マネできます。

どんなツールが入っているかなどは、 [devcontainer.json](https://containers.dev/implementors/spec/) と `Dockerfile` ですべてコード化されます。

ぜひみなさんも **Development Environment as Code** しましょう。

## 🏃 開発環境のセットアップが要らなくなる

**DevEnv as Code のおかげです。**

買ってきたばかりの新しい MacBook でも、[Visual Studio Code](https://code.visualstudio.com/)[^1] をインストールして、[GitHub.com](https://github.com) にアクセスして、Codespaces を起動すれば、すぐ開発を始められます！

[^1]: [Neovim](https://neovim.io/) じゃなきゃやだ？そんなあなたに朗報です。[Dev Container](https://docs.github.com/ja/codespaces/setting-up-your-project-for-codespaces/configuring-dev-containers/adding-features-to-a-devcontainer-file?tool=webui)で[Neovim](https://github.com/devcontainers-extra/features/tree/main/src/neovim-apt-get)がインストールされた[プレビルドを構成](https://docs.github.com/ja/codespaces/prebuilding-your-codespaces/configuring-prebuilds)して、[`gh cs create`](https://cli.github.com/manual/gh_codespace_create) して [`gh cs ssh`](https://cli.github.com/manual/gh_codespace_ssh) して `nvim` してください！

新規にジョインしたメンバーも、リポジトリへのアクセス権を付与したら、Codespaces を起動してもらうだけですぐ開発を始めてもらえます。

「私たちのチームへようこそ。あなたを歓迎します。じゃあまずこれが開発環境のセットアップマニュアルなので、セットアップお願いします。初日はこれで終わると思います」

あーもったいないもったいない。

## 👥 全員に同じ環境を簡単に展開できる

「全体連絡です！[Prettier](https://prettier.io/) じゃなくて [Biome](https://biomejs.dev/) に移行したので、インストールお願いします！」

**こんな連絡もう必要ありません。**

Codespaces なら、Pull Request を出して、レビューしてもらってメンバーの合意を取り（Approve してもらい）、マージするだけです。

Pull Request の中で「なぜ Prettier をやめたのか？」「なぜ Biome にしたのか？」の議論や意思決定の記録も残ります。メリットが大きいですね。

強いて言うなら、マージ後に Codespaces を作り直してもらう必要はありますが、そんなに手間じゃありません。

## 📦 リポジトリごとに環境を用意できる

プロダクトによってバージョンが違うから、`venv` でバージョン切り替えできるようにする？

**もう要りません。**

あるリポジトリ用の Codespaces 環境は、そのプロダクトでしか使いません。なので、直接そのプロダクトで使うバージョンをコンテナ内に入れてしまえば良いのです。

他への影響を考慮する必要がなく、対象のプロダクトのためだけに設定すればいい、というのはかなり楽ですよ。

## 🌍 どこでもどんなデバイスでも開発できる

「うーん次の予定までちょっとだけあるな。でも iPad しか持ってないから開発できないな…」

Codespaces ならブラウザで VS Code が動かせるので、iPad でも開発できます！[^2]

[^2]: バリバリ効率よく開発できるとは言いません。。前にやったことありますが、数行変えるのもかなり大変でした。。。

開発中毒なあなたにぜひおすすめです。

## ⚠️ たまにモタつく・落ちる

これはまぁリモートのVMにネットワーク経由で繋いでいる状態なので、ある程度仕方ないかなと思います。

このデメリットより、明らかにメリットが上回っています。

そう感じます。

## 🔄 複数リポジトリ間（Codespaces間）のファイルコピーが面倒くさい

素直にやろうとすると、まずローカルにダウンロードして、それをアップロードし直す、というのが必要なんですよね。

同じPC内に両方のリポジトリがあれば、`cp` だけで済むので、これは地味に面倒でした。

ただ、これは不思議なもので、この制約がある状況でずっと作業しているうちに、自然とそういうことが必要な作業のやり方をしなくなりました。
なので今はあまりデメリットに感じていないです。

数か月に1回ぐらい必要なケースが出てきますが、その時は片方のCodespacesにもう片方のリポジトリをクローンして、`cp` すればおしまいです。

## 📝 まとめ

GitHub Codespaces を使うべき理由を紹介しました。

みなさんもぜひ `Development Environment as Code` しませんか？

**「すべて」をコード化しましょう。**
