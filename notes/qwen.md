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
Qwen3-32B-MoE ... https://ollama.com/library/qwen3:32b

See the Kaggle notebook with GPT-OSS-20B, Qwen-30B, Qwen-32B (slow - 2 x T4 x 10-11 GB))

...

Ollama: 
ollama run gemma3:1b
ollama run gemma3:4b
ollama run qwen3:1.7b
https://openai.com/index/introducing-gpt-oss/

https://openai.com/index/deliberative-alignment/
