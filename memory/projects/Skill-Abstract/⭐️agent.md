![alt text](image.png)
https://github.com/earendil-works/pi

https://pi.dev/


![alt text](image-1.png)


1.探索cc的使用方法
2./grill me的使用方法
3.ai对话的梳理


| 问题 ｜实践 <=> 论文/工程调研｜
ai与人多轮对话（模型记忆） -> 从实践中吸取教训迭代更新（？）<=> ai-agent 自进化的论文与工程实践 <参考（codex、claude code）> 





相关资料：


参考（codex、claude code）：



设想：
数据来源：
1.运行harness，调用脚本会话自动总结会话内容，总结成问题文档
2.针对提交的hotfix修改comment，总结成问题文档

Agent训练：





问题：
1.harness 本质是基于 上下文、工具（mcp等）扩展，agent自进化类似于GRPO，会不会存在过拟合问题（即过多skill和约束导致运行受限）？
    搜索结论：
        1.在llm基座模型很弱情况下会存在无法扩散
        2.对于deepseek等商用api模型，扩散能力很强，一般不会存在过多的约束导致性能下降
2.不同的错误得到经验如何分类
3.个人

⭐️下一步做什么：
1.个人pi从零开始的agent
2.harness关于进化（自己迭代）插件
3.总结trea主流模型对于进化的实现方式

参考资料
1.https://forum.trae.cn/t/topic/13529
