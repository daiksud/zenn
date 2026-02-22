---
title: 「pull_request_target」トリガーを理解する
emoji: ⛲
type: tech
topics: ['github', 'githubactions', 'security']
published: true
published_at: 2025-08-11
---

> [!WARNING]
> この記事は2025年8月11日ごろのGitHubドキュメントを参照して書いています。記事中の引用文が最新のドキュメントと異なる可能性があります。

GitHub Actions には Pull Request のトリガーとして、 `pull_request` トリガーと `pull_request_target` トリガーの2つがあります。非常に似ていますが、この 2 つは仕様がかなり異なり、特に `pull_request_target` トリガーは **脆弱性となりやすい** ため、注意が必要です。この記事では、その注意点についてと、使い所について、自分の理解を書いてみようと思います。

## とりあえず CodeQL を有効にしよう

[GitHub Security Lab の記事](https://securitylab.github.com/resources/github-actions-new-patterns-and-mitigations/) でも紹介されていますが、2025年ごろからは CodeQL が GitHub Actions をサポートしているようです。これから紹介する `pull_request_target` トリガーを使用する場合の注意点なども、カバーしているようです。

ただ、過信は禁物です。理解してなくても指摘してくれるから、脆弱性は発生し得ないというわけでもないので、きちんと理解しておいた方が良いでしょう。

## `pull_request_target` トリガーとは

`pull_request_target` トリガーは、Pull Request に関するイベントが発生した時にワークフローを起動するためのトリガーです。

代表的なイベントアクティビティは `opened`, `synchronize`, `reopened` です。`types` キーワードを指定しない場合、この 3 つがデフォルトとなります。

つまり、`pull_request_target` トリガーを指定したワークフローが起動する条件は、ほとんど `pull_request` と同じです。基本的には `pull_request` と同様、Pull Request がオープンされたり、Pull Request に新しいコミットがプッシュされたりすると、ワークフローがトリガーされます。

## `pull_request` と最も違う部分はセキュリティ

`pull_request_target` と `pull_request` の一番の違いは、セキュリティに関係する以下の 2 点です。

1. **ターゲットリポジトリへの書き込み権限を持つ（`permissions` を指定しない場合のデフォルト）**
2. **シークレットの読み取り権限を持つ**

これらは **フォークされたリポジトリ（信頼できないユーザー）からの Pull Request であっても**、権限が付与されます。

`pull_request` の場合は、フォークされたリポジトリ（信頼できないユーザー）からの Pull Request に上記権限は付与されません。また、承認しない限り実行されない、というセキュリティ機構も持ちます。

信頼できないユーザーに権限を与えず、むやみに信頼できないコード（ワークフロー）を実行しないようにするのは、当然と言えば当然です。しかし `pull_request_target` の場合は、信頼できないユーザーからの Pull Request であっても、そのワークフローは書き込み権限を持ち、承認せずとも実行されます。

なんとなく危険そうな雰囲気を感じていただけたでしょうか。

`pull_request_target` トリガーは上記のような特徴を持つため、「安全に使うための理屈が 120% 理解できた」という自信がない場合は使わないほうが無難です。

## コンテキストの違い

[ワークフローをトリガーするイベント#pull_request_target - GitHub ドキュメント](https://docs.github.com/ja/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request_target) によると、以下のように書かれています。

> このイベントは、`pull_request` イベントのようにマージコミットのコンテキストではなく、pull request のベースのコンテキストで実行されます。

`pull_request_target` の場合、マージ先のブランチ（ベースブランチ）のコンテキストで実行されます。つまり、ベースブランチにワークフローが存在している必要があります。

一方 `pull_request` イベントの場合、新規にワークフローを作るような Pull Request の場合でも、その Pull Request 自身で追加するワークフローが実行されます。つまり、まだ存在していないワークフローを自由に作って実行できる、ということです。

そのため、フォークされたリポジトリ（信頼できないユーザー）からの Pull Request の場合は、セキュリティを強化する必要があります。

その強化策として、書き込み権限やシークレット読み取り権限を付与せず、所有者が承認しない限り実行させない、となっているのです。

## 安全ではないコードが実行されるのを避けられる

[ワークフローをトリガーするイベント#pull_request_target - GitHub ドキュメント](https://docs.github.com/ja/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request_target) には以下の文もあります。

> リポジトリを変更したり、ワークフローで使うシークレットを盗んだりする可能性がある、pull request の head から安全ではないコードが実行されるのを避けることができます。

これはどういうことかというと、`pull_request_target` トリガーでは [コンテキストの違い](#コンテキストの違い) でも書いた通り、**ベースブランチのコンテキスト** でワークフローが実行されます。つまり、Pull Request を出してきたユーザーの **信頼できないコードやワークフロー** は実行されないということです。

説明では「コード」と書いてありますが、これには **ワークフロー自身も含まれる** ところがポイントです。攻撃者が `pull_request_target` トリガーのワークフローを改変して Pull Request で出してきたとしても、それが実行されるわけではありません。あくまでもベースブランチに存在しているワークフローが実行されます。

ベースブランチにあるワークフローということは、そのリポジトリの所有者がレビュー済みのはずです。レビュー済み、つまり信頼できるワークフローなのだから、リポジトリの書き込み権限やシークレットのアクセス権限を持っていても問題ないのです。

よって、`pull_request_target` トリガーのワークフローは、リポジトリの書き込み権限やシークレットのアクセス権限を持っていても、（信頼できないコードを実行しない限り）それが悪用されることはありません。

## Pull Request からコードをビルドまたは実行する場合は使ってはならない

続いて、[ワークフローをトリガーするイベント#pull_request_target - GitHub ドキュメント](https://docs.github.com/ja/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request_target) に以下の文もあります。

> Pull Request からコードをビルドまたは実行する必要がある場合は、このイベントを使わないでください。

この文のポイントは **Pull Request から** の部分です。これはどういうことかというと、「Pull Request で変更されたもの」という意味です。つまり、**「Pull Request によって提出された、外部ユーザーによって作られたコードをビルドまたは実行する場合」** は `pull_request_target` を使ってはならない、ということです。

なぜでしょうか。

もちろん、`pull_request_target` トリガーで起動したワークフローが、 **リポジトリへの書き込み権限** や、 **シークレットへのアクセス権限** を持つからです。そのような権限を持つ状態で、どこの誰とも分からない Pull Request 作成者の信頼できない任意のプログラムコードを実行することは、当然やってはいけません。

**「権限」と「信頼できないコード」の 2 つを出会わせてはいけない** のです。

## GitHub ドキュメントの警告文

さらに [ワークフローをトリガーするイベント#pull_request_target - GitHub ドキュメント](https://docs.github.com/ja/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request_target) の説明に以下のような警告があります。

> **警告:** `pull_request_target` イベントによってトリガーされるワークフローでは、フォークからトリガーされているのであっても、`permissions` キーが指定されてワークフローがシークレットにアクセスできるのでない限り、読み取り/書き込みのリポジトリアクセス許可が `GITHUB_TOKEN` に付与されます。
>
> ワークフローは Pull Request のベースのコンテキストで実行されますが、このイベントで Pull Request から信頼できないコードをチェックアウトしたり、ビルドしたり、実行したりしないようにしなければなりません。
> さらに、キャッシュではベースブランチと同じスコープを共有します。キャッシュポイズニングを防ぐために、キャッシュの内容が変更された可能性がある場合は、キャッシュを保存しないでください。
>
> 詳細については、GitHub Security Lab の Web サイトの [GitHub Actions およびワークフローのセキュリティ保護の維持: pwn 要求の阻止](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/) に関する記事を参照してください。

なるほど。分からん。

分からんのですが、ちょっと読み解いてみましょう。

### 1 文目の解釈

まず 1 文目がよく分かりませんね。[英語版](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request_target) だと以下のように書いてあります。

> For workflows that are triggered by the `pull_request_target` event, the `GITHUB_TOKEN` is granted read/write repository permission unless the `permissions` key is specified and the workflow can access secrets, even when it is triggered from a fork.

英語は得意じゃないので自信はありませんが、ここから推測すると恐らく以下が正しい解釈です。

> `pull_request_target` イベントによってトリガーされるワークフローは、`GITHUB_TOKEN` に、リポジトリの読み取り/書き込みアクセス許可が（`permissions` キーを指定してない場合）付与され、シークレットのアクセス許可も付与されます。これはフォークからトリガーされた時も同様です。

要するに、フォークからの Pull Request でも、デフォルトで書き込み権限を持つし、シークレットアクセス権も持つよ、ということですね。

リポジトリの書き込み権限は `permissions` で制御できますが、シークレット読み取り権限はコントロールできません。なので、やはり注意すべきです。

### 2 文目の解釈

さて、2 文目は以下です。

> ワークフローは Pull Request のベースのコンテキストで実行されますが、このイベントで Pull Request から信頼できないコードをチェックアウトしたり、ビルドしたり、実行したりしないようにしなければなりません。

これも分かりにくいですね。最初の「ワークフローは Pull Request のベースのコンテキストで実行されますが」は恐らく無視して問題ありません。文全体をややこしくしているだけです。

重要なのはその後で、「このイベント（`pull_request_target`）で、信頼できないコードをチェックアウト・ビルド・実行してはいけない」と言っています。

厳密にはチェックアウトだけでは必ずしも脆弱性になるわけではないですが、チェックアウトする時点で相当危険なことです。何のためにチェックアウトするのか、入念に考える必要があります。一歩先は脆弱性です。

### 最初 2 文をまとめると

以下のように言っています。

- **`pull_request_target` トリガーのワークフローは、デフォルトでリポジトリの書き込み権限を持ち、シークレットにもアクセスできます。**
- **だから信頼できない Pull Request（＝フォークからの Pull Request）のコードをチェックアウトしてビルド・実行してはいけません。**

### 3 文目の解釈

では、3 文目にいきましょう。

> さらに、キャッシュではベースブランチと同じスコープを共有します。キャッシュポイズニングを防ぐために、キャッシュの内容が変更された可能性がある場合は、キャッシュを保存しないでください。

この文は「変更された」ではなく「変更される」にすると分かりやすいです。キャッシュを書き換えられる可能性のあるワークフローなら、キャッシュを保存しないようにしようねということです。

「さらに」と最初に書いてあるので、直前の文章に付け加えています。つまり、「（Pull Request からの信頼できないコードによって）キャッシュを書き換えられる可能性がある場合」ということです。

ちなみに、英語版は以下です。

> Additionally, any caches share the same scope as the base branch. To help prevent cache poisoning, you should not save the cache if there is a possibility that the cache contents were altered.

英語では最後の `the cache contents were altered` が過去分詞になので「変更された」に訳されちゃっていると思われます。しかし、`if` が付いているので、恐らくこれは仮定法です。でも仮定法未来なら `were to alter` になるはずですが、「別にネイティブはこれでも通じる」とかそういうケースかなぁと予想しています。

## まとめ

`pull_request_target` トリガーについて、ドキュメントや GitHub の公式ブログを参考に仕様や注意点を説明してきました。

- フォークからの信頼できない Pull Request であっても、リポジトリ書き込み権限とシークレットアクセス権限を持つ
- Pull Request のマージ先であるベースブランチにあるワークフローが実行される
- Pull Request の信頼できないコードをビルド・実行してはならない（シークレットアクセス権を持つから）
- Pull Request の信頼できないコードでキャッシュが書き換えられる場合はキャッシュを保存しない（キャッシュ汚染を防ぐため）
- CodeQL で脆弱な書き方はある程度検知してくれる

Google で `pull_request_target` を検索しても、日本語でちゃんと紐解いている記事が見当たらなかったので、少しでも役に立てれば幸いです。

## 参考

- [GitHub Docs](https://docs.github.com/ja/actions/reference/workflows-and-actions/events-that-trigger-workflows#pull_request_target)
- [Jaroslav Lobačevski. (2021). Keeping your GitHub Actions and workflows secure Part 1: Preventing pwn requests](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/)
- [Alvaro Munoz. (2025). Keeping your GitHub Actions and workflows secure Part 4: New vulnerability patterns and mitigation strategies](https://securitylab.github.com/resources/github-actions-new-patterns-and-mitigations/)
