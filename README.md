# into

#### 介绍
into V2 社交为核心。链辅助扩展特殊功能的社交工具。

#### 软件架构
1.  Poetry 管理项目依赖
2.  

#### 安装教程

1. brew install poetry
2. cd project_dir
3. poetry install --no-root
4. docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=123456 -d postgres
5. 编辑app/settings/.dev.env
6. 编辑alembic/env.py->get_url()的链接字符串。但不要提交git
7. bash ./prestart.sh
8. uvicorn app.main:app --host 0.0.0.0 --port 5897 --reload
9. http://127.0.0.1:5897/api/v1/

#### 使用说明

2.  xxx

#### 参与贡献

1.  Fork 本仓库
2.  新建 Feat_xxx 分支
3.  提交代码
4.  新建 Pull Request


#### 特技

1. alembic tool
alembic revision --autogenerate -m 'first_revision'

alembic upgrade head
