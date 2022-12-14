import os
import json
from typing import List, Dict, Set, Any

import orjson

from utils.paths import ENTITY_LINKER
from entity_linker.entity_linking_pipeline.candidates_generator import BaseCandidatesGenerator


class StringMatchCandidatesGenerator(BaseCandidatesGenerator):
    """ Генерация кандидатов по построковому совпадению """

    def __init__(self, config, is_use_predefined_candidates=False):
        super().__init__(config)
        self._predefined_candidates = None
        if is_use_predefined_candidates:
            predefined_dump_path = os.path.join(ENTITY_LINKER, 'additional_data/predicted_entities_dump.json')
            with open(predefined_dump_path, 'r') as f:
                self._predefined_candidates = json.load(f)

    def create_candidates_set(self, normalized_term: str, queries: Set[str]):
        if self._predefined_candidates:
            candidates = self._predefined_candidates[normalized_term]
        else:
            candidates = self._get_string_match_candidates(normalized_term, queries)
        return candidates

    def _get_string_match_candidates(self, normalized_term: str, queries: Set[str]) -> List[Dict[str, Any]]:
        result = list()
        print(f'iter dump for entity [{normalized_term}]...')
        with open(self._dump_path, 'r') as f:
            for line in f:
                if line == '\n':
                    continue
                try:
                    entity = orjson.loads(line)
                except orjson.JSONDecodeError:
                    continue
                if entity['type'] != 'item':
                    continue
                entity_names = set()
                if 'label' in entity:
                    entity_names.add(entity['label']['value'].lower())
                if 'alias' in entity:
                    for alias in entity['alias']:
                        entity_names.add(alias.lower())
                desc = ''
                if 'description' in entity:
                    desc = entity['description']['value']
                    if 'страница значений' in desc.lower():
                        continue
                if normalized_term in entity_names:
                    result.append({'id': entity['id'], 'desc': desc, 'names': list(entity_names)})
                else:
                    for t in queries:
                        if t in entity_names:
                            result.append({'id': entity['id'], 'desc': desc, 'names': list(entity_names)})
                            break
        return result