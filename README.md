# text-mining
* [BLUE](https://github.com/ncbi-nlp/BLUE_Benchmark)
* [BLINK](https://github.com/facebookresearch/BLINK)
### [BLUE-BERT](https://github.com/ncbi-nlp/bluebert)

0. `cd bluebert && pip install -r requirements.txt`
1. get blue-data: `wget https://github.com/ncbi-nlp/BLUE_Benchmark/releases/download/0.1/bert_data.zip -O tmp.zip && unzip tmp.zip && rm tmp.zip`
2. get bluebert: `wget --trust-server-names https://ftp.ncbi.nlm.nih.gov/pub/lu/Suppl/NCBI-BERT/NCBI_BERT_pubmed_mimic_uncased_L-12_H-768_A-12.zip && unzip NCBI_BERT_pubmed_mimic_uncased_L-12_H-768_A-12.zip -d bluebert`
3. train ner: 
```shell script
export PYTHONPATH=${pwd}:${PYTHONPATH}
export BlueBERT_DIR=~/data/IE/bluebert_base
export DATASET_DIR=~/data/IE/bert_data/BC5CDR/disease
export OUTPUT_DIR=output

python bluebert/run_bluebert_ner.py \
  --do_prepare=true \
  --do_train=true \
  --do_eval=true \
  --do_predict=true \
  --task_name="bc5cdr" \
  --vocab_file=$BlueBERT_DIR/vocab.txt \
  --bert_config_file=$BlueBERT_DIR/bert_config.json \
  --init_checkpoint=$BlueBERT_DIR/bert_model.ckpt \
  --num_train_epochs=30.0 \
  --do_lower_case=true \
  --data_dir=$DATASET_DIR \
  --output_dir=$OUTPUT_DIR
```
### [PubTator](https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/PubTator/)
1. get data: `wget --trust-server-names ftp://ftp.ncbi.nlm.nih.gov/pub/lu/PubTator/bioconcepts2pubtator_offsets.gz`


### sematic search

1. install sentence-transformers: `git clone https://github.com/UKPLab/sentence-transformers.git && cd sentence-transformers && pip install -e .`