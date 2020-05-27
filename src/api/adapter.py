from typing import Final

from requests.adapters import HTTPAdapter

TIME_OUT: Final = 3.05


class APIAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self._time_out = TIME_OUT
        if "timeout" in kwargs:
            self._time_out = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        if kwargs.get("timeout") is None:
            kwargs["timeout"] = self._time_out
        return super().send(request, **kwargs)
