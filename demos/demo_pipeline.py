#!/usr/bin/env python3
"""
演示完整流程脚本 - 从输入到检索的端到端演示

演示流程：
1. 从文件读取样例文本
2. 使用输入模块进行文本切分
3. 使用灵感提取模块提取创作灵感（支持 MockLLM 和真实 LLM）
4. 将提取结果存储到 SQLite 数据库
5. 使用检索模块进行关键词搜索并展示结果

Usage:
    python demo_pipeline.py --input ../data/sample_novel.txt --db test_pipeline.db --keyword "武功"
    python demo_pipeline.py --input ../data/sample_novel.txt --db test_pipeline.db --keyword "勇气" --use-llm
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional

# 添加项目根目录到 Python 路径
current_dir = Path(__file__).parent
project_root = current_dir.parent
sys.path.insert(0, str(project_root))

from src.input_module import InputModule
from src.extractor import InspirationExtractor
from src.database import save_batch, DatabaseError
from src.search import search_inspirations, SearchError
from src.search_enhancement import SearchEnhancement, SearchEnhancementError
from src.llm_manager import LLMManager, LLMConfig


class PipelineError(Exception):
    """管道执行错误"""
    pass


class DemoPipeline:
    """演示管道主类"""
    
    def __init__(self, db_path: str, use_llm: bool = False, model_name: Optional[str] = None,
                 use_semantic_search: bool = False):
        """
        初始化演示管道
        
        Args:
            db_path: 数据库文件路径
            use_llm: 是否使用真实的 LLM（需要 API key）
            model_name: 指定使用的模型名称
            use_semantic_search: 是否使用语义检索增强
        """
        self.db_path = db_path
        self.use_llm = use_llm
        self.model_name = model_name
        self.use_semantic_search = use_semantic_search
        self.input_module = InputModule()
        
        # 初始化 LLM 管理器
        self.llm_manager = LLMManager()
        
        # 初始化检索增强模块
        if use_semantic_search:
            self.search_enhancement = SearchEnhancement(db_path, self.llm_manager)
        else:
            self.search_enhancement = None
        
        # 初始化提取器
        if use_llm and model_name:
            # 使用指定的模型
            try:
                llm = self.llm_manager.get_model(model_name)
                print(f"✓ 使用指定模型: {model_name}")
            except ValueError:
                print(f"⚠ 指定模型 '{model_name}' 不存在，使用默认模型")
                llm = self._get_best_available_llm()
        elif use_llm:
            # 使用最佳可用的 LLM
            llm = self._get_best_available_llm()
        else:
            # 使用 MockLLM
            llm = self.llm_manager.get_model('mock')
        
        # 创建兼容的 LLM 实例（使用老的接口）
        if hasattr(llm, 'generate_text'):
            # 新的 LLM 管理器接口，需要适配器
            from src.extractor import LLMInterface as ExtractorLLMInterface
            
            class LLMAdapter(ExtractorLLMInterface):
                def __init__(self, new_llm):
                    self.new_llm = new_llm
                
                def generate(self, prompt: str) -> str:
                    return self.new_llm.generate_text(prompt)
                
                def get_model_name(self) -> str:
                    info = self.new_llm.get_model_info()
                    return f"{info.get('provider', 'unknown')}-{info.get('model_name', 'unknown')}"
            
            adapted_llm = LLMAdapter(llm)
        else:
            # 旧的接口，直接使用
            adapted_llm = llm
        
        self.extractor = InspirationExtractor(llm=adapted_llm)  # type: ignore
        
        print(f"✓ 初始化完成")
        print(f"  - 数据库路径: {db_path}")
        print(f"  - LLM模式: {'真实LLM' if use_llm else 'MockLLM'}")
        print(f"  - 模型: {llm.get_model_info()['model_name']}")
        
        # 显示可用模型
        available_models = self.llm_manager.get_available_models()
        print(f"  - 可用模型: {', '.join(available_models)}")
    
    def _get_best_available_llm(self):
        """获取最佳可用的 LLM"""
        available = self.llm_manager.get_available_models()
        
        # 优先级顺序：OpenAI > Claude > Qwen > DeepSeek > Mock
        preference_order = ['openai', 'claude', 'qwen', 'deepseek', 'mock']
        
        for preferred in preference_order:
            if preferred in available:
                print(f"✓ 使用可用模型: {preferred}")
                return self.llm_manager.get_model(preferred)
        
        # 如果都不可用，使用 mock
        print("⚠ 没有可用的真实 LLM，使用 MockLLM")
        return self.llm_manager.get_model('mock')
    
    def run(self, input_file: str, keyword: str) -> Dict[str, Any]:
        """
        运行完整的演示流程
        
        Args:
            input_file: 输入文件路径
            keyword: 检索关键词
            
        Returns:
            包含各步骤结果的字典
        """
        results = {
            'input_file': input_file,
            'keyword': keyword,
            'text_chunks': [],
            'inspirations': [],
            'saved_count': 0,
            'search_results': []
        }
        
        try:
            # 步骤1: 读取和切分文本
            print(f"\n📖 步骤1: 读取文件 {input_file}")
            if not Path(input_file).exists():
                raise PipelineError(f"输入文件不存在: {input_file}")
            
            process_result = self.input_module.process_file(input_file)
            text_chunks = process_result['chunks']
            results['text_chunks'] = text_chunks
            
            print(f"✓ 文件读取完成")
            print(f"  - 切分块数: {len(text_chunks)}")
            if text_chunks:
                avg_length = sum(len(chunk.get('content', '')) for chunk in text_chunks) / len(text_chunks)
                print(f"  - 平均块长度: {avg_length:.0f} 字符")
            
            # 步骤2: 提取灵感
            print(f"\n🎯 步骤2: 提取创作灵感")
            inspirations = []
            
            for i, chunk in enumerate(text_chunks, 1):
                print(f"  处理第 {i}/{len(text_chunks)} 块...")
                
                try:
                    # 提取灵感
                    inspiration_data = self.extractor.extract_inspiration(chunk['content'])
                    
                    # 准备保存到数据库的数据格式
                    db_data = {
                        'source_file': input_file,
                        'chapter': chunk.get('title', f'第{i}块'),
                        'raw_text': chunk['content'][:500],  # 限制原文长度
                        'idea': inspiration_data['theme'],
                        'tags': f"{inspiration_data['world_elements']}, {', '.join(inspiration_data['characters'])}"[:200]  # 限制标签长度
                    }
                    
                    inspirations.append(db_data)
                    
                except Exception as e:
                    print(f"    警告: 提取第 {i} 块时出错: {e}")
                    continue
            
            results['inspirations'] = inspirations
            print(f"✓ 灵感提取完成")
            print(f"  - 成功提取: {len(inspirations)} 条灵感")
            
            # 步骤3: 保存到数据库
            print(f"\n💾 步骤3: 保存到数据库")
            if inspirations:
                try:
                    saved_ids = save_batch(inspirations, self.db_path)
                    results['saved_count'] = len(saved_ids)
                    
                    print(f"✓ 数据保存完成")
                    print(f"  - 保存记录数: {len(saved_ids)}")
                    print(f"  - 记录ID范围: {min(saved_ids)} - {max(saved_ids)}")
                
                except DatabaseError as e:
                    raise PipelineError(f"数据库保存失败: {e}")
            else:
                print("⚠ 没有有效的灵感数据需要保存")
            
            # 步骤4: 检索演示
            print(f"\n🔍 步骤4: 检索演示")
            try:
                if self.use_semantic_search and self.search_enhancement:
                    # 使用语义检索增强
                    print(f"  使用语义检索增强模块")
                    
                    # 构建向量索引（如果需要）
                    stats = self.search_enhancement.get_index_stats()
                    if not stats['index_complete']:
                        print(f"  构建向量索引...")
                        processed = self.search_enhancement.build_index()
                        print(f"  ✓ 向量索引构建完成：处理 {processed} 条记录")
                    
                    # 执行不同类型的检索
                    print(f"\n  🔍 关键词检索：")
                    keyword_results = self.search_enhancement.search(keyword, mode='keyword', limit=5)
                    print(f"    匹配结果: {len(keyword_results)} 条")
                    
                    print(f"  🧠 语义检索：")
                    semantic_results = self.search_enhancement.search(keyword, mode='semantic', limit=5)
                    print(f"    匹配结果: {len(semantic_results)} 条")
                    
                    print(f"  🌐 混合检索：")
                    hybrid_results = self.search_enhancement.search(keyword, mode='hybrid', limit=10)
                    search_results = hybrid_results
                    
                    print(f"\n✓ 语义检索完成")
                    print(f"  - 关键词匹配: {len(keyword_results)} 条")
                    print(f"  - 语义匹配: {len(semantic_results)} 条")
                    print(f"  - 混合检索: {len(hybrid_results)} 条")
                    
                    # 展示混合检索结果
                    if hybrid_results:
                        print(f"\n🎆 混合检索结果预览：")
                        for i, result in enumerate(hybrid_results[:5], 1):
                            print(f"  [{i}] ID: {result['id']} | 综合评分: {result['composite_score']:.3f}")
                            print(f"      来源: {result['source_file']}")
                            print(f"      创意: {result['idea'][:60]}...")
                            print(f"      评分明细: 关键词={result['keyword_score']:.3f}, 模糊={result['fuzzy_score']:.3f}, 语义={result['semantic_score']:.3f}")
                            print()
                    
                else:
                    # 使用传统检索
                    print(f"  使用传统关键词检索")
                    search_results = search_inspirations(self.db_path, keyword, limit=10)
                    
                    print(f"✓ 检索完成")
                    print(f"  - 关键词: '{keyword}'")
                    print(f"  - 匹配结果: {len(search_results)} 条")
                    
                    # 展示前几条结果
                    if search_results:
                        print(f"\n🎯 检索结果预览：")
                        for i, result in enumerate(search_results[:5], 1):
                            print(f"  [{i}] ID: {result['id']}")
                            print(f"      来源: {result['source_file']}")
                            print(f"      章节: {result['chapter']}")
                            print(f"      创意: {result['idea'][:80]}...")
                            print(f"      标签: {result['tags'][:50]}..." if result['tags'] else "      标签: 无")
                            print()
                    else:
                        print(f"  ❌ 未找到包含关键词 '{keyword}' 的记录")
                        
                results['search_results'] = search_results
            
            except SearchError as e:
                print(f"  ❌ 检索失败: {e}")
                results['search_results'] = []
            
            return results
            
        except Exception as e:
            raise PipelineError(f"流程执行失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="小说灵感提取系统 - 完整流程演示",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 使用 MockLLM 进行演示
  python demo_pipeline.py --input ../data/sample_novel.txt --db demo.db --keyword "武功"
  
  # 使用真实 LLM（需要设置 API key）
  python demo_pipeline.py --input ../data/sample_novel.txt --db demo.db --keyword "勇气" --use-llm
  
  # 使用自定义文件
  python demo_pipeline.py --input /path/to/novel.txt --db custom.db --keyword "友情"
        """
    )
    
    parser.add_argument(
        '--input', 
        required=True,
        help='输入文件路径 (支持 TXT 格式)'
    )
    
    parser.add_argument(
        '--db', 
        required=True,
        help='SQLite 数据库文件路径'
    )
    
    parser.add_argument(
        '--keyword', 
        required=True,
        help='检索关键词'
    )
    
    parser.add_argument(
        '--use-llm', 
        action='store_true',
        help='使用真实的 LLM（需要 API key），否则使用 MockLLM'
    )
    
    parser.add_argument(
        '--model', 
        help='指定使用的模型名称 (openai, claude, qwen, deepseek, mock)'
    )
    
    parser.add_argument(
        '--semantic', 
        action='store_true',
        help='使用语义检索增强功能（基于向量相似度）'
    )
    
    args = parser.parse_args()
    
    # 验证输入文件
    if not Path(args.input).exists():
        print(f"❌ 错误: 输入文件不存在: {args.input}")
        sys.exit(1)
    
    print("🚀 小说灵感提取系统 - 完整流程演示")
    print("=" * 50)
    
    try:
        # 创建并运行管道
        pipeline = DemoPipeline(
            db_path=args.db, 
            use_llm=args.use_llm, 
            model_name=args.model,
            use_semantic_search=args.semantic
        )
        results = pipeline.run(input_file=args.input, keyword=args.keyword)
        
        # 总结报告
        print("\n📊 执行总结")
        print("=" * 30)
        print(f"✓ 输入文件: {results['input_file']}")
        print(f"✓ 文本块数: {len(results['text_chunks'])}")
        print(f"✓ 提取灵感: {len(results['inspirations'])} 条")
        print(f"✓ 保存记录: {results['saved_count']} 条")
        print(f"✓ 检索结果: {len(results['search_results'])} 条")
        print(f"✓ 数据库文件: {args.db}")
        print("\n🎉 演示完成！")
        
    except PipelineError as e:
        print(f"\n❌ 管道执行失败: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n⏹ 用户中断执行")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 未预期错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()