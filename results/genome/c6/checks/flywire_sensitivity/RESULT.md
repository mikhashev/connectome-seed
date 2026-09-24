# FlyWire bank variants against flyvis-30 (registration section 3b)

Pairs of flyvis-30 missing from the primary FlyWire bank: 69; pairs only in the primary FlyWire bank: 6.

| bank | offset rows | nonempty pairs | rows by max(abs du, abs dv) | rows at >= 3 | max | flyvis-30 pairs present | recovered of the missing |
|---|---|---|---|---|---|---|---|
| flyvis-30 (json rows) | 710 | 228 | {'0': 188, '1': 404, '2': 86, '3+': 32} | 32 | 5 | - | - |
| FlyWire primary | 393 | 165 | {'0': 147, '1': 245, '2': 1} | 0 | 2 | 159 | 0 |
| FlyWire geo | 419 | 171 | {'0': 151, '1': 267, '2': 1} | 0 | 2 | 164 | 5 |
| FlyWire geo_interior | 422 | 176 | {'0': 155, '1': 267} | 0 | 1 | 167 | 8 |

Reading rule: primary verdict labelled pipeline-contaminated iff a diagnostic variant recovers >= 50 of the pairs missing from the primary bank AND has an offset row with max(|du|,|dv|) >= 3.

**Label for the primary verdict: support difference real, reading stands.**
