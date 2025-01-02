# mi_proyecto/_init_.py
from __future__ import absolute_import, unicode_literals

# Importar Celery
from kiaJC.celery import app as celery_app

_all_ = ['celery_app']