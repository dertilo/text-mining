import os

import codecs
import re
from typing import List, NamedTuple
from util import data_io


def doc_generator(file_path):
    """
    PubTator docs are of the form:

    UID|TITLE|TEXT
    UID|ABSTRACT|TEXT
    UID   SPAN   MENTION   ENTITY_TYPE  MESH_ID
    ...

    See -- data/bioconcepts2pubtator_offsets.sample

    """
    with codecs.open(file_path, "rU", encoding="utf-8") as fp:
        lines = []
        for line in fp:
            if len(line.rstrip()) == 0:
                if len(lines) > 0:
                    # filter docs to target set
                    doc_id = re.split(r'\|', lines[0].rstrip(), maxsplit=2)
                    yield lines
                    lines = []
            else:
                lines.append(line)

def get_stable_id(doc_id):
    return "%s::document:0:0" % doc_id

def parse_annotations(content):
    annos = []
    for line in content[2:]:
        anno = line.rstrip('\n').rstrip('\r').split('\t')
        if anno[3] == 'NO ABSTRACT':
            continue
        else:

            # Handle cases where no CID is provided...
            if len(anno) == 5:
                anno.append("")

            _,starti,endi,mention,typpe,concept_id = anno
            # Handle leading / trailing whitespace
            if mention.lstrip() != mention:
                d = len(mention) - len(mention.lstrip())
                starti = int(starti) + d
                mention = mention.lstrip()

            if mention.rstrip() != mention:
                d = len(mention) - len(mention.rstrip())
                endi = int(endi) - d
                mention = mention.rstrip()

            annos.append({
                'start': starti,
                'end': endi,
                'mention': mention,
                'type': typpe,
                'concept-id': concept_id,
            })
    return annos

def pubtator_parser(content:List[str]):
    """
    based on: https://github.com/HazyResearch/snorkel-biocorpus/blob/464c8905b445a73c58cfd1d51bfcb093c21bb1f1/pubtator/parsers.py#L247
        1. PMID:       PubMed abstract identifier
        2. start:      Start-char-idx of Mention
        3. end:       End-char-idx of Mention
        7. Mention:
        4. Type:       i.e., gene, disease, chemical, species, and mutation
        6. Concept ID: Corresponding database identifier

    """
    # First line is the title
    split = re.split(r'\|', content[0].rstrip(), maxsplit=2)
    doc_id = int(split[0])

    stable_id = get_stable_id(doc_id)

    doc_text = split[2]

    # Second line is the abstract
    # Assume these are newline-separated; is this true?
    # Note: some articles do not have abstracts, however they still have this line
    doc_text += ' ' + re.split(r'\|', content[1].rstrip(), maxsplit=2)[2]

    annos = parse_annotations(content)

    return {'PMID':doc_id,
            'stable_id':stable_id,
            'text':doc_text,
            'annos':annos}


if __name__ == '__main__':

    file_path = os.environ["HOME"]+'/code/NLP/IE/pubtator/download/bioconcepts2pubtatorcentral.offset.sample'
    g = (pubtator_parser(content) for content in doc_generator(file_path))
    data_io.write_jsonl('./parsed.jsonl',g)

