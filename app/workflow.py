import re
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, SystemMessage
from .models import ResearchState, CompanyInfo, CompanyAnalysis
from .firecrawl import FirecrawlService
from .prompts import DeveloperToolsPrompts
from .logger import ProgressLogger


class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()
        self.llm = ChatAnthropic(model="claude-3-5-haiku-latest", temperature=0.1)
        self.prompts = DeveloperToolsPrompts()
        self.workflow = self._build_workflow()
        self.logger = ProgressLogger()


    def _build_workflow(self):
        graph = StateGraph(ResearchState)
        graph.add_node("extract_tools", self._extract_tools_step)
        graph.add_node("research", self._research_step)
        graph.add_node("analyze", self._analyze_step)
        graph.set_entry_point("extract_tools")
        graph.add_edge("extract_tools", "research")
        graph.add_edge("research", "analyze")
        graph.add_edge("analyze", END)
        return graph.compile()


    def _extract_tools_step(self, state: ResearchState) -> Dict[str, Any]:
        print(f"🌐 Finding articles about: {state.query}")

        self.logger.start_spinner("Searching for relevant articles...")
        
        try:
            article_query = f"{state.query} tools comparison best alternatives"
            search_results = self.firecrawl.search_companies(article_query, num_results=3)
            self.logger.stop_spinner(f"Found {len(search_results.data)} articles")
        except Exception as e:
            self.logger.stop_spinner("")
            self.logger.log_error("Failed to search articles", e)
            return {"extracted_tools": []}
            
        self.logger.start_spinner("Scraping article content...")
        all_content = ""
        scraped_count = 0
        
        for i, result in enumerate(search_results.data):
            url = result.get("url", "")
            scraped = self.firecrawl.scrape_company_page(url)
            if scraped:
                all_content += scraped.markdown[:1500] + "\n\n"
                scraped_count += 1
            
            self.logger.stop_spinner(f"Scraped {scraped_count} articles ({len(all_content)} characters)")
            
            self.logger.start_spinner("Analyzing content to extract tool names...")

            messages = [
            SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.tool_extraction_user(state.query, all_content))
        ]
        
        try:
            response = self.llm.invoke(messages)
            self.logger.start_spinner("Content analysis complete")
            
            extracted_text = response.content.strip()
            tools = []
            original_query_terms = set(state.query.lower().split())
            
            for line in extracted_text.split("\n"):
                line = line.strip()
                
                if not line:
                    continue
                
                line = re.sub(r'^\d+\.\s*', '', line)
                line = re.sub(r'^[-•]\s*', '', line)
                line = line.strip()
                
                if (line and 
                len(line) <= 50 and
                not line.startswith(('Based on', 'The article', 'Note:', 'Here are', 'These are')) and
                not line.endswith(('alternatives', 'solutions', 'options', 'tools')) and
                not any(skip_word in line.lower() for skip_word in ['alternative', 'vs', 'comparison', 'article']) and
                line.lower() not in [term.lower() for term in original_query_terms]):
                    
                    tools.append(line)
                
            seen = set()
            tools = [tool for tool in tools if not (tool.lower() in seen or seen.add(tool.lower()))]
            
            tools = tools[:5]
            
            if not tools:
                tools = ["No specific tools found"]
            
            self.logger.log_step("⛏️", f"Extracted tools: {', '.join(tools)}")
            return {"extracted_tools": tools}
        
        except Exception as e:
            self.logger.stop_spinner("")
            self.logger.log_error("Failed to extract tools", e)
            return {"extracted_tools": []}


    def _analyze_company_content(self, company_name: str, content: str) -> CompanyAnalysis:
        structured_llm = self.llm.with_structured_output(CompanyAnalysis)
        
        messages = [
            SystemMessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.tool_analysis_user(company_name, content))
        ]

        try:
            analysis = structured_llm.invoke(messages)
            return analysis
        except Exception as e:
            print(f"Error: {e}")
            return CompanyAnalysis(
                pricing_model="Unknown",
                is_open_source=None,
                tech_stack=[],
                description="Failed",
                api_available=None,
                language_support=[],
                integration_capabilities=[],
            )


    def _research_step(self, state: ResearchState) -> Dict[str, Any]:
        extracted_tools = getattr(state, "extracted_tools", [])
        
        if not extracted_tools:
            self.logger.log_warning("No extracted tools found, using direct search")
            search_results = self.firecrawl.search_companies(state.query, num_results=4)
            tool_names = [
                result.get("metadata", {}).get("title", "Unknown")
                for result in search_results.data
            ]
        else:
            tool_names = extracted_tools[:4]

        self.logger.log_step("🔬", f"Researching {len(tool_names)} specific tools...")
        
        companies = []
        for i, tool_name in enumerate(tool_names):
            self.logger.start_spinner(f"Researching {tool_name} ({i+1}/{len(tool_names)})...")
            
            try:
                tool_search_results = self.firecrawl.search_companies(tool_name + " official site", num_results=1)

                if tool_search_results:
                    result = tool_search_results.data[0]
                    url = result.get("url", "")

                    company = CompanyInfo(
                        name=tool_name,
                        description=result.get("markdown", ""),
                        website=url,
                        tech_stack=[],
                        competitors=[]
                    )

                    scraped = self.firecrawl.scrape_company_page(url)
                    if scraped:
                        content = scraped.markdown
                        analysis = self._analyze_company_content(company.name, content)
                        
                        company.pricing_model = analysis.pricing_model
                        company.is_open_source = analysis.is_open_source
                        company.tech_stack = analysis.tech_stack
                        company.description = analysis.description
                        company.api_available = analysis.api_available 
                        company.language_support = analysis.language_support
                        company.integration_capabilities = analysis.integration_capabilities
                
                    companies.append(company)
                    self.logger.stop_spinner(f"{tool_name} research complete")
                else:
                    self.logger.stop_spinner("")
                    self.logger.log_warning(f"No results found for {tool_name}")
            
            except Exception as e:
                self.logger.stop_spinner("")
                self.logger.log_error(f"Failed to research {tool_name}", e)

        self.logger.log_substep(f"Successfully researched {len(companies)} tools")        
        return {"companies": companies}
    
    
    def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
        self.logger.start_spinner("Generating personalized recommendations...")
        
        try:
            company_data = ", ".join([
                company.json() for company in state.companies[:4]
            ])
        
            messages = [
                SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
                HumanMessage(content=self.prompts.recommendations_user(state.query, company_data))
            ]
            
            response = self.llm.invoke(messages)
            analysis_content = response.content[:1000]
            
            last_period = analysis_content.rfind(".")
            if last_period > 500:
                analysis_content = analysis_content[:last_period + 1]
                
            self.logger.stop_spinner("Recommendations generated")
            self.logger.log_step("🕗", "Analysis complete")
            return {"analysis": response.content}
        
        except Exception as e:
            self.logger.stop_spinner("")
            self.logger.log_error("Failed to generate recommendations", e)
            return {"analysis": "Unable to generate recommendations in given time"}
    
    
    def run(self, query: str) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = self.workflow.invoke(initial_state)
        return ResearchState(**final_state)