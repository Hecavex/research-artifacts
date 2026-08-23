# Exact-hash reproduction notes

HECAVEX snapshot: 2026-08-08.

The `02ff86c7f9fe609a753ff15bda90baa3c3e0d4a2e559ec4fcf8a3de0954b7c55` response can be reproduced without executing JavaScript from the archived `a04461bbdccb15378182cdf77281ec29628f1c1386ae0fe89b62f359471fdeb6` two-block response.

Source response:

<https://web.archive.org/web/20260727004110id_/http://s2.adform.net/banners/scripts/st/trackpoint-async.js>

Static byte operation:

```python
from hashlib import sha256

body = open("wayback-20260727004110.js", "rb").read()
assert len(body) == 89672
assert sha256(body).hexdigest() == "a04461bbdccb15378182cdf77281ec29628f1c1386ae0fe89b62f359471fdeb6"

advanced_only = body[:82721] + body[-4777:]
assert len(advanced_only) == 87498
assert sha256(advanced_only).hexdigest() == "02ff86c7f9fe609a753ff15bda90baa3c3e0d4a2e559ec4fcf8a3de0954b7c55"
```

This is slicing and hashing only. The JavaScript is not evaluated or executed. The retained final block contains the statically decoded valid Bitcoin and Ethereum replacement destinations plus DOM, form-value and clipboard rewrite handlers.

This establishes a byte-level link between the archived two-block response and the `02ff86c7...` response observed in six URLScan page contexts.
