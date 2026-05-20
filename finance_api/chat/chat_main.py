"""
pip3 install fastapi
pip install uvicorn
解决网络问题
pip install fastapi -i https://pypi.tuna.tsinghua.edu.cn/simple

解决用户权限问题
pip install fastapi --user

1. 建fastapi
2. 定时服骢-APScheduler

"""
from fastapi import Request
from app.app_fastapi import create_fastapi_app, jinja2_templates
from fastapi.responses import HTMLResponse
app = create_fastapi_app()



@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, id: str):
    return jinja2_templates.TemplateResponse("index.html", {"request": request, "id": id})

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)