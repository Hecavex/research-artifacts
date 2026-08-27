# Reproduction notes

## Safety model

The public release reproduces offline transformations only. Its defanged domain inventory is a historical evidence record, not a crawler, live-state feed, credential form, receiver test, archive wordlist or command that contacts the campaign. Do not submit data, execute preserved JavaScript, follow personalised links or probe shared provider infrastructure.

## Exact hostname family

Normalize the saved public-scan task hostname to lowercase, remove a trailing dot and retain only exact matches for:

```python
HOST_RE = re.compile(
    r"^hostinger-mail-ewgjnwrkgnkrw-(?P<suffix>[a-z]{24})\.pages\.dev$"
)
```

Deduplicate by task hostname. The primary query has 298 unique task names. A separate cross-pivot union adds one exact-family value observed only as a final page, so the publication reports 299 names across roles without calling all 299 task domains.

## Domain inventory construction

Normalize retained task and final-page domains to lowercase, remove a trailing dot, deduplicate scan records by their private scan identifier, and retain only the domain plus its observation role and timestamp. The public inventory reconciles these distinct sets:

- 298 exact long-family task domains;
- one additional exact-family name observed only as a final page;
- one confirmed core precursor;
- one weak context lead and one grammar-only lead; and
- one PythonAnywhere name observed only inside a redirect chain.

This produces 302 Hostinger-labelled Pages names across roles and 303 classified domain records after redirect context is included. Evidence tiers must not be flattened: the two lead-only Pages names are not confirmed family members, and the redirect-context name is not an output of the Pages project-name generator. Every public value is defanged. Full URLs, paths, query strings, fragments and private scan identifiers are omitted.

## Descriptive suffix statistics

The entropy calculation uses the observed character counts across unique suffixes:

```python
counts = Counter("".join(suffixes))
total = sum(counts.values())
entropy = -sum((n / total) * math.log2(n / total) for n in counts.values())
```

The result is descriptive, not a cryptographic RNG proof. The output cannot distinguish Python `random`, `secrets`, JavaScript `Math.random`, a custom base-26 encoding, a seeded PRNG or a pregenerated list. No client-side routine that calculates future names was recovered, so this release uses `deployment-name randomization`, not a predictive malware-DGA claim.

## Exact-hash pivots

Hash comparisons are byte-for-byte SHA-256 matches. Search-result counts record the returned public metadata and are not victim, delivery or success counts. A truncated result is labelled as truncated instead of treating missing rows as examined evidence.

## Cross-brand context

The 67-name context is selected from a corpus already sharing unusual path or parameter grammar. It is not a neutral sample of Cloudflare Pages and cannot support prevalence estimates. The exact Hostinger credential-harvester and current tracker hashes did not cross into those other lure prefixes in the saved partial corpus.

## Bounded negative archive result

The later check used five exact-root hash gates, five fixed candidate basenames, one request at a time, disabled redirects and structural ZIP validation. It produced 25 HTML responses and zero valid ZIP archives. This is negative only for those names, hosts and the 5 minute 23 second interval. Candidate bodies and raw attempt ledgers are not part of the public release.

## Fixed-path response comparison

A separate later check used one previously confirmed host and required its root body to match SHA-256 `728d235b2ad22aa3e0f9147f267256d06b80e5ebd7bd61daa1499c1ab6f50af5` before any path request. Ten paths were fixed in advance and requested sequentially with a two-second delay, disabled redirects, a response-size cap, no query strings or cookies and no browser rendering. Nine responses were HTTP 200 `text/html`, 186,751 bytes and byte-identical to the root document. `/index.html` returned an empty HTTP 308 response pointing to `/`, which was not followed.

This result supports a single-page-application fallback assessment for the checked host. It does not reproduce browser execution, prove why one manual VM visit stayed visible, or establish the behavior of every project. The public summary omits the host, response bodies and private request ledger.

## Synthetic request-shape reconstruction

The request shape was reconstructed once with built-in synthetic values against an ephemeral HTTP receiver bound only to `127.0.0.1`. The test destination could not be supplied by an operator, the receiver rejected values outside the fixture and neither the original HTML nor JavaScript was imported or executed. `local-mock-flow.json` records the controls, field names and body hash. It does not reproduce or test the campaign receiver and cannot show successful credential collection.

## Withheld material

The private case retains the original public-scan responses, raw bodies, full task URLs, paths, query strings, private scan identifiers, acquisition manifests and provider communication. Their omission prevents recipient-like values and unnecessary operational detail from becoming a permanent public dataset. The publication-safe domain-only inventory is intentionally public.
