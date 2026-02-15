# Python imports

# Lib imports

# Application imports



class InvalidPluginException(Exception):
    ...



class PluginsControllerMixin:

    def requests_ui_element(self, target_id: str):
        builder   = settings_manager.get_builder()
        ui_target = builder.get_object(target_id)

        if not ui_target:
            raise InvalidPluginException('Unknown "target_id" given in requests.')

        return ui_target
