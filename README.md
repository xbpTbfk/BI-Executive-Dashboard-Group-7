# BI-Executive-Dashboard-Group-7

A production-ready Business Intelligence agent system built with Google's Agent Development Kit (ADK) featuring dual interfaces: ADK web and Gradio.

The system converts natural language questions into SQL queries, executes them against Microsoft SQL Server, and automatically generates visualizations and explanations using Google's Gemini AI.

# Architecture Overview
<img width="1414" height="2000" alt="User Question (1)" src="https://github.com/user-attachments/assets/5b1b6653-7b40-4ef6-bb17-7ce7dd1d14f9" />

# How It Works 

  1. **User Question** enters the bi_runner

  2. **Bi_expert_agent** retrieves schema, generates SQL query, and prepares results for visualization

  3. All outputs displayed in **Gradio UI**

# The Agent Architecture : Optimized Single-Agent Design

The system is built using a Unified BI Expert Agent architecture, specifically optimized for quota efficiency and low latency. Unlike multi-agent systems that require multiple API calls, this design leverages a single high-capability agent to manage the entire data-to-insight pipeline.

**1. Root Agent: The BI Expert**
  
  The root_agent (driven by the bi_expert_agent) acts as the central intelligence of the system:

  Context Awareness: The agent maintains a understanding of the user's intent from query generation to final explanation.

  Multitask Execution: It handles SQL generation, data reasoning, and visualization logic within a single execution context.

**2. Integrated Toolset**
  
  The agent is equipped with specialized tools to interact safely with the Microsoft SQL Server environment:

  get_database_schema(): Automatically retrieves table structures and column metadata, allowing the agent to write accurate T-SQL queries based on real-time database schema.

  execute_sql_and_format(): A secure execution bridge that validates queries (ensuring they are SELECT statements) and formats the raw result sets into structured data for the agent.



# Prerequisites
Important : You need uv, a Gemini API key, and access to a SQL Server database.

   **Required Software**
   
- uv package manager -[Installation guide](https://github.com/kirenz/uv-setup)
      
- Python 3.12+
      
- ODBC Driver 18 for SQL Server

**API Access**
   
- Free Gemini API key from [Google AI Studio](https://aistudio.google.com/prompts/new_chat)

- Microsoft SQL Server database access

# How to use?
1. Clone and Install
   
   Clone repository

   ```
   git clone https://github.com/xbpTbfk/BI-Executive-Dashboard-Group-7.git
   ```

   Navigate to project directory

   ```
   cd BI-Executive-Dashboard-Group-7
   ```

   Install dependencies

   ```
   uv sync
   ```

2. Configure Environment
   
   Go to folder bi_agent and rename .example.env to .env and fill in your credentials:

   ```
   # Google API Key
   GOOGLE_API_KEY=your_gemini_api_key_here
   
   # SQL Server Configuration
   MSSQL_SERVER=your_server_address
   MSSQL_DATABASE=your_database_name
   MSSQL_USERNAME=your_username
   MSSQL_PASSWORD=your_password
   ```
3. Run the Application

      **Gradio Interface**

      ```
      uv run app.py
      ```
      Access at: http://127.0.0.1:7860
   

   Both interfaces use the same root_agent pipeline!

# Project Structure
```bash
gradio-adk-agent/
├── bi_agent/                    # Agent package
│   ├── __init__.py              # Package exports
│   ├── agent.py                 # root_agent + all sub-agents
│   ├── tools.py                 # Database tools (schema, SQL execution)
│   ├── bi_service.py            # BI service utilities
│   ├── db_config.py             # Database configuration
│   ├── sql_executor.py          # SQL validation and execution
│   └── .env                     # API keys and credentials
│
├── app.py                       # Gradio web interface
├── pyproject.toml               # Project dependencies (uv managed)
├── .python-version              # Python version (3.12)
└── README.md                    # This file
```

# Prompts
| **Component** | **Purpose** | **Example** |
| :--- | :--- | :--- |
| **Context** | Defines the environment in which the agent operates | “You are a BI Expert. Follow this sequence: …” |
| **Objective** | Specifies the primary goal of the agent | “Follow this sequence: 1. DISCOVER…” |
| **Mode** | Defines the persona or expertise of the agent | “You are a BI Expert.” |
| **People** | Identifies the target audience | “BI Executive Dashboard / business users” |
| **Attitude** | Establishes behavioral guidelines | “JSON SAFETY RULES -Your entire response MUST be a single JSON object…” |
| **Style** | Defines the output format | “OUTPUT TEMPLATE For example type:..., text_response:...,  sql_used :...., Raw_data :..., Chart_code:..., structure:.....” |
| **Specifications** | Hard constraints and technical rules | “PRECISE VISUALIZATION rules such as tooltip , chart style, axis formatting, chart size…”, “Dangerous SQL keywords that should be blocked contain in ‘BLACKLIST_KEYWORDS’ such as DROP, DELETE,…” |

# Safety Measure

  1. SQL Validation : Enforces a "SELECT-only" policy using regex-based filtering and a keyword blacklist (DROP, DELETE, EXEC) to prevent unauthorized data manipulation.

  2. Row Limits : Automatically injects TOP N into every generated statement to ensure manageable result sets and prevent memory overflow. 

  3. Connection Management : Utilizes SQLAlchemy context managers to ensure reliable database connection pooling and proper cleanup after each execution. 

  4. Credential Security : Protects sensitive database credentials by retrieving them exclusively via environment variables, ensuring no sensitive data is hardcoded in the repository.

# Evaluation Procedure

  1. Ground Truth for testing AGENT : Evaluate AI agents by establishing ground truths to test their performance. The agents should be capable of addressing all established ground truth scenarios.
```
#Example

Easy/Basic Question : Which region or territory generated the highest revenue in Q3 of 2023? Provide a pie chart or a donut chart for the revenue distribution. 

Medium Question : Show me the top 10 most profitable products for the year 2023, including their category names. Present this in a horizontal bar chart.

Hard Question : Compare monthly sales performance between 2022 and 2023. Highlight the months where 2023 performed better than 2022. 
```

  2. Workflow Sequence Validation : We validated the agent's workflow sequence to ensure all tasks are executed in the correct order.

# Implementation Challenges 

  1. During system development, API quota limitations were encountered under the free-tier configuration, which restricts usage to a maximum of 20 requests per day per model. This constraint temporarily limited large-scale testing and iterative experimentation. The experience highlights the importance of proactive quota management, usage monitoring, and cost-aware AI system design when deploying generative AI solutions in production environments. 

  2. System performance was further impacted by slow response times and occasional errors. The need for frequent retries due to these failures led to inefficient quota usage and delayed testing milestones. 

  3. Due to the large number of tables in the database schema, the system may encounter ambiguity when interpreting user queries. This complexity can lead to variations in how the AI understands and maps the user's request to the underlying data structure. Consequently, the generated SQL query may differ from the intended query logic, which can result in discrepancies in the returned results and negatively impact the system’s execution accuracy during evaluation. 

  4. Differences in decimal precision may cause slight discrepancies in percentage calculations. Due to rounding during numerical operations, the computed values may not exactly match the expected results, which can sometimes affect the evaluation outcome and reduce execution accuracy.
