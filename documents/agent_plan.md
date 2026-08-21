# CRIPI Streamlit Agent — Product & Implementation Plan

## 1. Purpose

This document proposes the design and build plan for a **three-page Streamlit decision-support application** built on the **Climate Resilience Investment Priority Index (CRIPI)** framework for Mexico's 32 federal entities.

The app combines:

- **Executive-ready visual analytics** for quick strategic overview
- **Analyst-ready drill-down** into dimensions, rankings, and clusters
- **An AI assistant** on both pages so users can ask natural-language questions about the data

The primary audience is professionals working in international development cooperation — for example, sustainability analysts, economists, and senior managers at agencies such as **GIZ** — who need evidence-based inputs for climate resilience investment prioritization, not a raw dataset or notebook.

---

## 2. Product Vision

> *"A single application where a development agency user can see where climate resilience investments may matter most in Mexico, understand why through IPCC-inspired dimensions, explore how states naturally group by vulnerability profile, and ask follow-up questions in plain language."*

### Design principles

| Principle | What it means in practice |
|-----------|---------------------------|
| **Decision-first** | Lead with maps, KPIs, and comparisons — not methodology |
| **Transparent** | Always show CRIPI score + priority category + dimension context |
| **Complementary analytics** | CRIPI ranking and K-Means clusters are shown as two lenses, not competing truths |
| **Accessible to non-technical users** | Plain-language labels, tooltips, and an AI assistant |
| **Analyst-friendly** | Hover details, sortable tables, and export where useful |

### Important framing (shown in app footer or info panel)

Results are **decision-support outputs**, not definitive funding mandates. The framework uses official public indicators and equal weighting across IPCC-inspired dimensions for transparency and reproducibility.

---

## 3. Target Users & Jobs-to-be-Done

### Primary personas

**1. Senior executive / program director**
- Needs a fast national overview before meetings or portfolio discussions
- Wants to know: *Which states stand out? How uneven is vulnerability?*
- Uses **CRIPI Dashboard** primarily; may ask high-level questions to the agent

**2. Sustainability / climate analyst**
- Needs to compare states across Hazard, Exposure, Sensitivity, and Adaptive Capacity
- Wants to validate whether priority groups differ meaningfully by dimension
- Uses **CRIPI Dashboard** deeply; uses **State Clusters** to interpret cluster patterns

**3. Economist / M&E specialist**
- Needs transparent indicators, rankings, and group comparisons
- Wants to explore outliers and cross-check clustering against CRIPI categories
- Uses both pages and asks precise questions through the agent

### Core user questions the app should answer

1. Which Mexican states have the highest and lowest investment priority?
2. How is priority distributed geographically?
3. Which states score highest on each vulnerability dimension?
4. How far apart are Very High and Low priority states in their dimension profiles?
5. Do states form natural groups beyond the CRIPI ranking?
6. What drives a specific state's priority classification?

---

## 4. Application Structure

### Navigation model

Use Streamlit **`st.navigation`** multipage architecture (sidebar icons and labels defined in `app.py`):

```
app.py                         # Entry point — st.navigation + shared config
pages/
  0_CRIPI_Explained.py         # Home — methodology and audience overview
  1_CRIPI_Dashboard.py         # Main dashboard — map, profiles, rankings, chat
  2_State_Clusters.py          # Unsupervised learning view — PCA, clusters, chat
components/
  kpi_cards.py                 # KPI row (Page 1)
  state_sidebar.py             # State + national average indicator profiles
  chat_panel.py                # Shared AI chat widget
  page_style.py                # Shared CSS (beige/blue theme)
  theme.py                     # Colors, dimension labels, chart theme
  indicator_catalog.py         # 12 indicator metadata
  formatting.py                # Shared number formatting (1 decimal)
  cluster_utils.py             # PCA, national/cluster means, delta tables
  charts/
    mexico_map.py
    dimension_rankings.py
    priority_gap.py
    cluster_scatter.py
    cluster_dimension_profile.py
    cluster_indicator_profile.py   # Indicator delta tables (4 dimensions)
    cluster_priority_crosstab.py
ai/                            # Agent layer (Phase 1 complete)
data/
  climate_resilience_dashboard.csv
  geo/
    mexico_states.geojson
```

All three pages share:

- Branding and sidebar navigation (📘 CRIPI Explained · 📊 CRIPI Dashboard · 🧩 State Clusters)
- The same underlying dataset (`climate_resilience_dashboard.csv`)
- A reusable **chat panel** at the bottom (dashboard and clusters pages)
- Consistent color palette (`components/theme.py`, `components/page_style.py`)

---

### Page 0 — CRIPI Explained (home)

**Sidebar label:** 📘 CRIPI Explained

**Purpose:** Orient non-technical users before they explore the data.

**Sections (implemented):**
- What CRIPI is
- What the app can be used for
- Target audience (international development cooperation)
- Methodology at a glance (four dimensions, CRIPI index, K-Means, AI assistant)
- How to navigate the three pages

Uses the same styled panels as the dashboard (`intro-panel`, `cluster-summary-card`).

---

## 5. Page 1 — CRIPI Dashboard

### Page title

**Climate Resilience Investment Priority Framework - Mexico 🇲🇽**

Subtitle: *IPCC-informed decision support for international development cooperation*

**Sidebar label:** 📊 CRIPI Dashboard

### 5.1 Top KPI cards (4 cards in one row)

| Card | Content | Source field | Example value |
|------|---------|--------------|---------------|
| **CRIPI Range** | Min – Max index | `cripi` | **16.1 – 56.8** |
| **Highest Priority State** | State name + CRIPI | `state`, `cripi`, `investment_priority_rank` | **Chiapas · 56.8** |
| **Lowest Priority State** | State name + CRIPI | `state`, `cripi` | **Nuevo León · 16.1** |
| **States Analyzed** | Count of entities | dataset row count | **32** |

Optional small caption under cards:
- Priority groups in dataset: 6 Very High · 9 High · 11 Moderate · 6 Low

#### Visual recommendation

Use `st.columns(4)` with metric-style cards:

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ CRIPI Range  │ │ Highest      │ │ Lowest       │ │ States       │
│ 16.1 – 56.8  │ │ Chiapas      │ │ Nuevo León   │ │ 32           │
│              │ │ 56.8         │ │ 16.1         │ │              │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

---

### 5.2 Mexico map — CRIPI priority classification

**Goal:** Show geographic distribution of investment priority at a glance.

**Chart type:** Choropleth map of Mexico by state

**Mapped variable:** `investment_priority_category`

**Categories & suggested colors**

| Category | Suggested color | Count in current data |
|----------|-----------------|------------------------|
| Very High Priority | `#8B0000` (dark red) | 6 |
| High Priority | `#E67E22` (orange) | 9 |
| Moderate Priority | `#F4D03F` (amber) | 11 |
| Low Priority | `#27AE60` (green) | 6 |

**Interaction**
- Hover tooltip: State, CRIPI, rank, priority category
- Optional click/select state → highlights state in charts below and pre-fills chat suggestion

**Technical note**
- Join CSV `state_code` (INEGI 2-digit code) with a GeoJSON of Mexican states
- Recommended libraries: **Plotly Express** (`px.choropleth`) or **Pydeck** (already in requirements)
- Add `data/geo/mexico_states.geojson` to the repo

**Suggested layout width:** Full page width below KPI cards

---

### 5.3 Top 5 states by dimension index

**Goal:** Show which states dominate each dimension.

**Recommended layout:** 2 × 2 grid of horizontal bar charts

| Chart | Metric | Sort |
|-------|--------|------|
| Hazard | `hazard_dimension_index` | Top 5 descending |
| Exposure | `exposure_dimension_index` | Top 5 descending |
| Sensitivity | `sensitivity_dimension_index` | Top 5 descending |
| Adaptive Capacity Gap | `adaptive_capacity_dimension_index` | Top 5 descending |

**Labeling note for executives**

Use **"Adaptive Capacity Gap"** in the UI rather than raw index language. In your framework, higher values on this dimension index indicate **lower adaptive capacity / higher vulnerability**, so the chart title should make that explicit:

> *Top 5 states by Adaptive Capacity Gap (lower capacity → higher score)*

**Optional enhancement**
- Color bars by `investment_priority_category` to connect dimension leaders with overall priority

**Example layout**

```
┌─────────────────────┐  ┌─────────────────────┐
│ Top 5 Hazard        │  │ Top 5 Exposure      │
└─────────────────────┘  └─────────────────────┘
┌─────────────────────┐  ┌─────────────────────┐
│ Top 5 Sensitivity   │  │ Top 5 Adaptive Cap. │
└─────────────────────┘  └─────────────────────┘
```

---

### 5.4 Priority gap chart — Very High vs Low states

**Goal:** Communicate *how different* the extreme priority groups are across dimensions.

**Recommended chart:** Grouped bar chart or radar chart

**Logic**
1. Filter states with `investment_priority_category == "Very High Priority"`
2. Filter states with `investment_priority_category == "Low Priority"`
3. Compute the **mean** of each dimension index for each group
4. Plot side-by-side bars for the four dimensions

**Dimensions on x-axis**
- Hazard
- Exposure
- Sensitivity
- Adaptive Capacity Gap

**Series**
- Very High Priority (group average)
- Low Priority (group average)

**Why this works for GIZ users**
- Executives immediately see whether priority differences are driven by one dimension or all four
- Analysts can discuss policy implications ("high priority states are especially separated on Sensitivity and Adaptive Capacity")

**Alternative:** dumbbell chart showing group mean vs group mean per dimension — very effective for "distance" storytelling

**Suggested insight callout (auto-generated text block)**

> Very High priority states average **XX** points higher on Sensitivity and **YY** points higher on Adaptive Capacity Gap than Low priority states.

This can later be agent-generated in Phase 2.

---

### 5.5 Indicator drill-down — showing the 12 underlying indicators

The dimension indices give executives a fast summary, but development-agency analysts will ask **which specific indicators** drive a state's score. The app should expose a clear three-level hierarchy:

```
CRIPI (composite)
 └── 4 Dimension Indices
      └── 12 Indicators (official input variables)
```

#### Indicator inventory (from your framework)

| Dimension | Dimension index | Underlying indicators | Scale in data |
|-----------|-----------------|----------------------|---------------|
| **Hazard** | `hazard_dimension_index` | Flood hazard · Cyclone hazard · Drought hazard | 1–5 |
| **Exposure** | `exposure_dimension_index` | Population density · Agricultural land share | Mixed units |
| **Sensitivity** | `sensitivity_dimension_index` | Multidimensional poverty · Marginalization score · Employment in primary sector | % / index / % |
| **Adaptive Capacity** | `adaptive_capacity_dimension_index` | Educational attainment · Access to piped water · Access to drainage · Health service affiliation | Years / % / % / % |

All 12 indicators are already present in `climate_resilience_dashboard.csv` and mapped in `ai/data_loader.py` under `DIMENSION_COLUMNS`.

#### Design principle: state-level indicators on Page 1

On **Page 1**, indicators are shown for a **selected state** or, when **All states** is selected, the **national average** across all 32 states.

On **Page 2**, indicators are shown at the **cluster level** — as the mean of each of the 12 indicators across all states in a selected cluster (see Section 6.3).

| Page | Indicator granularity | Primary question answered |
|------|----------------------|---------------------------|
| Page 1 | **State level** or **national average** | *"What drives this state's priority score?"* / *"What does Mexico average look like?"* |
| Page 2 | **Cluster level (deltas)** | *"What indicator profile defines this group of states?"* |

---

#### Page 1 — State indicator profile (primary indicator view)

**Placement:** Directly below the Mexico map and above the dimension top-5 charts — or in a two-column layout with the map on the left and the profile on the right.

**State selection**

- Dropdown: `Select a state` with **All states** as default
- **All states:** map shows full priority coloring; profile panel shows **National average**
- **Single state:** map highlights selected state; profile shows that state's 2×2 dimension grid with 12 indicators
- Dimension card label uses **Adaptive Capacity** (not "Adaptive Capacity Gap") in the profile UI

**Profile layout**

| Block | Content |
|-------|---------|
| **Header** | State name · CRIPI · Rank · Priority category · Cluster |
| **Dimension summary** | 4 cards in 2×2 grid: Hazard · Exposure · Sensitivity · Adaptive Capacity |
| **Indicator breakdown** | All 12 indicators grouped by dimension |

**Indicator row pattern (repeat × 12)**

Each indicator shows:
- Plain-language label + unit + data source
- **State value** (raw, in original units)
- **Comparison bar** vs national median or national mean
- Optional delta label (e.g. *+24 pp vs national median*)

```
Chiapas · CRIPI 56.8 · Rank 1 · Very High Priority · Cluster 1
────────────────────────────────────────────────────────────────

Dimensions          Hazard 17.8 │ Exposure 36.1 │ Sensitivity 97.3 │ Adaptive Capacity Gap 75.9

Hazard (CENAPRED 2020)
  Flood hazard              2.95   ████████░░░░░░░░  (near median)
  Cyclone hazard            1.40   ████░░░░░░░░░░░░  (low)
  Drought hazard            2.18   ██████░░░░░░░░░░  (moderate)

Sensitivity
  Multidimensional poverty  67.4%  ████████████████  (+24 pp vs median)
  Marginalization score     11.45  ████████████████  (very high)
  Primary sector employment 31.4%  ████████████░░░░  (high)

Adaptive Capacity
  Educational attainment     7.8 yrs ████████░░░░░░░░  (below median)
  Access to piped water     52.4%  ████████░░░░░░░░  (low)
  ...
```

**Optional compact views within the state profile**

- `st.tabs` inside the profile: **Overview | Hazard | Exposure | Sensitivity | Adaptive Capacity** — each tab lists only that dimension's indicators for the selected state
- Keeps 12 indicators organized without leaving the state context

**Why state-level works for Page 1**
- Matches how executives ask questions: *"Tell me about Chiapas"*, not *"Who ranks top 5 on flood hazard?"*
- Connects directly to map interaction
- Natural handoff to the AI chat: *"Explain Chiapas's sensitivity indicators"*
- Dimension top-5 charts (Section 5.3) remain national context; the state profile adds the indicator depth

---

#### Page 1 — Optional secondary indicator views

These are **supporting**, not primary:

| View | Purpose | When to show |
|------|---------|--------------|
| **State comparison mode** | Two selected states, indicators side-by-side | Analyst toggle |
| **Gap chart at indicator level** (Section 5.4 toggle) | Very High vs Low group means | Executive summary only |
| ~~Dimension tabs with national top-5 per indicator~~ | Removed from Page 1 | Use Page 2 cluster means instead |

Do **not** build national-level indicator ranking charts on Page 1 — that role belongs to the dimension top-5 charts (5.3) at the aggregate level, and to cluster indicator means on Page 2.

---

#### Recommended Page 1 layout (updated)

| Layer | Component | Indicator level |
|-------|-----------|-----------------|
| 1 | KPI cards | National |
| 2 | Mexico map + **state selector** (`All states` or one state) | State selection / national |
| 3 | **State or national indicator profile** (12 indicators, 2×2 grid) | **State** or **national average** |
| 4 | Dimension top-5 charts (5.3) | National (dimension indices only) |
| 5 | Very High vs Low gap chart (5.4) | National (dimensions; optional indicator toggle) |
| 6 | AI chat | State-aware prompts |

---

### 5.6 AI chat panel (bottom of Page 1)

**Placement:** Fixed section at bottom with divider: `Ask the CRIPI Assistant`

**Behavior (implemented)**
- Agent in `ai/agent.py` uses a **two-step loop**: tool call → JSON result → Grok synthesizes a text answer
- Answers include interpretation and **2–4 data-grounded recommendations** when the question is analytical
- Optional small markdown tables in the reply; tools no longer render duplicate Streamlit charts in chat
- Separate conversation history per page (`messages_priorities`, `messages_clusters`)
- Suggested prompt chips (examples):

  - *Why is Chiapas ranked first?*
  - *Why are Very High Priority states similar?*
  - *What investments would you recommend for Chiapas?*

**Page 1 agent persona emphasis**
- Investment prioritization for a **selected state**
- Dimension and **state-level indicator** interpretation
- State comparisons and rankings

**Agent integration with state selector**
- Pass the currently selected state into the chat context (Phase 4)
- Example: user selects Chiapas on the map → chat system prompt includes *"User is viewing Chiapas"*

**UI pattern**

```
────────────────────────────────────────
💬 Ask the CRIPI Assistant
[ suggested prompt chips ]

[ chat history ]

[ user input box ]
────────────────────────────────────────
```

---

## 6. Page 2 — State Clusters & Vulnerability Profiles

### Page title

**State Clustering Analysis 🧩**

Subtitle: *How Mexican states group by similar climate vulnerability profiles (K-Means, k = 4)*

**Sidebar label:** 🧩 State Clusters

### 6.1 Conceptual framing (short intro block)

Explain in 2–3 sentences:

- K-Means clustering groups states by similarity across the **four dimension indices**
- Clustering **validates and complements** CRIPI; it does not replace the investment priority ranking
- Clusters help identify states that may need **similar policy interventions** even if their CRIPI rank differs

This mirrors the methodology in `notebooks/04_climate_resilience_framework.ipynb`.

---

### 6.2 Main visualization — cluster scatter plot

**Goal:** Show how the 32 states naturally group in vulnerability space.

**Recommended approach (consistent with notebook):**

1. Use the 4 dimension indices as clustering features:
   - `hazard_dimension_index`
   - `exposure_dimension_index`
   - `sensitivity_dimension_index`
   - `adaptive_capacity_dimension_index`
2. Apply **PCA** to reduce to 2 components for visualization
3. Plot a scatter chart:
   - X = PC1
   - Y = PC2
   - Color = `cluster` (1–4)
   - Label each point with state abbreviation or name

**Current cluster distribution in data**

| Cluster | States | Size |
|---------|--------|------|
| 1 | Chiapas, Guerrero, Oaxaca | 3 |
| 2 | Mostly northern / lower-priority states | 14 |
| 3 | Mixed central and southern states | 7 |
| 4 | Campeche, Tabasco, Veracruz, etc. | 8 |

**Interaction**
- Hover: state, cluster, CRIPI, priority category, 4 dimension values
- Optional toggle: color points by **cluster** or by **investment_priority_category** to compare the two lenses

**Why PCA here**
- Keeps the chart faithful to the notebook workflow
- Makes an unsupervised model understandable to non-ML executives

---

### 6.3 Supporting visuals for Page 2

#### A. Cluster indicator profile — indicator deltas (implemented)

**This is the main indicator view on Page 2.** While Page 1 shows indicators for one state (or national average), Page 2 shows **indicator deltas** — how a selected cluster's average differs from the national mean.

**Design decision:** Grouped bar charts for all 12 indicators were **not implemented** because indicators use mixed units (% vs years vs 1–5 scale). Delta **tables** per dimension avoid misleading visual comparisons.

**Cluster selection**
- Dropdown: `Select a cluster` (1–4) in the sidebar panel
- Member states shown as chips with cluster summary label
- PCA scatter highlights the selected cluster; toggle to color by cluster or investment priority

**Implemented layout:**
1. **Cluster dimension profile** — grouped bar: cluster vs national mean for 4 dimension indices
2. **Indicator deltas** — legend explaining the tables; four 2×2 tables (one per dimension)
3. Each table: Indicator · Cluster mean · National mean · Delta (sorted by distinctiveness within dimension)
4. **Highlighted row** = most distinctive indicator in that dimension for the selected cluster
5. Dimension header uses **Adaptive Capacity** in the profile UI

**Companion table columns**

| Indicator | Cluster mean | National mean | Delta |
|-----------|-------------|---------------|-------|
| Multidimensional poverty | 62.1% | 35.2% | +26.9 pp |
| Access to piped water | 47.4% | 78.6% | −31.2 pp |

All numeric values formatted to **one decimal place**.

---

#### B. Cluster scatter plot (see 6.2)

Dimension-level PCA view — keep as the entry point for cluster exploration.

---

#### C. Cluster dimension profile (implemented)

Grouped bar of the **4 dimension index means** per cluster vs national mean — shown above the indicator delta tables.

---

#### D. Cluster membership table

~~Sortable table of all states~~ — **Removed from UI** (not needed for executive/analyst flow; state detail available on CRIPI Dashboard).

Component removed from Page 2 UI; cluster membership is shown via the cluster selector chips and PCA map.

---

#### E. Cluster vs priority cross-tab (implemented)

Stacked bar showing how CRIPI priority categories distribute within each cluster. Hover shows **number of states** per segment. No summary table below the chart.

---

### 6.4 AI chat panel (bottom of Page 2)

Same component as Page 1, but with **cluster-aware suggested prompts** (examples):

- *Which states belong to Cluster 1 and what do they have in common?*
- *What makes Cluster 1 distinctive compared to the national average?*
- *What interventions would you recommend for Cluster 1?*

**Page 2 agent persona emphasis**
- Cluster interpretation
- Similarity between states
- Relationship between clusters and CRIPI categories
- Indicator-level cluster profiles via `get_cluster_profile`

**Implemented tools for clusters**
- `get_cluster_profile(cluster_id)` — membership, dimension means vs national, top indicator deltas

**Optional future tools**
- `compare_clusters(a, b)` — side-by-side cluster comparison
- Pass selected cluster from the UI into chat context (Phase D)

---

## 7. End-to-End User Journey Examples

### Journey A — Executive briefing (5 minutes)

1. Opens **CRIPI Explained** or **CRIPI Dashboard**
2. Reads KPI cards → sees Chiapas highest, Nuevo León lowest
3. Looks at Mexico map → identifies southern and Gulf concentration of Very High priority states
4. Scans dimension top-5 charts → notices Sensitivity and Adaptive Capacity dominate separation
5. Asks agent: *"Give me a 3-sentence summary for a director about where to focus resilience investments."*

### Journey B — Analyst deep dive (15 minutes)

1. Opens **CRIPI Explained** or **CRIPI Dashboard** → compares Very High vs Low dimension gap chart
2. Moves to **State Clusters** → inspects PCA cluster plot and cluster profile table
3. Notices a state with High priority sitting in a mostly moderate cluster
4. Asks agent: *"Explain why Michoacán is High Priority but clusters with states that have different vulnerability profiles."*

### Journey C — Portfolio planning workshop

1. Facilitator projects Page 1 map and gap chart
2. Team selects three states on the map
3. Uses chat to compare indicators and dimensions live
4. Switches to **State Clusters** to discuss whether selected states belong to the same intervention archetype

---

## 8. Visual Design Proposal

### Tone

Professional, institutional, calm — suitable for development cooperation audiences. Avoid flashy or startup-style UI.

### Color system

**Priority categories**
- Very High: `#8B0000`
- High: `#D35400`
- Moderate: `#F1C40F`
- Low: `#1E8449`

**Clusters (Page 2)**
- Cluster 1: `#E74C3C`
- Cluster 2: `#3498DB`
- Cluster 3: `#9B59B6`
- Cluster 4: `#16A085`

Use the same colors consistently in maps, bars, scatter plots, and chat result tables.

### Typography & layout

- `layout="wide"` for both pages
- Page header + short subtitle + optional methodology expander
- Charts in cards with concise titles
- Chat panel visually separated at the bottom

### Accessibility

- Do not rely on color alone: add labels and tooltips
- Include text summaries for each main chart
- Keep chart titles plain-language (avoid internal notebook variable names)

---

## 9. Technical Architecture

### 9.1 Data layer

**Primary source:** `data/climate_resilience_dashboard.csv`

Already normalized in `ai/data_loader.py` with snake_case columns.

**Indicator metadata (implemented):**

`components/indicator_catalog.py` — single source of truth for UI labels, units, sources, and dimension grouping:

```python
INDICATOR_CATALOG = {
    "flood_hazard_index": {
        "label": "Flood hazard",
        "dimension": "hazard",
        "unit": "1–5 scale",
        "source": "CENAPRED 2020",
        "description": "Population-weighted flood hazard exposure",
    },
    ...
}
```

Use this catalog in charts, tooltips, state profiles, and agent prompts so indicator names stay consistent across the app.

**Additional asset needed for Page 1 map:**
- `data/geo/mexico_states.geojson` with INEGI state codes joinable to `state_code`

**Optional future assets:**
- `data/processed/cluster_coordinates.csv` — precomputed PCA coordinates exported from notebook for exact parity with analysis

### 9.2 Visualization stack

| Component | Recommended library | Why |
|-----------|---------------------|-----|
| KPI cards | Streamlit `st.metric` | Native, fast |
| Mexico map | Plotly Express or Pydeck | Good hover + color scales |
| Bar charts | Plotly or Altair | Already in requirements |
| Gap chart | Plotly grouped bar | Easy comparison |
| State indicator profile | HTML grid in `state_sidebar.py` | **Page 1:** state or national average |
| Cluster indicator profile | Four delta tables by dimension | **Page 2:** cluster mean vs national mean |
| Cluster scatter | Plotly scatter + PCA (`cluster_utils.py`) | Labels, hover, color toggle |
| Cluster vs priority | Stacked bar (`cluster_priority_crosstab.py`) | Hover: state counts |

### 9.3 Agent layer

**Implemented (`ai/`)**

| Component | Role |
|-----------|------|
| `agent.py` | Grok API client; two-step tool loop (up to 3 rounds) |
| `tools.py` | Four tools returning JSON for the LLM to analyze |
| `prompts.py` | System prompt: persona, synthesis rules, recommendations |
| `cripi_schema.py` | Dataset schema injected into the prompt |
| `domain_context.py` | Indicator glossary injected into the prompt |

**Tools**

| Tool | Use when |
|------|----------|
| `get_state_data` | Specific states, columns, priority filters |
| `rank_states` | Top/bottom rankings |
| `summarize_priority_group` | Why states in a priority category are similar |
| `get_cluster_profile` | Cluster membership and vs-national profile |

**Flow**

```
User message → Grok → (optional) tool(s) → JSON → Grok → markdown answer
```

Tools do **not** render Streamlit dataframes; the assistant reply carries analysis and optional markdown tables.

**Optional future enhancements**

| Phase | Enhancement |
|-------|-------------|
| Phase D | Chart-aware context (selected state / cluster passed into prompt) |
| Phase D | `compare_clusters(a, b)` tool |
| Phase D | Streaming responses |

### 9.4 Shared chat component design

```python
# components/chat_panel.py
def render_chat_panel(page_key: str, suggestions: list[str], system_prompt: str):
    ...
```

Store messages in:
- `st.session_state[f"messages_{page_key}"]`

This prevents Page 1 ranking questions from polluting Page 2 cluster conversations.

---

## 10. Proposed Page Wireframes

### Page 0 — wireframe

```
┌────────────────────────────────────────────────────────────────────────────┐
│ CRIPI Explained 📘                                                          │
│ Climate Resilience Investment Priority Index for Mexico                    │
├────────────────────────────────────────────────────────────────────────────┤
│ [ Intro panel — what CRIPI is ]                                            │
│ 🎯 What can it be used for?                                                │
│ 👥 Who is this app for?                                                    │
│ 🔬 Methodology at a glance (4 summary cards)                               │
│ 🧭 How to navigate the app                                                 │
└────────────────────────────────────────────────────────────────────────────┘
```

### Page 1 — wireframe (CRIPI Dashboard)

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Climate Resilience Investment Priority Framework - Mexico 🇲🇽               │
│ IPCC-informed decision support for international development cooperation  │
├──────────────┬──────────────┬──────────────┬──────────────────────────────┤
│ CRIPI Range  │ Highest      │ Lowest       │ States Analyzed              │
│ 16.1–56.8    │ Chiapas 56.8 │ Nuevo León   │ 32                           │
├────────────────────────────────────────────────────────────────────────────┤
│ 🗺️ Geographic overview                                                    │
│ [ Mexico choropleth map ]          │  [ State selector: All states ▼ ]   │
├────────────────────────────────────┴─────────────────────────────────────────┤
│ STATE / NATIONAL INDICATOR PROFILE (2×2 dimension grid · 12 indicators)     │
│  National average  OR  Chiapas · Hazard · Exposure · Sensitivity · Adaptive Capacity │
├───────────────────────────────┬────────────────────────────────────────────┤
│ 📊 Top 5 Hazard               │ Top 5 Exposure                             │
├───────────────────────────────┼────────────────────────────────────────────┤
│ Top 5 Sensitivity             │ Top 5 Adaptive Capacity Gap                │
├────────────────────────────────────────────────────────────────────────────┤
│ ⚖️ [ Very High vs Low priority dimension gap chart ]                        │
├────────────────────────────────────────────────────────────────────────────┤
│ 💬 Ask the CRIPI Assistant (state-aware prompts)                            │
│ [chips] [chat history] [input]                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

### Page 2 — wireframe

```
┌────────────────────────────────────────────────────────────────────────────┐
│ State Clustering Analysis 🧩                                                │
│ K-Means vulnerability profiles · k = 4                                      │
├────────────────────────────────────────────────────────────────────────────┤
│ [ Intro panel — methodology note ]                                           │
├───────────────────────────────┬────────────────────────────────────────────┤
│ 📍 [ PCA cluster scatter ]    │ 🔍 [ Cluster selector + member chips ]     │
│                               │ [ Color by: Cluster / Priority ]           │
├────────────────────────────────────────────────────────────────────────────┤
│ 📊 Cluster dimension profile (cluster vs national · 4 indices)             │
├────────────────────────────────────────────────────────────────────────────┤
│ 📋 Cluster indicator profile — INDICATOR DELTAS (4 tables by dimension)    │
│  [ legend panel ]                                                          │
│  ⚠️ Hazard │ 🏙️ Exposure │ 🏚️ Sensitivity │ 🛡️ Adaptive Capacity          │
│  each table: indicator | cluster mean | national mean | delta              │
│  highlighted row = most distinctive indicator in dimension                   │
├────────────────────────────────────────────────────────────────────────────┤
│ 🔀 Clusters vs investment priority (stacked bar · hover = state count)     │
├────────────────────────────────────────────────────────────────────────────┤
│ 💬 Ask the CRIPI Assistant (cluster-aware prompts)                          │
│ [chips] [chat history] [input]                                              │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## 11. Implementation Roadmap

### Phase 0 — Home page (CRIPI Explained)
- [x] Add `pages/0_CRIPI_Explained.py` with methodology and audience overview
- [x] Configure `st.navigation` sidebar with icons (📘 📊 🧩)

### Phase A — CRIPI Dashboard (Page 1)
- [x] Convert to multipage Streamlit app (`app.py` + `pages/`)
- [x] Build shared `load_cripi_data()` and `indicator_catalog.py`
- [x] Implement KPI cards
- [x] Add GeoJSON and Mexico choropleth with state selector (`All states` default)
- [x] Build **state / national indicator profile** (12 indicators, 2×2 grid)
- [x] Build 4 top-5 dimension charts
- [x] Build Very High vs Low dimension gap chart (values rounded to 1 decimal)
- [x] Embed state-aware chat panel
- [x] Shared page styling (`page_style.py`, `theme.py`)

### Phase B — State Clusters (Page 2)
- [x] PCA scatter on 4 dimension indices (`cluster_utils.py`, `cluster_scatter.py`)
- [x] Cluster selector with member chips and color toggle
- [x] Cluster dimension profile (cluster vs national means)
- [x] **Indicator delta tables** (4 dimensions; no mixed-unit bar charts)
- [x] Clusters vs investment priority stacked bar (hover state counts)
- [x] Embed cluster-aware chat panel

### Phase C — Chat integration and synthesis
- [x] Extract reusable `chat_panel` component
- [x] Separate session histories per page (`messages_priorities`, `messages_clusters`)
- [x] Page-specific prompt suggestions
- [x] Two-step tool loop — natural-language answers with analysis and recommendations
- [x] Analytical tools: `summarize_priority_group`, `get_cluster_profile`
- [x] Markdown rendering for assistant replies

### Phase D — Executive polish
- [x] CRIPI Explained home page (methodology context)
- [ ] Methodology expander with link to `documents/project_design.md` on dashboard
- [ ] Chart insight callouts
- [ ] State/cluster selection linked to chat context
- [ ] Export table / screenshot-friendly layout
- [ ] `compare_clusters(a, b)` tool

---

## 12. Success Criteria

The app is successful if a GIZ-type user can, without reading the notebook:

1. Identify the highest-priority states within 30 seconds
2. Explain geographically where priority is concentrated
3. Name the dominant dimension drivers for top-priority states
4. Describe how Very High and Low groups differ
5. **Name the specific indicators** (e.g. poverty, water access) behind a state's dimension score
6. Understand that clusters represent similar vulnerability profiles
7. Ask a follow-up question and receive a relevant, data-grounded answer

---

## 13. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Map join fails due to state name/code mismatch | Standardize on INEGI `state_code` in GeoJSON join |
| Executives misread Adaptive Capacity index direction | Use "Adaptive Capacity Gap" label and tooltip |
| Agent returns raw JSON or overly technical answers | Two-step synthesis loop in `ai/agent.py`; tools return JSON internally; user sees markdown analysis |
| Notebook and app clustering diverge | Export PCA coordinates and cluster labels from notebook to CSV |
| User confuses CRIPI categories with ML clusters | Dedicated explainer on Page 2 + cross-tab visual |
| 12 indicators overwhelm executives | State profile shown only for one selected state at a time |
| Indicators use different units (1–5 vs % vs years) | Page 2 uses **delta tables** by dimension instead of combined bar charts; raw units shown in cells |
| Page 1 vs Page 2 indicator views feel redundant | Clear split: **state/national (P1)** vs **cluster deltas (P2)** |

---

## 14. Recommended Next Step

Phases A, B, and **C (agent synthesis)** are **complete**. Optional next work:

1. **Phase D** — Chart-aware chat context; `compare_clusters` tool; export
2. Keep `documents/agent_plan.md` updated as the UI evolves

Current entry point:

```bash
streamlit run app.py
```

Bootcamp shortcut (dashboard page only):

```bash
streamlit run app_solution.py
```

---

## 15. Appendix — Current Data Snapshot

From `data/climate_resilience_dashboard.csv`:

- **CRIPI range:** 16.1 – 56.8
- **Highest priority:** Chiapas (56.8, rank 1, Very High Priority)
- **Lowest priority:** Nuevo León (16.1, rank 32, Low Priority)
- **Priority distribution:** 6 Very High · 9 High · 11 Moderate · 6 Low
- **Clusters (k = 4):** Cluster 1 (3 states) · Cluster 2 (14) · Cluster 3 (7) · Cluster 4 (8)

These values should appear in the KPI cards and be used to validate chart correctness during development.
