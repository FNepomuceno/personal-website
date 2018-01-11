from django import template
from django.utils.text import slugify
from markdown import markdown as to_markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree
from re import search

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

class Sectionizer(Treeprocessor):
    def run(self, root):
        section_list = self.divide_sections(root)
        new_tree = self.assemble_tree(section_list)
        return new_tree

    def divide_sections(self, root):
        section_list = []
        new_tree = etree.Element("section")
        for child in root:
            if self.header_level(child) > 0 and len(list(new_tree)) > 0:
                section_list.append(new_tree)
                new_tree = etree.Element("section")
            new_tree.append(child)
        section_list.append(new_tree)
        return section_list

    def header_level(self, child):
        header_match = search("h([1-6])", child.tag)
        if header_match is None:
            return 0
        else:
            return int(header_match.group(1))

    def assemble_tree(self, section_list):
        new_tree = etree.Element("div")
        section_stack = [None] * 7
        current_level = 0
        for section in section_list:
            new_level = self.header_level(section[0])
            self.add_new_section(section_stack, section,
                current_level, new_level)
            current_level = new_level
        new_tree.append(section_stack[0])
        return new_tree

    def add_new_section(self, section_stack, section,
        old_level, new_level):
        if old_level > new_level:
            print('decrease from {} to {}'.format(old_level, new_level))
            self.append_section(section_stack, new_level, section)
        elif old_level < new_level:
            print('increase from {} to {}'.format(old_level, new_level))
            if old_level == 0 and not section_stack[0]:
                section_stack[0] = etree.Element("section")
            for i in range(old_level+1, new_level):
                section_stack[i] = etree.Element("section")
                if i > 0:
                    section_stack[i-1].append(section_stack[i])
            self.append_section(section_stack, new_level, section)
            pass
        elif old_level == 0:
            print('initial section')
            section_stack[0] = section
        else:
            print('stay at {}'.format(old_level))
            self.append_section(section_stack, new_level, section)

    def append_section(self, section_stack, new_level, section):
        section_stack[new_level] = section
        print(len(section_stack[new_level-1]))
        section_stack[new_level-1].append(section_stack[new_level])
        print(len(section_stack[new_level-1]))

class MakeSections(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('sectionizer', Sectionizer(md), '_end')

@register.filter
def mark_sections(text):
    return to_markdown(text, extensions=[EscapeHtml(), TagsPlus(),
        MakeSections()], output_format='html5')
