# Python imports

# Lib imports

# Application imports
from .markdown_template_mixin import MarkdownTemplateMixin

from .. import markdown



class MarkdownPreviewMixin(MarkdownTemplateMixin):
    def _do_markdown_translate(self, buffer):
        if self.is_preview_paused: return

        if not self.is_markdown(buffer):
            data = self.wrap_html_to_body("<h1>Not a Markdown file...</h1>")
            self._load_html(data)
            return

        data = self.get_rendered_markdown(buffer)
        self._load_html(data)

    def _load_html(self, data: str):
        self._markdown_view.load_html(
            content = data, base_uri = None
        )

    def get_rendered_markdown(self, buffer) -> str:
        start_itr = buffer.get_start_iter()
        end_itr   = buffer.get_end_iter()
        text      = buffer.get_text(start_itr, end_itr, include_hidden_chars = False)
        html      = markdown.markdown(text)

        return self.wrap_html_to_body(html)
    
    def is_markdown(self, buffer) -> bool:
        return buffer.get_language() and buffer.get_language().get_id() == "markdown"