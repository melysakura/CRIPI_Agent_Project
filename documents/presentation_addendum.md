# Presentation addendum — agent upgrade (post-presentation)

**Full slide copy (updated for 4 tools):** see [`documents/presentation.md`](presentation.md), especially **Slide 3** and the **Chat demo** section.

If you already delivered your bootcamp presentation, only **Slide 3 (How the agent works)** and the **demo chat section** need minor updates. App structure (Slide 2) is unchanged.

## What changed after the presentation

### Before
- Agent called a tool once and stopped
- Chat showed a **Streamlit table** (similar to dashboard charts) plus a short line like *"Retrieved data for 6 states"*
- Only **2 tools**: `get_state_data`, `rank_states`
- No structured analysis or recommendations in the reply

### After (current)
- **Two-step loop** in `ai/agent.py`: tool → JSON → Grok writes a **full text answer**
- Tools return **JSON only** (no duplicate charts in chat)
- **4 tools**: added `summarize_priority_group`, `get_cluster_profile`
- System prompt asks for **interpretation** and **2–4 data-grounded recommendations**
- Chat renders **markdown** (bullets, small tables inside the message)

## Updated talking points (Slide 3)

**Old line:** *"The agent often returns a table confirmation; full synthesis is planned."*

**New line:** *"When the user asks an analytical question, Grok calls a tool to pull real data from our CSV, then writes a second response that explains patterns and suggests practical interventions — for example, why Very High Priority states share high sensitivity and low adaptive capacity."*

**Updated tool table (say "four tools"):**

| Tool | Plain English |
|------|----------------|
| `get_state_data` | Look up specific states or filters |
| `rank_states` | Top/bottom rankings |
| `summarize_priority_group` | Why states in a priority group are similar |
| `get_cluster_profile` | What defines a K-Means cluster (membership + profile) |

**Updated flow (one sentence):** User question → Grok picks a tool → Python returns JSON → Grok synthesizes analysis + recommendations → markdown in chat.

## Demo script adjustment (~1 min chat)

Replace showing a bare table with:

1. **Dashboard:** *"Why are Very High Priority states similar?"*  
   — Expect a paragraph on shared dimensions/indicators plus recommendation bullets.

2. **Clusters:** *"What makes Cluster 1 distinctive?"*  
   — Expect use of `get_cluster_profile` and mention of Chiapas, Guerrero, Oaxaca.

**Timing note:** Each analytical question may take **5–10 seconds** (two API calls). Mention that briefly if the audience waits.

## What you do NOT need to redo

- Slide 1 (problem / solution)
- Slide 2 (app structure, three pages, components)
- Slide 4 (Cursor learnings) — optional add: *"Iterated agent from table-only to two-step synthesis"*
- Live walkthrough of KPIs, map, profiles, clusters (unchanged)

## Files touched by the agent upgrade

- `ai/agent.py` — two-step loop
- `ai/tools.py` — four tools, JSON output
- `ai/prompts.py` — synthesis and recommendation rules
- `components/chat_panel.py` — markdown replies
- `pages/1_CRIPI_Dashboard.py` / `pages/2_State_Clusters.py` — new suggested prompts, session version `v8`
