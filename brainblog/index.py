# coding: utf-8
import logging
import json

from django.conf import settings

from elasticsearch.client import IndicesClient

from brainblog import get_es
from .models import ThoughtEncoder


logger = logging.getLogger(__name__)


#operation types
CREATE, UPDATE, DELETE = 1, 2, 3


def create_index(name):
    es = get_es()
    ic = IndicesClient(es)
    body = {'mappings': settings.MAPPINGS}
    resp = ic.create(name, json.dumps(body))
    logger.info(resp)


def create_thought(thought):
    es = get_es()
    username = thought.author
    thought_json = json.dumps(thought, cls=ThoughtEncoder)
    resp = es.create(index=username, doc_type='thought', id=str(thought.id), body=thought_json)
    logger.info(resp)


def update_thought(thought):
    es = get_es()
    username = thought.author
    # perform upsert
    body = {'doc': thought.to_dict(), 'doc_as_upsert': 'true'}
    resp = es.update(index=username, doc_type='thought', id=str(thought.id), body=json.dumps(body))
    logger.info(resp)


def delete_thought(thought):
    es = get_es()
    resp = es.delete(index=thought.author, doc_type='thought', id=str(thought.id))
    logger.info(resp)
