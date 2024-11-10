import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff_url(self):
        node = TextNode("dicks", TextType.ITALIC, url="string that isn't a url")
        node2 = TextNode("dicks", TextType.ITALIC, url="string that is a url, trust me bro")
        self.assertNotEqual(node, node2)

    def test_diff_name(self):
        node = TextNode("poop", TextType.ITALIC, url="string that isn't a url")
        node2 = TextNode("dicks", TextType.ITALIC, url="string that isn't a url")
        self.assertNotEqual(node, node2)

    def test_diff_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_empty_name(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("", TextType.BOLD)
        self.assertNotEqual(node, node2)

    

if __name__ == "__main__":
    unittest.main()