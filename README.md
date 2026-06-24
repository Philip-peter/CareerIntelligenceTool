# Job Switch Intelligence System

A multi-agent research system that helps job applicants make informed career transition decisions by analyzing a prospect company across multiple dimensions and comparing it against their current employer.

---

## What It Does

Given a job posting and a candidate's current employer, the system runs parallel research agents to profile the prospect company, aggregates the findings, and produces a structured recommendation on whether the candidate should proceed with the application or stay.

---

## Agent Pipeline

```
            Input: job_posting + current_employer
                          ⬇️
-------------------------------------------------------------
│                                                           │
│                 Research Agents (Parallel)                │
│  Leadership │ Industry │ Workforce │ Finance │ Direction  │
│                                                           │
-------------------------------------------------------------
                          ⬇️
                      Aggregator
    (groups results by job_id into aggregated_analysis)
                          ⬇️
                    Synthesis Agent
          (scores, flags, compares, recommends)
                          ⬇️
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

## Limitations

- Private companies (e.g., Deloitte, McKinsey) return limited financial data since SEC filings are unavailable. The synthesis agent adjusts confidence level rather than penalizing scores.
- Tavily search results vary in quality depending on how publicly documented a company is. Smaller or less prominent companies may return sparse results across multiple dimensions.
- All research reflects publicly available data only. Internal culture, unreported layoffs, and unannounced strategic decisions are outside the system's visibility.
