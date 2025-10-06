# 🤖 Auto-Running Frontend Agent

An AI-powered system that automatically generates, builds, and runs React applications based on natural language descriptions. The system uses multiple specialized AI agents to plan, create dependencies, and generate components for a complete frontend project.

## 🌟 Features

- **Natural Language to Code**: Describe your UI in plain English and get a working React application
- **Multi-Agent Architecture**: Specialized agents for planning, dependency management, and component creation
- **Template-Based Generation**: Uses Vite + React + shadcn/ui template with TypeScript
- **Automatic Dependency Management**: Installs both npm packages and shadcn/ui components automatically
- **Live Preview**: Automatically starts a development server for immediate preview
- **Modern Tech Stack**: Built with React, TypeScript, Vite, and shadcn/ui

## 🏗️ Architecture

The system consists of several specialized agents:

### Core Agents

- **`PlannerAgent`**: Creates structured project plans from user requests
- **`ComponentAgent`**: Generates React/TSX component code
- **`DependencyAgent`**: Manages npm and shadcn/ui dependency installation
- **`Coordinator`**: Orchestrates the entire build process

### Services & Tools

- **`OpenRouterClient`**: Handles AI model API communication
- **`shell_tools.py`**: Executes shell commands for project setup
- **`file_system_tools.py`**: Handles file creation and management
- **`project_scanner.py`**: Scans and analyzes project structures

## 📋 Prerequisites

- Python 3.8+
- Node.js 16+
- pnpm (Package manager)
- Git

## 🚀 Installation

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd junior-frontend-developer
   ```

2. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:

   ```bash
   OPENROUTER_API_KEY="your-openrouter-api-key-here"
   YOUR_SITE_URL="http://localhost:8501"
   YOUR_SITE_NAME="Frontend Agent Builder"
   ```

4. **Get an OpenRouter API key:**
   - Sign up at [OpenRouter](https://openrouter.ai/)
   - Generate an API key
   - Add it to your `.env` file

## 🎯 Usage

1. **Start the Streamlit application:**

   ```bash
   streamlit run app.py
   ```

2. **Access the web interface:**

   - Open your browser to `http://localhost:8501`

3. **Create your application:**

   - Enter a description of the UI you want to build
   - Provide a base repository URL (default: Vite + React + shadcn/ui template)
   - Click "🚀 Build & Run Frontend"

4. **View your application:**
   - The system will automatically create and start your React application
   - Access it at `http://localhost:5173` once build is complete

## 📁 Project Structure

```
junior-frontend-developer/
├── agents/                 # AI agent implementations
│   ├── __init__.py
│   ├── base_agent.py      # Base agent class with common functionality
│   ├── planner_agent.py   # Creates project plans from descriptions
│   ├── component_agent.py # Generates React components
│   ├── dependency_agent.py# Manages dependencies
│   └── coordinator.py     # Orchestrates the build process
├── services/              # External service integrations
│   ├── __init__.py
│   └── open_router_client.py # OpenRouter API client
├── tools/                 # Utility tools for file and shell operations
│   ├── __init__.py
│   ├── file_system_tools.py
│   ├── project_scanner.py
│   └── shell_tools.py
├── app.py                 # Streamlit web interface
├── config.py             # Configuration management
├── template_context.md   # Template conventions and rules
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (create this)
└── .gitignore           # Git ignore rules
```

## 🔧 Configuration

### Model Configuration

The system uses DeepSeek Chat v3.1 by default. You can change this in `config.py`:

```python
MODEL_NAME = "deepseek/deepseek-chat-v3.1:free"
```

### Generated Project Location

By default, projects are generated in the `generated_frontend_project` directory. Change this in `config.py`:

```python
WORKSPACE_DIR = "your_custom_directory"
```

### Template Conventions

The system follows specific conventions defined in `template_context.md`. These include:

- File structure requirements
- Import conventions
- Component naming patterns
- CSS organization rules

## 🧪 Example Usage

**Input Description:**

```
Create a simple portfolio landing page for a developer named 'Alex Doe'.
It should have a retro, 8-bit theme. Include a header with navigation,
a hero section with a typing animation, a project gallery using cards,
and a simple footer.
```

**Generated Output:**

- Complete React application with TypeScript
- Proper component structure following conventions
- Installed dependencies (animations, UI components)
- Live development server at `http://localhost:5173`

## 🛠️ Development

### Adding New Tools

1. Create a new tool function in the appropriate file under `tools/`
2. Add the tool definition following the OpenAI function calling format
3. Register the tool in `BaseAgent`

### Adding New Agents

1. Extend `BaseAgent`
2. Define specialized system prompts
3. Implement agent-specific methods
4. Register in `Coordinator`

### Template Base Repository

The system uses a Vite + React + shadcn/ui template by default:

- Repository: `https://github.com/dan5py/react-vite-shadcn-ui`
- You can use any compatible React template with Vite and pnpm

## 🔍 How It Works

1. **Planning Phase**: The `PlannerAgent` analyzes your description and creates a structured plan
2. **Dependency Resolution**: The `DependencyAgent` identifies required packages and shadcn/ui components
3. **Component Generation**: The `ComponentAgent` creates React components following template conventions
4. **Build & Run**: The `Coordinator` orchestrates the entire process and starts the dev server

## 📝 Template Requirements

Generated projects must follow these conventions:

- **Global CSS**: Only imported once in `src/main.tsx`
- **Component Structure**: Follows shadcn/ui patterns
- **Path Aliases**: Uses `@/` for src directory imports
- **File Organization**: Components in appropriate subdirectories
- **TypeScript**: Full TypeScript support with proper types

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🐛 Troubleshooting

### Common Issues

1. **API Key Not Working**:

   - Ensure your OpenRouter API key is valid and has sufficient credits
   - Check that the `.env` file is in the project root

2. **Build Failures**:

   - Check that Node.js (16+) and pnpm are properly installed
   - Verify the base repository URL is accessible

3. **Port Conflicts**:

   - Streamlit runs on port 8501
   - Generated React dev server runs on port 5173
   - Ensure these ports are available

4. **Template Errors**:
   - Ensure the base repository URL is a valid Vite + React project
   - Check that pnpm is configured as the package manager

### Debug Information

- Generated project files are created in `generated_frontend_project/`
- Check the Streamlit interface for detailed logs during the build process
- Review the console output for any shell command errors

## 🔮 Future Enhancements

- Support for additional frameworks (Vue, Angular)
- Custom template support
- Advanced component libraries
- Deployment automation
- Version control integration
- Real-time collaboration features

## 📚 Dependencies

### Python Dependencies

- `streamlit`: Web interface framework
- `requests`: HTTP client for API calls
- `python-dotenv`: Environment variable management

### Generated Project Dependencies

- React 18+
- TypeScript
- Vite (build tool)
- shadcn/ui (component library)
- Tailwind CSS (styling)

## 🎨 Supported UI Components

The system can generate applications using shadcn/ui components including:

- Navigation components
- Form elements
- Data display components
- Feedback components
- Layout components
- Typography elements

All components are automatically installed and configured as needed based on your description.
