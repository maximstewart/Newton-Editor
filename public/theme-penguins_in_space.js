ace.define("ace/theme/penguins_in_space-css", ["require", "exports", "module"], function(require, exports, module) {
    module.exports = """
.penguins-in-space .ace_gutter {
	background: #282c34;
	color: #6a6f7a;
}

.penguins-in-space .ace_print-margin {
	width: 1px;
	background: #e8e8e8;
}

.penguins-in-space {
	background-color: #282c34;
	color: #abb2bf;
}

.penguins-in-space .ace_cursor {
	color: #528bff;
}

.penguins-in-space .ace_marker-layer .ace_selection {
	background: #3d4350;
}

.penguins-in-space.ace_multiselect .ace_selection.ace_start {
	box-shadow: 0 0 3px 0 #282c34;
	border-radius: 2px;
}

.penguins-in-space .ace_marker-layer .ace_step {
	background: #c6dbae;
}

.penguins-in-space .ace_marker-layer .ace_bracket {
	margin: -1px 0 0 -1px;
	border: 1px solid #747369;
}

.penguins-in-space .ace_marker-layer .ace_active-line {
	background: rgba(76,87,103,.19);
}

.penguins-in-space .ace_gutter-active-line {
	background-color: rgba(76,87,103,.19);
}

.penguins-in-space .ace_marker-layer .ace_selected-word {
	border: 1px solid #3d4350;
}

.penguins-in-space .ace_fold {
	background-color: #61afef;
	border-color: #abb2bf;
}

.penguins-in-space .ace_keyword {
	color: #00a8c6;
}

.penguins-in-space .ace_keyword.ace_operator {
	color: #00a8c6;
}

.penguins-in-space .ace_keyword.ace_other.ace_unit {
	color: #d19a66;
}

.penguins-in-space .ace_constant.ace_language {
	color: #d19a66;
}

.penguins-in-space .ace_constant.ace_numeric {
	color: #d19a66;
}

.penguins-in-space .ace_constant.ace_character {
	color: #56b6c2;
}

.penguins-in-space .ace_constant.ace_other {
	color: #56b6c2;
}

.penguins-in-space .ace_support.ace_function {
	color: #61afef;
}

.penguins-in-space .ace_support.ace_constant {
	color: #d19a66;
}

.penguins-in-space .ace_support.ace_class {
	color: #ff5d38;
}

.penguins-in-space .ace_support.ace_type {
	color: #ff5d38;
}

.penguins-in-space .ace_storage {
	color: #c678dd;
}

.penguins-in-space .ace_storage.ace_type {
	color: #E6DB74;
}

.penguins-in-space .ace_invalid {
	color: #fff;
	background-color: #f2777a;
}

.penguins-in-space .ace_invalid.ace_deprecated {
	color: #272b33;
	background-color: #d27b53;
}

.penguins-in-space .ace_string {
	color: #e6db74;
}

.penguins-in-space .ace_string.ace_regexp {
	color: #e6db74;
}

.penguins-in-space .ace_comment {
	font-style: italic;
	color: #454a54;
}

.penguins-in-space .ace_variable {
	color: #e06c75;
}

.penguins-in-space .ace_variable.ace_parameter {
	color: #d19a66;
}

.penguins-in-space .ace_meta.ace_tag {
	color: #e06c75;
}

.penguins-in-space .ace_entity.ace_other.ace_attribute-name {
	color: #e06c75;
}

.penguins-in-space .ace_entity.ace_name.ace_function {
	color: #61afef;
}

.penguins-in-space .ace_entity.ace_name.ace_tag {
	color: #e06c75;
}

.penguins-in-space .ace_markup.ace_heading {
	color: #98c379;
}

.penguins-in-space .ace_indent-guide {
	background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAAEklEQVQImWPQ09NrYAgMjP4PAAtGAwchHMyAAAAAAElFTkSuQmCC) right repeat-y;
}

.penguins-in-space .ace_indent-guide-active {
	background: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAACCAYAAACZgbYnAAAAEklEQVQIW2PQ1dX9zzBz5sz/ABCcBFFentLlAAAAAElFTkSuQmCC) right repeat-y;
}
    """;

});

ace.define("ace/theme/penguins_in_space", ["require", "exports", "module", "ace/theme/penguins_in_space-css", "ace/lib/dom"], function(require, exports, module) {
    exports.isDark = true;
    exports.cssClass = "penguins-in-space";
    exports.cssText = require("./penguins_in_space-css");
    var dom = require("../lib/dom");
    dom.importCssString(exports.cssText, exports.cssClass, false);

});
(function() {
    ace.require(["ace/theme/penguins_in_space"], function(m) {
        if (typeof module == "object" && typeof exports == "object" && module) {
            module.exports = m;
        }
    });
})();