"""Plugin to integrate Zapier into InvenTree."""

import json

from django.http import JsonResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# InvenTree plugin libs
from plugin import InvenTreePlugin
from plugin.mixins import APICallMixin, AppMixin, EventMixin, UrlsMixin


class ZapierPlugin(AppMixin, APICallMixin, EventMixin, UrlsMixin, InvenTreePlugin):
    """Integrate Zapier into InvenTree."""

    AUTHOR = "Matthias Mair"
    DESCRIPTION = "Zapier plugin for InvenTree"

    NAME = "inventree_zapier"
    SLUG = "zapier"
    TITLE = "Zapier connector for InvenTree"

    def view_connection_test(self, request):
        """For testing the connection."""
        return JsonResponse({"user": request.user.username}, safe=False)

    @csrf_exempt
    def view_event_reg(self, request):
        """Register a hook."""
        from .models import ZapierHook

        ZapierHook.objects.create(hookurl=self.get_hookurl(request))
        return JsonResponse({"response": "ok"})

    def get_hookurl(self, request):
        """Get the hookurl from the request."""
        ret = json.loads(str(request.body, "utf-8"))
        return ret.get("hookUrl")

    @csrf_exempt
    def view_event_unsub(self, request):
        """Unregister a hook."""
        from .models import ZapierHook

        obj = ZapierHook.objects.filter(hookurl=self.get_hookurl(request))
        if obj:
            obj.delete()
            return JsonResponse({"response": "ok. Hook deleted"})
        return JsonResponse({"response": "Hook not found"})

    def view_event_list(self, request):
        """For getting a sample list."""
        return JsonResponse(
            [
                {
                    "event": "instance.created",
                    "id": 1,
                    "model": "Part",
                    "table": "part.Part",
                    "args": "",
                    "kwargs": "",
                },
                {
                    "event": "instance.saved",
                    "id": 1,
                    "model": "Part",
                    "table": "part.Part",
                    "args": "",
                    "kwargs": "",
                },
            ],
            safe=False,
        )

    def process_event(self, event, *args, **kwargs):
        """Custom event processing."""
        from .models import ZapierHook

        if kwargs.get("model") == "ZapierHook":
            return

        obj = ZapierHook.objects.all()
        if obj.count() > 0:
            for item in obj:
                ret = self.api_call(
                    item.hookurl,
                    endpoint_is_url=True,
                    simple_response=False,
                    method="POST",
                    data={
                        "event": event,
                        "model": str(kwargs.get("model", "")),
                        "table": str(kwargs.get("table", "")),
                        "id": str(kwargs.get("id", "")),
                        "args": str(args),
                        "kwargs": str(kwargs),
                    },
                )
                print(ret)

    def setup_urls(self):
        """URLs for app."""
        return [
            path(r"^test/", self.view_connection_test, name="test"),
            path(r"^event/register/", self.view_event_reg, name="event-register"),
            path(r"^event/unsub/", self.view_event_unsub, name="event-unsub"),
            path(r"^event/list/", self.view_event_list, name="event-list"),
        ]
