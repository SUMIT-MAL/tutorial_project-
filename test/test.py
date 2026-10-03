from app.service import run_agent
import sys
import os

root_dir = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# 1. Force Python to see the root 'pc_bulider' folder as a lookup directory


async def main(inputs):
    async for chunk in run_agent(user_inputs=inputs):
        if isinstance(chunk, dict) and "model" in chunk:
            messages = chunk["model"].get("messages", [])
            if messages:
                last_msg = messages[-1]
                yield last_msg.content


if __name__ == "__main__":
    import asyncio

    user_input = "I want to build a gaming PC with a budget of $1500. Can you suggest the best components for it?"

    async def test_run_agent():
        async for chunk in main(inputs=user_input):
            print(chunk)

    asyncio.run(test_run_agent())
