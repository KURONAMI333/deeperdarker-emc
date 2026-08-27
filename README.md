# ProjectE: EMC for Deeper and Darker

> Deeper and Darker の素材を ProjectE の変換系に載せる。このアドオンが無いと ProjectE はそれらに値を付けられない。

[![License: All Rights Reserved](https://img.shields.io/badge/License-All%20Rights%20Reserved-lightgrey.svg)](LICENSE)

---

## なぜ必要か

Deeper and Darker の素材は ProjectE から見ると「値の付かない未知のアイテム」で、賢者の石を持っていても変換テーブルに載らない。この MOD は深層の素材・ワーデン由来の素材・遺物に EMC 値を与える data-only アドオンで、中身は変換定義 JSON 1本（Java コードなし）。手付けしたのは 1.21.1 で 46 id、1.20.1 で 33 id。残りはホスト自身のバニラ型レシピを ProjectE が辿って自動導出する。

---

## 設計

- **進行順を崩さない** — resonarium 768 < warden carapace 1024 < reinforced echo shard 5056（導出）< sculk catalyst 8040。後段の素材が前段より安くならないので、変換で段を飛ばせない
- **gloomsherd 216** — 9枚がバニラの陶片帯と揃う位置に置いた
- **heart of the deep 4096** — ワーデンの確定ドロップであることを根拠にした値（乱数ドロップ扱いにしていない）
- **ancient vase 7497 = ルートボックスの穴を塞ぐ値** — 中身の期待値をルートテーブル全体で計算すると約 7,195〜7,443。壺をその上に置いてあるので、開ける行為が EMC の利得になる目が無い
- **鍛冶型 2種 = 7497** — バニラのネザライト型と同帯。ホストは型の自己複製レシピを持つが、その材料のダイヤが 7497 より高いので、複製しても元の値を下回らない
- **sculk transmitter の染色 16色（1.21.1 のみ）** — ProjectE はこの染色レシピを読まないので、16本の変換を明示的に宣言している（触媒として dye を計上）

## セル差

| | 1.21.1 NeoForge | 1.20.1 Forge |
|---|---|---|
| 手付け id 数 | 46 | 33（新しいホストにしか無いブロックの分だけ少ない） |
| echo logs | `#minecraft:logs` タグ経由で 32 | タグ経路が無いので手付けで 32 |
| resonarium plate | 3264 | 3456（ホスト自身のレシピ差。揃えずそのまま） |
| sculk transmitter の染色 | 16本あり | なし |

## 値を付けていないもの

- **soul elytra・道具・武器・防具** — 耐久値とエンチャントはアイテムの状態であって、変換で消したり作り直したりするものではない
- コンポスター投入可能な 16 品はすべてバニラのシダ以下に収まることを確認済み（堆肥ループから EMC が湧かない）

## 導入

1. Minecraft 1.21.1 + NeoForge、または 1.20.1 + Forge
2. ProjectE と Deeper and Darker を入れる
3. この jar を `mods/` へ入れる

**サーバー側のデータ MOD**。クライアントには不要。

## ライセンス

All Rights Reserved。modpack への同梱はプラットフォーム・収益化を問わず自由（許可も credit も不要）。ソースは公開しているので中身をそのまま読める。

## Credits

Author: KURONAMI
