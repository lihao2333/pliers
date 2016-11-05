import pytest
from featurex.graph import Graph, Node
from featurex.extractors.image import BrightnessExtractor
from featurex.stimuli.image import ImageStim
from .utils import get_test_data_path
from os.path import join
from numpy.testing import assert_almost_equal


def test_node_init():
    n = Node('my_node', BrightnessExtractor())
    assert isinstance(n.transformer, BrightnessExtractor)
    assert n.name == 'my_node'
    n = Node('my_node', 'brightnessextractor')    
    assert isinstance(n.transformer, BrightnessExtractor)


def test_node_arg_parsing():
    n1, n2 = 'MyLovelyExtractor', ['MyLovelyExtractor']
    args1 = Graph._parse_node_args(n1)
    args2 = Graph._parse_node_args(n2)
    assert args1 == args2 == {'transformer': 'MyLovelyExtractor'}

    node = ('saliencyextractor', 'saliency')
    args = Graph._parse_node_args(node)
    assert set(args.keys()) == {'transformer', 'name'}

    node = ('saliencyextractor', 'my_name', [('child1'), ('child2')])
    args = Graph._parse_node_args(node)
    assert set(args.keys()) == {'transformer', 'name', 'children'}
    assert len(args['children']) == 2

    node = { 'transformer': '...', 'name': '...'}
    args = Graph._parse_node_args(node)
    assert args == node


def test_graph_smoke_test():
    
    filename = join(get_test_data_path(), 'image', 'obama.jpg')
    stim = ImageStim(filename)
    nodes = [(BrightnessExtractor(), 'brightness')]
    graph = Graph(nodes)
    result = graph.extract([stim])
    brightness = result[('BrightnessExtractor', 'avg_brightness')].values[0]
    assert_almost_equal(brightness, 0.556134, 5)
