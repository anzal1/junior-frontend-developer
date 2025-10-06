# agents/planner_agent.py
from agents.base_agent import BaseAgent
import json


class PlannerAgent(BaseAgent):
    def __init__(self, template_context=""):
        system_prompt = f"""
You are an expert React developer and project planner. Your job is to create a structured plan based on a user's request and a set of template conventions.

{template_context}
---
Your plan MUST be a JSON object with four keys: `codename`, `npm_dependencies`, `shadcn_dependencies`, and `components`.
- `codename`: A creative, two-word, lowercase, snake_cased project name.
- `npm_dependencies`: A list of any NEW npm packages to install.
- `shadcn_dependencies`: A list of any NEW shadcn-ui components to add.
- `components`: A list of objects for custom components to create. Each component object MUST have:
  - `file_path`: The relative path from src directory (e.g., "components/Header.tsx", "App.tsx")
  - `description`: A clear description of what the component should do

**CRITICAL RULE:** If a UI element is a standard shadcn-ui component, you **MUST** list its name in `shadcn_dependencies`. **DO NOT** add it to `components`.

Your output MUST be ONLY the raw JSON object.
"""
        super().__init__("PlannerAgent", system_prompt)

    def create_plan(self, user_request_with_context):
        plan_str = self.execute(user_request_with_context).get("text", "")
        try:
            clean_str = plan_str.strip().removeprefix(
                "```json").removesuffix("```").strip()
            plan = json.loads(clean_str)

            if isinstance(plan.get("npm_dependencies"), dict):
                plan["npm_dependencies"] = list(
                    plan["npm_dependencies"].values())
            if isinstance(plan.get("shadcn_dependencies"), dict):
                plan["shadcn_dependencies"] = list(
                    plan["shadcn_dependencies"].values())
            if isinstance(plan.get("components"), dict):
                plan["components"] = list(plan["components"].values())

            return plan
        except json.JSONDecodeError:
            print(
                f"--- Planner Agent Failed to produce valid JSON ---\n{plan_str}")
            return None
