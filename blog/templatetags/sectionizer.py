from django import template
from django.utils.text import slugify
from itertools import count
from markdown import markdown as to_markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree
from re import search
from .markdown import EscapeHtml, TagsPlus

register = template.Library()

class DocumentDivider(Treeprocessor):
    def run(self, root):
        section_list = self.divide_sections(root)
        return self.assemble_tree(section_list)

    def divide_sections(self, root):
        section_list = []
        id_list = []
        new_tree = etree.Element("section")
        for child in root:
            if self.header_level(child) > 0 and len(list(new_tree)) > 0:
                self.finalize_section(section_list, new_tree, id_list)
                new_tree = etree.Element("section")
            new_tree.append(child)
        self.finalize_section(section_list, new_tree, id_list)
        return section_list

    def header_level(self, child):
        header_match = search("h([1-6])", child.tag)
        if header_match is None:
            return 0
        else:
            return int(header_match.group(1))

    def finalize_section(self, section_list, section, id_list):
        section_id = "article-top"
        if self.header_level(section[0]) > 0:
            section_id = "article-{}".format(slugify(section[0].text))
            section_id = self.make_unique_slug(section_id, id_list)
        id_list.append(section_id)
        section.set("id", section_id)
        section_list.append(section)

    def make_unique_slug(self, id_proposed, id_list):
        slug = id_proposed
        for x in count(1):
            if slug not in id_list:
                break
            slug = "{}-{}".format(id_proposed, x)
        return slug

    def assemble_tree(self, section_list):
        new_tree = etree.Element("div")
        for section in section_list:
            new_tree.append(section)
        return new_tree

class Sectionizer(Treeprocessor):
    def run(self, root):
        section_list = list(DocumentDivider().run(root))
        return self.assemble_tree(section_list)

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

    def header_level(self, child):
        header_match = search("h([1-6])", child.tag)
        if header_match is None:
            return 0
        else:
            return int(header_match.group(1))

    def add_new_section(self, section_stack, section,
        old_level, new_level):
        if old_level > new_level:
            self.append_section(section_stack, new_level, section)
        elif old_level < new_level:
            if old_level == 0 and not section_stack[0]:
                section_stack[0] = etree.Element("section")
            section_stack[new_level] = section
            section_stack[old_level].append(section_stack[new_level])
        elif old_level == 0:
            section_stack[0] = section
        else:
            self.append_section(section_stack, new_level, section)

    def append_section(self, section_stack, new_level, section):
        section_stack[new_level] = section
        section_stack[new_level-1].append(section_stack[new_level])

class MakeSections(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('sectionizer', Sectionizer(md), '_end')

@register.filter
def mark_sections(text):
    return to_markdown(text, extensions=[EscapeHtml(), TagsPlus(),
        MakeSections()], output_format='html5')
