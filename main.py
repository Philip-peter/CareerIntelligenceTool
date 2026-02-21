import asyncio

from src import agent


async def main():
    # initialize agent
    my_agent = agent.Workflow()

    while True:
        # get target company
        target_company = input("TARGET COMPANY: ")

        # run agent
        await my_agent.run(target_company=target_company)


if __name__ == "__main__":
    asyncio.run(main())
