# Two Stage Automatic Speech Recognition System With Large Language Model
[中文文档](./README_Chinise.md)
## Project Overview
Developed by the Dain team at Huazhong University of Science and Technology, this project aims to integrate large language models (LLMs) into ASR systems to improve recognition accuracy. Note that the current work is based on the framework of existing datasets and requires pre-recognized text files.

### Workflow Diagram
![Two Stage Recognition Workflow](./two_stage_recognition.png)

## Usage Guide

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configuration File Settings
1. **Select and Edit Configuration File**: Choose the appropriate configuration file in the `config` directory based on the API provider.
2. **Fill in API Information**: Example:

    ```yaml
    # Example: gpt_conformer.yaml
    provider: openai
    model: gpt-3.5-turbo
    api_key: YOUR_API_KEY
    base_url: YOUR_BASE_URL

    # Example: azure_conformer.yaml
    provider: azure
    model: gpt4o
    api_key: YOUR_API_KEY
    base_url: YOUR_AZURE_ENDPOINT
    api_version: YOUR_API_VERSION
    ```

3. **Specify Text Path and Label Information**:

    ```yaml
    path:
        example1: "path_to_text1"
        example2: "path_to_text2"
    text: "path_to_label"
    ```

4. **Set Parameters**: Adjust parameters based on the task language.

    ```yaml
    combination_num: 30 # Number of sentences per request
    thread_num: 100 # Number of concurrent threads
    temperature: 0.2
    max_repeat_times: 1 # Number of repeat inquiries
    top_p: 0.8
    ```

5. **Add Prompt**: Add as needed in the configuration file. Refer to [PromptList](./config/PromptList.md)

    ```yaml
    prompt: "Your custom prompt here"
    ```

6. **Configuration File Path**: Specify the configuration file path in `main.py`.

    ```python
    with open("path_to_your_config", 'r') as f:
    ```

7. **Run the Program**: Execute the command and generate the result directory.

    ```bash
    python main.py
    ```

### Contents of Result Directory
- `config`: The configuration file used.
- `diff`: Details of text modifications.
- `err`: Error examples.
- `response`: Responses from the LLM.
- `skips`: Texts skipped based on filter settings.
- `text`: Modified texts.
- `total`: Statistical results.
- `wer`: Word error rate files.
- `wrong_sentence`: List of incorrect sentences.

### Notes

- Tokens: Using the Deepseekv2 model, the token consumption on the AISHELL-1 and Librispeech datasets is 250k(input)+260k(output) and 640k(input)+650k(output) respectively, with the combination numbers set to 30 and 10.
- You can see the historical results in the result directory

### Testing LLM Capabilities
1. Fill in the `config/test/Chinese/gpt.yaml` configuration file.
2. Run the test script:

    ```bash
    python tools/test_model_capability.py
    ```

    Results will be printed directly and need to be recorded manually. The testing process may take a long time without multithreading.

You can also fill in a new test
## Result
### AISHELL-1
| Model                | Decode Method | Chunk API Params | Task | num | sentence | CER(%) | Change | Temp | Top p | Change Error |
|---------------------|---------------|------------------|------|-----|----------|---------|--------|------|--------|--------------|
| attention            | full          | -                | -    | -   | -        | 5.06    | -      | -    | -      | -            |
| attention rescore    | full          | -                | -    | -   | -        | 4.62    | -      | -    | -      | -            |
| ctc greedy search    | full          | -                | -    | -   | -        | 5.17    | -      | -    | -      | -            |
| ctc prefix search    | full          | -                | -    | -   | -        | 5.17    | -      | -    | -      | -            |
| deepseekv2 attention | full          | 0.2 0.8 20       | -    | 1568| 2365     | 4.69    | -0.37   | -    | -      | 7.3%         |
| deepseekv2 attention rescore | full | 0.2 0.8 20       | -    | 1451| 2189     | 4.21    | -0.41   | -    | -      | 8.8%         |
| deepseekv2 ctc greedy search | full | 0.2 0.8 20       | -    | 1892| 2331     | 4.51    | -0.66   | -    | -      | 12.7%        |
| deepseekv2 ctc prefix search | full | 0.2 0.8 20       | -    | 1860| 2324     | 4.48    | -0.69   | -    | -      | 13%          |
| gpt-3.5-turbo attention | full | 0.8 0.8 20       | -    | 595 | 2651     | 5.09    | +0.03   | -    | -      | 0.5%         |
| gpt-3.5-turbo attention rescore | full | 0.8 0.8 20       | -    | 568 | 2502     | 4.69    | +0.07   | -    | -      | 1.5%         |
| gpt-3.5-turbo ctc greedy search | full | 0.8 0.8 20       | -    | 519 | 2798     | 5.20    | +0.03   | -    | -      | 0.6%         |
| gpt-3.5-turbo ctc prefix search | full | 0.8 0.8 20       | -    | 433 | 2785     | 5.21    | +0.04   | -    | -      | 0.7%         |
| gpt-4o attention     | full          | 0.2 0.8 20       | -    | 1715| 2295     | 4.32    | -0.74   | -    | -      | 14.6%        |
| gpt-4o attention rescore | full | 0.2 0.8 20       | -    | 1736| 2153     | 4.01    | -0.61   | -    | -      | 13%          |
| gpt-4o ctc greedy search | full | 0.2 0.8 20       | -    | 2075| 2272     | 4.06    | -1.11   | -    | -      | 21%          |
| gpt-4o ctc prefix search | full | 0.2 0.8 20       | -    | 2137| 2234     | 4.06    | -1.11   | -    | -      | 21%          |

### AISHELL-2
| Model               | Decode Method      | Chunk API Params | Task | num   | sentence | CER(%) | Change    | Temp | Top p | Changed Error |
|---------------------|--------------------|------------------|------|-------|----------|---------|-----------|------|--------|---------------|
| attention rescore   | -                  | 16               | -    | 1715  | -        | 5.57    | -         | -    | -      | -             |
| GPT4o attention rescore | -                | 16               | 0.8  | 896   | 1517     | 4.95    | -0.62(11%) | 0.2  | -      | 11%           |
| deepseekv2 attention rescore | -          | 16               | 0.8  | 223   | 1510     | 6.09    | +0.52(9%)  | 0.8  | -      | 9%            |
| GPT3.5-turbo attention rescore | -      | 16               | 0.8  | 389   | 1715     | 5.65    | +0.08(1.5%)| 0.4  | -      | 1.5%          |


### Librispeech

| Model                  | Decode Method    | Chunk API Params | Task | Temp   | Top p | test-clean WER(%) | Change test-clean | test-other WER(%) | Change test-other |
|------------------------|------------------|------------------|------|--------|--------|-------------------|-------------------|-------------------|-------------------|
| attention              | full             | -                | -    | -      | -      | 3.82              | -                 | 8.79              | -                 |
| attention rescore      | full             | -                | -    | -      | -      | 3.35              | -                 | 8.77              | -                 |
| ctc greedy search      | full             | -                | -    | -      | -      | 3.77              | -                 | 9.52              | -                 |
| ctc prefix search      | full             | -                | -    | -      | -      | 3.75              | -                 | 9.50              | -                 |
| deepseekv2 attention   | full             | 0.8 0.8 10       | -    | 0.8    | 0.8    | 4.58              | +0.76(19%)        | 10.11            | +1.32(-15%)       |
| deepseekv2 attention rescore | full   | 0.8 0.8 10       | -    | 0.8    | 0.8    | 4.21              | +0.86(25%)        | 10.42            | +1.65(18%)        |
| deepseekv2 ctc greedy search | full | 0.8 0.8 10       | -    | 0.8    | 0.8    | 4.45              | +0.68(18%)        | 10.20            | +0.68(7%)         |
| deepseekv2 ctc prefix search | full | 0.8 0.8 10       | -    | 0.8    | 0.8    | 4.93              | +1.18(31%)        | 9.97             | +0.47(4.9%)       |
| gpt-4o attention       | full             | 0.8 0.8 10       | -    | 0.8    | 0.8    | 3.64              | -0.18(4.7%)       | 8.32             | -0.47(5.3%)       |
| gpt-4o attention rescore | full   | 0.8 0.8 10       | -    | 0.8    | 0.8    | 3.19              | -0.16(4.7%)       | 8.38             | -0.39(4.4%)       |
| gpt-4o ctc greedy search | full   | 0.8 0.8 10       | -    | 0.8    | 0.8    | 3.43              | -0.34(9%)         | 8.45             | -1.07(11.2%)      |
| gpt-4o ctc prefix search | full   | 0.8 0.8 10       | -    | 0.8    | 0.8    | 3.58              | -0.17(4.5%)       | 8.41             | -1.09(11.4%)      |
## Acknowledgments
Thanks to [wenet](https://github.com/wenet-e2e/wenet/blob/main/README.md) for providing tools and pre-trained models.

## Citation
