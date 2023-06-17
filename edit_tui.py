from pathlib import Path

from rich.text import Text

from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Tree, ContentSwitcher, Input
from textual.widgets.tree import TreeNode
from textual.containers import Container

class TreeApp(App):

    CSS_PATH = "edit_tui.css"

    BINDINGS = [
        ("a", "add", "Add node"),
        ("e", "edit", "Edit node"),
        ("c", "clear", "Clear"),
        ("t", "toggle_root", "Toggle root"),
    ]

    def __init__(self, action_list):
        self.action_list=action_list
        self.foot=True
        App.__init__(self)
        

    def compose(self) -> ComposeResult:
        yield Header()
        with Container(id="vertical-layout"):
            yield Tree("Root", id="dest_tree")
            yield Tree("Root", id="dupe_tree")
        with ContentSwitcher(initial="footer", id="footer_input"):
            yield Input(id="input")
            with Container(id="footer"):
                yield Footer()
    


    @classmethod
    def add_file_actions(cls, self, tree: Tree) -> None:

        from rich.highlighter import ReprHighlighter
        highlighter = ReprHighlighter()

        def add_node(name: str, node: TreeNode, action) -> None:
            if isinstance(action, dict):
                node.set_label(Text(f"{{}} {name}"))
                for key, value in action.items():
                    new_node = node.add("")
                    add_node(key, new_node, value)
            elif isinstance(action, list):
                node.set_label(Text(f"[] {name}"))
                for index, value in enumerate(action):
                    new_node = node.add("")
                    add_node(str(index), new_node, value)
            else:
                node.allow_expand = True
                if name:
                    label = Text.assemble(
                        Text.from_markup(f"[b]{name}[/b]="), highlighter(repr(action))
                    )
                else:
                    label = Text(repr(action))
                node.set_label(label)

        root_node = tree.root.add("file_actions")
        add_node("file_actions", root_node, self.action_list)
    

    def on_mount(self) -> None:
        """Builds up the initial tree."""
        tree = self.query_one("#dest_tree")
        self.add_file_actions(self, tree)
        tree.show_root = False
        tree.root.expand()

    def on_resize(self) -> None:
        tree = self.query_one("#dest_tree")
        self.tree_widget_size=tree.size #self.screen.children[2].size

    def action_edit(self) -> None:
        """Edit a node to the tree."""
        self.foot=not self.foot
        if self.foot:
            self.query_one(ContentSwitcher).current = "footer"
        else:
            self.query_one(ContentSwitcher).current = "input"

        #footer = self.query_one("#footer")
        #footer=self.screen.children[1]
        
        #footer.display=self.foot

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
def edit_tui(action_list):
    app = TreeApp(action_list)
    app.run()
