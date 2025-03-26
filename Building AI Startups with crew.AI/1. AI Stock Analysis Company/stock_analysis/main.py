import streamlit as st
from crewai import crew
from textwrap import dedent
from stock_analysis_agents import StockAnalysisAgents
from stock_analysis_tasks import StockAnalysisTasks
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

class FinancialCrew:
    def __init__(self, company):
        self.company = company

    def run(self):
        agents = StockAnalysisAgents()
        tasks = StockAnalysisTasks()

        research_analyst_agent = agents.research_analyst()
        financial_analyst_agent = agents.financial_analyst()
        investment_advisor_agent = agents.investment_advisor()

        research_task = tasks.research(research_analyst_agent, self.company)
        financial_task = tasks.financial_analysis(financial_analyst_agent)
        filings_task = tasks.filings_analysis(financial_analyst_agent)
        recommend_task = tasks.recommend(investment_advisor_agent)

        crew = Crew(
            agents=[
                research_analyst_agent,
                financial_analyst_agent,
                investment_advisor_agent
            ],
            tasks=[
                research_task,
                financial_task,
                filings_task,
                recommend_task
            ],
            verbose=True
        )

        result = crew.kickoff()
        return result

def main():
    # Streamlit UI configuration
    st.set_page_config(page_title="Financial Analysis Crew", page_icon="📈")
    st.title("Financial Analysis Crew")
    st.subheader("Analyze any company's financial data")

    # Input form
    with st.form(key='company_form'):
        company = st.text_input("Enter the company name you want to analyze:")
        submit_button = st.form_submit_button(label='Analyze')

    # Process and display results
    if submit_button and company:
        with st.spinner('Analyzing financial data... This may take a moment.'):
            try:
                financial_crew = FinancialCrew(company)
                result = financial_crew.run()
                
                # Display results
                st.success('Analysis Complete!')
                st.markdown("## Analysis Report")
                st.write(result)

                # Option to download report
                st.download_button(
                    label="Download Report",
                    data=result,
                    file_name=f"{company}_financial_report.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

    # Add some footer information
    st.markdown("---")
    st.markdown("Built with ❤️ using Streamlit and CrewAI")

if __name__ == "__main__":
    main()
