import asyncio

from src import agent
from src.nodes.job_listing.theirstack import theirstack_provider


async def main():
    # initialize agent
    my_agent = agent.Workflow()

    # Test their stack job listing
    job_listing = theirstack_provider.fetch_jobs()
    print(job_listing)

    while True:
        job_link = input("JOB LINK: ")
        target_company = input("TARGET COMPANY: ")

        # run agent
        research = await my_agent.run(
            job_link=job_link,
            target_company=target_company,
            # current_company=current_company,
            # currently_employed=currently_employed,
            # current_role=current_role,
            # current_job_tenure=current_job_tenure,
            # risk_tolerance=risk_tolerance,
            # career_stage=career_stage,
            # career_priority=career_priority,
        )

        print(research["final_report"])


if __name__ == "__main__":
    asyncio.run(main())
