# Python imports

# Lib imports

# Application imports
from .mixins.code_comment_tags_mixin import CodeCommentTagsMixin



class Commenter(CodeCommentTagsMixin):
    def __init__(self):
        ...


    def keyboard_tggl_comment(self, buffer):
        language   = buffer.get_language()
        if language is None: return

        start_tag, end_tag = self.get_comment_tags(language)
        # Note: Only handling line comment tag- no block comment option
        if not start_tag and not end_tag: return

        bounds = buffer.get_selection_bounds()
        if bounds:
            self._bounds_comment(
                start_tag, end_tag, bounds, buffer
            )
        else:
            self._line_comment(start_tag, end_tag, buffer)


    def _line_comment(self, start_tag, end_tag, buffer):
        start_itr = buffer.get_iter_at_mark( buffer.get_insert() ).copy()
        end_itr   = start_itr.copy()
        if not start_itr.starts_line():
            start_itr.set_line_offset(0)
        if not end_itr.ends_line():
            end_itr.forward_to_line_end()

        text = buffer.get_text(start_itr, end_itr, True)
        text = text.replace(start_tag, "") if text.startswith(start_tag) else start_tag + text

        buffer.begin_user_action()
        buffer.delete(start_itr, end_itr)
        buffer.insert(start_itr, text)
        buffer.end_user_action()


    def _bounds_comment(self, start_tag, end_tag, bounds, buffer):
        start_itr, end_itr = bounds
        if not start_itr.starts_line():
            start_itr.set_line_offset(0)
        if not end_itr.ends_line():
            end_itr.forward_to_line_end()

        text = buffer.get_text(start_itr, end_itr, True)
        text = "\n".join(
            line.replace(start_tag, "") if line.startswith(start_tag) else start_tag + line
            for line in text.splitlines()
        )

        buffer.begin_user_action()
        buffer.delete(start_itr, end_itr)
        buffer.insert(start_itr, text)
        buffer.end_user_action()

