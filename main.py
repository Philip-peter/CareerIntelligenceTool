import warnings

warnings.filterwarnings(
    "ignore", message="PydanticSerializationUnexpectedValue", category=UserWarning
)

import asyncio  # noqa: E402

from src import agent  # noqa: E402


async def main():
    # initialize agent
    my_agent = agent.Workflow()

    # run agent
    research = await my_agent.run()

    print(research["final_report"])


if __name__ == "__main__":
    asyncio.run(main())
