"""
Business Intelligence Agent Package (Optimized Version)

This package contains the unified BI agent, tools, and database utilities.
Now optimized to use a single-agent architecture for quota efficiency.
"""

from bi_agent.agent import (
    bi_expert_agent,
    bi_runner,
    GEMINI_MODEL
)

from bi_agent.bi_service import BIService
from bi_agent.tools import (
    execute_sql_and_format, 
    get_database_schema
)

root_agent = bi_expert_agent
root_runner = bi_runner

__all__ = [
    'bi_expert_agent',
    'bi_runner',
    'root_agent',
    'root_runner',
    'GEMINI_MODEL',
    'BIService',
    'execute_sql_and_format',
    'get_database_schema',
]