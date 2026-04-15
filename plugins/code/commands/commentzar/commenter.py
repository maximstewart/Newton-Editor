# Python imports

# Lib imports

# Application imports
from .mixins.code_comment_tags_mixin import CodeCommentTagsMixin



class Commenter(CodeCommentTagsMixin):
    def __init__(self):
        ...


    def keyboard_tggl_comment(self, buffer):
        language = buffer.get_language()
        if not language: return

        start_tag, end_tag = self.get_comment_tags(language)
        if not (start_tag or end_tag): return

        start_tag += " "
        end_tag    = end_tag or ""
        bounds     = buffer.get_selection_bounds()

        (self._bounds_comment if bounds else self._line_comment)(
            buffer, start_tag, end_tag, bounds
        )

    def _line_comment(self, buffer, start_tag: str, end_tag: str, bounds):
        start = buffer.get_iter_at_mark(buffer.get_insert()).copy()
        end   = start.copy()
        line, col = start.get_line() + 1, start.get_line_offset()

        if not start.starts_line():
            start.set_line_offset(0)
        if not end.ends_line():
            end.forward_to_line_end()

        text     = buffer.get_text(start, end, True)
        stripped = text.lstrip()
        indent   = text[:-len(stripped)] if stripped else text

        if stripped.startswith(start_tag):
            stripped = stripped[len(start_tag):].lstrip().replace(end_tag, "", 1)
        else:
            stripped = f"{start_tag}{stripped}{end_tag}"

        buffer.begin_user_action()
        buffer.delete(start, end)
        buffer.insert(start, indent + stripped)
        buffer.end_user_action()

        buffer.place_cursor(buffer.get_iter_at_line_offset(line, col))

    def _bounds_comment(self, buffer, start_tag: str, end_tag: str, bounds):
        def indent_len(s): return len(s) - len(s.lstrip())

        def insert(line, idx):
            return f"{line[:idx]}{start_tag}{line[idx:]}{end_tag}"

        def process(lines):
            base_indent = min(
                (indent_len(l) for l in lines if l.strip()),
                default = 0
            )

            is_commented = all(
                l.lstrip().startswith(start_tag)
                for l in lines if l.strip()
            )

            if is_commented:
                return [
                    l.replace(start_tag, "", 1).replace(end_tag, "", 1)
                    if l.lstrip().startswith(start_tag.lstrip())
                    else l
                    for l in lines
                ]

            return [
                l if not l.strip()
                else insert(l, base_indent)
                for l in lines
            ]

        start, end  = bounds
        sline, scol = start.get_line(), start.get_line_offset()
        eline, ecol = end.get_line(), end.get_line_offset()

        if not start.starts_line():
            start.set_line_offset(0)
        if not end.ends_line():
            end.forward_to_line_end()

        lines    = buffer.get_text(start, end, True).splitlines()
        new_text = "\n".join(process(lines))

        buffer.begin_user_action()
        buffer.delete(start, end)
        buffer.insert(start, new_text)
        buffer.end_user_action()

        buffer.select_range(
            buffer.get_iter_at_line_offset(sline, scol),
            buffer.get_iter_at_line_offset(eline, ecol),
        )
