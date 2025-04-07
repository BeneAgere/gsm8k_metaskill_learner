from autogen_agentchat.agents import AssistantAgent
from autogen_core import CancellationToken
from autogen_agentchat.messages import TextMessage, ToolCallRequestEvent, BaseMessage, ToolCallExecutionEvent
import os
import json
from tools import initial_tools

async def eval_single_question(question, client):

    assistant = AssistantAgent(
        name="assistant",
        system_message="You are a helpful assistant.",
        model_client = client,
        tools=initial_tools
    )

    cancellation_token = CancellationToken()
    response = await assistant.on_messages([TextMessage(content=question, source="user")], cancellation_token)
    return response.chat_message.content

async def run_agent(messages, client, tools):
    assistant = AssistantAgent(
        name="assistant",
        model_client = client,
        tools=tools
    )

    cancellation_token = CancellationToken()
    return await assistant.on_messages(messages, cancellation_token)

async def run_math_solver(question, client, tools, max_iterations=10):

      system_message ='''You are an expert math problem solver. You have these tools: (divide, multiply, add, submit_answer, etc.). 
        Follow these rules:
        1. Never finalize with partial results. 
        2. Always do each arithmetic step via the tools. 
        3. When you have the final numeric result, call submit_answer only then.
        If you do not call submit_final_answer, your solution is incomplete and counted as incorrect.'''
      messages: list[BaseMessage] = [
            TextMessage(content=system_message, source="system"),
            TextMessage(content=question, source="user")
        ]

      tools_used = []
      conversation_history = []
      for _ in range(max_iterations):
            try:
                response = await run_agent(messages, client, tools)
                messages.append(response.chat_message)
        
                for inner_msg in response.inner_messages:
                    conversation_history.append(inner_msg)
                    # 3) Check if there's a tool call to "submit_final_answer"
                    if isinstance(inner_msg, ToolCallRequestEvent):
                        for fn_call in inner_msg.content:  # each is a FunctionCall
                            tools_used.append(fn_call.name)
                            fn_args = json.loads(fn_call.arguments)
                            if fn_call.name == "submit_answer":
                                # 4) Parse arguments, immediately return the final answer
                                final_value = fn_args.get("answer", None)
                                return (final_value, tools_used) if final_value is not None else "No answer in submit_final_answer"
                    elif isinstance(inner_msg, ToolCallExecutionEvent):
                                for line in inner_msg.content:
                                    exec_summary = TextMessage(
                                        content=f"[Tool result event] with name: {inner_msg.content[0].name} and result {inner_msg.content[0].content} {line}",
                                        source="assistant"
                                    )
                                    messages.append(exec_summary)
                                    print(exec_summary)
            except Exception as e:
                messages.append(TextMessage(content="Previons execution failed with {}".format(e.with_traceback), source="system"),)

      return ("Unable to finalize an answer.", tools_used)