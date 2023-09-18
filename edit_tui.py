from pathlib import Path

from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree, ContentSwitcher, Input, DataTable, Checkbox, Button
from textual.widgets.tree import TreeNode
from textual.containers import Container

ROWS = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]
  
class TreeApp(App):

    CSS_PATH = "edit_tui.css"

    BINDINGS = [
        ("a", "add", "Add node"),
        ("e", "edit", "Edit node"),
        ("c", "clear", "Clear"),
        ("t", "toggle_root", "Toggle root"),
        ("v", "view_filter", "View"),
    ]

    def __init__(self, file_list):
        self.file_list=file_list
        self.foot=True
        App.__init__(self)
        

    def compose(self) -> ComposeResult:
        yield Header()
        with ContentSwitcher(initial="main", id="tui"):
            with Container(id="main"):
                with Container(id="vertical-layout"):
                    with Container(id="dest-horizontal-layout"):
                        yield Tree("Root", id="dest_tree")
                        yield DataTable(id="dest_table")
                    with Container(id="dupe-horizontal-layout"):
                        yield Tree("Root", id="dupe_tree")
                        yield DataTable(id="dupe_table")
                with ContentSwitcher(initial="footer", id="footer_input"):
                    yield Input(id="input")
                    with Container(id="footer"):
                        yield Footer()
            with Container(id="view_filter"):
                yield Checkbox("Arrakis :sweat:")
            with Container(id="whatever"):
                  yield Button("Default")

    @classmethod
    def add_file_list(cls, self, tree: Tree) -> None:

        from rich.highlighter import ReprHighlighter
        highlighter = ReprHighlighter()

        def add_node(name: str, node: TreeNode, file_list) -> None:
            if isinstance(file_list, dict):
                node.set_label(Text(f"{{}} {name}"))
                for key, value in file_list.items():
                    new_node = node.add("")
                    if key != "parent":
                        add_node(key, new_node, value)
            elif isinstance(file_list, list):
                node.set_label(Text(f"[] {name}"))
                for index, value in enumerate(file_list):
                    new_node = node.add("")
                    add_node(str(index), new_node, value)
            else:
                node.allow_expand = True
                if name:
                    label = Text.assemble(
                        Text.from_markup(f"[b]{name}[/b]="), highlighter(repr(file_list))
                    )
                else:
                    label = Text(repr(file_list))
                node.set_label(label)

        root_node = tree.root.add("file_list")
        add_node("file_list", root_node, self.file_list)
    

    def on_mount(self) -> None:
        """Builds up the initial tree."""
        tree = self.query_one("#dest_tree")
        self.add_file_list(self, tree)
        tree.show_root = False
        tree.root.expand()
        table = self.query_one("#dest_table")
        table.cursor_type = "row"
        table.add_columns(*ROWS[0])
        table.add_rows(ROWS[1:])
 
    def on_resize(self) -> None:
        tree = self.query_one("#dest_tree")
        self.tree_widget_size=tree.size #self.screen.children[2].size

    def action_edit(self) -> None:
        """Edit a node to the tree."""
        self.foot=not self.foot
        if self.foot:
            self.query_one("#footer_input").current = "footer"
        else:
            self.query_one("#footer_input").current = "input"

        #footer = self.query_one("#footer")
        #footer=self.screen.children[1]
        
        #footer.display=self.foot

    def action_view_filter(self) -> None:
        curr=self.query_one("#tui").current
        if curr=="main":
            self.query_one("#tui").current="view_filter"
        elif curr=="view_filter":
            self.query_one("#tui").current="whatever"
        else:
            self.query_one("#tui").current="main"

    def action_add(self) -> None:
        """Add a node to the tree."""
        pass

    def action_clear(self) -> None:
        """Clear the tree (remove all nodes)."""
        tree = self.query_one("#dest_tree")
        tree.clear()

    def action_toggle_root(self) -> None:
        """Toggle the root node."""
        tree = self.query_one("#dest_tree")
        tree.show_root = not tree.show_root


#if __name__ == "__main__":
def edit_tui(file_list):
    app = TreeApp(file_list)
    app.run()
