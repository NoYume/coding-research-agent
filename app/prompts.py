class DeveloperToolsPrompts:
    """Collection of prompts for analyzing developer tools and technologies"""

    # Tool extraction prompts
    TOOL_EXTRACTION_SYSTEM = """You are a specialized tech tool extractor. Your job is to identify and extract ONLY specific product/service names from articles.
                                CRITICAL EXTRACTION RULES:
                                - Extract ONLY actual product names, brands, or service names
                                - Do NOT extract descriptions, explanations, or generic terms  
                                - Do NOT extract the original tool being compared against
                                - Focus on tools developers can actually use or implement
                                - Return maximum 5 most relevant tools
                                - If no specific tools found, return "No specific tools found"

                                VALID EXTRACTION EXAMPLES:
                                ✅ "Vercel", "Netlify", "Railway" 
                                ✅ "Claude", "Gemini", "Llama"
                                ✅ "ChromaDB", "Pinecone", "Weaviate"

                                INVALID EXTRACTIONS:
                                ❌ "Based on the content, here are alternatives..."
                                ❌ "AI language models" or "hosting platforms"  
                                ❌ "The article discusses..." or "Note: While..."
                                ❌ Long phrases or sentences"""


    @staticmethod
    def tool_extraction_user(query: str, content: str) -> str:
        query_lower = query.lower()
        
        # Define query categories and their characteristics
        if any(term in query_lower for term in ['vercel', 'netlify', 'hosting', 'deploy', 'railway', 'render', 'cloud']):
            category = "hosting/deployment platforms"
            examples = "Vercel\nNetlify\nRender\nRailway\nFly.io"
            exclude_terms = ["hosting platform", "deployment service", "cloud provider"]
        
        elif any(term in query_lower for term in ['chatgpt', 'llm', 'language model', 'ai model', 'gpt', 'claude']):
            category = "AI language models and LLM services"  
            examples = "Claude\nGemini\nLlama\nMistral\nCopilot"
            exclude_terms = ["AI model", "language model", "chatbot", "ChatGPT"]
        
        elif any(term in query_lower for term in ['database', 'db', 'chroma', 'vector', 'pinecone', 'storage']):
            category = "databases and data storage solutions"
            examples = "ChromaDB\nPinecone\nWeaviate\nQdrant\nMilvus"
            exclude_terms = ["database", "vector database", "storage solution"]
            
        elif any(term in query_lower for term in ['framework', 'library', 'react', 'vue', 'angular']):
            category = "frameworks and libraries"
            examples = "React\nVue.js\nAngular\nSvelte\nNext.js"
            exclude_terms = ["framework", "library", "tool"]
            
        else:
            category = "developer tools, platforms, and services"
            examples = "Tool1\nTool2\nTool3"
            exclude_terms = ["tool", "platform", "service"]
    
    # Build the extraction prompt
        return f"""Query: {query}
                Article Content: {content[:3000]}

                Extract ONLY specific {category} mentioned in this content.

                EXAMPLES OF CORRECT FORMAT:
                {examples}

                STRICT RULES:
                - Return ONLY product names, one per line
                - No descriptions, explanations, or sentences
                - Skip these generic terms: {', '.join(exclude_terms)}
                - Maximum 5 tools
                - One tool name per line
                - No numbering, bullets, or formatting"""


    # Company/Tool analysis prompts
    TOOL_ANALYSIS_SYSTEM = """You are analyzing developer tools and programming technologies. 
                            Focus on extracting information relevant to programmers and software developers. 
                            Pay special attention to programming languages, frameworks, APIs, SDKs, and development workflows."""


    @staticmethod
    def tool_analysis_user(company_name: str, content: str) -> str:
        return f"""Company/Tool: {company_name}
                Website Content: {content[:2500]}

                Analyze this content from a developer's perspective and provide:
                - pricing_model: One of "Free", "Paid", "Enterprise", or "Unknown"
                - is_open_source: true if open source, false if proprietary, null if unclear
                - tech_stack: List of programming languages, frameworks, databases, APIs, or technologies supported/used
                - description: Brief 1-sentence description focusing on what this tool does for developers
                - api_available: true if REST API, GraphQL, SDK, or programmatic access is mentioned
                - language_support: List of programming languages explicitly supported (e.g., Python, JavaScript, Go, etc.)
                - integration_capabilities: List of tools/platforms it integrates with (e.g., GitHub, VS Code, Docker, AWS, etc.)

                Focus on developer-relevant features like APIs, SDKs, language support, integrations, and development workflows."""


    # Recommendation prompts
    RECOMMENDATIONS_SYSTEM = """You are a senior software engineer providing quick, concise tech recommendations. 
                            Keep responses brief and actionable - maximum 3-4 sentences total."""


    @staticmethod
    def recommendations_user(query: str, company_data: str) -> str:
        return f"""Developer Query: {query}
                Tools/Technologies Analyzed: {company_data[:2000]}

                Provide a brief recommendation (3-4 sentences max) covering:
                - Which tool is best and why
                - Key cost/pricing consideration
                - Main technical advantage

                Be concise and direct - no long explanations needed."""