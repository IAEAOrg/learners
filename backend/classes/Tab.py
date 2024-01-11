import numbers
import string


class Tab:
    def __init__(
        self,
        name: string,
        _type: string = "",
        base_url: string = "",
        user_role: string = "participant",
        language: string = "en",
        icon: string = None,
        tooltip: string = None,
        url: string = None,
        index: numbers = 0,
        proxy: bool = False,
        show: list = ["all"],
    ):
        self.id = name
        self._type = _type
        self.icon = icon or defaultIcon(_type or name)
        self.tooltip = tooltip if tooltip else name
        self.index = index
        self.url = url if url else defaultUrl(name, user_role, language, base_url)

    def toJson(self):
        return {"id": self.id}


def defaultUrl(id: string, user_role: string, language: string, base_url: string) -> string:
    return f"{base_url}/statics/hugo/{user_role}/{language}/{id}"


def defaultIcon(name: string) -> string:
    icon_map = {
        "documentation": "clipboard-document-list",
        "hilfestellung": "clipboard-document-list",
        "exercises": "play-circle",
        "presentations": "presentation-chart-line",
        "folien": "presentation-chart-line",
        "mitre": "mitre",
        "drawio": "drawio",
        "admin": "bookmark",
        "user": "user",
        "client": "tv",
        "mattermost": "mattermost",
        "injects": "book-open",
    }

    if name in icon_map:
        return icon_map[name]
    else:
        return "document-text"
