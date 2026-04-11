# Python imports

# Lib imports
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('GtkSource', '4')

from gi.repository import Gtk
from gi.repository import GtkSource

# Application imports



class Commands:
    lsp_manager: callable = None

    class lsp_manager_toggle:
        @staticmethod
        def execute(
            source_view: GtkSource,
            char_str: str,
            modkeys_states: tuple
        ):
            logger.debug("Command: LSP Manager Toggle")
            if Commands.lsp_manager.ui_manager.is_visible():
                Commands.lsp_manager.ui_manager.hide()
            else:
                Commands.lsp_manager.ui_manager.show()

    class lsp_references:
        @staticmethod
        def execute(
            view: GtkSource,
            char_str: str,
            modkeys_states: tuple
        ):
            logger.debug("Command: LSP References")

            file   = view.command.exec("get_current_file")
            buffer = view.get_buffer()
            iter   = buffer.get_iter_at_mark( buffer.get_insert() )
            line   = iter.get_line()
            column = iter.get_line_offset()

            Commands.lsp_manager.client_manager.process_references_definition(
                file.ftype, file.fpath, line, column
            )

    class lsp_implementation:
        @staticmethod
        def execute(
            view: GtkSource,
            char_str: str,
            modkeys_states: tuple
        ):
            logger.debug("Command: LSP Implements")

            file   = view.command.exec("get_current_file")
            buffer = view.get_buffer()
            iter   = buffer.get_iter_at_mark( buffer.get_insert() )
            line   = iter.get_line()
            column = iter.get_line_offset()

            Commands.lsp_manager.client_manager.process_implementation_definition(
                file.ftype, file.fpath, line, column
            )

    class lsp_definition:
        @staticmethod
        def execute(
            view: GtkSource,
            char_str: str,
            modkeys_states: tuple
        ):
            logger.debug("Command: LSP Definition (Go-To)")

            file   = view.command.exec("get_current_file")
            buffer = view.get_buffer()
            iter   = buffer.get_iter_at_mark( buffer.get_insert() )
            line   = iter.get_line()
            column = iter.get_line_offset()

            Commands.lsp_manager.client_manager.process_definition(
                file.ftype, file.fpath, line, column
            )
