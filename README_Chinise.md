
# Two Stage Automatic Speech Recognition System With Large Language Model
[English_doc](./README.md)
## 项目简介
华中科技大学Dain团队开发的项目，目的在于将大型语言模型（LLM）集成到ASR系统中，以提高识别的准确性。但是注意现在的本文工作是基于现有数据集的框架，必须已有识别出的文本文件text。

### 工作流程图
![两阶段识别流程图](./two_stage_recognition.png)


## 使用指南

### 安装依赖
```bash
pip install -r requirements.txt
```

### 配置文件设置
1. **选择并编辑配置文件**：在`config`目录下根据API供应商选择合适的配置文件。
2. **填写API信息**：示例如下：

    ```yaml
    # 示例：gpt_conformer.yaml
    provider: openai
    model: gpt-3.5-turbo
    api_key: YOUR_API_KEY
    base_url: YOUR_BASE_URL

    # 示例：azure_conformer.yaml
    provider: azure
    model: gpt4o
    api_key: YOUR_API_KEY
    base_url: YOUR_AZURE_ENDPOINT
    api_version: YOUR_API_VERSION
    ```

3. **指定文本路径和标签信息**：

    ```yaml
    path:
        example1: "path_to_text1"
        example2: "path_to_text2"
    text: "path_to_label"
    ```

4. **设置参数**：根据任务语言调整参数。

    ```yaml
    combination_num: 30 # 每请求的句子数
    thread_num: 100 # 并发线程数
    temperature: 0.2
    max_repeat_times: 1 # 重复询问数
    top_p: 0.8
    ```

5. **添加Prompt**：根据需要在配置文件后添加。参考[PromptList](./config/PromptList.md)

    ```yaml
    prompt: "Your custom prompt here"
    ```

6. **配置文件路径**：在`main.py`中指定配置文件路径。

    ```python
    with open("path_to_your_config", 'r') as f:
    ```

7. **运行程序**：执行命令并生成结果目录。

    ```bash
    python main.py
    ```

### 结果目录内容
- `config`：使用的配置文件。
- `diff`：文本的修改详情。
- `err`：错误示例。
- `response`：LLM的回答。
- `skips`：根据filter设置跳过的文本。
- `text`：修改后的文本。
- `total`：统计结果。
- `wer`：词错误率文件。
- `wrong_sentence`：错误句子列表。

### 注意事项


- Tokens:使用Deepseekv2模型在AISHELL-1和Librispeech数据集上的tokens消耗情况分别为250k(input)+260k(output)和640k(input)+650k(output)，设置的组合数分别为30和10。
- 你可以在result的目录下查看历史结果
### 测试LLM能力
1. 填写`config/test/Chinese/gpt.yaml`配置文件。
2. 执行测试脚本：

    ```bash
    python tools/test_model_capability.py
    ```

    结果将直接打印，需手动记录。未使用多线程，测试过程可能较长。

你也可以填写新的测试

## 致谢
感谢[wenet](https://github.com/wenet-e2e/wenet/blob/main/README.md)提供的工具和预训练模型。

## 引用

