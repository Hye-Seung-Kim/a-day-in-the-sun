# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Standalone HTML, CSS, and JavaScript preview. Selected by the user for a lightweight, directly runnable prototype with no framework dependency.

## Users

Primary readers are interaction-design faculty, peers, and research participants reviewing an MFA thesis investigation into sunlight, sunscreen use, and everyday outdoor behavior.

## Product Purpose

“A Day in the Sun” is an interactive editorial data story. It helps readers understand selected weighted estimates from the CDC/NCHS Rapid Surveys System and then see why those survey patterns motivate further primary design research about outdoor experience.

Success means a reader can follow the argument through ordinary scrolling, understand when the analytical population changes, make a prediction and operate the chart controls, inspect the underlying values as text, and distinguish survey evidence from the researcher’s next questions.

## Positioning

The story uses one continuous illustrated beach world to move between population-level survey patterns, product priorities, and an open design-research question. The beach is narrative scaffolding, not a claim about who answered the survey.

## Operating Context

The artifact will be viewed as a desktop and mobile web preview and may later inform a thesis presentation, Figma work, or a deployed editorial story.

## Capabilities and Constraints

- An interactive prediction, five survey chapters, and a thesis closing. A sticky chart stage is used from 760px; mobile keeps the same controls in readable inline scenes.
- Face and other exposed skin toggle for reported use, with persistent percentage marks and a grid/group arrangement switch.
- Selectable sunscreen purchase considerations through both illustration labels and chart rows.
- Frequent/less-frequent association comparison on one fixed 0–100% scale.
- Prediction slider with reveal/reset; guesses remain on the page and are never collected.
- Clickable chapter navigation, scroll-triggered chart entrances, subtle illustration parallax, and an explicit pause-motion control.
- Text-table access to every displayed value.
- Native scrolling only. No forced scrolling or long scroll locks.
- Every percentage is a weighted valid-response estimate. Listed n values are unweighted valid respondent counts.
- Human icons are rounded percentage marks, not survey respondents or longitudinal individuals.
- No simulation of sunburn, skin damage, shade use, reapplication behavior, or product effectiveness.
- No causal interpretation of cross-sectional self-reported associations.

## Brand Commitments

- Name: A Day in the Sun.
- English-language page copy.
- Warm sand, pale ocean, dark ink, with purple, yellow, and coral accents inherited from the existing deck.
- Distinctive flat 2D editorial illustration viewed slightly from above.
- Recurring beach people, striped parasol, towels, sunscreen, and beach bag.
- Skin color never encodes data.
- Parasols and shadows create place only and never classify protection behavior.

## Evidence on Hand

- CDC/NCHS Rapid Surveys System, Round 1, August 2023.
- Total sample: 7,599 U.S. adults.
- Analysis weight: WEIGHT_M1.
- Official codebook: https://www.cdc.gov/nchs/data/rss/codebook.pdf
- Local validated analysis and source files: the parent `CDC_Sunscreen_DataViz/` folder (kept local, not in this repository).
- The brief supplies every displayed estimate, recode, and unweighted valid n.
- Sunburn history and outdoor enjoyment were not measured in this survey. No participant stories, names, or quotations are available and none may be invented.

## Product Principles

1. Make denominator changes visible before visual transitions.
2. Keep belief, stated importance, reported use, and lived outdoor experience conceptually distinct.
3. Let the illustrated world sustain attention without turning scenery into unmeasured data.
4. Preserve uncertainty and limitations near the claims they qualify.
5. End with an open research question rather than a predetermined product solution.

## Accessibility & Inclusion

- Meaning is conveyed through labels and position in addition to color.
- Interactive controls support keyboard and touch input with visible focus states.
- Motion respects `prefers-reduced-motion` and content remains readable without animation.
- A text table provides an alternate representation of chart data.
- Responsive layouts prevent illustrations and charts from obscuring the article on narrow screens.

## Interaction revision — October 15, 2026

Motion purpose: explanation, state indication, and continuity in an occasional editorial experience. CSS transform/opacity transitions handle chart regrouping and scene changes; clip-path reveals the story introduction. The standard curve is cubic-bezier(0.23, 1, 0.32, 1), and on-screen regrouping uses cubic-bezier(0.77, 0, 0.175, 1). Controls use 160–240ms; explanatory movement uses 600ms with 40ms row stagger. Keyboard actions resolve instantly. System reduced-motion settings and the page's pause control remove movement.

Interaction references: https://pudding.cool/2026/06/love-story/ and https://pudding.cool/2026/05/kpop-generations/. No reference-site artwork or story content is reused.
