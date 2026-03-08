# Python imports

# Lib imports

# Application imports



class CodeCommentTagsMixin:
    def get_comment_tags(self, language):
        start_tag, end_tag = self.get_line_comment_tags(language)
        if (start_tag, end_tag) == (None, None):
            start_tag, end_tag = self.get_block_comment_tags(language)

        return start_tag, end_tag

    def get_block_comment_tags(self, language):
        start_tag = language.get_metadata('block-comment-start')
        end_tag   = language.get_metadata('block-comment-end')

        if start_tag and end_tag: return (start_tag, end_tag)

        return (None, None)

    def get_line_comment_tags(self, language):
        start_tag = language.get_metadata('line-comment-start')

        if start_tag: return (start_tag, None)

        return (None, None)
