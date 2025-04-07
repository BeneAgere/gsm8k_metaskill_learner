# Multi-Agent Math Problem Solver with Tool Learning  


## Overview  
This repository demonstrates a multi-agent system that solves grade-school math problems using a collection of “tools.” The system relies on LLM-based agents (via Azure OpenAI or OpenAI) that:  
1. Discover available tools at runtime.  
2. Sequence tool calls to solve math problems (arithmetic, word problems, etc.).  
3. Learn from tool usage results to create new 'virtual tools,' bundling repeated successful tool sequences into a single call for future reuse.  

Notably, some tools silently fail or return incorrect answers 40% of the time, so our multi-agent approach must handle these errors gracefully.  

## Features  
• Multiple Agents: At least two different agents (e.g., planning/solver agent, optimization agent) coordinate tool usage to solve math problems.  
• Tools with Random Failures: Some basic arithmetic tools randomly produce incorrect results, requiring the higher-level agent or coordinator to detect these errors and adapt.  
• Virtual Tool Creation: Whenever the system identifies a successful sequence of tool calls that solves certain types of problems, it bundles these calls into a new “virtual tool.” This new tool can then be quickly invoked the next time a similar problem arises.  
• Automated Evaluations: Demonstrates success on a subset of GSM8k (Grade-School Math) problems, with final accuracy and tool usage statistics displayed in the console.  
• Optional Vector Database of Tools: The system can embed each tool’s description and store them in a simple vector database (VectorDatabase). When a question arrives, the most relevant tools are retrieved and provided to the agent.  

## Repository Structure  
1. tools.py:  
   - Defines an initial set of arithmetic or logic tools (e.g., add, multiply, subtract).  
   - Some of these tools are intentionally unreliable, returning incorrect values part of the time.  
   - Can also define a GET_USER_INPUT tool or a submit_answer tool.  

2. toolshed.py:  
   - Implements a ToolShed class that embeds tool descriptions and stores them in a vector database (VectorDatabase).  
   - retrieve_relevant_tools(...) ranks tools based on semantic similarity to the user’s question.  

3. mathematician_agent.py:  
   - Contains run_math_solver(...), an asynchronous function that orchestrates the conversation with an LLM-based assistant agent, passing relevant tools, capturing tool usage, etc.  

4. gsm8k.py:  
   - Utility file to load the GSM8k dataset (grade-school level math problems). Contains load_gsm8k(...) which returns a list of question/answer pairs.  

5. tool_optimizer_agent.py:  
   - Contains logic for updating tool usage statistics and creating new “virtual tools” from successful tool combinations.  

6. oai_client.py:  
   - Helper functions to create an OpenAI or Azure OpenAI client, specifying the model to be used (text-davinci-003, or any specified model).  
   - Also includes create_embedding_client(...) for embeddings usage.  

7. evaluate_grade_school_math(...) and evaluate_grade_school_math_v2(...):  
   - Evaluate the system by reading GSM8k data, running the solver, collecting stats, and optionally incorporating the vector database or new virtual tools.  

8. main / __main__ block:  
   - Example usage: loads GSM8k data from a JSONL file, runs the solver on multiple questions, and prints correct/total results.  

9. env.yml:  
   - A conda environment specification to set up the correct Python environment for your convenience.  

## Quick Start  
1. Prerequisites:  
   - Conda (Miniconda or Anaconda)  
   - Python 3.8+ (recommended Python 3.10)
   - Git (optional, for cloning the repository)  
   - An API key for Azure OpenAI or OpenAI, if you want to run the system live.  

2. Installation with Conda:  
   1. Clone or download the repository.  
   2. Navigate to the folder containing env.yml.  
   3. Run:  
      conda env create -f env.yml
   4. Activate the environment:  
      conda activate metaskill_learner

3. Setup Environment Variables (If Using Azure OpenAI):  
   - AZURE_OPENAI_API_KEY: Your Azure API key.  
   - AZURE_OPENAI_ENDPOINT: The endpoint URL for your Azure instance.  
   - (Optionally) For standard OpenAI usage, set the OPENAI_API_KEY environment variable.  

4. Run the Evaluation Script:  
   - Make sure the GSM8k data file (train.jsonl) is in the correct path (by default grade-school-math/grade_school_math/data/train.jsonl).  
   - From the project root, run:  
     python orchestrator.py

   - The script:  
     1. Creates or loads clients from oai_client.py.  
     2. Loads the GSM8k dataset via load_gsm8k.  
     3. Calls evaluate_grade_school_math(...) or a variant, which:  
        • Embeds the tools (if using ToolShed + vector DB).  
        • Iterates over math problems, attempts to solve them by sequencing tool calls.  
        • Displays the final pass/fail stats.  

5. Inspect or Modify Tools:  
   - Check out tools.py to see the initial 'arithmetic' tools. Some intentionally fail randomly.  
   - Add or remove tools as needed.  
   - If you want to debug the tool calls, watch the console output or adapt the code in run_math_solver(...) to print more debug logs.  

6. Creating and Using Virtual Tools:  
   - tool_optimizer_agent.py includes logic for bundling repeated successful sequences of tool calls into a new 'virtual tool.'  
   - After enough data is collected on successive calls, these new tools become available in the environment.  

##Known Limitations  
• The random failures in several tools may reduce final accuracy. The aggregator agent or the 'tool optimizer' agent can partially mitigate this, but you may need more sophisticated logic for production readiness.  
• This is a prototype. For large-scale use or complicated math workflows, consider advanced reliability strategies for tool calling.  
• VectorDatabase is a simple, custom prototype. For heavy usage, consider a specialized vector store.