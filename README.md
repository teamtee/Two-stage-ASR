# Two Stage Automatic Speech Recognition System With Large Language Model

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

### Testing LLM Capabilities
1. Fill in the `config/test/Chinese/gpt.yaml` configuration file.
2. Run the test script:

    ```bash
    python tools/test_model_capability.py
    ```

    Results will be printed directly and need to be recorded manually. The testing process may take a long time without multithreading.

You can also fill in a new test

## Acknowledgments
Thanks to [wenet](https://github.com/wenet-e2e/wenet/blob/main/README.md) for providing tools and pre-trained models.

## Citation