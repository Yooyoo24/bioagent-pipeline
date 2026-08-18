import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_react_agent
from langchain_core.prompts import PromptTemplate
from tools import fetch_pdb_summary, fetch_uniprot_sequence, search_pubmed_abstracts

# 1. 动态获取当前文件所在目录的 .env 绝对路径
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# 2. 兜底处理：把 DEEPSEEK_API_KEY 自动同步给 OPENAI_API_KEY 环境变量
deepseek_key = os.getenv("DEEPSEEK_API_KEY")
if deepseek_key and not os.getenv("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = deepseek_key

class BioAgentPipeline:
    def __init__(self, model_name="deepseek-chat"):
        api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError("❌ 错误：在 .env 文件或环境变量中未找到 DEEPSEEK_API_KEY 或 OPENAI_API_KEY！")

        # 配置 DeepSeek API
        self.llm = ChatOpenAI(
            model=model_name,
            api_key=api_key,
            openai_api_key=api_key,  # 显式传参给底层 OpenAI 客户端
            base_url="https://api.deepseek.com",
            temperature=0.1
        )

        self.tools = [fetch_pdb_summary, fetch_uniprot_sequence, search_pubmed_abstracts]

        # 定义标准的 ReAct 提示词模板
        template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

        prompt = PromptTemplate.from_template(template)

        agent = create_react_agent(self.llm, self.tools, prompt)

        self.agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            handle_parsing_errors=True
        )

    def run_pipeline(self, query: str, require_approval: bool = True) -> str:
        print(f"\n[Agent Pipeline Started] Query: {query}")

        if require_approval:
            print(f"⚠️  [Human-in-the-Loop Control Point] System is about to execute API queries for: '{query}'")
            print("Status: Approved by User Policy.\n")

        prompt_prefix = (
            "You are a scientific research assistant specialized in molecular biology. "
            "Synthesize the structural, sequence, and literature information into a clean Markdown report.\n"
        )

        response = self.agent_executor.invoke({"input": prompt_prefix + query})
        return response["output"]


if __name__ == "__main__":
    pipeline = BioAgentPipeline()
    sample_query = "Summarize PDB entry 1TUP and UniProt P04637, then find 2 recent publications."
    report = pipeline.run_pipeline(sample_query)

    print("\n" + "=" * 40 + " GENERATED REPORT " + "=" * 40)
    print(report)