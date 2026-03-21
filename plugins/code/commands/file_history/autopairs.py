# Python imports

# Lib imports

# Application imports



class Autopairs:
    def __init__(self):
        ...

    def handle_word_wrap(self, buffer, char_str: str):
        wrap_block = self.get_wrap_block(char_str)
        if not wrap_block: return

        selection = buffer.get_selection_bounds()
        if not selection:
            self.insert_pair(buffer, char_str, wrap_block)
            return True

        self.wrap_selection(buffer, char_str, wrap_block, selection)

        return True

    def insert_pair(
        self, buffer, char_str: str, wrap_block: tuple
    ):
        buffer.begin_user_action()

        left_block, right_block = wrap_block
        insert_mark = buffer.get_insert()

        insert_itr = buffer.get_iter_at_mark(insert_mark)
        buffer.insert(insert_itr, f"{left_block}{right_block}")
        insert_itr = buffer.get_iter_at_mark( insert_mark )
        insert_itr.backward_char()

        buffer.place_cursor(insert_itr)

        buffer.end_user_action()

    def wrap_selection(
        self, buffer, char_str: str, wrap_block: tuple, selection
    ):
        left_block, \
        right_block = wrap_block
        start_itr,  \
        end_itr     = selection
        data        = buffer.get_text(
            start_itr, end_itr, include_hidden_chars = False
        )
        start_mark  = buffer.create_mark("startclose", start_itr, False)
        end_mark    = buffer.create_mark("endclose", end_itr, True)

        buffer.begin_user_action()

        buffer.insert(start_itr, left_block)
        end_itr = buffer.get_iter_at_mark(end_mark)
        buffer.insert(end_itr, right_block)

        start = buffer.get_iter_at_mark(start_mark)
        end   = buffer.get_iter_at_mark(end_mark)

        buffer.select_range(start, end)
        buffer.delete_mark_by_name("startclose")
        buffer.delete_mark_by_name("endclose")

        buffer.end_user_action()

    def get_wrap_block(self, char_str) -> tuple:
        left_block  = ""
        right_block = ""

        match char_str:
            case "(" | ")":
                left_block  = "("
                right_block = ")"
            case "[" | "]":
                left_block  = "["
                right_block = "]"
            case "{" | "}":
                left_block  = "{"
                right_block = "}"
            case '"':
                left_block  = '"'
                right_block = '"'
            case "'":
                left_block  = "'"
                right_block = "'"
            case "`":
                left_block  = "`"
                right_block = "`"
            case _:
                return ()

        return left_block, right_block
