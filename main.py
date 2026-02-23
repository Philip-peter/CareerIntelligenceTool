import asyncio

from src import agent
from src.state import State


async def main():
    # initialize agent
    my_agent = agent.Workflow()

    while True:
        # get target company
        target_company = input("TARGET COMPANY: ")
        current_company = input("CURRENT COMPANY: ")
        currently_employed = input("CURRENTLY EMPLOYED: ")
        current_role = input("CURRENT ROLE: ")
        current_job_tenure = input("CURRENT JOB TENURE: ")
        risk_tolerance = int(input("RISK TOLERANCE: "))
        career_stage = input("CAREER STAGE: ")
        career_priority = input("CAREER PRIORITY: ")

        # run agent
        research = await my_agent.run(
            target_company=target_company,
            current_company=current_company,
            currently_employed=currently_employed,
            current_role=current_role,
            current_job_tenure=current_job_tenure,
            risk_tolerance=risk_tolerance,
            career_stage=career_stage,
            career_priority=career_priority,
        )

        print(research["industry_research"])


if __name__ == "__main__":
    asyncio.run(main())
