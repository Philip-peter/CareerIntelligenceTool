# Job Switch Intelligence System

A multi-agent research system that helps job applicants make informed career transition decisions by analyzing a prospect company across five dimensions and comparing it against their current employer.

---

## What It Does

Given a job posting and a candidate's current employer, the system runs parallel research agents to profile the prospect company, aggregates the findings, and produces a structured recommendation on whether the candidate should proceed with the application or stay.

---

## Project Structure

```
project/
├── agents/                     # Thin orchestration logic per agent
│   ├── leadership_agent.py
│   ├── industry_agent.py
│   ├── workforce_agent.py
│   ├── finance_agent.py
│   ├── direction_agent.py
│   ├── synthesis_agent.py
│   └── aggregator.py
│
├── prompts/                    # System and user prompt builders
│   ├── leadership_prompts.py
│   ├── industry_prompts.py
│   ├── workforce_prompts.py
│   ├── finance_prompts.py
│   ├── direction_prompts.py
│   └── synthesis_prompts.py
│
├── queries/                    # Tavily search query builders
│   ├── leadership_queries.py
│   ├── industry_queries.py
│   ├── workforce_queries.py
│   ├── finance_queries.py
│   └── direction_queries.py
│
├── models/                     # Pydantic output schemas
│   ├── leadership_models.py    # LeadershipContextModels
│   ├── industry_models.py      # IndustryContextModels
│   ├── workforce_models.py     # WorkforceContextModels
│   ├── finance_models.py       # FinancialContextModels
│   ├── direction_models.py     # CompanyDirectionModels
│   └── synthesis_models.py     # JobSwitchRecommendation
│
├── tools/                      # Module-level tool singletons
│   ├── tavily_tool.py
│   └── llm_tool.py
│
├── graph.py                    # LangGraph wiring and state definition
├── state.py                    # State TypedDict
└── main.py                     # Entry point
```

---

## Agent Pipeline

```
Input: job_posting + current_employer
        │
        ▼
┌───────────────────────────────────────────────────┐
│              Research Agents (Parallel)            │
│  Leadership │ Industry │ Workforce │ Finance │ Direction │
└───────────────────────────────────────────────────┘
        │
        ▼
   Aggregator
   (groups results by job_id into aggregated_analysis)
        │
        ▼
   Synthesis Agent
   (scores, flags, compares, recommends)
        │
        ▼
Output: JobSwitchRecommendation
```

---

## Research Dimensions

| Agent | What It Researches |
|---|---|
| **Leadership** | CEO tenure, founder involvement, executive reputation, management style, DEI, employee development |
| **Industry** | Cyclicality, regulatory environment, AI disruption, competition, growth trajectory, M&A and offshoring risk |
| **Workforce** | Layoff history, hiring trends, employee sentiment, compensation, remote policy, retention signals |
| **Finance** | Revenue growth, profitability, debt, cash flow, investor sentiment, funding runway, distress signals |
| **Direction** | Earnings call guidance, CEO strategic narrative, M&A activity, hiring signals, product roadmap, expansion plans |

---

## Synthesis Output

The synthesis agent produces a `JobSwitchRecommendation` containing:

- **Category Scorecards** — 1–10 scores per dimension for both prospect and current employer
- **Red Flags** — top 3–5 material employment risks at the prospect company
- **Watch Items** — 2–3 findings requiring further due diligence
- **Green Flags** — top 3–5 strongest positive signals
- **Head-to-Head Summary** — narrative comparison of both employers
- **Recommendation** — one of: `Strong Proceed`, `Lean Proceed`, `Lean Stay`, `Strong Stay`
- **Confidence Level** — `High`, `Medium`, or `Low` based on data completeness
- **Deciding Factor** — the single finding that tips the recommendation

---

## Setup

### Prerequisites
- Python 3.11+
- [Tavily API key](https://tavily.com)
- [Anthropic API key](https://console.anthropic.com)

### Installation

```bash
git clone https://github.com/your-org/job-switch-intelligence.git
cd job-switch-intelligence
pip install -r requirements.txt
```

### Environment Variables

```bash
cp .env.example .env
```

```env
ANTHROPIC_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
```

### Run

```bash
python main.py
```

---

## Key Design Decisions

**Module-level tool singletons** — `tavily_tool` and `llm_tool` are instantiated once at the module level and imported by reference across all agents. Python's module system guarantees a single initialization per process regardless of how many agents import them.

**Prompts and queries separated from agents** — each agent module contains only orchestration logic (~30–40 lines). Prompts, query builders, and Pydantic models live in their own focused modules and can be edited, versioned, and tested independently.

**`RunnableConfig` used correctly** — config carries only per-invocation context (`thread_id`, `job_id`, `candidate_id`), callbacks for tracing, and graph execution limits. Tools and shared configuration are injected at construction, not passed through config.

**Data absence treated as a signal** — the synthesis agent distinguishes between missing data caused by research failure and missing data caused by a private company's limited disclosure. Scores are not penalized for private company data gaps; confidence level is adjusted instead.

---

## Limitations

- Private companies (e.g., Deloitte, McKinsey) return limited financial data since SEC filings are unavailable. The synthesis agent adjusts confidence level rather than penalizing scores.
- Tavily search results vary in quality depending on how publicly documented a company is. Smaller or less prominent companies may return sparse results across multiple dimensions.
- All research reflects publicly available data only. Internal culture, unreported layoffs, and unannounced strategic decisions are outside the system's visibility.
