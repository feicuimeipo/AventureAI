import asyncio
from typing import List

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI


class ReasonGenerator:
    def __init__(self):
        # 初始化 ChatOpenAI 模型
        # 确保环境变量 OPENAI_API_KEY 已设置，或者在此处直接传入 api_key
        self.llm = ChatOpenAI(
            model="gpt-4o",  # 根据实际需求选择模型，如 gpt-3.5-turbo, gpt-4o 等
            temperature=0.7,
            max_tokens=200
        )

    def gen_reasons(self, source_intro, source_skills,
                          target_intro, target_skills) -> List[str]:
        """
        异步生成匹配推荐理由
        """
        prompt = f"""
             发布者需求：{source_intro}
             需求技能：{source_skills}
             候选人档案：{target_intro}
             候选人技能：{target_skills}
             请生成3-4条简洁的匹配推荐理由，每条15字以内，直接列举，不用序号。
         """

        # 构建消息列表
        messages = [HumanMessage(content=prompt)]

        # 异步调用 LangChain 模型
        # ainvoke 是 LangChain 提供的异步调用方法
        response = asyncio.run(self.llm.ainvoke(messages))

        # 获取返回的内容文本
        content_text = response.content

        # 解析结果：按行分割，去除空白行和首尾空格
        reasons = [line.strip() for line in content_text.split('\n') if line.strip()]

        return reasons



if __name__ == "__main__":
    pass
    ## 运行异步主函数
    ## # 模拟数据
    # need = Need(description="寻找高级Python后端开发", skill_req="Python, Django, PostgreSQL")
    # candidate = Candidate(bio="5年后端开发经验，擅长高并发系统", skill_tags="Python, Django, Redis, Docker")
    # asyncio.run(generate_reason())
    # generator = ReasonGenerator()
    # reasons = generator.gen_reasons(','.join(source_intro), ','.join(source_skills),
    #                       ','.join(target_intro), ','.join(target_skills))
    #
    # data = []
    # print("生成的推荐理由：")
    # for reason in reasons:
    #     data.append(reason)
    # return data
