from ipywidgets import register, Widget, DOMWidget, widget_serialization
from traitlets import (
    default, TraitError,
    Bool, Unicode, Enum, Tuple, Instance
)
import uuid


def id_gen():
    return uuid.uuid4().urn[9:]


@register
class Node(Widget):
    """ The node widget """
    _view_name = Unicode('NodeView').tag(sync=True)
    _model_name = Unicode('NodeModel').tag(sync=True)
    _view_module = Unicode('ipytree').tag(sync=True)
    _model_module = Unicode('ipytree').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    name = Unicode("Node").tag(sync=True)
    opened = Bool(True).tag(sync=True)
    disabled = Bool(False).tag(sync=True)
    selected = Bool(False).tag(sync=True)
    show_icon = Bool(True).tag(sync=True)
    icon = Unicode("folder").tag(sync=True)
    icon_color = Enum([
        "navy", "blue", "aqua", "teal", "olive", "green", "lime", "yellow",
        "orange", "red", "fuchsia", "purple", "maroon", "white",
        "silver", "gray", "black"
    ], default_value="silver").tag(sync=True)
    nodes = Tuple(trait=Instance(Widget)).tag(
        sync=True, **widget_serialization)

    _id = Unicode(read_only=True).tag(sync=True)

    @default('_id')
    def _default_id(self):
        return id_gen()

    def add_node(self, node, position=None):
        if not isinstance(node, Node):
            raise TraitError('The added node must be a Node instance')

        nodes = list(self.nodes)
        if position is None or position > len(nodes):
            position = len(nodes)
        nodes.insert(position, node)
        self.nodes = tuple(nodes)

    def remove_node(self, node):
        if node not in self.nodes:
            raise RuntimeError(
                '{} is not a children of {}'.format(node.name, self.name)
            )
        self.nodes = tuple([n for n in self.nodes if n._id != node._id])


@register
class Tree(DOMWidget):
    """ The base Tree widget """
    _view_name = Unicode('TreeView').tag(sync=True)
    _model_name = Unicode('TreeModel').tag(sync=True)
    _view_module = Unicode('ipytree').tag(sync=True)
    _model_module = Unicode('ipytree').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    nodes = Tuple(trait=Instance(Node)).tag(sync=True, **widget_serialization)
    theme = Unicode('default', read_only=True).tag(sync=True)
    stripes = Bool(False, read_only=True).tag(sync=True)
    multiple_selection = Bool(True, read_only=True).tag(sync=True)

    _id = Unicode('#', read_only=True).tag(sync=True)

    def __init__(
            self, nodes=[], theme='default', stripes=False,
            multiple_selection=True,
            **kwargs):
        super(Tree, self).__init__(**kwargs)

        self.nodes = nodes
        self.set_trait('theme', theme)
        self.set_trait('stripes', stripes)
        self.set_trait('multiple_selection', multiple_selection)

    def add_node(self, node, position=None):
        if not isinstance(node, Node):
            raise TraitError('The added node must be a Node instance')

        nodes = list(self.nodes)
        if position is None or position > len(nodes):
            position = len(nodes)
        nodes.insert(position, node)
        self.nodes = tuple(nodes)

    def remove_node(self, node):
        if node not in self.nodes:
            raise RuntimeError(
                '{} is not a children of the tree'.format(node.name)
            )
        self.nodes = tuple([n for n in self.nodes if n._id != node._id])
