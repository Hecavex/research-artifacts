# On-chain follow-up methodology

Snapshot: 23 August 2026, approximately 18:00 UTC.

- Bitcoin boundary: block `963754`.
- Ethereum boundary: block `25819340`.
- Reported Adform incident window: `2026-07-26T21:49:00Z` through `2026-07-27T17:16:00Z`.

## Evidence classes

`observed` records are direct public-ledger fields. `observed-decoded` records additionally preserve decoded parameters from verified contract calls. `observed-plus-heuristic` identifies a real transaction whose ownership interpretation relies on a stated heuristic.

Transaction identifiers, timestamps, sender and recipient addresses and native units were reproduced through Mempool, Blockstream or Blockscout. Canonical Ethereum USDT and USDC contract transfers were separated from tokens that merely copied a symbol. `onchain-transfers.csv` contains selected evidentiary paths needed to reproduce the assessments; it is not a complete or raw ledger export. Zero-value activity, homoglyph tokens and obvious address-poisoning dust are excluded from that table and from substantive totals.

## Labels

Public labels were checked on 23 August 2026 and are mutable third-party metadata. A label on an immediate sender can establish that a pooled service wallet created a transaction. It does not identify the customer who requested it, the owner of the recipient, the payment purpose, complicity by the named service or incident-specific victim status.

BitInfoCharts and Whale Alert displayed a KuCoin label for `bc1q9wvygkq7h9xgcp59mc6ghzczrqlgrj9k3ey9tz` when checked. The bundle records that mutable third-party label as investigative context, not provider-supplied ownership proof. High transaction volume does not independently confirm the label or establish an exchange or mixer relationship.

## Cross-chain path

The BTC destination `bc1qtrw0lkv2pxd43r4n3lppex5y3gp7j87vt6mq3w` appears verbatim in five Harbor `depositWithExpiry` memos and two Bridgers `swap` destination fields. This is strong evidence that the ETH-side relays requested conversion to that destination. It is different from the embedded BTC seed `bc1qmplgt0hcg62jc2guz86wn2sms7tqrsulkkrrls`, so the decoded route does not establish an on-chain link between the two embedded wallet destinations. Harbor describes a native-asset DEX and liquidity rail. Bridgers publishes the Ethereum contract used. Neither is classified as a mixer in this release.

The seven visible minimum-return values total 1.41724796 BTC. They do not map perfectly onto individual BTC payouts because routing, slippage and output batching intervene. The destination received 3.05867741 BTC through 13 external funding transactions and 16 outputs on 18 July, a 1.64142945 BTC difference that suggests additional source wallets or chains. The unexplained difference is not assigned to Adform or called stolen funds.

## Stop conditions

Tracing stops when assets enter a high-volume pooled address without a reliable label, when transaction structure commingles many independent inputs, or when the next step requires provider-side customer records. No natural-person attribution is made from proximity alone.

No active wallet, contract, suspicious host or payload was executed or interacted with during this work.
