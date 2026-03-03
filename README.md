# BI-Executive-Dashboard-Group-7

A production-ready Business Intelligence agent system built with Google's Agent Development Kit (ADK) featuring dual interfaces: ADK web and Gradio.

The system converts natural language questions into SQL queries, executes them against Microsoft SQL Server, and automatically generates visualizations and explanations using Google's Gemini AI.

# How to use?
1. Clone and Install
   
   Clone repository

   ```
   git clone https://github.com/xbpTbfk/BI-Executive-Dashboard-Group-7.git
   ```

   Navigate to project directory

   ```
   cd gradio-adk-agent
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
   Choose your preferred interface:

      **Option 1: ADK Web Interface**
   
      ```
      uv run adk web
      ``` 
      Access at: http://127.0.0.1:8000

      **Option 2: Gradio Interface**

      ```
      uv run app.py
      ```
      Access at: http://127.0.0.1:7860
   

   Both interfaces use the same root_agent pipeline!
