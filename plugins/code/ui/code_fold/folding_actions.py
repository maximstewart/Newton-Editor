# Python imports

# Lib imports

# Application imports



def collapse_range(view, fold):
    buffer = view.get_buffer()
    start  = buffer.get_iter_at_line(fold["start_line"] + 1)
    end    = buffer.get_iter_at_line(fold["end_line"]   + 1)

    buffer.apply_tag_by_name("invisible", start, end)


def expand_range(view, fold):
    buffer = view.get_buffer()
    start  = buffer.get_iter_at_line(fold["start_line"] + 1)
    end    = buffer.get_iter_at_line(fold["end_line"]   + 1)

    buffer.remove_tag_by_name("invisible", start, end)


