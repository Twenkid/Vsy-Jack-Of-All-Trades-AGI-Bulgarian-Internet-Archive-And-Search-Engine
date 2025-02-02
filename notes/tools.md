# VSY * ВСЕДЪРЖЕЦ
## Libs and Tools etc.

* 21.8.2024
 
__*Data extraction and processing from docs and imgs:__ https://github.com/katanaml/sparrow
... forms, invoices, receipts, and other unstructured data sources. ... using tools and frameworks like LlamaIndex, Haystack, or Unstructured. Sparrow enables local LLM data extraction pipelines through Ollama or Apple MLX. ...

Currently I've used GPT4ALL with Whisper and my Autoclap and custom script, should be connected with Smarty 2 and ACS.
See also pdf ... used locally for building corpora from pdf papers.

* Async concurrency and IO and Async httplib for Py: 

https://github.com/python-trio/trio

https://github.com/theelous3/asks

* CLIP image sorter in the browser locally
https://josephrocca.github.io/clip-image-sorter/

* NAVIGU: 
https://navigu.net
https://discuss.huggingface.co/t/visual-exploration-of-the-imagenet-1k-dataset/44615 | 
https://navigu.net/#pixabay#2013/07/18/14/59/vintage-164162__340.jpg | 
https://navigu.net/#imagenet#n04127249/n04127249_460.jpg

* Imagent classes: (WN3.0)

 https://www.google.com/search?q=imagenet+synsets&oq=imagenet+synsets&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBwgBEAAYgAQyCAgCEAAYFhgeMggIAxAAGBYYHjIMCAQQABgKGA8YFhgeMg0IBRAAGIYDGIAEGIoFMg0IBhAAGIYDGIAEGIoFMg0IBxAAGIYDGIAEGIoFMg0ICBAAGIYDGIAEGIoF0gEIMjEwNGoxajeoAgCwAgA&sourceid=chrome&ie=UTF-8
 
https://www.image-net.org/challenges/LSVRC/2012/browse-synsets.php

https://gist.github.com/fnielsen/4a5c94eaa6dcdf29b7a62d886f540372


* clip embeddings explorer online

https://huggingface.co/spaces/sohojoe/soho-clip-embeddings-explorer | https://github.com/josephrocca/clip-image-sorter  | https://github.com/josephrocca/openai-clip-js


* Image embeddings and similarity search
https://nbviewer.org/github/roboflow/notebooks/blob/main/notebooks/dinov2-image-retrieval.ipynb
https://huggingface.co/docs/hub/en/open_clip
```python
!pip install open_clip_torch
import open_clip

model, preprocess = open_clip.create_model_from_pretrained('hf-hub:laion/CLIP-ViT-g-14-laion2B-s12B-b42K')
tokenizer = open_clip.get_tokenizer('hf-hub:laion/CLIP-ViT-g-14-laion2B-s12B-b42K')
import torch
from PIL import Image

url = 'http://images.cocodataset.org/val2017/000000039769.jpg'
image = Image.open(requests.get(url, stream=True).raw)
image = preprocess(image).unsqueeze(0)
text = tokenizer(["a diagram", "a dog", "a cat"])

with torch.no_grad(), torch.cuda.amp.autocast():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)
    image_features /= image_features.norm(dim=-1, keepdim=True)
    text_features /= text_features.norm(dim=-1, keepdim=True)

    text_probs = (100.0 * image_features @ text_features.T).softmax(dim=-1)

print("Label probs:", text_probs) 
```

Image Datasets: https://www.google.com/search?q=free+images+datasets+pixel&oq=free+images+datasets+pixel&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIHCAEQIRigATIHCAIQIRigAdIBCDc5ODRqMWo3qAIAsAIA&sourceid=chrome&ie=UTF-8

https://research.google/blog/introducing-the-open-images-dataset/
https://storage.googleapis.com/openimages/web/visualizer/index.html?type=localized%20narratives&set=train&c=%2Fm%2F03tz3g

Localized narratives, ... 

Visual Genome: https://homes.cs.washington.edu/~ranjay/visualgenome/index.html | https://huggingface.co/datasets/ranjaykrishna/visual_genome

* Now You See Me (CME): Concept-based Model Extraction
Dmitry Kazhdan a,c
, Botty Dimanov a,c
, Mateja Jamnika
, Pietro Liòa
and Adrian Weller
https://arxiv.org/pdf/2010.13233

Tenyks service, Botty Dimanov: "The Data-Centric Approach to Computer Vision"
https://www.tenyks.ai/  


* CRFs, WSD WN - Conditional Random Fields classifier & Word-sense disambiguation with wordnet NLTK [note 3.2.2025]

https://sklearn-crfsuite.readthedocs.io/en/latest/tutorial.html#features
  
NLPTK & pywsd
https://github.com/alvations/pywsd   

See NB Optimizations test

  

