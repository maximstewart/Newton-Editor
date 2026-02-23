# Python imports

# Lib imports

# Application imports
from libs.event_factory import Event_Factory, Code_Event_Types

from plugins.plugin_types import PluginCode

from .markdown_preview import MarkdownPreview



markdown_preview = MarkdownPreview()



class Plugin(PluginCode):
    def __init__(self):
        super(Plugin, self).__init__()


    def _set_file(self, buffer):
        event = Event_Factory.create_event(
            "get_file", buffer = buffer
        )
        self.message_to("files", event)
        if not event.response.get_location(): return

        markdown_preview.fpath = event.response.get_location().get_path()

    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.FocusedViewEvent):
            self._set_file(event.view.get_buffer())
            markdown_preview._do_markdown_translate(event.view.get_buffer())
        elif isinstance(event, Code_Event_Types.TextChangedEvent):
            self._set_file(event.buffer)
            markdown_preview._do_markdown_translate(event.buffer)

    def load(self):
        separator_right  = self.requests_ui_element("separator-right")
        markdown_preview.set_relative_to(separator_right)

        event = Event_Factory.create_event("register_command",
            command_name = "tggle_markdown_preview",
            command      = Handler,
            binding_mode = "released",
            binding      = "<Shift><Control>m"
        )

        self.message_to("source_views", event)

    def run(self):
        ...


class Handler:
    @staticmethod
    def execute(
        view: any
    ):
        logger.debug("Command: Markdown Preview")

        if not markdown_preview.can_hide:
            markdown_preview.can_hide = True

        markdown_preview.popdown() if markdown_preview.is_visible() else markdown_preview.popup()
