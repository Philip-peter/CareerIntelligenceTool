import asyncio

from src import agent


async def main():
    # initialize agent
    my_agent = agent.Workflow()

    # run agent
    research = await my_agent.run()

    print(research["job_queue"])


if __name__ == "__main__":
    asyncio.run(main())
