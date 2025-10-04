# agents/base_agent.py
import json
from services.open_router_client import OpenRouterClient
import tools.file_system_tools as fs_tools
import tools.shell_tools as shell_tools


class BaseAgent:
    def __init__(self, name, system_prompt, tools_list=None):
        self.name = name
        self.system_prompt = system_prompt
        self.client = OpenRouterClient()
        self.available_tools = {}
        self.tool_definitions = []

        if tools_list:
            for tool_name in tools_list:
                if tool_name == 'write_react_component':
                    self.available_tools['write_react_component'] = fs_tools.write_react_component
                    self.tool_definitions.append(
                        fs_tools.write_react_component_tool_def)
                elif tool_name == 'execute_shell_command':
                    self.available_tools['execute_shell_command'] = shell_tools.execute_shell_command
                    self.tool_definitions.append(
                        shell_tools.execute_shell_tool_def)

    def execute(self, user_prompt):
        history = [{"role": "system", "content": self.system_prompt}, {
            "role": "user", "content": user_prompt}]
        response = self.client.create_chat_completion(
            messages=history, tools=self.tool_definitions if self.tool_definitions else None
        )

        if not response or not response.get('choices'):
            return {"text": "Agent failed to get a valid response from the API."}

        response_message = response['choices'][0]['message']
        tool_calls = response_message.get("tool_calls")

        if not tool_calls:
            return {"text": response_message.get("content")}

        tool_results = []
        for tool_call in tool_calls:
            tool_name = tool_call['function']['name']
            tool_function = self.available_tools.get(tool_name)
            if not tool_function:
                tool_results.append(
                    {"output": f"Error: Tool '{tool_name}' not found."})
                continue
            try:
                tool_args = json.loads(tool_call['function']['arguments'])
                tool_output = tool_function(**tool_args)
                tool_results.append({"output": tool_output})
            except Exception as e:
                tool_results.append({"output": f"Error executing tool: {e}"})

        return {"tool_results": tool_results}
