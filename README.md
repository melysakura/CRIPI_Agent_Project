# CRIPI Climate Resilience Dashboard

Decision-support application for the **Climate Resilience Investment Priority Index (CRIPI)** — an IPCC-informed framework for prioritizing climate resilience investments across Mexico's 32 states.

## Quick start

1. **Install dependencies**

```bash
pip install -r requirements.txt
```

2. **Configure environment**

Copy `.env.sample` to `.env` and add your xAI API key:

```bash
cp .env.sample .env
```

3. **Run the app**

```bash
streamlit run app.py
```

For the dashboard page only (bootcamp shortcut):

```bash
streamlit run app_solution.py
```

## App pages

| Sidebar | File | Purpose |
|---------|------|---------|
| 📘 **CRIPI Explained** | `pages/0_CRIPI_Explained.py` | Methodology overview, audience, and navigation guide |
| 📊 **CRIPI Dashboard** | `pages/1_CRIPI_Dashboard.py` | KPIs, Mexico map, state/national indicator profiles, dimension rankings, priority gap chart |
| 🧩 **State Clusters** | `pages/2_State_Clusters.py` | PCA cluster map, cluster dimension profile, indicator deltas, clusters vs. priority chart |
| 💬 **CRIPI Assistant** | `pages/3_CRIPI_Assistant.py` | AI chat for priorities, indicators, and cluster questions |

Navigation is defined in `app.py` using `st.navigation`.

## Project structure

```
app.py                          # Entry point (sidebar navigation)
pages/
  0_CRIPI_Explained.py          # Home / methodology page
  1_CRIPI_Dashboard.py          # Main dashboard
  2_State_Clusters.py           # Cluster analysis
  3_CRIPI_Assistant.py          # AI assistant (dedicated page)
components/                     # UI modules (charts, KPI cards, chat, styling)
ai/                             # Agent, tools, data loader, prompts
data/
  climate_resilience_dashboard.csv
  geo/mexico_states.geojson
documents/                      # Project design and implementation plan
notebooks/                      # Data collection and analysis workflow
```

## Data & methodology

- **Dataset:** `data/climate_resilience_dashboard.csv` (32 states, CRIPI, 4 dimension indices, 12 indicators, K-Means clusters)
- **Framework:** IPCC-inspired dimensions — Hazard, Exposure, Sensitivity, Adaptive Capacity
- **Clustering:** K-Means (k = 4) on dimension indices; PCA used for the cluster scatter plot

See `documents/project_design.md` and `documents/agent_plan.md` for full methodology and product design.

## AI assistant

The chat panel lives on its own sidebar page (**CRIPI Assistant**) so users can explore charts and ask questions side by side. It uses the **Grok API** (`XAI_API_KEY`).

**How it works:**
1. User asks a question; greetings are answered locally (no API call).
2. Grok may call one or more **tools** that query the same CSV as the dashboard.
3. Tool results are returned as JSON; Grok then writes a **natural-language answer** with analysis and, when relevant, **actionable recommendations**.
4. Replies render as markdown in the chat (bullets, small tables).

**Tools** (`ai/tools.py`):

| Tool | Purpose |
|------|---------|
| `get_state_data` | Look up specific states, columns, or priority filters |
| `rank_states` | Top/bottom rankings by CRIPI or any indicator |
| `summarize_priority_group` | Explain what states in a priority category share (vs national mean) |
| `get_cluster_profile` | Cluster membership, dimension profile, distinctive indicators |

Separate chat history on the assistant page (`messages_assistant`). See `ai/agent.py` for the two-step tool loop.

## Deploy on Streamlit Community Cloud

1. Push this repository to GitHub (do **not** commit `.env`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and create a new app from the repo.
3. Use these settings:

| Setting | Value |
|---------|--------|
| **Main file path** | `app.py` |
| **Branch** | `main` |

4. Open **Advanced settings → Secrets** and add:

```toml
XAI_API_KEY = "your-xai-api-key"
```

5. Deploy, then verify all four sidebar pages load and one assistant question returns an answer.

**Notes**
- Charts and maps work without the API key; only the **CRIPI Assistant** page needs `XAI_API_KEY`.
- The app has no login — anyone with the URL can use the chat and consume API credits. Share the link only with intended viewers.
- After code changes, redeploy from the Streamlit Cloud dashboard or push to `main` if auto-deploy is enabled.

## Documentation

| Document | Description |
|----------|-------------|
| `documents/project_design.md` | Research question, IPCC framework, methodology |
| `documents/agent_plan.md` | Product plan, wireframes, implementation status |
| `documents/indicator_selection.md` | Indicator rationale and sources |

## Implementation status

- **Phase 1 (AI agent):** Complete — CSV tools, Grok agent, system prompt, schema, glossary
- **Phase A (CRIPI Dashboard):** Complete
- **Phase B (State Clusters):** Complete
- **Phase C (Chat synthesis):** Complete — two-step tool loop, analytical tools, markdown replies
- **Phase D (Polish):** Partial — optional chart-aware context, export, compare-clusters tool
