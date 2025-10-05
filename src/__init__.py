"""
小说灵感提取 Agent
"""

__version__ = "0.1.0"
__author__ = "Your Name"

# 导入主要模块，使其可以通过包名直接访问
from .extractor import (
    MockLLM, OpenAIModel, ClaudeModel,
    InspirationExtractor, PromptTemplate,
    InspirationData, LLMInterface
)
from .input_module import InputModule
from .database import (
    InspirationDatabase, DatabaseError, ValidationError,
    save_inspiration, save_batch, query_by_keyword, delete_by_id
)
from .search import (
    SearchError,
    search_inspirations, search_by_source, search_by_date_range
)
from .llm_manager import (
    LLMConfig, LLMProvider, LLMInterface,
    OpenAILLM, ClaudeLLM, QwenLLM, DeepSeekLLM, MockLLM,
    LLMManager, get_llm_manager, create_llm_manager
)
from .search_enhancement import (
    SearchEnhancement, SearchEnhancementError, VectorDatabase,
    SemanticSearcher, HybridSearcher
)

__all__ = [
    'MockLLM', 'OpenAIModel', 'ClaudeModel',
    'InspirationExtractor', 'PromptTemplate',
    'InspirationData', 'LLMInterface',
    'InputModule',
    'InspirationDatabase', 'DatabaseError', 'ValidationError',
    'save_inspiration', 'save_batch', 'query_by_keyword', 'delete_by_id',
    'SearchError',
    'search_inspirations', 'search_by_source', 'search_by_date_range',
    'LLMConfig', 'LLMProvider',
    'OpenAILLM', 'ClaudeLLM', 'QwenLLM', 'DeepSeekLLM',
    'LLMManager', 'get_llm_manager', 'create_llm_manager',
    'SearchEnhancement', 'SearchEnhancementError', 'VectorDatabase',
    'SemanticSearcher', 'HybridSearcher'
]