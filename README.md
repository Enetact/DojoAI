README.md
 DojoAI is a local AI workbench for building, chaining, and running custom tool-augmented LLM agents. It
 allows you to design sophisticated multi-agent workflows that automate complex tasks by combining
 large language models (LLMs) with specialized tools – all within your local environment. By leveraging
 DojoAI, you maintain privacy (your data stays local) and gain flexibility in customizing how agents and tools
 interact.
 Key Features
 • 
• 
• 
• 
Build & Chain Custom Agents: Define agents by selecting an LLM, crafting a system prompt
 (persona or goal), and assigning specific tools. Orchestrate sequences of these custom agents to
 handle complex, multi-step tasks. This enables modular AI behaviors where each agent specializes in
 a sub-task.
 Dynamic Tool Integration (MCP): Extend agents with tools via the Model Context Protocol (MCP).
 You can connect any command-line tool or external service by specifying how to invoke it (command,
 arguments, environment). Agents can then use these tools during execution, allowing them to
 interact with files, databases, APIs, or other systems as part of their reasoning.
 Interactive LLM Chat Interface: DojoAI provides a chat interface to converse with your agents.
 Agents leverage their assigned LLMs to understand queries and can call on configured tools to fetch
 information or take actions in real-time. You can chat with a single agent or even a chain of agents
 working together.
 Local and Extensible: The entire system runs on your machine, ensuring data privacy and low
latency responses. You can deeply customize agent behaviors, add new tools, or integrate additional
 AI models. The architecture is extensible – developers can plug in new tool adapters or support for
 other AI providers with ease.
 Project Overview
 DojoAI is organized as a Turborepo monorepo with a front-end and back-end: - Front-End: A Next.js-based
 web application (React) that provides the user interface for configuring agents, tools, and workflows, as well
 as a real-time chat UI. - Back-End: A Node.js server (integrated with the Next.js API routes) that manages
 agent execution, tool processes, and data persistence. It acts as the MCP server, orchestrating
 communication between LLMs and tools. - Shared Packages: Common libraries for agent logic, tool
 integration, database access, and AI model integrations are kept in reusable packages. This modular design
 promotes maintainability and reuse.
 (See the 
developer_guide.md for a detailed breakdown of the project structure and modules.)
 1
Quick Start
 Follow these steps to quickly get DojoAI up and running:
 1. 
2. 
3. 
4. 
5. 
6. 
7. 
8. 
Clone the Repository: Download the DojoAI code from GitHub and navigate into the project
 directory.
 Set Up Environment Variables: Copy the file 
.env.example to 
.env in the project root. Open
 .env and provide the required API keys and settings (e.g. OpenAI API key, etc.). At minimum, set
 an OpenAI API key so you have an LLM to work with – any AI model without a configured key will be
 disabled in the app.
 Install Dependencies: Ensure you have Node.js 18+ (or Bun runtime) installed. Then install
 packages:
 Using Bun: run 
bun install in the repository root.
 Using npm: run 
npm install (or 
yarn install ) in the repository root.
 Launch Supporting Services: DojoAI uses a SQLite database (local file) and optionally a Chroma
 vector database for embeddings. If you plan to use the vector memory features, start a ChromaDB
 server (see Setup guide). The easiest way is via Docker: for example, 
docker run -p 8000:8000 
ghcr.io/chroma-core/chroma:latest to run Chroma on port 8000.
 Run DojoAI: Start the development server for the app:
 If using Docker Compose (recommended for quick start): simply run 
9. 
10. 
docker-compose up in the
 project directory. This will build and start the DojoAI web app and a ChromaDB service together.
 If running locally without Docker: use the Turborepo scripts. For example, 
npm run dev (or 
bun 
run dev ) will start the front-end (and back-end) concurrently. By default the web interface will be
 available at http://localhost:3000 (unless otherwise noted in console output).
 Open the App: Once the server is running, open your browser to the DojoAI interface (e.g., 
http://localhost:3000 ). You should see the DojoAI dashboard. From here you can begin
 connecting tools, creating agents, and building workflows.
 (For full installation details, see 
common solutions.)
 Basic Usage
 • 
setup.md. If you encounter issues starting the app, consult 
troubleshooting.md for
 Configure Tools: In the DojoAI dashboard, begin by configuring MCP tool connections. For example,
 you might add a tool for running shell commands, database queries, or calling an external API.
 Provide the command details (name, command to execute, any environment variables or
 arguments). This makes the tool available for agents to use.
 • 
• 
• 
Create Agents: Define one or more AI agents. For each agent, choose an AI model (e.g., GPT-4 or
 another LLM you have a key for), and write a system prompt describing the agent’s role or task
 objective. Attach one or more of the configured tools that the agent is allowed to use. For instance,
 you could create an agent "DataAnalyzer" that uses a Python tool for data analysis.
 Build Workflows: Chain agents into a workflow to tackle multi-step tasks. In the Workflows builder,
 you can add multiple agents as steps in sequence. The output of one agent can be passed as input
 to the next. This allows complex processes to be automated – for example, Agent A searches for
 information, Agent B analyzes it, Agent C prepares a report.
 Interact via Chat: Use the Chat interface to engage with your agents or workflows. You can pose a
 question or command, and the selected agent (or workflow) will respond. During chat, you’ll see the
 2
agent’s reasoning steps, tool usage, and final answers. This is a great way to test single agents. For
 workflows, you can trigger the whole chain and observe each step’s output.
 • 
Model Panel: The interface also provides a Model panel where you can directly interact with a
 chosen LLM (without any custom agent prompt or tools). This is useful for quick queries or
 comparing responses from different raw models.
 (Detailed instructions and tips for using the interface are available in 
Community and Support
 usage.md.)
 DojoAI is an open-source project (MIT licensed) and welcomes contributions. If you have questions or run
 into problems: - Check the 
troubleshooting.md guide for common issues and resolutions. - Review the
 developer_guide.md for insight into how things work under the hood. - Feel free to open an issue on GitHub
 or contribute via pull requests. 
Happy building with DojoAI – we can’t wait to see what workflows and agents you create!
 setup.md
 Overview
 This guide covers the full environment setup for DojoAI. It will walk you through required dependencies and
 detailed installation steps on Windows 11 (as well as notes for Linux/Mac), including configuring SQLite and
 ChromaDB, and preparing LLM access. By the end of this guide, you’ll have all components ready to run
 DojoAI.
 1. System Requirements
 • 
• 
• 
• 
Operating System: Windows 11 (64-bit) or Linux/macOS. (This guide highlights Windows 11 specifics,
 but DojoAI is cross-platform.)
 Node.js Runtime: Node.js v18+ is recommended. Download from the official website and ensure 
node --version works in your terminal. (Alternatively, DojoAI supports the Bun runtime for
 improved performance. Bun is optional – if you choose to use it, install Bun v1.0+ and ensure 
bun -
version is available.)
 Package Manager: npm (comes with Node) or Yarn. If using Bun, it will act as the package manager.
 Python (optional): If you plan on running a local ChromaDB server or other Python-based tools,
 ensure Python 3.x is installed (for Windows, add it to PATH).
 • 
Git: to clone the repository (or you can download the ZIP from GitHub).
 2. Cloning the Repository
 Open a terminal (PowerShell on Windows, or Bash on Linux/macOS) and run:
 3
git clone https://github.com/Enetact/DojoAI.git
 cd DojoAI
 This will create a 
DojoAI directory with the project files.
 3. Environment Variables Configuration
 DojoAI uses a number of environment variables for configuration. All needed variables are listed in the
 .env.example file in the project root. Before running the app, create your own 
1. 
2. 
3. 
4. 
5. 
Copy the example:
 Windows (PowerShell):
 Copy-Item .env.example .env
 Linux/Mac:
 cp .env.example .env
 Open the 
.env :
 .env file in a text editor and fill in the values:
 OPENAI_API_KEY: Required for OpenAI GPT-3.5/GPT-4 usage. Get this from your OpenAI account
 dashboard.
 ANTHROPIC_API_KEY: (Optional) for Anthropic’s Claude model. If you have an Anthropic key and
 want to use Claude, provide it here.
 OTHER LLM API KEYS: The config may include placeholders for other providers (e.g., 
AZURE_OPENAI_KEY , 
6. 
7. 
COHERE_API_KEY , etc.). Provide those if you intend to use those models. If
 a model’s key is missing, that model will simply be unavailable in the UI.
 CHROMA_URL: The endpoint URL for ChromaDB (if using). Default is 
http://localhost:8000
 (the standard local URL). Adjust if your Chroma server is elsewhere.
 DATABASE_URL or SQLITE_PATH: (Depending on how it’s named in .env) Points to the SQLite
 database. This might be a file path like 
sqlite.db or a connection string. By default, DojoAI uses a
 local SQLite file (e.g., 
dojo.sqlite ) in the project directory. You can leave the default or change
 8. 
the path as desired.
 Auth Credentials: If the application supports user login via GitHub or others, you might see
 variables like 
GITHUB_CLIENT_ID and 
GITHUB_CLIENT_SECRET . These are only needed if you
 want to enable OAuth login. For local usage, you can initially skip these (the app will allow a guest
 session).
 Save the 
.env file after editing. Never share your API keys publicly or commit them to Git.
 4. Installing Dependencies
 Next, install the required packages and build the project:
 • 
• 
• 
Install Node Packages: In the project root, run:
 npm install (uses npm) OR
 bun install (if using Bun, which will utilize the 
bun.lock for fast installs)
 4
This will install all dependencies for the monorepo (both frontend and backend packages).
 • 
• 
• 
• 
Windows 11 Specific – Build Tools: If you are on Windows, some dependencies (like the SQLite
 driver or other native addons) might need build tools. If the install process fails with errors about
 building modules (e.g., involving node-gyp, Python, or Visual Studio), you may need to:
 Install the Windows Build Tools. The easiest way is: open an elevated PowerShell (as Administrator)
 and run:
 npm install --global windows-build-tools (for npm) or follow Microsoft’s instructions to
 install the C++ Build Tools.
 After that, retry 
npm install . This step ensures libraries like SQLite can compile native bindings
 on Windows.
 (Optional) Verify Installation: After installation, you can run 
npm run build (or 
bun run 
build ) to compile the TypeScript code. This isn’t strictly necessary for development (the dev server
 will build on the fly), but it can confirm that everything is set up correctly. You should see no errors in
 the build output.
 5. Setting up SQLite Database
 DojoAI uses SQLite for storing local data such as configured agents, tools, user sessions, etc. SQLite is file
based and does not require a separate server process.
 Initial setup: The first time you run the app, it will create a SQLite database file (as defined in your 
.env ,
 e.g., 
dojo.sqlite ). There is no manual setup required for SQLite itself. The app will handle creating
 tables or running migrations on first run (if applicable).
 Windows note: The database file will be created in the project directory (or the path you set). Ensure the
 path is writable. No additional installation is needed for SQLite on Windows, as it’s included via libraries.
 If you ever need to inspect or backup the database, you can use any SQLite GUI or the 
sqlite3
 command-line tool. For example, to open the DB: 
sqlite3 dojo.sqlite (after installing SQLite CLI).
 6. Setting up ChromaDB (Vector Database)
 ChromaDB is an optional component that DojoAI can use to store and retrieve embeddings for long-term
 memory or knowledge base functionality. If you plan to use features like document Q&A or memory beyond
 the immediate conversation, setting up Chroma is recommended.
 There are two main ways to use ChromaDB with DojoAI:
 • 
• 
• 
Run ChromaDB via Docker (Recommended): The Chroma team provides a Docker image for the
 Chroma server. 
Ensure you have Docker installed (on Windows 11 you can use Docker Desktop).
 Pull and run the Chroma container:
 5
docker run-d-p 8000:8000 ghcr.io/chroma-core/chroma:latest
 This launches the Chroma server in a container, listening on port 8000 by default.
 • 
In your 
.env , ensure 
CHROMA_URL is set to 
port).
 http://localhost:8000 (or the appropriate host/
 Windows 11 Tip: When using Docker on Windows, containers run in a VM. Your Node.js app might not
 directly see 
localhost for the Chroma service. Use 
host.docker.internal as the host to let the
 DojoAI app reach the Docker container’s service. For example, set 
CHROMA_URL=http://
 host.docker.internal:8000 on Windows. This isn’t necessary on Linux (where localhost works) – on
 Linux, if the app is running on the same machine as Docker, use 
localhost or the Docker container’s IP
 (e.g., 172.17.x.x).
 • 
• 
• 
• 
Run ChromaDB locally (Python): Alternatively, you can install ChromaDB as a Python package and
 run it on your host machine:
 Install Chroma: 
pip install chromadb
 Run the Chroma server: 
chromadb --listen 0.0.0.0 --port 8000 (adjust host/port as
 needed).
 Set 
CHROMA_URL accordingly (e.g., 
http://localhost:8000 ).
 This method may require a Python environment and is essentially what the Docker image does under the
 hood. Use whichever is more comfortable.
 If you do not need vector search or memory features, you can skip running ChromaDB. The app will still
 run; attempts to use memory search may just fail or return nothing if Chroma is not available.
 7. LLM Providers Setup
 DojoAI is model-agnostic: it can work with multiple LLM providers as long as you configure the API access.
 Out-of-the-box, it supports at least: - OpenAI (GPT-3.5, GPT-4): Requires 
OPENAI_API_KEY . Sign up at
 OpenAI and obtain an API key. Enter it in your 
.env . The app will use OpenAI’s API for chat completions
 and embeddings (for memory) by default if this key is present. - Anthropic (Claude v1/v2): If you have
 access to Anthropic’s API, provide 
ANTHROPIC_API_KEY . Claude can be used as an agent’s model in place
 of OpenAI. - Others: The architecture allows adding other providers (e.g., Cohere, AI21, HuggingFace
 Inference). If support for these exists (check 
.env.example for hints of variables like 
etc.), you can add the keys similarly. Without a key, those options will be hidden in the UI.
 COHERE_API_KEY
 Local LLMs: Currently, DojoAI relies on API-based models. If you wish to use local models (like running
 Llama 2 on your machine), you would typically set up an API for them (for instance, through a local server
 that mimics OpenAI’s API or via the MCP tool interface). Advanced users can integrate local models by
 either: - Using an MCP tool that calls a local model (for example, an 
ollama or 
LocalAI server) – you’d
 configure it as a tool the agents can use. - Extending the codebase’s AI module to add a new provider class
 that calls the local model.
 For initial setup, we recommend starting with OpenAI’s API to ensure everything works. You can explore
 more advanced configurations once the basics are running.
 6
8. Running the Application
 With dependencies installed and environment configured, you are ready to run DojoAI:
 • 
Using Docker Compose: If you prefer an all-in-one approach, the repository includes a 
compose.yml that defines the services. Ensure your 
.env is configured, then run: 
docker-compose up--build
 docker
This will build the DojoAI app image and start it along with a ChromaDB service. Once running, skip
 to the Accessing the App section below. (If you need to stop it later, press Ctrl+C or run 
docker
compose down .)
 • 
Using Local Node (Development Mode): To run without Docker, start the Turborepo dev script: 
npm run dev
 This should spawn both the front-end (Next.js dev server) and back-end as needed. You should see
 log output indicating the server is listening (usually on port 3000 for the Next.js app).
 Note: The first run might take a bit longer due to building the TypeScript code. Subsequent runs will be
 faster.
 • 
• 
• 
Using Local Node (Production Mode): If you want to simulate a production build:
 Run 
npm run build to compile the app.
 Run 
npm run start to launch the production server. This will serve the app likely on port 3000.
 Use this mode if you intend to deploy DojoAI or run it continuously.
 9. Accessing the App
 Once the server is running, open your web browser and go to: 
default port 3000). You should see the DojoAI interface loading. 
• 
http://localhost:3000 (assuming
 If you configured everything correctly, you’ll be able to navigate the dashboard, configure tools, and
 create agents. 
• 
If the page doesn’t load or you get an error, check the terminal output where the app is running.
 Common issues include missing environment variables (the app may log an error if an API key is
 missing and a feature is used) or port conflicts (see Troubleshooting if another app is using port
 3000).
 For Windows 11 users running the app in WSL2: use the address 
http://localhost:3000 from
 Windows as well – WSL will forward the port. If using Docker, ensure you used 
host.docker.internal in
 config if needed (see ChromaDB notes above).
 7
10. Additional Configurations
 • 
• 
• 
GitHub OAuth (Optional): DojoAI supports GitHub login for saving your data under an account
 (especially useful if you deploy it for multiple users). To enable this, you need to register a GitHub
 OAuth App and provide the Client ID and Secret in the 
.env (
 GITHUB_CLIENT_ID , 
GITHUB_CLIENT_SECRET ). Also set the callback URL as directed by the GitHub OAuth setup (likely 
http://localhost:3000/api/auth/callback/github for dev). With these set, the app’s "Sign
 in with GitHub" option will work. If not configured, the app will run in guest mode, allowing you to
 use it without login – data will be stored locally for your session.
 Ports and Hostnames: By default, the web app runs on port 3000. To change this, you can set an
 environment variable (e.g., Next.js uses 
PORT ). For the Docker setup, you can edit 
docker
compose.yml to map to a different host port if needed. ChromaDB default port is 8000; if you
 change it, update 
CHROMA_URL .
 Proxy Settings: If you are behind a corporate proxy and the app needs internet (for accessing LLM
 APIs), ensure your system proxy is configured. Node will respect environment vars like 
HTTP_PROXY if set.
 With this setup complete, you can now proceed to actually use DojoAI. Continue to the 
a walkthrough of running the application, creating agents, and building AI workflows.
 usage.md guide for
 usage.md
 Running the Application
 After setting up the environment (see setup.md), you can run DojoAI either via Docker or directly:
 • 
• 
Via Docker: If you used 
docker-compose up , the application and ChromaDB should already be
 running in containers. Check Docker’s output to see if the web server started successfully (it should
 indicate listening on port 3000 or similar). 
Via Local Dev Server: If you ran 
npm run dev (or 
bun dev ), you’ll see logs in your terminal for
 the Next.js development server. It typically prints a message like 
0.0.0.0:3000 .
 ready - started server on 
Once running, open a web browser and navigate to 
http://localhost:3000 (or the appropriate host/
 port if you changed it). You should see the DojoAI web interface load.
 Using the Web Interface
 The DojoAI UI is designed to be beginner-friendly, with a dashboard guiding you through connecting tools,
 creating agents, and chaining them into workflows. Here’s how to get started:
 8
1. Connect Your Tools (MCP Connections)
 On the dashboard, the first panel is "Connect your tools". Click Configure MCP Connections. This will take
 you to a page or modal where you can add external tools for the AI to use. 
• 
• 
• 
• 
• 
• 
• 
• 
What are tools? Tools are external commands or services the AI agents can invoke to perform
 specific tasks (e.g., searching a database, running a script, calling an API). DojoAI uses the Model
 Context Protocol (MCP) to interface with these tools in a standardized way.
 Adding a tool: Provide details for the tool:
 Name: A friendly name (e.g., "Shell" or "GoogleSearch").
 Command/Endpoint: How to run the tool. For a local command, this might be the shell command (like
 python or a script path). For an API, it could be an HTTP endpoint.
 Arguments/Params: If the tool requires arguments, define a template or leave it dynamic. For
 instance, a tool "Shell" might have an argument placeholder for the command it will execute.
 Environment Variables: (If needed) Provide any env vars the tool process requires (for example, API
 keys for an API tool).
 MCP Settings: Some tools might have MCP-specific settings like a timeout, context restrictions, etc.
 Tool examples: You could add a simple "Shell" tool that allows execution of terminal commands
 (useful for file operations or running Python snippets). Another example is a "WebSearch" tool that
 calls an external search API.
 After adding tools, ensure they appear in the connections list as active. The AI agents can now call these
 tools when needed.
 2. Build AI Agents
 Next, click Configure Agents on the dashboard. This is where you create one or more AI agents, each with
 a specific role and capabilities.
 When creating an agent, you will specify: - Agent Name: A descriptive name (e.g., "DataSummarizer" or
 "CodeAssistant"). - Base LLM Model: Choose which large language model the agent uses. The options here
 correspond to the API keys you configured. For example, you might see "OpenAI GPT-4" or "OpenAI
 GPT-3.5" (if your OpenAI API key is set), "Anthropic Claude" (if that key is set), etc. Agents with no available
 model (due to missing API keys) will be disabled or hidden. - System Prompt: This is where you define the
 agent’s persona or task. It’s a prompt that stays in the agent’s context to guide its behavior. For example, for
 a coding assistant agent, the prompt might be: "You are an AI developer assistant that outputs clean,
 commented code." This prompt helps shape all the agent’s responses. - Allowed Tools: Select which of the
 MCP tools (from step 1) this agent can use. You might allow a general assistant agent to use all tools, or
 restrict a specialized agent to only use a specific tool. During operation, the agent will be able to invoke only
 the tools you permit here. - Memory Settings (optional): If the agent should utilize long-term memory or a
 knowledge base, ensure ChromaDB is running. The agent’s design might automatically vectorize and store
 chat history or documents for recall. (There may not be a UI field for this in initial versions – some of this
 happens behind the scenes whenever you use the "seed data" function described later.)
 Save the agent. You can create multiple agents for different tasks. For instance, one agent could be good at
 web research (with a web search tool), another at coding (with a shell/Python tool), and another could be an
 orchestrator.
 9
3. Chain Agents into Workflows
 The third panel on the dashboard, "Chain agents together", leads to Build Workflows. A workflow lets you
 link multiple agents in sequence, so they can hand off tasks to each other automatically.
 Workflow creation interface: - Create a new Workflow: Give it a name (e.g., "Research and Report
 Workflow"). - Add Steps/Agents: You’ll be able to add steps to the workflow. Each step is essentially one of
 the agents you created. For each step, select which agent to use. - Ordering & Data Flow: Arrange steps in
 the desired order. The output of a step can be fed as input to the next. For example, in a two-step workflow,
 Agent A’s answer could become the prompt or data for Agent B. - Configurations: Depending on the
 interface, you might be able to specify how data flows. Some workflow builders allow specifying which part
 of Agent A’s output goes to Agent B (the whole response or a part of it). Check for any options like "Use
 previous output as context". - MCP Connection Management: Workflows ensure that any needed tool
 connections are established for each step. DojoAI will automatically handle setting up and tearing down
 tool sessions when a workflow runs, so you usually don’t need to do anything extra. Just make sure the
 agents in the workflow have the tools they need.
 Save the workflow. You should now see it listed in the workflows page.
 4. Seeding Data (Knowledge Base)
 (This is an advanced/optional step, relevant if you want your agents to have a custom knowledge base or long
term memory.)
 DojoAI can use a vector database (ChromaDB) to store embeddings of text data. This allows agents to recall
 information outside the immediate conversation by searching the vector store.
 To seed data: - Prepare your data in text form (for example, a set of FAQs, a manual, or documents you
 want the AI to know about). - Currently, seeding might require using a script or API call, as the UI may not
 have a full data uploader yet. Check the repository for any scripts (perhaps in a 
scripts/ directory or
 within the backend code) that handle indexing data into Chroma. - If a script is provided (e.g., 
scripts/
 index_data.js or similar), run it with your data source. It likely will read documents and use an
 embedding model (possibly OpenAI embeddings) to store vectors in Chroma. - Another approach: use the
 chat interface with an agent to feed information. For example, you could copy-paste some text into the chat
 and have an agent designed to store it. If the code supports it, the agent might vectorize and save any text
 you tag for memorization. - After seeding, the data is in ChromaDB. Agents (if coded to do so) can perform
 similarity searches on new queries to retrieve relevant info. For instance, if you ask a question that matches
 something in the knowledge base, the agent can fetch that info via Chroma.
 (Refer to the developer guide for more on how the system handles memory. If there’s no ready-made UI for
 seeding, you may need to directly interface with the Chroma API or extend the code.)
 5. Managing and Using Agents/Workflows
 Now that you have tools, agents, and optionally workflows: - Go to the Chat section of the app. This might
 be accessible via a navigation link or directly from the dashboard ("Chat" panel). - In the chat interface, you
 typically can select either a single agent or a workflow to interact with: - To chat with a single agent, pick the
 10
agent from a dropdown (if available) or open its dedicated chat. - To run a workflow, select the workflow.
 The UI might present it as a scenario or just as an agent with combined skills. - Type a message or question
 in the chat box and send it. The agent will process your input. You will see the conversation appear. - If the
 agent uses tools, you might see intermediate steps (like "Agent is executing Tool X..."). The interface may
 show these tool outputs live, so you can understand what the AI is doing (for example, calling an API or
 running a calculation). - Finally, the agent (or final agent in a workflow) will respond with an answer.
 You can have back-and-forth dialogue. Each new user message will continue the conversation context (the
 agent remembers what was said earlier in the session, within the context limit of the model). If you have
 ChromaDB enabled and the agent is designed to use it, the agent might also pull in older context beyond
 the immediate history by doing a similarity search on the conversation (this would appear as a tool action if
 implemented).
 6. Using the Model Panel
 DojoAI’s interface might include a "Model" or "Console" panel (as hinted on the dashboard). This likely
 allows direct interaction with a raw model without agent tooling: - You choose a model (from those
 configured, e.g., GPT-4). - You can send it prompts and get completions, similar to a basic ChatGPT interface.- This is useful for quick tests or comparing how the raw model responds versus how your agent (with its
 system prompt and tools) responds.
 7. Saving and Loading Configurations
 • 
• 
• 
• 
All your agents, tools, and workflows are saved in the SQLite database. If you restart the app (and
 you’re using the same 
.env and database file), your configurations persist.
 If you used GitHub login, your data is tied to your user account and will persist across sessions
 (stored in the database). If you ran as guest (no login), your data is still saved locally, but be aware it
 might not differentiate between different users/machines. In a multi-user scenario, enabling proper
 auth is recommended.
 You can modify or delete agents and workflows via their respective UI pages. For example, to edit an
 agent’s prompt or tools, go back to the Agents configuration, select the agent, and update it.
 It’s good practice to test each agent individually in chat to ensure it behaves as expected (uses its
 tools correctly, etc.) before chaining it in a workflow.
 8. Managing the AI (Settings)
 DojoAI might provide a settings section where you can: - Adjust model parameters (e.g., temperature, max
 tokens) for the LLMs. Look for sliders or fields in the UI when selecting a model or agent. For instance, you
 might set a lower temperature for more deterministic outputs if the use-case demands. - View logs or
 execution traces. In development mode, the terminal running the backend will log detailed info like tool
 execution results, errors, or debugging info. Use this to troubleshoot agent behaviors. - Manage API keys or
 environment settings (though most of these are set via 
.env , the UI might allow you to input some keys
 at runtime). If you add a new API key (for a new model) while the server is running, you may need to restart
 the app for it to pick up the change, unless the app specifically allows dynamic entry.
 11
9. Example Workflow Usage
 To illustrate a typical usage scenario: 1. Suppose you want to automate researching a topic and
 summarizing it. You created: - Tool: "WebSearch" (calls a search API or uses a browser automation). - Agent
 A: "Researcher" (uses GPT-4, allowed to use WebSearch tool). Its prompt: "You are a research assistant who
 provides detailed factual answers with sources." - Agent B: "Summarizer" (uses GPT-3.5, no external tool).
 Prompt: "You are an assistant that summarizes input text concisely." - Workflow: "Research-and-Summarize"
 with Agent A followed by Agent B. 2. In chat, select the "Research-and-Summarize" workflow. 3. Ask: "Give
 me a summary of the latest developments in renewable energy storage." 4. Agent A ("Researcher") triggers: It
 might use the WebSearch tool to gather info (you may see in the log or UI: Searching for 'latest developments
 in renewable energy storage'...). It then formulates an answer with the info. 5. Agent A’s output (a detailed
 explanation with data) passes to Agent B. 6. Agent B ("Summarizer") takes that text and generates a concise
 summary. 7. You get the final answer: a crisp summary of the research, possibly with references if Agent A
 provided any.
 Throughout, you could follow what tools were used and the intermediate output. If anything goes wrong
 (say, the search tool failed), you’d see an error and could adjust your configuration or question.
 10. Shutting Down
 • 
• 
• 
If running via Docker, stop the containers with Ctrl+C in the terminal where 
running, or use 
docker-compose is
 docker-compose down to cleanly stop and remove containers.
 If running via npm dev server, Ctrl+C in that terminal will stop the servers.
 No data will be lost as long as the SQLite database file and any ChromaDB volumes persist. By
 default, the Docker setup likely doesn’t destroy the database file on down (unless you set it up that
 way). Your 
.env and any created files remain in the project folder.
 You now have a functioning DojoAI environment and know how to use it. Experiment with different tools
 and agent prompts to see how the system can solve various tasks. For any issues or advanced usage
 questions, refer to the 
troubleshooting.md and 
developer_guide.md.
 developer_guide.md
 Introduction
 This guide dives into the internals of DojoAI, explaining the project structure, key modules, configuration
 points, and how to extend the system. It’s intended for developers who want to contribute to DojoAI or
 customize it beyond typical usage.
 DojoAI is structured as a monorepo (managed with Turborepo) containing multiple projects: - A frontend
 app (the web UI, built with Next.js and React). - A backend service (handling agent logic, tool execution,
 and serving the MCP protocol). - Several shared packages (for agents, tools, AI model integrations, etc.).
 Understanding this structure will help you navigate the codebase.
 12
Repository Structure
 At the root of the repository, you’ll see directories like 
apps/ and 
packages/ :
 • 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
• 
apps/frontend (or similar): This is the Next.js application. It contains the pages, components, and
 front-end logic. The Next.js app also includes API route handlers (under 
pages/api or the newer 
app/api structure) which act as the backend endpoints. This app is what serves the web
 dashboard you interact with.
 apps/backend (if present): In some setups, there might be a separate Node.js backend service. In
 DojoAI, the backend may be integrated into the Next.js app (since Next.js can serve API routes).
 However, given the complexity (especially with MCP and long-running agent processes), there could
 be a dedicated backend service to manage agent workflows. Check if 
apps/ contains a directory
 like 
backend or 
server . If it does:
 This backend likely runs an Express.js or Fastify server (or even a Bun server) that maintains
 WebSocket connections or manages tool processes independently of the Next.js lifecycle.
 It might be responsible for launching subprocesses for tools and handling inter-process
 communication.
 packages/agents (module managing agent definitions): This would contain code for the Agent class– handling the agent’s state (its prompt, allowed tools, selected model) and the logic to execute an
 agent’s reasoning cycle. It likely includes:
 Code to construct the prompt (e.g., combining system prompt, user query, and maybe tool context).
 Logic to interact with the LLM API (calling OpenAI, etc., possibly via a unified interface).
 Handling of the agent’s memory: short-term (conversation history) and long-term (via ChromaDB).
 packages/tools (module for MCP tools integration): Here you’d find:
 Definitions of the Tool interface, specifying how a tool is invoked.
 Perhaps specific implementations for common tools (like a ShellTool class, or HTTPTool class).
 MCP server/client implementation: The backend likely acts as an MCP server, exposing tools to the
 LLM. If an LLM (like OpenAI’s functions or tools interface) calls the MCP, the server executes the
 corresponding tool. The code for this protocol lives here. For example, it might open a port for MCP,
 or more simply, the backend might just simulate the protocol internally.
 packages/ai (module for AI model integration): This could hold classes or utilities for different LLM
 providers:
 For OpenAI, a class or function to call the Chat Completion API.
 For Anthropic, a similar function for Claude.
 These might abstract differences in API (so the rest of the system calls a generic interface).
 It might also include code for handling streaming responses and converting them to the format
 needed by the frontend (like server-sent events or Next.js API streaming).
 packages/db or packages/core: Possibly a module for database access and core logic:
 Database schemas or ORMs for agents, tools, workflows, user accounts, etc.
 If an ORM like Prisma or an query builder is used, you’d find schema definitions here. (Check if
 there’s a 
prisma/ directory or similar. If Prisma is used, 
DATABASE_URL in .env would be relevant
 and migration files would be present.)
 Core might also include types and utilities shared across front and back end (like TypeScript types for
 Agent, Workflow, etc., so that the frontend knows what shape of data to expect from the backend).
 Other configs: 
turbo.json (already in root) defines the Turborepo pipeline (which projects to build/test/deploy
 together).
 13
• 
• 
docker-compose.yml defines how to containerize the app (likely includes a service for the Next.js
 app and one for ChromaDB).
 .env.example we saw lists environment variables needed.
 Data Flow and Key Components
 Here’s an overview of how things work when you use DojoAI: 1. Front-End (Next.js React): Renders the UI
 (dashboards, forms for tools/agents, chat interface). It communicates with the backend via: - API calls:
 Standard REST or Next.js API routes. For example, when you create a new agent in the UI, it likely sends a
 POST request to an API endpoint like 
/api/agents with the agent data. The backend then saves this to
 the database. - WebSockets / SSE: For real-time updates (such as streaming chat responses or tool
 execution logs), the frontend might open a WebSocket or use Server-Sent Events to get a live feed from the
 backend. The developer logs mention streaming responses, so the backend likely streams tokens from the
 LLM and tool outputs to the front-end. 2. Agents Module: When a chat request or workflow execution is
 initiated, the backend uses the agents module to handle it: - It fetches the agent(s) definition from the
 database (including the system prompt, selected model, and allowed tools). - Creates a context for the
 conversation (e.g., composes the prompt, adds conversation history). - Calls the LLM via the AI module. If
 the LLM responds with an action (like a tool invocation request), the agent logic captures that. 3. MCP/Tools
 Module: If an LLM’s response indicates a tool use (for instance, using a special token or JSON indicating the
 tool name and parameters, as per Anthropic’s MCP or OpenAI function calling), the tools module kicks in: 
The MCP server within DojoAI matches the requested tool name to one of the configured tools (ensuring
 the agent is allowed to use it). - It then executes the tool. If it’s a shell command, it might spawn a child
 process (Node’s 
spawn or 
exec ). If it’s an API call, it might send an HTTP request. - Captures the output
 or result of the tool. - Returns that result back to the LLM (this may be done by appending the tool output to
 the conversation and continuing the LLM conversation). - This cycle may repeat if the LLM decides to use
 multiple tools in a turn. 4. Workflow Engine: If the user invoked a workflow (multiple agents): - The
 backend likely has a 
WorkflowExecutor class or similar that manages running each agent in sequence. 
It takes the initial user query, feeds it to the first agent. Once agent 1 produces an output, it may pass that
 output (or a processed form of it) as the input to agent 2, and so on. - There might be an internal format for
 passing data between agents (e.g., the entire conversation vs just a summary). - The executor handles any
 necessary setup and teardown at each step (the commit logs show improvements in establishing/cleaning
 tool connections per step). - It accumulates results or logs, which can be streamed to the user as well. 5.
 Database (SQLite): The application state (tools, agents, workflows, user profiles) is persisted: - On agent/
 tool creation, the backend writes to SQLite. Likely via an ORM or direct SQL queries. - During a chat,
 ephemeral data (like each message) might not be immediately stored unless needed. Possibly conversation
 history is in memory or cached. If a session is meant to persist (especially for logged-in users), chat
 transcripts could be saved too. - The DB also stores API credentials if you input them via UI (though since we
 use .env for keys, maybe not – keys are usually kept server-side only). - If using NextAuth for GitHub login,
 SQLite would store user accounts and sessions.
 1. 
2. 
3. 
Authentication & Sessions:
 If OAuth login is enabled, NextAuth (or a similar library) might be used. NextAuth would use API
 routes for callbacks and use the DB for storing sessions. The commit 
feat(ui): update GitHub 
sign-in flow indicates this is part of the app.
 For guest users, the app might create a temporary session (possibly identified by a cookie or in
memory ID) just to associate data. The commit about using user session for guest instead of local
 storage suggests that previously data might have been stored in browser localStorage, but now they
 14
4. 
moved to a session on the server side. Likely they use a session cookie so that even guest usage is
 tracked on server (for multi-tab consistency and easier upgrade to login).
 Developer note: if looking in the code, search for something like 
next-auth config or a custom
 auth middleware.
 Key Configuration Files
 • 
• 
• 
.env and Config.ts: The environment variables control things like API keys and endpoints. The
 code might have a config module that reads these. For example, a 
config.ts might load
 process.env variables for openAI keys, etc. If you want to change providers or add one, you’d update
 both .env and possibly extend the config and AI modules.
 next.config.js : If present, check it for any custom settings. Possibly used to enable streaming,
 webpack configs for bundling any native modules, etc. For instance, if using WASM or specific Node
 APIs in frontend, Next config would allow them.
 package.json scripts: These show how to run and build each part. For example, you might see 
"dev": "turbo run dev" meaning it runs dev scripts in parallel for all apps. Or separate 
dev:frontend and 
dev:backend scripts. Understanding these helps in custom running or
 deploying the app.
 Extending DojoAI
 One of the goals of DojoAI is extensibility. Here are some common extension points and how to work with
 them:
 Adding a New Tool
 If you want to add support for a new kind of tool (beyond simple shell or HTTP calls), you can: - Define the
 Tool in the UI: Currently, you can manually configure tools via the interface. But for a deeper integration or
 a custom tool type, you might add a default configuration in code. For example, suppose you want an
 EmailTool that can send emails. You could: - Create a definition in the tools module (e.g., a class or function
 to send email via SMTP or an API like SendGrid). - Register this tool so that if an agent tries to use
 "EmailTool", the MCP server knows how to execute it. - Provide a way in the UI for users to add it (or
 automatically include it by default with required settings in .env or config). - Tool Execution Security: Be
 mindful that tools can execute arbitrary commands. The current design assumes you trust the agents (since
 this is running locally for you). If you plan to extend for multiple users, implement proper sandboxing or
 permission checks for tools.
 Supporting a New LLM Provider
 Out of the box, DojoAI supports OpenAI and possibly Anthropic. To add another: - Identify API differences:
 e.g., Cohere requires a different API call and doesn’t support function calling like OpenAI. You’d implement a
 wrapper in the AI module for Cohere’s generate API. - Add environment vars: e.g., 
COHERE_API_KEY . 
Integrate with Agent logic: The Agent class may switch logic based on model/provider. You might add
 cases for the new provider, especially if it doesn’t support streaming or tool usage in the same way. For
 instance, OpenAI uses function calling to integrate tools, while others might not – you might implement a
 simpler loop: agent gets response, parse if there’s a tool request in text, etc. - UI Exposure: Add the
 15
provider to the list of model choices. This could be as simple as adding it to a constant list if keys exist.
 Ensure that if key is missing, it doesn’t show (the app already hides those without keys).
 Modifying Workflow Behavior
 If you need more complex workflows (conditional branching, parallel agent execution): - The current
 WorkflowExecutor runs steps sequentially by design. You could extend it to support branching logic by
 analyzing agent outputs or adding a small DSL for workflows. This is non-trivial and would involve front-end
 changes too (to design such workflows). - For simple modifications, you can adjust how data passes
 between steps. For example, you might change it to include not just the last agent’s output but also the
 original question to each subsequent agent (giving more context). - The workflow UI code (likely in the
 frontend app under something like 
components/WorkflowBuilder.tsx ) can be adjusted to reflect any
 changes in logic (like capturing a setting “pass entire conversation vs last answer only”).
 Database and Models
 If you plan to extend what data is stored (say, track analytics or store every conversation turn for review): 
Update (or create) the database schema. If using an ORM like Prisma, update the schema file and run
 migrations. If using raw SQL or another lightweight method (some projects use plain SQLite with minimal
 ORMs), adapt those as needed. - Add new models or fields in the code where appropriate (e.g., a
 Conversation or Message model to log chats). - Ensure to handle migrations for existing data if needed (for
 your development, you can wipe and rebuild the DB since it’s local, but for any production usage consider
 migrations).
 Configuration & Constants
 Some configurable aspects: - Agent parameters: You might want to tweak default temperature or max
 tokens for models. Look in the AI module for where the API call is made (likely something like
 openai.createChatCompletion({...}) ). You can expose these as settings or adjust defaults. - Tool
 timeouts or limits: The tools module might have default timeouts for tool execution to prevent hanging.
 You can configure those (for example, limit a shell command to 30 seconds). - UI constants: Like the default
 welcome message or instructions in the landing page can be changed in the React components.
 Tips for Development
 • 
• 
• 
• 
Live Reload: In dev mode (
 npm run dev ), any changes to the front-end code will hot-reload the
 page. Changes to backend (API routes or Node scripts) may restart the server. Keep an eye on the
 terminal for errors.
 Testing Agents & Tools: Use the chat interface extensively to test. Open the browser console and
 network tab – you can see the requests to 
/api/... and maybe server-sent events for streaming.
 This helps debug where an issue might be (front-end state vs backend logic).
 Logging: The code likely uses 
console.log or a logging library. If you need more insight, add
 logs in the agent or tool execution flow. For example, log the full prompt sent to OpenAI, or log
 when a tool process starts and ends. This output will appear in the terminal.
 Error Handling: Agents might encounter errors (e.g., a tool command fails, or OpenAI API returns
 an error due to rate limit or invalid prompt). The backend should catch these and relay a message to
 the UI. If extending, ensure you handle exceptions and either retry or inform the user. For instance, if
 16
a tool throws, you might want the agent to catch that and continue the conversation gracefully
 (maybe apologizing or asking for correction).
 Architecture Summary
 To summarize the design: - Monorepo & Modules: Logical separation of front-end UI, agent logic, tool
 integration, and model API integration, but all parts work in concert. - MCP (Model Context Protocol): A
 central concept enabling the AI to use external tools. DojoAI’s implementation allows any CLI or service to
 be plugged in, making the system highly extensible for different use cases. - Workflow Orchestration:
 Chains multiple agents. This shows the system is built not just for single Q&A, but for multi-agent
 collaboration. The architecture is prepared for scaling up complexity (the commit history suggests
 continuous improvements in workflow execution). - Local-first and Privacy: Running everything locally
 (including vector DB) is a conscious choice. It trades off some convenience (no managed cloud services by
 default) for control and privacy, which many developers appreciate.
 By understanding these pieces, you can confidently dive into the code. We encourage you to explore the
 repository files with this guide in mind: - Check out 
apps/frontend for UI components and how forms
 call APIs. - Look at 
packages/agents and 
packages/tools to see how agents think and act. - Review
 packages/ai to see how it interfaces with OpenAI/Anthropic (this will also clarify how to add more
 models). - Inspect the database or config to see how data is structured.
 Happy hacking! If you make improvements or extensions, consider contributing back to the project.
 troubleshooting.md
 Introduction
 Even with careful setup, you might encounter issues when installing or running DojoAI. This guide lists
 common problems and their solutions. If you run into an error, scan through these topics to see if it
 matches your situation.
 1. Installation Issues
 Problem: Installation (npm install) fails on Windows with errors about Python or building packages.
 Solution: This usually means a native dependency (like the SQLite library) failed to compile. Ensure you
 installed the Windows Build Tools【setup.md】. Open an admin PowerShell and run 
npm install -
global windows-build-tools to automatically set up Python and Visual Studio Build Tools.
 Alternatively, manually install the latest Build Tools from Microsoft. After that, delete any partially built
 modules (
 rm -rf node_modules ) and run 
npm install again.
 Problem:
 bun install fails or bun isn’t recognized on Windows.
 Solution: Bun’s Windows support is still evolving. It might require WSL (Windows Subsystem for Linux) at
 the moment. If Bun doesn’t work, use Node.js + npm which is fully supported on Windows. You can also run
 DojoAI inside WSL2 Ubuntu for a smoother Unix-like experience on Windows.
 17
Problem: Slow installation or network issues when installing packages.
 Solution: Some dependencies might be large. Ensure you have a stable internet connection. If behind a
 proxy, configure npm to use the proxy. You can also try using Yarn as an alternative installer if npm is slow.
 Running 
npm cache clean --force and then reinstalling can help if the cache was corrupted.
 2. Configuration Problems
 Problem: Blank page or error when accessing 
http://localhost:3000 .
 Solution: First, check the terminal running the app: - If there’s an error about missing environment
 variables, double-check your 
.env . A common oversight is forgetting to populate the API key fields. For
 instance, if 
OPENAI_API_KEY is empty, the backend might throw an error or the frontend might disable
 features. - If the app started but you still see nothing, ensure you’re using the correct port. The default is
 3000. If you changed it, use that port in the URL. - Also ensure the build compiled. If using Next.js dev
 server, an uncaught build error would show a message (and possibly a stack trace) in the terminal or
 browser. Solve any TypeScript/compile errors if present.
 Problem: OpenAI (or other LLM) not responding or timing out.
 Solution: This could be: - Wrong API key: Verify the key is correct and has access to the model (GPT-4 access
 is limited; if you only have a GPT-3.5 key and you try to use GPT-4, you might get an error). - API usage limit:
 Check if you exhausted your quota or hit rate limits. OpenAI might return an error message in the backend
 logs. If so, reduce usage or increase your quota. - Network issue: If you’re offline or behind a firewall that
 blocks the API, the requests will fail. Ensure the machine can reach the API endpoints (e.g.,
 api.openai.com ). A quick test is to 
curl https://api.openai.com/v1/models with your key
 (should return JSON of models if working).
 Problem: ChromaDB connection errors.
 Solution: If you enabled Chroma, but see errors like "Failed to connect to Chroma" or timeouts: - Ensure
 Chroma server is running. If via Docker, run 
docker ps to see if the container is up. If it exited, check
 docker logs <container> for clues (maybe a port conflict or startup error). - Check 
in .env. For local Docker on Windows, as noted, use 
CHROMA_URL
 host.docker.internal . On Linux/mac, 
http://
 localhost:8000 should work if on same host. - If running Chroma via Python, ensure you started it on
 the correct host/port and that the port is open. Also check if any firewall is blocking access to port 8000. - As
 a workaround, if issues persist, you can disable Chroma usage: simply don’t start it and avoid using features
 that require it (like long-term memory search). The app should handle its absence gracefully in most cases.
 Problem: Database (SQLite) errors, e.g., "database is locked" or "unable to open database file".
 Solution: SQLite can produce "locked" errors if two processes try to write at the same time: - This shouldn’t
 happen often with a single app instance. But if you for example launched two instances of the server (or
 one instance via Docker and one via local run) pointing to the same DB file, they will conflict. Only run one
 DojoAI instance at a time (or configure separate DBs). - If you see "unable to open", check the path in
 DATABASE_URL . Relative paths are resolved from the working directory – ensure it points to a valid
 location. If running via Docker, note that inside the container the path might differ. The docker-compose
 might mount a volume for the db; if not, the data might be ephemeral inside container. - On Windows,
 paths with spaces or special characters could cause issues – quote them or use the 8.3 filename as needed,
 or move the project to a simpler path. - In worst case, to reset, you can stop the app and delete the SQLite
 f
 ile (this will lose data like configured agents, but sometimes starting fresh is okay during dev).
 18
3. Runtime Errors & Exceptions
 Problem: An agent query fails with an error message (in chat) like "Tool X failed" or "Error: something went
 wrong".
 Solution: This means something in the agent’s process caused an exception. For example, if an agent tries
 to use a tool: - Check the backend log for the exact error. Perhaps the tool’s command wasn’t found (e.g.,
 you configured a tool to use 
python but Python isn’t installed or not in PATH). - If it’s a Python script or
 shell command, the error might be coming from that script. You might need to adjust the command or
 ensure the environment is correct (e.g., a tool to run a specific program requires that program installed). - If
 the error is from the AI model (like it couldn’t parse the response or a function call name that doesn’t exist),
 it might be a bug in how the agent interprets the model output. In dev, you can reproduce the scenario and
 then improve the parsing logic or add a guard. For now, you can try rephrasing your query or giving the
 agent different instructions as a workaround.
 Problem: The UI becomes unresponsive or shows a "Disconnected" message during a long operation.
 Solution: Long-running tool calls or very long LLM responses can sometimes cause timeouts or the front
end to disconnect (especially if using Next.js API routes which might have a time limit, e.g., Vercel free tier
 has 10 sec for serverless functions). - For local dev, you can increase Next.js timeout or ensure you’re using
 Node server (Next dev should be fine though). - If a tool is long-running by nature (say a complex data
 processing script), consider modifying the tool to stream output periodically so the front-end knows it’s still
 alive, or increase any configured timeout in the tools module. - As a user workaround, avoid extremely long
 single queries. Break them down if possible. E.g., instead of asking the agent to do 10 things at once, do 5
 then the next 5.
 Problem: High memory or CPU usage.
 Solution: Running LLMs and multiple processes can be intensive: - If you are using local models or have
 many agents parallel, you might simply be hitting system limits. Close other programs, or consider
 upgrading hardware for heavy tasks. - If not using local models, high CPU might indicate a runaway process
 (maybe a tool script stuck in a loop). Use your OS process manager to see what is consuming resources. If
 it’s a specific tool, you might need to add safeguards in that tool’s implementation (like a timeout or kill
 after certain usage). - Node memory usage can grow if a lot of data is kept. The dev mode also isn’t as
 optimized as production. If you notice issues, try running a production build (
 npm run start ) which may
 handle memory more efficiently.
 4. Multi-Agent and Workflow Issues
 Problem: Agents in a workflow don’t seem to pass information to each other.
 Solution: Ensure that the workflow was configured correctly: - Check that Agent A’s output is indeed meant
 to be input to Agent B. If the workflow builder has a setting for this, make sure it’s enabled. Some systems
 might require a placeholder like 
<OUTPUT> in Agent B’s prompt where A’s output will go. - It’s possible the
 workflow execution encountered an error at Agent A but still tried Agent B. Review the logs for the workflow
 run. The backend might log something like "Workflow step 1 error: ...". - If the issue is logical (the second
 agent didn’t understand the first agent’s output), you might need to refine the agent prompts. Agent B
 might need a clearer instruction to expect input from Agent A. For instance, Agent B’s system prompt could
 include: "You will receive information from a previous agent in your input. Summarize or process it as required."
 19
Problem: Tool connections not closing or too many open files/processes.
 Solution: The application is supposed to clean up tool processes after use. If you find defunct processes: 
This could be a bug. As a quick fix, restart the app which will clean up all child processes. - If you’re
 developing, ensure that for every 
spawn or external connection, the code handles termination. The
 commit history suggests improvements were made, so make sure you have the latest code. If a process like
 a database connection or an SSH stays open, you might need to add explicit close calls after use. - On
 Windows, also be careful with how processes are spawned; ensure they terminate even if the parent exits
 (some might not, leading to orphans).
 5. Port Conflicts
 Problem: Address already in use (EADDRINUSE) errors when starting the server.
 Solution: This means something is already running on a port needed by DojoAI. - By default, port 3000 for
 the front-end. If something else (another dev server) is using it, either stop that process or change DojoAI’s
 port. To change, set the 
PORT environment variable before running (e.g., 
PORT=3001 npm run dev to
 use 3001) or configure in next.config if applicable. - Port 8000 for ChromaDB. If you get a conflict there,
 perhaps another service is using 8000. You can modify the Chroma startup to use a different port: e.g.,
 docker run -p 8001:8000 ... to map to a different host port, and set 
CHROMA_URL=http://
 localhost:8001 . Alternatively, stop the other service using 8000. - If using Docker, note that Docker
 Compose by default will fail to start if ports are taken. Edit 
docker-compose.yml to resolve conflicts
 (change the ports mapping).
 Problem: Cannot bind to port (permission denied).
 Solution: On Unix systems, binding to ports below 1024 requires root. But 3000 and 8000 are high ports, so
 you shouldn’t see this unless you changed to a low port. If you did, run the process as admin or choose a
 higher port.
 6. GPU and Local Model Issues
 (DojoAI primarily uses API models, but if you integrate local models, here are some general pointers.)
 Problem: GPU out-of-memory errors when running a local model.
 Solution: If you have integrated something like a local PyTorch model or 
llama.cpp , you might hit VRAM
 limits: - Try reducing the model size or using CPU mode. For example, load a 7B model instead of 13B, or if
 using 
llama.cpp , load 4-bit quantized models to save memory. - Ensure no other heavy GPU apps are
 running (like games or other ML tasks). - If using Docker for a local model, make sure you enabled GPU
 support (nvidia runtime) and allocated enough GPU memory. - If all else fails, use the cloud models
 (OpenAI/Anthropic) which offload the heavy lifting to their servers.
 Problem: No CUDA/GPU available error.
 Solution: This likely means a library expected a CUDA-compatible GPU but didn’t find one: - Install proper
 NVIDIA drivers and CUDA toolkit if you actually have a GPU and want to use it. - If you don’t have a GPU,
 ensure the libraries are set to CPU mode. Some libraries auto-detect; others might need a flag (e.g., in code
 use 
.to('cpu') for PyTorch, or install CPU-only versions of libraries). - For 
llama.cpp or similar, no
 GPU needed if you compile accordingly. Check that you didn’t set an env var that forces GPU.
 20
7. Data and Results Issues
 Problem: The AI’s answers are poor or irrelevant.
 Solution: This might not be a bug but rather a prompt/design issue: - Make sure your system prompt for
 the agent is well-crafted. A clear instruction can significantly improve results. - If the agent needs
 knowledge it doesn’t have, consider using tools or seed data. For example, asking coding questions without
 an internet tool means the AI relies purely on its training (which might be fine up to 2021 data, but anything
 after that it won’t know). Integrating a documentation search tool or providing context can help. - If using
 GPT-3.5 and getting bad answers, note that GPT-4 usually performs better on complex tasks. If you have
 access, try that model. - Check if the agent might be hitting token limits (especially with long chats). If so, it
 might forget context. The fix could be enabling vector memory (Chroma) or breaking the task into smaller
 pieces.
 Problem: Data seeded in Chroma is not being used by the agent.
 Solution: Ensure that: - The agent is actually coded to do a vector search. Likely the agent logic will do
 something like: if a question is asked, search the ChromaDB for relevant context. If that’s not happening,
 you may need to integrate that logic. Possibly a specific agent type or prompt triggers it (e.g., maybe only a
 QA agent does that). - Check that the Chroma instance has the data (you can use the Chroma client or REST
 API to query the collections to verify your data is there). - The embeddings should match the model’s
 expectations. If you used OpenAI embeddings, ensure the agent is also using an OpenAI model
 (embedding vector size must match). Mixing embedding models can lead to poor results (e.g., don’t use
 Cohere embeddings with an index expected for OpenAI). - If the agent is using tools, maybe it expects to
 use a specific tool to retrieve info rather than directly pulling from memory. Confirm in agent code if there’s
 a step like 
agent.retrieveMemory(query) and if not, that feature might not be implemented yet.
 8. Session and Persistence
 Problem: Agents/Tools I created yesterday are gone today.
 Solution: This could be due to running as guest and the session data not being persistent: - If no login was
 used, data should still have been saved in SQLite. It shouldn’t disappear on its own unless the DB was
 removed or not saved. If you ran in Docker without a volume for the DB, the data might have been lost
 when container stopped. To persist, ensure the 
docker-compose.yml mounts the sqlite file to the host. 
If using GitHub login, maybe you signed in with a different account or the session expired. Check the SQLite
 to see if multiple user entries exist. The agents you created could be tied to a user ID. Logging back in as
 that user should show them. - In development, sometimes schema changes can wipe out data if you reset
 the DB. If that happened, unfortunately you’d have to recreate the agents. For future, consider exporting
 configurations (not implemented yet, but you could manually copy the SQLite file as a backup).
 Problem: Cannot log in with GitHub (OAuth error). Solution: If you attempted GitHub login: - Double-check
 your OAuth app setup. The Client ID/Secret in .env must match the GitHub OAuth App you created. Also, the
 callback URL configured in GitHub must match your running app’s URL. In dev, usually 
http://
 localhost:3000/api/auth/callback/github . If you see an error like "redirect_uri_mismatch", it’s the
 callback URL issue. - Ensure your site URL is correct in NextAuth (if used). NextAuth might use an
 environment variable like 
NEXTAUTH_URL . Set that to 
http://localhost:3000 in dev. - If you don’t
 need login in dev, you can operate as guest and skip OAuth setup entirely.
 21
9. Miscellaneous
 Problem: The UI layout looks broken or styling is off.
 Solution: This might happen if assets didn’t build or load: - Run a fresh build (
 npm run build ) to ensure
 all CSS is generated (especially if using Tailwind or any CSS-in-JS). - Check the browser console for 404s on
 CSS or JS files. If using Next.js, maybe the static files path is wrong due to an incorrect 
basePath or
 something in config. - Try a hard refresh (Ctrl+F5) to clear cached assets. - If only on a specific browser,
 ensure compatibility (the app should work on modern browsers like Chrome/Firefox/Edge; older IE is not
 supported likely).
 Problem: I want to reset everything and start from scratch.
 Solution: If things got messy and you want a clean slate: - Stop the app, delete the SQLite database file (and
 maybe the 
./chromadb data directory if one was created for Chroma). - Clear or delete the 
.env if you
 suspect a config issue, then re-copy from 
.env.example and put keys fresh. - Run 
npm install again
 to ensure deps are fine. - Then launch as new. This will be as if first time run.
 If your issue isn’t listed here or persists after trying these solutions, consider reaching out via GitHub issues.
 Include any error logs and a description of what you did when the issue occurred. Since DojoAI is under
 active development, you might also pull the latest changes from the repository to see if the problem has
 already been fixed in a newer commit.
 Remember, troubleshooting is a normal part of working with cutting-edge projects – with patience and the
 above guidance, you’ll be up and running. Good luck, and enjoy building with DojoAI! 
22
