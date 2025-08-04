import os
import time
from dotenv import load_dotenv
from app.workflow import Workflow

load_dotenv()


def print_intro(): 
    banner = r"""
╔═════════════════════════════════════════════════════════╗
║              Coding Research AI Agent 🤖                ║
╚═════════════════════════════════════════════════════════╝
    """
    
    print(banner)
    print("🔍 Discover • Compare • Analyze Developer Tools")
    print("\nReady to help you find the perfect tools for your project!")
    print("Type your query below or 'help' for assistance.")
    print("-" * 50)


def show_help():
    help_text = """
            📚 HELP - Available Commands:

            🔍 Research Commands:
            • Just type your question naturally
            • "alternatives to [tool name]"
            • "best [category] tools"
            • "free alternatives to [tool]"

            💡 Example Queries:
            • "React alternatives"
            • "databases better than MySQL" 
            • "hosting platforms like AWS"
            • "vector databases for AI apps"

            ⚙️  System Commands:
            • help    - Show this help menu
            • clear   - Clear the screen
            • exit    - Quit the application
            • quit    - Quit the application

            💬 Tips:
            • Be specific about your needs
            • Mention your use case for better recommendations
            • Ask about pricing, features, or integrations
        """
    print(help_text)
    

def main():
    print_intro()
    workflow = Workflow()

    while True:
        query = input("\n❔ Developer Tools Question: ").strip()
        if query.lower() in {"quit", "exit"}:
            print("\n👋 Thanks for using Coding Research AI Agent!")
            break
        elif query.lower() == "help":
            show_help()
            continue
        elif query.lower() == "clear":
            os.system('cls' if os.name == 'nt' else 'clear')
            print_intro()
            continue
        elif query:
            result = workflow.run(query)
            print(f"\n📊 Results for: {query}")
            print("=" * 60)

            for i, company in enumerate(result.companies, 1):
                print(f"\n{i}. 🏢 {company.name}")
                print(f"   🌐 Website: {company.website}")
                print(f"   💰 Pricing: {company.pricing_model}")
                print(f"   📖 Open Source: {company.is_open_source}")

                if company.tech_stack:
                    print(f"   🛠️  Tech Stack: {', '.join(company.tech_stack[:5])}")

                if company.language_support:
                    print(
                        f"   💻 Language Support: {', '.join(company.language_support[:5])}"
                    )

                if company.api_available is not None:
                    api_status = (
                        "✅ Available" if company.api_available else "❌ Not Available"
                    )
                    print(f"   🔌 API: {api_status}")

                if company.integration_capabilities:
                    print(
                        f"   🔗 Integrations: {', '.join(company.integration_capabilities[:4])}"
                    )

                if company.description and company.description != "Analysis failed":
                    print(f"   📝 Description: {company.description}")

                print()

            if result.analysis:
                print("Developer Recommendations: ")
                print("-" * 40)
                print(result.analysis)


if __name__ == "__main__":
    main()