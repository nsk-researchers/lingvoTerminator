# Terminator
_Intelligent Tool for Information extraction from texts written in Russian language_  

This tool includes the following modules: 
* <strong>Terms extraction</strong> — identifying phrases which fulfil the criteria for terms. 
* <strong>Relation extraction</strong> — predicting attributes and relations for entities in a sentence. 
* <strong>Entity linking</strong> — matching an entity mentioned in a text with an entity in a structured knowledge base.
* <strong>Aspect extraction</strong> — identifying and extracting terms relevant for opinion mining and sentiment analysis.

## Installation and preparation
 
If you want to try our extractor, do next steps: 

`git clone https://github.com/nsk-researchers/lingvoterminator` 

To use this tool one should download the files:
1. For terms extraction download weights file from [here](https://drive.google.com/file/d/1ed4aCPPnP4Yvl5k_OmhB8eYgnSNlcM1n/view?usp=sharing) 
and put it to `terms_extractor/dl_extractor/weights`
 
2. For relation extraction: 
 
 2.1. Download config file from [here](https://drive.google.com/file/d/1JtD3-GAs58xqrKiquFtcSsrV42DeGE0r/view?usp=sharing)
 
 2.2. Download model file from [here](https://drive.google.com/file/d/1ksg-ZXDa8Fd10w3wPNxU8j-bk8B2YhTb/view?usp=sharing)
 
 2.3. Download model arguments file from [here](https://drive.google.com/file/d/1IvCCwj7-68MFx71bFX9kkUm_A1RQzxs-/view?usp=sharing) and put it all to `relation_extractor/dl_relation_extractor/weights`

3. For entity linking:  

 3.1. Download prepocessed wikidata dump from [here](https://drive.google.com/file/d/1cSWLrbpq3f4PtRkAgIKiw_UNhshTgQOx/view?usp=sharing),
  unzip and put it to `entity_linker/wikidata_dump`;  
 
 3.2. Download fasttext model from [here](http://files.deeppavlov.ai/embeddings/ft_native_300_ru_wiki_lenta_remstopwords/ft_native_300_ru_wiki_lenta_remstopwords.bin)
 and put it to `entity_linker/fasttext_model`.

4. For aspect extraction download weights file from [here](https://drive.google.com/file/d/1uHjHWm4CC19TPCzVr1Jy-f_XAWr7hyA6/view?usp=sharing)
and put it to `aspect_extractor/weights`
## How to use

### Terms extraction
 
This module extracts terms from the raw text. 
 
```python
from terms_extractor.combined_extractor.combined_extractor import CombinedExtractor   

combined_extractor = CombinedExtractor()
text = 'Научные вычисления включают прикладную математику (особенно численный анализ), вычислительную технику ' \
       '(особенно высокопроизводительные вычисления) и математическое моделирование объектов изучаемых научной ' \
       'дисциплиной.'
result = combined_extractor.extract(text)
for token, tag in result:
    print(f'{token} -> {tag}')
```

### Relation extraction

This module extracts relations between two terms. 
To extract relations it requires text with terms highlighted by special tokens.

Example of relation extraction:

```python
from relation_extractor.combined_relation_extractor.combined_relation_extractor import CombinedRelationExtractor

combined_extractor = CombinedRelationExtractor()
sample = '<e1>Модель</e1> используется в методе генерации и определения форм слов для решения ' \ 
         '<e2>задач морфологического синтеза</e2> и анализа текстов.'

relation = combined_extractor.extract(sample) 
```

### Entity linking

This module links terms with entities in Wikidata. 
It requires extracted terms and their context as input.  

```python
from entity_linker.entity_linker import RussianEntityLinker

ru_el = RussianEntityLinker()
term = 'язык программирования Python'
context = ['язык программирования Python', 'использовался', 'в']
print(ru_el.get_linked_mention(term, context))
```

### Aspect extraction

This module extracts aspects from the raw text. 

```python
from aspect_extractor import AspectExtractor  

extractor = AspectExtractor()
text = "Определена модель для визуализации связей между объектами и их атрибутами в различных процессах. " \
           "На основании модели разработан универсальный абстрактный компонент графического пользовательского интерфейса и приведены примеры его программной реализации. " \
           "Также проведена апробация компонента для решения прикладной задачи по извлечению информации из документов."
result = extractor.extract(text)
for token, tag in result:
    print(f'{token} -> {tag}')
```

## Citation 

If you use this project, please cite this paper:

Elena Bruches, Anastasia Mezentseva, Tatiana Batura. 
A system for information extraction from scientific texts in Russian. 2021.

Link: https://arxiv.org/abs/2109.06703  
 
