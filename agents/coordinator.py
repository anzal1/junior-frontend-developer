# agents/coordinator.py
from collections import deque
from agents.planner_agent import PlannerAgent
from agents.component_agent import ComponentAgent
from agents.dependency_agent import DependencyAgent
import tools.shell_tools as shell
from tools.project_scanner import read_directory_structure
import os
import shutil
import subprocess
import atexit
import json

# ... load_template_context() function is unchanged ...


def load_template_context():
    try:
        with open("template_context.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print("Warning: template_context.md not found.")
        return ""


class Coordinator:
    # ... __init__, _cleanup_dev_server, log methods, _create_tsconfig are unchanged ...
    def __init__(self, streamlit_ui=None):
        template_context = load_template_context()
        self.planner = PlannerAgent(template_context=template_context)
        self.component_agent = ComponentAgent(
            template_context=template_context)
        self.dependency_agent = DependencyAgent()
        self.st = streamlit_ui
        self.task_queue = deque()
        self.project_path = ""
        self.dev_server_process = None
        atexit.register(self._cleanup_dev_server)

    def _cleanup_dev_server(self):
        if self.dev_server_process:
            self.log("Shutting down the Vite dev server.")
            self.dev_server_process.terminate()

    def log(self, message): print(message); self.st.info(message)
    def log_success(self, message): print(message); self.st.success(message)
    def log_error(self, message): print(message); self.st.error(message)

    def _create_tsconfig(self, project_path):
        tsconfig_content = {"compilerOptions": {"target": "ES2020", "useDefineForClassFields": True, "lib": ["ES2020", "DOM", "DOM.Iterable"], "module": "ESNext", "skipLibCheck": True, "moduleResolution": "bundler", "allowImportingTsExtensions": True, "resolveJsonModule": True,
                                                "isolatedModules": True, "noEmit": True, "jsx": "react-jsx", "strict": True, "noUnusedLocals": True, "noUnusedParameters": True, "noFallthroughCasesInSwitch": True, "baseUrl": ".", "paths": {"@/*": ["./src/*"]}}, "include": ["src"], "references": [{"path": "./tsconfig.node.json"}]}
        try:
            with open(os.path.join(project_path, "tsconfig.json"), "w") as f:
                json.dump(tsconfig_content, f, indent=2)
            self.log_success(
                "Successfully created tsconfig.json for path aliases.")
            return True
        except Exception as e:
            self.log_error(f"Failed to create tsconfig.json: {e}")
            return False

    def run_frontend_build(self, user_request, base_repo_url):
        self.log("Step 1: Creating a high-level plan...")
        initial_context = f'User\'s Request: "{user_request}"\n\n(This is a new project.)'
        plan = self.planner.create_plan(initial_context)

        if not plan or not all(k in plan for k in ["codename", "components"]):
            self.log_error("Failed to create a valid plan.")
            self.st.json(plan or {"error": "No plan returned."})
            return

        self.project_path = plan.get("codename", "generated_project")
        self.st.success(
            f"Plan created! Project codename: '{self.project_path}'")
        self.st.json(plan)

        if not self.initialize_project(base_repo_url):
            return

        if plan.get("npm_dependencies"):
            self.task_queue.append(
                {"type": "npm_dependencies", "payload": plan["npm_dependencies"]})
        if plan.get("shadcn_dependencies"):
            self.task_queue.append(
                {"type": "shadcn_dependencies", "payload": plan["shadcn_dependencies"]})
        if plan.get("components"):
            for component in plan["components"]:
                self.task_queue.append(
                    {"type": "component", "payload": component})

        self.process_task_queue()
        self.finalize_and_run_project()

    def initialize_project(self, base_repo_url):
        self.log(f"Step 2: Initializing project '{self.project_path}'...")
        if os.path.exists(self.project_path):
            shutil.rmtree(self.project_path)
        os.makedirs(self.project_path)
        if "Error" in shell.execute_shell_command(f"git clone {base_repo_url} .", cwd_override=self.project_path):
            self.log_error("Failed to clone base repo.")
            return False
        if not self._create_tsconfig(self.project_path):
            return False
        if "Error" in shell.execute_shell_command("pnpm install", cwd_override=self.project_path):
            self.log_error("Failed to install base dependencies.")
            return False
        self.log_success("Project initialized successfully.")
        return True

    def process_task_queue(self):
        self.log("Step 3: Processing task queue...")
        while self.task_queue:
            task = self.task_queue.popleft()

            with self.st.expander(f"Task: {task['type']}", expanded=True):
                # --- START: FIX ---
                if task["type"] == "npm_dependencies":
                    prompt = "Please install the following npm packages by creating a single `pnpm add` command."
                    result = self.dependency_agent.install(
                        task["payload"], self.project_path, prompt)
                    if result.get("tool_results"):
                        [self.st.code(res["output"], language="bash")
                         for res in result["tool_results"]]
                    self.log_success("Finished NPM installation.")

                elif task["type"] == "shadcn_dependencies":
                    prompt = "Please add the following shadcn-ui components by creating a single `pnpm dlx shadcn-ui@latest add ... --y --overwrite` command."
                    result = self.dependency_agent.install(
                        task["payload"], self.project_path, prompt)
                    if result.get("tool_results"):
                        [self.st.code(res["output"], language="bash")
                         for res in result["tool_results"]]
                    self.log_success("Finished ShadCN installation.")
                # --- END: FIX ---

                elif task["type"] == "component":
                    component_name = task['payload'].get('file_path', 'Unknown Component')
                    if not task['payload'].get('file_path'):
                        self.log_error(f"Component missing file_path: {task['payload']}")
                        continue
                    
                    self.st.write(f"Creating Component: {component_name}")
                    result = self.component_agent.create_component(
                        task["payload"], self.project_path)
                    if result.get("tool_results"):
                        [self.log_success(res["output"])
                         for res in result["tool_results"]]
                    else:
                        self.log_error(
                            f"Component agent failed for {task['payload'].get('file_path')}")
        self.log_success("✅ All components created!")

    def finalize_and_run_project(self):
        self.log("Step 4: Starting the Vite dev server...")
        try:
            self.dev_server_process = subprocess.Popen(["pnpm", "run", "dev"], cwd=self.project_path,
                                                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            self.log_success("Vite dev server is starting...")
            self.st.balloons()
            self.st.markdown(
                f"🎉 **Build Complete!** Your project **'{self.project_path}'** is running. [**Click here to preview**](http://localhost:5173)")
        except Exception as e:
            self.log_error(f"Failed to start dev server: {e}")
