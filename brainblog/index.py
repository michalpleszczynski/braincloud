# coding: utf-8
import logging
import json

from elasticsearch.client import IndicesClient

from brainblog import get_es


logger = logging.getLogger(__name__)


#operation types
CREATE, UPDATE, DELETE = 1, 2, 3

#TODO: (maybe) exclude _all and _source from index
MAPPINGS = {
    'text_thought': {
        'properties': {
            'title': {'type': 'string'},
            'content': {'type': 'string'},
            'pub_date': {'type': 'date'},
            'tags': {'type': 'string'},
        }
    }
}

TEXT_QUERY = {
    'query': {
        'match_phrase_prefix': {
            '_all': ''
        }
    }
}


def _search_phrase(phrase):
    query = TEXT_QUERY.copy()
    query['query']['match_phrase_prefix']['_all'] = phrase
    return json.dumps(query)


def create_index(name):
    es = get_es()
    ic = IndicesClient(es)
    body = {'mappings': MAPPINGS}
    resp = ic.create(name, json.dumps(body))
    logger.debug('index create: ' + str(resp))


def delete_index(name):
    es = get_es()
    ic = IndicesClient(es)
    resp = ic.delete(name)
    logger.debug('index delete: ' + str(resp))


def create_thought(thought):
    es = get_es()
    user_id = thought.author_id
    from .models import TextThoughtEncoder
    thought_json = json.dumps(thought, cls=TextThoughtEncoder)
    resp = es.create(index=user_id, doc_type='text_thought', id=str(thought.id), body=thought_json)
    logger.debug('thought create: ' + str(resp))


def update_thought(thought):
    es = get_es()
    user_id = thought.author_id
    # perform upsert
    body = {'doc': thought.to_dict(), 'doc_as_upsert': 'true'}
    resp = es.update(index=user_id, doc_type='text_thought', id=str(thought.id), body=json.dumps(body))
    logger.debug('update thought: ' + str(resp))


def delete_thought(thought):
    es = get_es()
    resp = es.delete(index=thought.author_id, doc_type='text_thought', id=str(thought.id))
    logger.debug('delete thought: ' + str(resp))


def search_by_phrase(user_id, phrase):
    logger.debug('index search by phrase: ' + phrase)
    es = get_es()
    body = _search_phrase(phrase)
    resp = es.search(index=user_id, doc_type='text_thought', body=body, fields='_id')
    ids = []
    for item in resp['hits']['hits']:
        ids.append(item['_id'])
    return ids