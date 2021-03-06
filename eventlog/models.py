import decimal

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
import jsonfield
from .signals import event_logged
import json
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.forms.jsonb import (
    InvalidJSONInput,
    JSONField as JSONFormField,
)


class UTF8JSONFormField(JSONFormField):

    def prepare_value(self, value):
        if isinstance(value, InvalidJSONInput):
            return value
        return json.dumps(value, ensure_ascii=False)


class UTF8JSONField(JSONField):
    """JSONField for postgres databases.

    Displays UTF-8 characters directly in the admin, i.e. äöü instead of
    unicode escape sequences.
    """

    def formfield(self, **kwargs):
        return super().formfield(**{
            **{'form_class': UTF8JSONFormField},
            **kwargs,
        })


class Log(models.Model):
    user = models.ForeignKey(
        getattr(settings, "AUTH_USER_MODEL", "auth.User"),
        null=True,
        on_delete=models.SET_NULL
    )
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)
    action = models.CharField(max_length=50, db_index=True)
    content_type = models.ForeignKey(ContentType, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(null=True)
    obj = GenericForeignKey("content_type", "object_id")
    extra = UTF8JSONField()

    @property
    def template_fragment_name(self):
        return "pinax/eventlog/{}.html".format(self.action.lower())

    class Meta:
        ordering = ["-timestamp"]


class LogginMixin(object):
    def log(self, user, action, extra=None, obj=None, dateof=None):
        if user is not None and not user.is_authenticated:
            user = None

        if extra is None:
            extra = {}
        else:  # Decimal insert시 에러발생
            for key, value in extra.items():
                if isinstance(value, decimal.Decimal):
                    extra[key] = float(value)

        content_type = None
        object_id = None

        if obj is not None:
            content_type = ContentType.objects.get_for_model(obj)
            object_id = obj.pk

        if dateof is None:
            dateof = timezone.now()

        event = Log.objects.create(
            user=user,
            action=action,
            extra=extra,
            content_type=content_type,
            object_id=object_id,
            timestamp=dateof
        )
        event_logged.send(sender=Log, event=event)
        return event