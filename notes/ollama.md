# Ollama cheatsheet ...
```
https://github.com/ollama/ollama-python/issues/101
https://github.com/ollama/ollama-python/blob/main/ollama/_client.py

  return self._request(
      GenerateResponse,
      'POST',
      '/api/generate',
      json=GenerateRequest(
        model=model,
        prompt=prompt,
        suffix=suffix,
        system=system,
        template=template,
        context=context,
        stream=stream,
        think=think,
        raw=raw,
        format=format,
        images=list(_copy_images(images)) if images else None,
        options=options,
        keep_alive=keep_alive,
      ).model_dump(exclude_none=True),
      stream=stream,
    )

```

https://github.com/ollama/ollama-python/issues/101
<img width="616" height="778" alt="image" src="https://github.com/user-attachments/assets/1059dfe8-4be2-4466-81f0-5e3a6c1c7796" />

...
stream = true ...


'''
Kaggle:

os.environ['OLLAMA_NUM_GPU'] = '2'  # Use both T4 GPUs
os.environ['OLLAMA_GPU_LAYERS'] = '35'  # Adjust

nvidia-smi -L
...
os.environ["CUDA_VISIBLE_DEVICES"] = "GPU-...123456-..." #1060 et.

os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['CUDA_VISIBLE_DEVICES'] = '1'
os.environ['CUDA_VISIBLE_DEVICES'] = '0,1'


17.10.2025 г. 
set CUDA_VISIBLE_DEVICES=0
```
```
c:\PY\2025\ollama>ollama serve
time=2025-10-16T15:28:45.149+03:00 level=INFO source=routes.go:1481 msg="server config" env="map[CUDA_VISIBLE_DEVICES:0 GPU_DEVICE_ORDINAL: HIP_VISIBLE_DEVICES: HSA_OVERRIDE_GFX_VERSION: HTTPS_PROXY: HTTP_PROXY: NO_PROXY: OLLAMA_CONTEXT_LENGTH:4096 OLLAMA_DEBUG:INFO OLLAMA_FLASH_ATTENTION:false OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://127.0.0.1:11434 OLLAMA_INTEL_GPU:false OLLAMA_KEEP_ALIVE:5m0s OLLAMA_KV_CACHE_TYPE: OLLAMA_LLM_LIBRARY: OLLAMA_LOAD_TIMEOUT:5m0s OLLAMA_MAX_LOADED_MODELS:0 OLLAMA_MAX_QUEUE:512 OLLAMA_MODELS:C:\\Users\\toshb\\.ollama\\models OLLAMA_MULTIUSER_CACHE:false OLLAMA_NEW_ENGINE:false OLLAMA_NOHISTORY:false OLLAMA_NOPRUNE:false OLLAMA_NUM_PARALLEL:1 OLLAMA_ORIGINS:[http://localhost https://localhost http://localhost:* https://localhost:* http://127.0.0.1 https://127.0.0.1 http://127.0.0.1:* https://127.0.0.1:* http://0.0.0.0 https://0.0.0.0 http://0.0.0.0:* https://0.0.0.0:* app://* file://* tauri://* vscode-webview://* vscode-file://*] OLLAMA_REMOTES:[ollama.com] OLLAMA

```

In order to use multiple GPU separately and avoid automatic allocation - turn off already running Ollama Windows program.
If one is running setting may not have the desired effect.
Spilling between GPUs of that kind might be slower than running independent threads due to memory overheads and unequal performance of the GPUs.
E.g. gemma3:4B on the 1060 - and gemma3:1b on the 750 Ti, or two 1b on both, reaching up to 60 tok/s on 1060 and 23 on 750 Ti and this machine (Core i5 6500)


**Setup:**
Two CUDA GPUs:
0: Geforce 1060 3 GB
1: Geforce 750 Ti 2 GB
Windows 10


Create console 1, cmd: #1
set CUDA_VISIBLE_DEVICES=0
ollama serve

#no quotes in set ...
time=2025-10-26T23:33:49.825+02:00 level=INFO source=routes.go:1481 msg="server config" env="map[CUDA_VISIBLE_DEVICES:0 GPU_DEVICE_ORDINAL: HIP_VISIBLE_DEVICES: HSA_OVERRIDE_GFX_VERSION: HTTPS_PROXY: HTTP_PROXY: NO_PROXY: OLLAMA_CONTEXT_LENGTH:4096 OLLAMA_DEBUG:INFO OLLAMA_FLASH_ATTENTION:false OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://127.0.0.1:11434 OLLAMA_INTEL_GPU:false OLLAMA_KEEP_ALIVE:5m0s OLLAMA_KV_CACHE_TYPE: OLLAMA_LLM_LIBRARY: OLLAMA_LOAD_TIMEOUT:5m0s OLLAMA_MAX_LOADED_MODELS:0 OLLAMA_MAX_QUEUE:512 OLLAMA_MODELS:C:\\Users\\toshb\\.ollama\\models OLLAMA_MULTIUSER_CACHE:false OLLAMA_NEW_ENGINE:false OLLAMA_NOHISTORY:false OLLAMA_NOPRUNE:false OLLAMA_NUM_PARALLEL:1 OLLAMA_ORIGINS:[http://localhost https://localhost http://localhost:* https://localhost:* http://127.0.0.1 https://127.0.0.1 http://127.0.0.1:* https://127.0.0.1:* http://0.0.0.0 https://0.0.0.0 http://0.0.0.0:* https://0.0.0.0:* app://* file://* tauri://* vscode-webview://* vscode-file://*] OLLAMA_REMOTES:[ollama.com] OLLAMA_SCHED_SPREAD:false ROCR_VISIBLE_DEVICES:]"
time=2025-10-26T23:33:49.855+02:00 level=INFO source=images.go:522 msg="total blobs: 36"
time=2025-10-26T23:33:49.858+02:00 level=INFO source=images.go:529 msg="total unused blobs removed: 0"
time=2025-10-26T23:33:49.861+02:00 level=INFO source=routes.go:1534 msg="Listening on 127.0.0.1:11434 (version 0.12.5)"
time=2025-10-26T23:33:49.862+02:00 level=INFO source=runner.go:80 msg="discovering available GPUs..."
time=2025-10-26T23:33:51.003+02:00 level=INFO source=types.go:112 msg="inference compute" id=GPU-... library=CUDA compute=6.1 name=CUDA0 description="NVIDIA GeForce GTX 1060 3GB" libdirs=ollama,cuda_v12 driver=12.6 pci_id=01:00.0 type=discrete total="3.0 GiB" available="2.2 GiB"
time=2025-10-26T23:33:51.004+02:00 level=INFO source=routes.go:1575 msg="entering low vram mode" "total vram"="3.0 GiB" threshold="20.0 GiB"

//Default: OLLAMA_HOST:http://127.0.0.1:11434 
(127.0.0.1:11434)

...

start cmd #2
set OLLAMA_HOST="http://127.0.0.1:11435"
python: import os; os.environ["OLLAMA_HOST"]="http://127.0.0.1:11435"
set CUDA_VISIBLE_DEVICES=1
ollama serve
--> 127.0.0.1:11435
#no quotes


start cmd  #3

python qwen3_...
py39 ...

client ...
...
ollama run gemma3:1b --verbose
ollama run gemma3:4b --verbose
ollama run qwen3:4b --verbose
...

ollama


set CUDA_VISIBLE_DEVICES=1 && set OLLAMA_HOST="http://127.0.0.1:11435" && ollama run gemma3:1b --verbose
ollama run gemma3:1b --verbose
...

Just:
ollama run ...
creates a server

c:\PY\2025\ollama

...
Watch GPUs memory, load:

CPUID HWmonitor
nvidia-smi...
