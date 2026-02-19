# Python imports

# Lib imports

# Application imports



class InvalidPluginException(Exception):
    ...



class PluginsControllerMixin:

    def requests_ui_element(self, target_id: str):
        if not target_id in widget_registery.objects:
            raise InvalidPluginException('Unknown UI "target_id" given in requests.')

        return widget_registery.objects[target_id]
