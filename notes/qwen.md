# VSY | ВСЕДЪРЖЕЦ

Notes: 30.10.2025

https://ollama.com/alibayram/Qwen3-30B-A3B-Instruct-2507  - comparable or better than GPT-4o in many benchrmarks - runs even on Tesla T4 x 2 in Kaggle 

"""
**Sampling Parameters:**

We suggest using Temperature=0.7, TopP=0.8, TopK=20, and MinP=0.
For supported frameworks, you can adjust the presence_penalty parameter between 0 and 2 to reduce endless repetitions. 
Math Problems: Include “Please reason step by step, and put your final answer within \boxed{}.” in the prompt.
Multiple-Choice Questions: Add the following JSON structure to the prompt to standardize responses: “Please show your choice in the answer field with only the choice letter, e.g., "answer": "C".”

See Agentic use.

Qwen3-4B-instruct

With Ollama:
* Qwen3-32B-MoE ... https://ollama.com/library/qwen3:32b
* Qwen3-30B-A3B-Instruct... Enhanced capabilities in 256K long-context understanding. ...   https://ollama.com/alibayram/Qwen3-30B-A3B-Instruct-2507
"Number of Parameters: 30.5B in total and 3.3B activated - Number of Paramaters (Non-Embedding): 29.9B - Number of Layers: 48 - Number of Attention Heads (GQA): 32 for Q and 4 for KV - Number of Experts: 128 - Number of Activated Experts: 8 - Context Length: 262,144 natively.
NOTE: This model supports only non-thinking mode and does not generate <think></think> blocks in its output. Meanwhile, specifying enable_thinking=False is no longer required."

https://huggingface.co/Qwen/Qwen3-32B
```
Number of Parameters: 32.8B
Number of Paramaters (Non-Embedding): 31.2B
Number of Layers: 64
Number of Attention Heads (GQA): 64 for Q and 8 for KV
Context Length: 32,768 natively and 131,072 tokens with YaRN.
```

See the Kaggle notebook with GPT-OSS-20B, Qwen-30B, Qwen-32B (slow - 2 x T4 x 10-11 GB))

...

Ollama: 
ollama run gemma3:1b
ollama run gemma3:4b
ollama run qwen3:1.7b
https://openai.com/index/introducing-gpt-oss/

https://openai.com/index/deliberative-alignment/
