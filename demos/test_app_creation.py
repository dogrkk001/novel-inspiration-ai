import sys
from pathlib import Path
sys.path.insert(0, str(Path('src')))

try:
    from src.web_ui import create_web_app
    app = create_web_app('test.db')
    print('✅ Web应用创建成功')
    print(f'✅ 路由数量: {len(app.routes)}')
    routes = [route.path for route in app.routes]
    main_routes = [r for r in routes if not r.startswith('/static')]
    print(f'✅ 主要路由: {main_routes}')
except Exception as e:
    print(f'❌ 创建失败: {e}')