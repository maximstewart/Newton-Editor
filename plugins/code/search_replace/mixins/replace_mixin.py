# Python imports

# Lib imports

# Application imports



class ReplaceMixin:

    def _replace_word(
        self,
        current_index: int,
        to_text: str,
        buffer: any
    ):
        self.clear_highlight(buffer)

        start_itr, end_itr = self.matches[current_index]
        self.active_view.scroll_to_iter(end_itr, 0.2, False, 0, 0)

        buffer.begin_user_action()
        buffer.delete(start_itr, end_itr)
        buffer.insert(start_itr, to_text)
        buffer.end_user_action()

    def _replace_all_words(self, to_text: str, buffer: any):
        marks: list = []

        for start_itr, end_itr in self.matches:
            start_mark = buffer.create_mark(None, start_itr, left_gravity = True)
            end_mark   = buffer.create_mark(None, end_itr, left_gravity = False)
            marks.append((start_mark, end_mark))

        buffer.begin_user_action()

        for start_mark, end_mark in reversed(marks):
            start_itr = buffer.get_iter_at_mark(start_mark)
            end_itr   = buffer.get_iter_at_mark(end_mark)

            buffer.delete(start_itr, end_itr)
            buffer.insert(start_itr, to_text)

        buffer.end_user_action()

        for start_mark, end_mark in marks:
            buffer.delete_mark(start_mark)
            buffer.delete_mark(end_mark)

        self.find_entry.grab_focus()
