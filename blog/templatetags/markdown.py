from django import template
from markdown import markdown as to_markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor

register = template.Library()

class EscapeHtml(Extension):
    def extendMarkdown(self, md, md_globals):
        del md.preprocessors['html_block']
        del md.inlinePatterns['html']

class ImageFluidifier(Treeprocessor):
    def run(self, root):
        for child in root:
            if child.tag == 'img':
                old_classes = child.get('class')
                new_classes = 'img-fluid'
                if old_class is not None:
                    new_classes = '{} {}'.format(old_classes, new_classes)
            self.run(child)

class TagsPlus(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('img-fluid', ImageFluidifier(md), '_end')

@register.filter
def markdown(text):
    return to_markdown(text, extensions=[EscapeHtml(), TagsPlus()],
        output_format='html5')
