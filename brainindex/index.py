# coding: utf-8
import logging
import json

from django.conf import settings

from elasticsearch.client import IndicesClient

from brainblog import get_es


logger = logging.getLogger(__name__)


#operation types
CREATE, UPDATE, DELETE = 1, 2, 3

TEXT_QUERY = {
    'query': {
        'multi_match': {

        },
    }
}


def _search_phrase(phrase, fields=['title', 'content', 'tags'], size=settings.DEFAULT_RESULT_SIZE):
    query = TEXT_QUERY.copy()
    query['size'] = size
    query['query']['multi_match'].update({
        'type': 'phrase_prefix',
        'query': phrase,
        'fields': fields,
        'max_expansions': 10,
    })
    return json.dumps(query)


def create_index(name):
    es = get_es()
    ic = IndicesClient(es)
    body = {}
    # body.update(settings.INDEX_SETTINGS)
    body.update(settings.INDEX_MAPPINGS)
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
    from brainblog.models import TextThoughtEncoder
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


def search_in_title_and_tags(user_id, phrase):
    logger.debug('index search in title and tags by phrase: ' + phrase)
    es = get_es()
    body = _search_phrase(phrase, fields=['title', 'tags'], size=settings.SEARCH_BAR_RESULT_SIZE)
    resp = es.search(index=user_id, doc_type='text_thought', body=body, fields='title')
    thoughts = []
    for item in resp['hits']['hits']:
        thoughts.append({'id': item['_id'], 'title': item['fields']['title']})
    return {'thoughts': thoughts}