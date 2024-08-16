
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
## 结果
## Result

下面的原始模型为U2++ Conforemr
### AISHELL-1

| Two-stage     | Decode            | Chunk | Temp | Top p | Task num | Changed Sentence | Error Sentence | CER(%)   | Changed        |
| ------------- | ----------------- | ----- | ---- | ----- | -------- | ---------------- | -------------- | -------- | -------------- |
| -             | attention         | full  | -    | -     | -        | -                | 2650           | 5.06     | -              |
| -             | attention rescore | full  | -    | -     | -        | -                | 2493           | 4.62     | -              |
| -             | ctc greedy search | full  | -    | -     | -        | -                | 2810           | 5.17     | -              |
| -             | ctc prefix search | full  | -    | -     | -        | -                | 2810           | 5.17     | -              |
| deepseekv2    | attention         | full  | 0.2  | 0.8   | 20       | 1568             | 2365           | 4.69     | -0.37(7.3%)    |
| deepseekv2    | attention rescore | full  | 0.2  | 0.8   | 20       | 1451             | 2189           | 4.21     | -0.41(8.8%)    |
| deepseekv2    | ctc greedy search | full  | 0.2  | 0.8   | 20       | 1892             | 2331           | 4.51     | -0.66(12.7%)   |
| deepseekv2    | ctc prefix search | full  | 0.2  | 0.8   | 20       | 1860             | 2324           | 4.48     | -0.69(13%)     |
| gpt-3.5-turbo | attention         | full  | 0.8  | 0.8   | 20       | 595              | 2651           | 5.09     | +0.03(0.5%)    |
| gpt-3.5-turbo | attention rescore | full  | 0.8  | 0.8   | 20       | 568              | 2502           | 4.69     | +0.07(1.5%)    |
| gpt-3.5-turbo | ctc greedy search | full  | 0.8  | 0.8   | 20       | 519              | 2798           | 5.20     | +0.03(0.6%)    |
| gpt-3.5-turbo | ctc prefix search | full  | 0.8  | 0.8   | 20       | 433              | 2785           | 5.21     | +0.04(0.7%)    |
| gpt-4o        | attention         | full  | 0.2  | 0.8   | 20       | 1715             | 2295           | **4.32** | -0.74(14.6%)   |
| gpt-4o        | attention rescore | full  | 0.2  | 0.8   | 20       | 1736             | 2153           | **4.01** | -0.61(13%)     |
| gpt-4o        | ctc greedy search | full  | 0.2  | 0.8   | 20       | 2075             | 2272           | 4.06     | **-1.11(21%)** |
| gpt-4o        | ctc prefix search | full  | 0.2  | 0.8   | 20       | 2137             | 2234           | 4.06     | **-1.11(21%)** |

### AISHELL-2
| Two-stage    | Decode              | Chunk  | Temp        | Top p     | Task num | Changed Sentence | Error  Sentence | CER(%)       | Change        |
| ------------ | ------------------- | ------ | ----------- | --------- | -------- | ---------------- | --------------- | ------------ | ------------- |
| -            | attention rescore   | 16     | -           | -         | -        | -                | 1715            | 5.57         | -             |
| GPT4o        | attention rescore   | 16     | 0.8         | 0.2       | 20       | 896              | 1517            | **4.95**     | -0.62(11%)    |
| deepseekv2   | attention rescore   | 16     | 0.8         | 0.8       | 20       | 223              | 1510            | 6.09         | +0.52(9%)     |
| GPT3.5-turbo | attention rescore   | 16     | 0.8         | 0.4       | 20       | 389              | 1715            | 5.65         | +0.08(1.5%)   |
### Librispeech

| Two-stage  | Decode            | Chunk | Temp | Top p | Task num | test-clean |               | test-other |                  |
| ---------- | ----------------- | ----- | ---- | ----- | -------- | ---------- | ------------- | ---------- | ---------------- |
|            |                   |       |      |       |          | WER(%)     | Change        | WER(%)     | Change           |
| -          | attention         | full  | -    | -     |          | 3.82       | 8.79          | -          |                  |
| -          | attention rescore | full  | -    | -     |          | 3.35       | 8.77          | -          |                  |
| -          | ctc greedy search | full  | -    | -     |          | 3.77       | 9.52          | -          |                  |
| -          | ctc prefix search | full  | -    | -     |          | 3.75       | 9.50          | -          |                  |
| deepseekv2 | attention         | full  | 0.8  | 0.8   | 10       | 4.58       | +0.76(19%)    | 10.11      | +1.32(-15%)      |
| deepseekv2 | attention rescore | full  | 0.8  | 0.8   | 10       | 4.21       | +0.86(25%)    | 10.42      | +1.65(18%)       |
| deepseekv2 | ctc greedy search | full  | 0.8  | 0.8   | 10       | 4.45       | +0.68(18%)    | 10.20      | +0.68(7%)        |
| deepseekv2 | ctc prefix search | full  | 0.8  | 0.8   | 10       | 4.93       | +1.18(31%)    | 9.97       | +0.47(4.9%)      |
| gpt-4o     | attention         | full  | 0.8  | 0.8   | 10       | 3.64       | -0.18(4.7%)   | **8.32**   | -0.47(5.3%)      |
| gpt-4o     | attention rescore | full  | 0.8  | 0.8   | 10       | **3.19**   | -0.16(4.7%)   | 8.38       | -0.39(4.4%)      |
| gpt-4o     | ctc greedy search | full  | 0.8  | 0.8   | 10       | 3.43       | **-0.34(9%)** | 8.45       | -1.07(11.2%)     |
| gpt-4o     | ctc prefix search | full  | 0.8  | 0.8   | 10       | 3.58       | -0.17(4.5%)   | 8.41       | **-1.09(11.4%)** |

## 致谢
感谢[wenet](https://github.com/wenet-e2e/wenet/blob/main/README.md)提供的工具和预训练模型。

## 引用

