# agents/component_agent.py
from agents.base_agent import BaseAgent


class ComponentAgent(BaseAgent):
    def __init__(self, template_context=""):
        system_prompt = f"""
You are a senior React developer AI that writes clean, modern TSX code. You MUST follow the template conventions provided below.

{template_context}
---
- Your task is to write the full code for a single React component.
- You MUST use the `write_react_component` tool to output the code.
- Your ONLY output must be a call to the `write_react_component` tool.
"""
        super().__init__("ComponentAgent", system_prompt,
                         tools_list=['write_react_component'])

    def create_component(self, component_task, project_path):
        description = component_task.get(
            'description', f"Create a component for {component_task.get('file_path', 'unknown')}.")
        prompt = f"""
The project is located at '{project_path}'.
Create the React component as described below, following all template conventions.

File Path: {component_task.get('file_path')}
Description: {description}

Write the complete code and use the `write_react_component` tool to save it.
"""
        return self.execute(prompt)
