import unittest
try:
    import xml.etree.cElementTree as e
except ImportError:
    import xml.etree.ElementTree as e

from datatree import Tree
from datatree.render.xmlrenderer import XmlRenderer

class test_XmlRenderer(unittest.TestCase):
    def test_get_attrs_str(self):
        input = {'age': '<b>300</b>', 'weight': 225}
        actual = XmlRenderer.get_attrs_str(input)

        self.assertIn('age=', actual)
        self.assertIn('&lt;b&gt;300&lt;/b&gt;"', actual,
                      "Age was not escaped properly")
        self.assertIn("weight=", actual)
        self.assertIn('"225"', actual,
                      "weight was not quoted properly")

    def get_author(self):
        tree = Tree()        
        with tree.author(rating="<b>5/6 Stars</b>") as author:
            author.name('Terry Pratchett')
            author.genere('Fantasy/Comedy')
            author.country(abbreviation="UK")
            author.living()
            with author.novels(count=2) as novels:
                novels.novel('Small Gods', year=1992)
                novels.novel('The Fifth Elephant', year=1999)
                with novels.shorts(count=2) as shorts:
                    shorts.short("Short Story 1")
                    shorts.short("Short Story 2")
        return tree
            
    def test_render_multi_levels(self):
        author = self.get_author()
        actual = e.fromstring(author.render('xml'))
        
        self.assertEqual(actual.find('name').text, 'Terry Pratchett')
        self.assertEqual(actual.find('.//shorts').attrib['count'], '2')

    def test_render_comment(self):
        tree = Tree()
        tree.root() // "Something Here"
        self.assertIn('<!-- Something Here -->', tree('xml'))

    def test_render_cdata_string(self):
        tree = Tree()
        tree.root().CDATA("Some Value")
        self.assertIn('<![CDATA[Some Value]]>', tree('xml'))
        
    def test_render_cdata_not_string(self):
        int_val = 1234567891011121314151617181920
        tree = Tree()
        tree.root().CDATA(int_val)
        self.assertIn('<![CDATA[{}]]>'.format(str(int_val)), tree('xml'))