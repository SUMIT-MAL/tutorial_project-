from langchain.agents import create_agent
from langgraph.graph.state import CompiledStateGraph
from langchain_groq.chat_models import ChatGroq
from app.src.excutable_fuction import tool_excute_internet_search
from app.utils import AiErrorHandeler
from langchain_community.tools import DuckDuckGoSearchRun
from loguru import logger
from langgraph.prebuilt import ToolNode
from app.config import seetings_manager


class AiAgentManger:
    def __init__(self):
        """
        Initializes the AiAgentManger class.
        This class is responsible for managing the AI agent that interacts with the PcPartsPicker tool.
        """

        self.logger = logger
        self.llm = ChatGroq(
            model=seetings_manager.model_agent,
            temperature=0.0,  # Set this to 0 for strict, deterministic tool execution
            api_key=seetings_manager.GROQ_API_KEY,
            max_tokens=500
        )
        agent_tools = [DuckDuckGoSearchRun()]

        # 2. Instantiate ToolNode with fallback exception mapping enabled
        tool_node = ToolNode(
            tools=agent_tools,
            # 💡 Automatically transforms errors into text instead of crashing!
            handle_tool_errors=True
        )

        structured_system_prompt = """You are an expert PC Builder Agent.
                Find the user's dream PC builds based on what they want.

                You MUST present the final response in this exact format structure:
                - image
                - amazon shopping link
                - description
                - and more information

                CRITICAL RULE: When you need to use a tool, rely entirely on the native tool-calling parameter engine framework.
                NEVER output raw XML string markup tags like '<tool_call>' or '<function>' in your text thoughts. Only provide clean text responses or valid function executions.
                """
        self.agent_object: CompiledStateGraph = create_agent(
            model=self.llm,
            tools=agent_tools,
            system_prompt=structured_system_prompt,
            debug=True
        )
        self.logger.warning(
            "debug is true agent corrently running in developement mode")

    async def run_agent(self, user_input: str):
        """
        Runs the AI agent with the provided user input.

        """
        try:
            async for chunkes in self.agent_object.astream(
                {"messages": [("user", user_input)]},
                version="v3",
                stream_mode="updates"
            ):
                if chunkes:
                    self.logger.info(
                        "checkig if client giving a string value")
                    yield chunkes

        except Exception as error:
            self.logger.error(f"Error in run_agent: {error}")
            raise AiErrorHandeler(error)
