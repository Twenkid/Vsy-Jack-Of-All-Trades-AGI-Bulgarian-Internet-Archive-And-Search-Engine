# VSY * ВСИ * ВСЕДЪРЖЕЦ

## Datasets

https://en.wikipedia.org/wiki/List_of_datasets_for_machine-learning_research

* Scroll: <a href="https://github.com/Twenkid/Vsy-Jack-Of-All-Trades-AGI-Bulgarian-Internet-Archive-And-Search-Engine/blob/main/notes/datasets.md/#27.1.2026">@27.1.2026</a> imagenet, COCO, LVIS, ADE20K, Places365: ~2x.1.2026; note 27.1.2026 - partial downloads, study -- no need for the whole
  
* Tools, tutorials, hf dataset, formats:

huggingface.co/docs/datasets/en/about_arrow

https://huggingface.co/datasets/legacy-datasets/wikipedia  <br>
https://huggingface.co/docs/datasets/en/loading <br>
https://huggingface.co/docs/dataset-viewer/en/filter <br>
https://huggingface.co/datasets/legacy-datasets/wikipedia/tree/main/data <br>
https://huggingface.co/datasets/legacy-datasets/wikipedia <br>
https://github.com/huggingface/datasets/blob/2.18.0/src/datasets/info.py#L92 <br>
https://huggingface.co/docs/datasets/en/about_mapstyle_vs_iterable <br>
https://huggingface.co/docs/datasets/en/tabular_load <br>
https://huggingface.co/docs/datasets/en/nlp_process <br>
https://huggingface.co/docs/datasets/en/stream  <br>
https://huggingface.co/docs/datasets/en/loading  <br>
https://huggingface.co/docs/datasets/v1.1.1/processing.html  <br>
https://huggingface.co/docs/dataset-viewer/en/filter  <br>
https://huggingface.co/docs/datasets/en/process  <br>

<br>
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html<br>
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.at.html<br>
https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes<br>
https://pandas.pydata.org/docs/reference/api/pandas.Index.html#pandas.Index<br>
https://pandas.pydata.org/docs/reference/api/pandas.Series.html#pandas.Series<br>
https://pandas.pydata.org/docs/development/extending.html#extending-extension-types<br>
https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sample.html<br>
https://github.com/daveshap/PlainTextWikipedia<br>
https://www.kaggle.com/datasets/ltcmdrdata/plain-text-wikipedia-202011<br>
https://dumps.wikimedia.org/bgwiki/latest/<br>
https://dumps.wikimedia.org/simplewiki/latest/<br>
https://lindat.mff.cuni.cz/repository/xmlui/handle/11234/1-2735<br>
<br>

Datasets-11-4-2024.ipynb: 
https://colab.research.google.com/drive/1TQwXKr9ocsU9xPyy8bJVYtlyBl08_hsb#scrollTo=OqdBsACkDrtL

Pandas_and_Datasets.ipynb: 
https://colab.research.google.com/drive/1sFbuAKKNgFiAB_dCvGX_T1P_dJDvZWQ-#scrollTo=206x9-KDY-qV

(Wiki.en ... explore. .. search with simple filters, regex etc.
```

computer = wiki.filter(lambda s: 'comput' in s['url'].lower()) # and 'cpu' in s['text']) #LOWER!!! otherwise skips /Computer etc. (may be faster with search for Computer but then will miss the others)
#wiki.filter()
#n=0
print(computer.shape)
for i in computer: print(i['url'])
#cpu = computer.filter(lambda s: 'CPU' in s['text'])
cpu = computer.filter(lambda s: 'cpu' in s['text'].lower()) #may be faster to search for CPU or cpu?
for i in cpu: print(i['url'], i['title'])
print(cpu.shape)
spec = cpu.filter(lambda s: '486' in s['text']) #computer...
print(spec.shape)
for i in spec: print(i['url'], i['title'])
span = 100
for i in spec['text']:
  f = i.find('486')
  print(f)
  if f > -1:
     print("<<<<<<<")
     print(i[int(max(f, f-span)):int(min(f+span,len(i)))])
     print(">>>>>>>")
print("====================")

for i in spec:
  f = i['text'].find('486')
  print(f)
  if f > -1:
     print("<<<<<<<")
     print(i['url'])
     print(i['title'])
     print( str(int(min(f, f-span))), str(int(min(f+span,len(i)))))
     print(i['text'][int(min(f, f-span)):int(min(f+span,len(i['text'])))])
     print(">>>>>>>")



computer_simple = simple.filter(lambda s: 'comput' in s['url'].lower()) # and 'cpu' in s['text'])
#wiki.filter()
#n=0
print(computer_simple.shape)
for i in computer_simple: print(i['url'])

(159, 4)
https://simple.wikipedia.org/wiki/Computer%20science
https://simple.wikipedia.org/wiki/Computer
https://simple.wikipedia.org/wiki/Computer%20program
https://simple.wikipedia.org/wiki/Computer%20jargon
https://simple.wikipedia.org/wiki/Computer%20hardware
https://simple.wikipedia.org/wiki/Computer%20mouse
https://simple.wikipedia.org/wiki/List%20of%20words%20about%20computers
https://simple.wikipedia.org/wiki/Computer%20graphics
https://simple.wikipedia.org/wiki/My%20Computer
https://simple.wikipedia.org/wiki/Computer%20printer
https://simple.wikipedia.org/wiki/Computer%20monitor
https://simple.wikipedia.org/wiki/Computer%20virus
https://simple.wikipedia.org/wiki/Hotspot%20%28computers%29


computer_simple_3 = computer_simple_2.filter(lambda s: s['title'].startswith('computer')) # and 'cpu' in s['text'])
#wiki.filter()
#n=0
print(computer_simple_3.shape)
for i in computer_simple_3: print(i['title']); print(i['url'])
```
### Dolma (3TB ... Olmo, Allen...), The Stack (code Github), BigScience ...

https://arxiv.org/pdf/2402.00159

https://www.semanticscholar.org/paper/The-BigScience-ROOTS-Corpus%3A-A-1.6TB-Composite-Laurenccon-Saulnier/16c64f74ce0e6a59b0709c0d8e66596a5bc08ed6

https://github.com/bigscience-workshop/data-preparation

https://arxiv.org/pdf/2402.00159

arxiv.org/abs/2211.15533

https://huggingface.co/datasets/bigcode/the-stack

https://arxiv.org/abs/2211.15533

The Stack: 3 TB of permissively licensed source code: 

https://colab.research.google.com/drive/1dDaYs2vdws1uEm9xkrRCDkvhUVATWWHS#scrollTo=0JH5SlHKy4mG

https://github.com/bigscience-workshop/data-preparation/tree/main/sourcing/cc_pseudo_crawl

https://allenai.github.io/dolma/

https://huggingface.co/datasets/allenai/dolma/tree/main

https://huggingface.co/datasets/allenai/dolma/blob/main/urls/v1_7.txt

https://olmo-data.org/dolma-v1_7/books/books-0002.json.gz

https://www.google.com/search?q=Dolma-1.7 dataset

https://huggingface.co/datasets/allenai/dolma

## Small image

https://www.kaggle.com/datasets/imbikramsaha/caltech-101/data

https://www.kaggle.com/datasets/jessicali9530/caltech256

https://docs.ultralytics.com/datasets/classify/caltech256/#what-is-the-caltech-256-dataset-and-why-is-it-important-for-machine-learning


### Domains, modalities, tasks ...

* **Maths**

Math word problem datasets: GSM, AQuA, SVAMP, TabMWP, MultiArith; Financial-QA datasets: FinQA, ConvFinQA, TATQA | https://arxiv.org/abs/2211.12588

https://huggingface.co/datasets/ChilleD/MultiArith?row=20

The Pile: An 800GB Dataset of Diverse Text for Language Modeling [Submitted on 31 Dec 2020] ... | https://arxiv.org/pdf/2101.00027 ... | ... https://huggingface.co/datasets/ArmelR/the-pile-splitted/tree/main
| ... https://huggingface.co/datasets/EleutherAI/pile


* https://github.com/RenzeLou/awesome-instruction-learning -- list to Datasets
* https://github.com/allenai/unifiedqa

----


### <a name="27.1.2026">@27.1.2026</a>

### Imagenet, COCO, LVIS, ADE20K, Places365

* Imagenet
* Download only a subset of 10-20 etc.: DONE --> generalize on; incremental features
* COCO - selective download of subsets; only 80 classes + "stuff" (not downloaded); only validation set
1. Dataset viewer - review; annotations
2. LVIS - more classes (600) similar annotations, but not the same - modifiying the viewer (started manually, completed with Claude 4.5)
3. Search for max classes 
4. ADE20K ...
5. Sample notebook - converted to normal python and run on the M93p/UBUNTU24.04 ... Petak I (P-I)
6. Places365 .. Download @ Petak I ; too slow eventually --> skip ... 50 per class slow (streaming, datasets .... 1.x-2-3 sec per item ... 24 min/370 it/ ... 29 min / 503 it ... //turned on another run and it sped up? ... 1147it /59:56 min  ; save 95% jpg -- too high quality, whatever - downloaded it as it is for nowl pet it run
7. Keep/watch/analyze -- connect the classes etc.
8. ADE20K - utliers ... special categories, rare (outliers) ...
