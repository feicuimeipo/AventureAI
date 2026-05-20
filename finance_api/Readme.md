rem 生成包含所有已安装包的requirements.txt
rem 包含所有已安装包，可能包含无关依赖
rem pip freeze > requirements.txt

rem 安装pipreqs
rem 精确，只包含项目实际依赖
rem 生成仅包含项目实际依赖的requirements.txt（UTF-8编码）
rem 生成requirements.txt
rem pip install pipreqs
pipreqs ./ --encoding=utf8 --force
rem pipreqs ./：扫描当前目录下的Python文件，分析其中的import语句。
rem   --encoding=utf8：指定文件编码为UTF-8，避免编码问题。
rem   --force：强制覆盖已存在的requirements.txt文件。
rem # 安装
rem pip install -r requirements.txt

# 生产环境准备
## 环境标准化

### 用venv创建隔离虚拟环境，避免依赖冲突：
```python
python -m venv flask_venv
source flask_venv/bin/activate  # Linux/macOS
flask_venv\Scripts\activate  # Windows
```


