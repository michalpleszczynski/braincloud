from elasticsearch import Elasticsearch

from django.conf import settings

DEFAULT_URLS = [settings.ELASTICSEARCH_URL]
DEFAULT_TIMEOUT = 5

"""
Copied from https://github.com/mozilla/elasticutils/blob/master/elasticutils/__init__.py
"""


def _build_key(urls, timeout, **settings):
    # Order the settings by key and then turn it into a string with
    # repr. There are a lot of edge cases here, but the worst that
    # happens is that the key is different and so you get a new
    # Elasticsearch. We'll probably have to tweak this.
    settings = sorted(settings.items(), key=lambda item: item[0])
    settings = repr([(k, v) for k, v in settings])

    # elasticsearch allows urls to be a string, so we make sure to
    # account for that when converting whatever it is into a tuple.
    if isinstance(urls, basestring):
        urls = (urls,)
    else:
        urls = tuple(urls)

    # Generate a tuple of all the bits and return that as the key
    # because that's hashable.
    key = (urls, timeout, settings)
    return key

_cached_elasticsearch = {}


def get_es(urls=None, timeout=DEFAULT_TIMEOUT, force_new=False, **settings):
    """Create an elasticsearch `Elasticsearch` object and return it.

This will aggressively re-use `Elasticsearch` objects with the
following rules:

1. if you pass the same argument values to `get_es()`, then it
will return the same `Elasticsearch` object
2. if you pass different argument values to `get_es()`, then it
will return different `Elasticsearch` object
3. it caches each `Elasticsearch` object that gets created
4. if you pass in `force_new=True`, then you are guaranteed to get
a fresh `Elasticsearch` object AND that object will not be
cached

:arg urls: list of uris; Elasticsearch hosts to connect to,
defaults to ``['http://localhost:9200']``
:arg timeout: int; the timeout in seconds, defaults to 5
:arg force_new: Forces get_es() to generate a new Elasticsearch
object rather than pulling it from cache.
:arg settings: other settings to pass into Elasticsearch
constructor; See
`<http://elasticsearch.readthedocs.org/>`_ for more details.

Examples::

# Returns cached Elasticsearch object
es = get_es()

# Returns a new Elasticsearch object
es = get_es(force_new=True)

es = get_es(urls=['localhost'])

es = get_es(urls=['localhost:9200'], timeout=10,
max_retries=3)

"""
    # Cheap way of de-None-ifying things
    urls = urls or DEFAULT_URLS

    if not force_new:
        key = _build_key(urls, timeout, **settings)
        if key in _cached_elasticsearch:
            return _cached_elasticsearch[key]

    es = Elasticsearch(urls, timeout=timeout, **settings)

    if not force_new:
        # We don't need to rebuild the key here since we built it in
        # the previous if block, so it's in the namespace. Having said
        # that, this is a little ew.
        _cached_elasticsearch[key] = es

    return es