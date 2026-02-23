# Python imports

# Lib imports
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk
from gi.repository import Gdk

# Application imports
from .color_converter_mixin import ColorConverterMixin



class Colorize(ColorConverterMixin):
    def __init__(self):
        super(Colorize, self).__init__()

        self.tag_stub_name: str       = "colorize-tag"
        self.is_colorize_paused: bool = True


    def handle_colorize(self, buffer):
        if self.is_colorize_paused: return

        tag_table    = buffer.get_tag_table()
        start_itr    = None
        end_itr      = buffer.get_iter_at_mark( buffer.get_insert() )

        i            = 0
        walker_iter  = end_itr.copy()
        working_tag  = self.find_working_tag(walker_iter, i)
        if working_tag:
            start_itr = self.find_start_range(walker_iter, working_tag)

            self.find_end_range(end_itr, working_tag)
            buffer.remove_tag(working_tag, start_itr, end_itr)
        else:
            start_itr = self.traverse_backward_25_or_less(walker_iter)
            self.traverse_forward_25_or_less(end_itr)

        self.do_colorize(buffer, start_itr, end_itr)

    def do_colorize(self, buffer = None, start_itr = None, end_itr = None):
        if not start_itr or not end_itr:
            start_itr = buffer.get_start_iter()
            end_itr   = buffer.get_end_iter()

        # rgb(a), hsl, hsv
        results = self.finalize_non_hex_matches(
            self.collect_preliminary_results(
                buffer, start_itr, end_itr
            )
        )
        self.process_results(buffer, results)

        # hex color search
        results = self.finalize_hex_matches(
            self.collect_preliminary_hex_results(
                buffer, start_itr, end_itr
            )
        )
        self.process_results(buffer, results)




    def collect_preliminary_results(self, buffer = None, start_itr = None, end_itr = None):
        if not buffer: return []

        if not start_itr:
            start_itr = buffer.get_start_iter()

        results1  = self.search(start_itr, end_itr, "rgb")
        results2  = self.search(start_itr, end_itr, "hsl")
        results3  = self.search(start_itr, end_itr, "hsv")

        return results1 + results2 + results3

    def find_working_tag(self, walker_iter, i):
        tags = walker_iter.get_tags()
        for tag in tags:
            if not tag.props.name or not self.tag_stub_name in tag.props.name: continue
            return tag

        result = walker_iter.backward_char()

        if not result: return
        if i > 25: return
        return self.find_working_tag(walker_iter, i + 1)

    def find_start_range(self, walker_iter, working_tag):
        tags = walker_iter.get_tags()
        for tag in tags:
            if not tag.props.name or not working_tag.props.name in tag.props.name: continue
            if not walker_iter.backward_char(): continue

            self.find_start_range(walker_iter, working_tag)

        return walker_iter

    def find_end_range(self, end_itr, working_tag):
        tags = end_itr.get_tags()
        for tag in tags:
            if not tag.props.name or not working_tag.props.name in tag.props.name: continue
            if not end_itr.forward_char(): continue

            self.find_end_range(end_itr, working_tag)

    def traverse_backward_25_or_less(self, walker_itr):
        i = 1
        while i <= 25:
            res = walker_itr.backward_char()
            if not res: break
            i += 1

    def traverse_forward_25_or_less(self, end_itr):
        i = 1
        while i <= 25:
            res = end_itr.forward_char()
            if not res: break
            i += 1

    def collect_preliminary_hex_results(
        self,
        buffer    = None,
        start_itr = None,
        end_itr   = None
    ) -> list:
        if not buffer: return []

        if not start_itr:
            start_itr = buffer.get_start_iter()

        results = self.search(start_itr, end_itr, "#")

        return results

    def search(self, start_itr = None, end_itr = None, query: str = None) -> list:
        if not start_itr or not query: return None, None

        results: list = []
        flags         = Gtk.TextSearchFlags.VISIBLE_ONLY | Gtk.TextSearchFlags.TEXT_ONLY
        while True:
            result = start_itr.forward_search(query, flags, end_itr)
            if not result: break

            results.append(result)
            start_itr = result[1]

        return results

    def finalize_non_hex_matches(self, result_hits: [] = []) -> list:
        results: list = []

        for start_itr, end_itr in result_hits:
            # If one of end chars of rgb/rgba/hsv/hsl
            if end_itr.get_char() in ["a", "b", "l", "v"]:
                end_itr.forward_char()

            # If afterwards no paren
            if end_itr.get_char() != "(":
                continue

            end_itr.forward_chars(21) # Check if best case (255, 255, 255, 0.64)
            if end_itr.get_char() == ")":
                end_itr.forward_char()
                results.append([start, end_itr])
                continue

            # Break loop if we get back to rgb/rgba/hsl/hsv -> (
            while end_itr.get_char() != "(":
                if end_itr.get_char() == ")":
                    end_itr.forward_char()
                    results.append([start_itr, end_itr])
                    break

                if not end_itr.backward_char(): break

        return results

    def finalize_hex_matches(self, result_hits: [] = []) -> list:
        results: list = []

        for start_itr, end_itr in result_hits:
            i   = 0
            _ch = end_itr.get_char()
            ch  = ord(end_itr.get_char()) if _ch else -1

            while (
                (ch >= 48 and ch <= 57) or \
                (ch >= 65 and ch <= 70) or \
                (ch >= 97 and ch <= 102)
            ):
                if i > 16: break

                i += 1
                end_itr.forward_char()
                _ch = end_itr.get_char()
                ch  = ord(end_itr.get_char()) if _ch else -1

            if i in [3, 4, 6, 8, 9, 12, 16]:
                results.append([start_itr, end_itr])

        return results

    def process_results(self, buffer, results):
        for start_itr, end_itr in results:
            text  = self.get_color_text(buffer, start_itr, end_itr)
            color = Gdk.RGBA()

            if not color.parse(text): continue

            tag = self.get_colorized_tag(buffer, text, color)
            buffer.apply_tag(tag, start_itr, end_itr)

    def get_colorized_tag(self, buffer, tag, color: Gdk.RGBA):
        tag_table    = buffer.get_tag_table()
        colorize_tag = f"{self.tag_stub_name}_{tag}"
        search_tag   = tag_table.lookup(colorize_tag)

        if not search_tag:
            search_tag = buffer.create_tag(
                colorize_tag, background_rgba = color
            )

        return search_tag

    def clear_color_tags(self, buffer):
        tag_table = buffer.get_tag_table()

        def traverse_tags(tag, user_data):
            name = tag.get_property("name")

            if not name: return
            if name.startswith(self.tag_stub_name):
                user_data.append(tag)

        tags = []
        tag_table.foreach(traverse_tags, tags)
        for tag in tags:
            tag_table.remove(tag)
