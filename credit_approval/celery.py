# credit_approval/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Yeh line Django ko batati hai ki Celery ke liye settings kahan milengi
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_approval.settings')

# Celery ka main app create kar rahe hain
app = Celery('credit_approval')

# Yeh line Django ke settings file se configuration load karti hai
app.config_from_object('django.conf:settings', namespace='CELERY')

# Yeh line sab apps ke andar "tasks.py" automatically find karegi
app.autodiscover_tasks()
