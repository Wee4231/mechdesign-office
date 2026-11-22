Project: Spring-Loaded Pusher

# Phase 1 - Sizing Calculations

Status: AWAITING USER APPROVAL. Nothing here is released for Phase 2 until the assumptions and numbers below are approved.

Units: millimetres (mm), grams (g), seconds (s). Forces in N, stresses in MPa. Every formula was evaluated in SI (m, kg, s, Pa) and converted back.

Calculation script (not part of the project): `C:\Users\TeeAik\AppData\Local\Temp\claude\dd61668dd1e76d8b\5949edae-ea99-49c9-9f8d-8df4cc1ff390\scratchpad\pusher_sizing.py`. It ends with assert-style self-checks; all passed.

---

## 1. Assumptions (none of these came from the user - all need review)

| # | Assumption | Value |
|---|---|---|
| A1 | Function | Pushes a workpiece sideways against a fixed datum stop in a jig and holds it; horizontal axis |
| A2 | Workpiece mass | 200 g, resting on a flat steel nest |
| A3 | Push force at working position | about 20 N |
| A4 | Total tip stroke | 10 mm (extended to fully retracted) |
| A5 | Part size tolerance | +/-0.5 mm |
| A6 | Split of the stroke | 2 mm take-up (extended to nominal working position) + 8 mm loading clearance |
| A7 | Retraction | By hand, pull knob at the rear |
| A8 | Hand pull comfort limit | 40 N, three-finger grip on a 25 mm diameter knob, once per part load. Rule-of-thumb design value, not taken from a standard |
| A9 | Friction, part on nest | 0.30 nominal, 0.60 pessimistic (for "can it slide the part"); 0.15 lower bound (for "how much does it hold") |
| A10 | Friction, oil-free bushing on steel shaft | 0.20 (dry, pessimistic) |
| A11 | Friction, tip on workpiece | 0.30 |
| A12 | Off-axis load case at the tip | Contact point 5 mm off the shaft axis, plus a transverse drag of 0.30 x push force (6.1 N) |
| A13 | Spring material | Music wire SWP-B, G = 78 500 MPa, closed and ground ends |
| A14 | Bushing dimensions | Typical oil-free series: ID 12 x OD 18 x L 20 flanged (flange 25 dia x 3); ID 8 x OD 12 x L 12 straight. To be confirmed against the catalogue in Phase 2 |
| A15 | Bushing running clearance | 0.05 mm on diameter per bushing (used only for the tip play estimate) |
| A16 | Housing material | Aluminium alloy block (the bushings carry the wear) |
| A17 | Centreline height | 20 mm above the mounting face (must suit the nest and part height, which are unknown) |

## 2. Layout adopted (and one deviation from the stated concept)

The stated concept was a single bushing with the spring in front of the housing against a collar. Sized that way, the tip sits about 53 mm in front of a 24 mm long guide, and the off-axis load case A12 costs 8.2 N of guide friction = 41 % of the 20 N clamp force. That fails the friction check in section 6.

Adopted instead (same parts list idea, spring moved inside the housing):

- Stepped plunger shaft: 12 mm diameter front section, 8 mm diameter rear section. The step is the spring shoulder, so no separate collar is needed.
- Front guide: flanged oil-free bushing ID 12 in the housing front face.
- Rear guide: straight oil-free bushing ID 8, pressed in from the front against a 3 mm rear web so the spring force traps it.
- Spring: around the 8 mm section, inside a 13 mm bore, between the rear bushing end face and the shaft shoulder.
- Tip: 16 mm diameter x 10 mm long, replaceable, M6 thread into the front of the shaft.
- Rear: M6 male thread carrying a stop nut and the pull knob. The stop nut against the housing rear face is the extend stop (adjustable, lock nut against knob).
- Retract stop: the back face of the tip meets the front bushing flange at exactly 10 mm stroke, so the spring can never be driven solid.

Axial stack-up, x measured from the housing rear face, positive toward the workpiece:

| Feature | x (mm) |
|---|---|
| Knob rear face, extended / pulled | -25 / -35 |
| Housing rear face (extend stop face) | 0 |
| Rear web | 0 to 3 |
| Rear bushing | 3 to 15 |
| Spring rear seat | 15 |
| Shaft shoulder, retracted / working / extended | 42 / 50 / 52 |
| Front bushing body | 55 to 72 |
| Housing front face | 72 |
| Front bushing flange face (retract stop) | 75 |
| Tip face, retracted / working / extended | 85 / 93 / 95 |

## 3. Spring

| Quantity | Value | Unit |
|---|---|---|
| Material | Music wire SWP-B, closed and ground ends | - |
| Wire diameter | 1.2 | mm |
| Outer diameter | 12.0 | mm |
| Inner diameter | 9.6 | mm |
| Mean diameter | 10.8 | mm |
| Spring index C | 9.0 | - |
| Active coils | 16 | - |
| Total coils | 18 | - |
| Rate | 1.01 | N/mm |
| Free length | 55.0 | mm |
| Installed length (extended, preload) | 37.0 | mm |
| Working length (nominal part) | 35.0 | mm |
| Length at full retraction | 27.0 | mm |
| Solid length | 21.6 | mm |
| Margin to solid at full retraction | 5.4 (19 % of max deflection) | mm |
| Preload force, extended | 18.2 | N |
| Force at working position | 20.2 | N |
| Force at full retraction | 28.3 | N |
| Force if driven solid | 33.7 | N |
| Wahl factor | 1.162 | - |
| Shear stress, working / retracted / solid | 373 / 523 / 624 | MPa |
| Estimated tensile strength of wire | 2153 | MPa |
| Allowable static shear (0.45 x tensile) | 969 | MPa |
| Pitch / pitch angle | 3.29 / 5.5 | mm / deg |
| OD when solid | 12.04 | mm |
| Slenderness, free length / mean diameter | 5.09 | - |
| Mass | 5.4 | g |

Checks:

- Shear stress at full retraction: 523 MPa against 969 MPa allowable. PASS, safety factor 1.85.
- Shear stress if driven solid: 624 MPa against 969 MPa. PASS, safety factor 1.55 (the spring would not take a set even if the retract stop were missing).
- Solid length below retracted length: 21.6 mm < 27.0 mm. PASS, 5.4 mm margin (19 %, rule used: at least 15 % of maximum deflection).
- Fatigue, informative (extended to retracted cycle, Zimmerli unpeened data with Goodman): alternating 93 MPa, mean 429 MPa, safety factor 1.71 for infinite life. PASS.
- Buckling: slenderness 5.09. Critical free length for flat parallel seats is 56.8 mm against 55.0 mm, so unguided it is stable by only 3 %. It is guided, inside by the 8 mm shaft (1.6 mm clearance on diameter) and outside by the 13 mm bore (1.0 mm clearance), so it cannot buckle. PASS because guided; expect light rubbing.
- Spring index 9.0 (range 4 to 12) and pitch angle 5.5 deg (below 12 deg). PASS.

## 4. Clamp force across the part tolerance

| Part size | Spring length (mm) | Force (N) |
|---|---|---|
| -0.5 mm (smallest) | 35.5 | 19.7 |
| Nominal | 35.0 | 20.2 |
| +0.5 mm (largest) | 34.5 | 20.7 |

Variation is +/-0.5 N = +/-2.5 %. PASS (target: within +/-5 %).

At the smallest part the plunger is still 1.5 mm short of the extend stop, so the stop never takes force away from the part. Loading clearance with the knob pulled is 8.0 mm nominal, 7.5 mm minimum.

A catalogue spring's own load tolerance (commonly around +/-10 %) will be larger than this geometric variation.

## 5. Is 20 N enough?

| Quantity | Value | Unit |
|---|---|---|
| Part weight | 1.96 | N |
| Force to slide the part on the nest, friction 0.30 | 0.59 | N |
| Same, friction 0.60 | 1.18 | N |
| Push force / sliding force | 34 (friction 0.30), 17 (friction 0.60) | x |
| Holds against a force pushing the part back off the datum | 20.0 | N |
| Holds against a force sliding the part along the datum (friction 0.15) | 6.2 (= 3.2 g on the part) | N |
| Holds against a force lifting the part off the nest (friction 0.15) | 7.9 | N |

PASS for locating: the push force is at least 17 times what is needed to seat the part.

Limits: this is a spring clamp, not a positive lock. Any force above about 20 N directed away from the datum moves the part. Sideways and lifting loads are held only by friction, 6 to 8 N. That is adequate for inspection, marking, light assembly or probing. It is not adequate for machining or pressing loads.

## 6. Plunger shaft and guiding

| Quantity | Value | Unit |
|---|---|---|
| Front section diameter x length | 12 x 33 | mm |
| Rear section diameter x length | 8 x 50 | mm |
| Rear thread | M6 x 18 | mm |
| Front thread (tip) | M6 tapped | - |
| Total shaft length | 101 | mm |
| Guided length (outer edge to outer edge of the two bushings) | 72 | mm |
| Bearing span, centre to centre | 56 | mm |
| Tip overhang from front bushing flange face, extended / working | 20 / 18 | mm |
| Tip overhang from front bushing centre, extended / working | 30 / 28 | mm |
| Ratio guided length / overhang (edges) | 3.6 | - |
| Ratio bearing span / overhang (centres, conservative) | 1.87 | - |
| Shaft mass / moving mass | 52 / 89 | g |

Binding check, load case A12 at the working position (6.1 N transverse at the tip plus 20.2 N acting 5 mm off axis, bushing friction 0.20):

| Quantity | Value | Unit |
|---|---|---|
| Rear / front bushing reaction | 4.8 / 10.9 | N |
| Guide friction from the off-axis load | 3.14 | N |
| Guide friction from the moving weight | 0.18 | N |
| Total guide friction | 3.32 (16.4 % of working force) | N |
| Preload / friction (will it always return) | 5.5 | x |
| Eccentricity at which a pure off-centre push would self-lock | 140 | mm |

- Jamming: PASS. Self-locking needs 140 mm eccentricity against 5 mm assumed; the preload is 5.5 times the friction.
- Friction loss: PASS but marginal, 16.4 % against a 20 % limit. Under this worst case the delivered clamp force is 20.2 N minus up to 3.3 N. With lubricated bushing friction of 0.10 the loss halves.
- For comparison, the single-bushing layout gave 8.2 N = 41 %. FAIL, which is why it was not adopted.

Bending:

- Elastic deflection of the tip under load case A12: 0.004 mm. PASS, negligible.
- Bending stress in the 12 mm section: 1.7 MPa. PASS, negligible.
- Tip play from bushing clearance (assumption A15): about +/-0.05 mm. This, not bending, sets the tip position accuracy.
- Abuse case, 50 N sideways knock on the knob: 70 MPa at the M6 thread root against 345 MPa yield (S45C). PASS, safety factor 4.9.

## 7. Operator pull force

| Quantity | Value | Unit |
|---|---|---|
| Spring force at full retraction | 28.3 | N |
| Friction allowance (guides + spring rubbing) | 1.2 | N |
| Peak pull force | 29.4 | N |
| Comfort limit used (A8) | 40 | N |

PASS, 74 % of the limit, 10.6 N margin. The pull starts at about 19 N and rises to 29 N.

If the knob is let go from full retraction the plunger (89 g) arrives at about 2300 mm/s with 232 mJ. Lower it by hand, or allow for a urethane washer under the stop nut.

## 8. Envelope and mounting

| Quantity | Value | Unit |
|---|---|---|
| Housing block, length x width x height | 72 x 50 x 35 | mm |
| Housing bores | 18 (front bushing), 13 (spring), 12 (rear bushing), 9 (web clearance) | mm |
| Housing mass, aluminium | about 300 | g |
| Centreline height above mounting face | 20 | mm |
| Mounting bolts | 4 x M5 socket head cap screw, from the top, counterbored | - |
| Bolt pattern | 50 along the axis x 34 across | mm |
| Bolt hole positions | 11 from each end face, 8 from each side face | mm |
| Tip | 16 dia x 10 long | mm |
| Knob | 25 dia x 20 long, with M6 stop nut 5 thick | mm |
| Overall mechanism, extended | 120 x 50 x 35 | mm |
| Overall swept length, knob pulled | 130 | mm |
| Total mass, estimate | about 430 | g |

Bolt check: overturning from 28.3 N at 20 mm height puts 11 N tension on a bolt pair, against 8236 N proof load for one M5 class 8.8 screw. PASS, the bolts are sized for handling, not for load. Counterbore to bore wall is 3.25 mm. PASS (minimum 3 mm).

Clearances: front flange 25 dia and knob 25 dia both sit 7.5 mm above the mounting face. PASS, but finger room under the knob is tight if the jig base extends behind the housing.

## 9. Anti-rotation

Not needed, provided the tip is round with a flat or domed face. Rotation of the plunger then changes nothing at the contact.

It becomes necessary only if the tip is shaped (V, angled face, offset pad). In that case: mill a flat on the 12 mm section and fit a keeper plate on the housing front face, or press a pin across the shaft running in a slot in the housing.

One related point: the operator can twist the knob, so the tip thread and the knob / stop nut pair need thread-locking.

## 10. Not verified

- All input requirements (section 1) are assumptions.
- Wire tensile strength is from the standard music-wire estimate (2153 MPa at 1.2 mm), not read from the JIS table for SWP-B.
- The 40 N comfort limit is a rule of thumb, not from an ergonomics standard.
- Bushing dimensions and running clearance are typical values, not catalogue values.
- No catalogue spring has been matched. The catalogue spring will have a slightly different rate, free length and coil count; forces, solid length and stress must be rechecked in Phase 2.
- Friction coefficients are handbook-range values, not measured.
- Nest height, part height and the datum position are unknown, so the 20 mm centreline height and the push point on the part are not checked.

## 11. Numbers to look at before approving

1. Guide friction loss 16.4 % against a 20 % limit, in the worst off-axis case. Keep the tip contact close to the shaft axis.
2. Pull force 29.4 N. Fine for occasional loading; for hundreds of cycles per shift a target nearer 20 to 25 N would be kinder, which means a lower clamp force or a lever.
3. Holding force sideways and upward is only 6 to 8 N. Confirm the process puts no larger load on the part.
4. Spring seat on the shaft shoulder: the spring OD equals the shoulder diameter (12 mm). The wire centreline is supported, but the shoulder edge must be kept sharp (chamfer 0.2 mm maximum) or a thin washer added.
5. The layout uses two bushings and a stepped shaft instead of one bushing and a collar.
6. Unguided buckling margin is only 3 %; the design relies on the shaft and bore guiding the spring.
