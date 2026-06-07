from . import llm_summarizer, tavily

# initialize tavily web search tool
web_research_tool = tavily.TavilyResearchTool()

# initialize llm summarizer tool
llm_analyzer_tool = llm_summarizer.LlmSummarizer()
