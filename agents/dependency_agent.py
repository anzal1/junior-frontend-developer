# agents/dependency_agent.py
from agents.base_agent import BaseAgent


class DependencyAgent(BaseAgent):
    def __init__(self):
        system_prompt = """
You are a dependency management expert for a Vite+React project using pnpm.
- You will be given a list of dependencies and told which command to use to install them.
- Group all dependencies into a single command where possible.
- You MUST use the `execute_shell_command` tool to run the installation command.
- For the tool call, you MUST specify the `cwd_override` argument with the project's root path.
"""
        super().__init__("DependencyAgent", system_prompt,
                         tools_list=['execute_shell_command'])

    def install(self, dependencies, project_path, install_command_prompt):
        """
        A generic method to install a list of dependencies.
        """
        prompt = f"""
The project is located at '{project_path}'.
{install_command_prompt}
The dependencies to install are: {', '.join(dependencies)}
"""
        return self.execute(prompt)
