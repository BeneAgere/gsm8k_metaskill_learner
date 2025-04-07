import random
import math
import os
import time
import json
import re
import asyncio

from mathematician_agent import run_math_solver
from gsm8k import load_gsm8k
from tools import initial_tools, submit_answer
from oai_client import create_open_ai_client, create_embedding_client, chat_completion_model
from toolshed import ToolShed
from tool_optimizer_agent import maybe_create_virtual_tools_from_pairs, update_tool_stats, create_two_step_virtual_tool


async def evaluate_grade_school_math(questions_data, client, use_virtual_tools = False, use_vector_db=False, verbose=True):
    """
    Loads math data from 'filepath' and then processes each question 
    using the run_math_solver routine.
    Compares the agent’s numeric result with official numeric, 
    tracks stats, and prints them.
    """
    correct = 0
    total = 0
    tool_stats, pair_stats = {}, {}
    virtual_tools = []
    tool_shed = ToolShed(create_embedding_client(), initial_tools)
    
    if not questions_data:
        return

    for question, official_answer_str, official_numeric in questions_data:
        
        if use_vector_db:
            tools = tool_shed.retrieve_relevant_tools(question, top_k=10)
        else:
            tools = initial_tools
            if use_virtual_tools:
                tools += virtual_tools


        tools = initial_tools + [submit_answer]
        agent_answer, tools_used = await run_math_solver(question, client, tools)

        try:
            agent_float = float(agent_answer)
        except (ValueError, TypeError):
            agent_float = None

        total += 1
        was_successful = False
        if official_numeric is not None and agent_float is not None:
            if abs(agent_float - official_numeric) < 1e-3:
                correct += 1
                outcome = "PASS"
                was_successful = True
            else:
                outcome = "FAIL"
        else:
            outcome = "NO_ANSWER"
        
        tool_stats, pair_stats = update_tool_stats(tool_stats, pair_stats, tools_used, was_successful)

        if use_virtual_tools:
            new_virtual_tools = maybe_create_virtual_tools_from_pairs(pair_stats, tools, client, chat_completion_model)
            for new_virtual_tool in new_virtual_tools:
                tool_shed.add_tool(new_virtual_tool)
                virtual_tools.append(new_virtual_tool)

        if verbose:
            print(f"Q: {question}")
            print(f"Agent: {agent_answer} | Official: {official_numeric} -> {outcome}\n")

    if total > 0:
        print(f"Final Score: {correct}/{total}  ({correct*100.0/total:.2f}%)")
    else:
        print("No questions processed.")

if __name__ == "__main__":
    client = create_open_ai_client(aad_auth=False)
    filepath = "grade-school-math/grade_school_math/data/train.jsonl"
    questions_data = list(load_gsm8k(filepath, n=100))
    asyncio.run(evaluate_grade_school_math(questions_data, client))
