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
        self.emit_to("files", event)

        if not event.response or not event.response.get_location(): return

        markdown_preview.fpath = event.response.get_location().get_path()

    def _controller_message(self, event: Code_Event_Types.CodeEvent):
        if isinstance(event, Code_Event_Types.FocusedViewEvent):
            self._set_file(event.view.get_buffer())
            markdown_preview._do_markdown_translate(event.view.get_buffer())
        elif isinstance(event, Code_Event_Types.TextChangedEvent):
            self._set_file(event.buffer)
            markdown_preview._do_markdown_translate(event.buffer)

    def load(self):
        separator_right  = self.request_ui_element("separator-right")
        markdown_preview.set_relative_to(separator_right)

        event = Event_Factory.create_event("register_command",
            command_name = "tggle_markdown_preview",
            command      = Handler,
            binding_mode = "released",
            binding      = "<Shift><Control>m"
        )

        self.emit_to("source_views", event)

    def unload(self):
        event = Event_Factory.create_event("unregister_command",
            command_name = "tggle_markdown_preview",
            command      = Handler,
            binding_mode = "released",
            binding      = "<Shift><Control>m"
        )

        self.emit_to("source_views", event)

        markdown_preview.destroy()

    def run(self):
        ...


class Handler:
    @staticmethod
    def execute(
        view: any,
        *args,
        **kwargs
    ):
        logger.debug("Command: Markdown Preview")

        if not markdown_preview.can_hide:
            markdown_preview.can_hide = True

        if markdown_preview.is_visible():
            markdown_preview.popdown()
            return

        file   = view.command.exec("get_current_file")
        if not file or not file.get_location(): return
        buffer = view.get_buffer()

        markdown_preview.popup()
        markdown_preview.fpath = file.get_location().get_path()
        markdown_preview._do_markdown_translate(buffer)
