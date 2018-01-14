from django import template
from markdown import markdown as to_markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from markdown.util import etree
from re import search
from .markdown import EscapeHtml, TagsPlus
from .sectionizer import DocumentDivider

register = template.Library()

class ContentExtractor(Treeprocessor):
    # gets contents and makes a list out of the contents
    def run(self, root):
        section_list = list(DocumentDivider().run(root))
        return self.extract_list(section_list)

    def extract_list(self, section_list):
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
        if old_level < new_level:
            if old_level == 0 and not section_stack[0]:
                list_item = etree.Element("ul")
                list_item.text = "article-top"
                section_stack[0] = list_item
            if section_stack[old_level].tag == "li":
                embed_list = etree.Element("ul")
                section_stack[old_level].append(embed_list)
                section_stack[old_level] = embed_list
            list_item = etree.Element("li")
            list_item.append(self.make_link(section[0].text,
                section.get("id")))
            self.append_section(section_stack, new_level, old_level,
                list_item)
        elif old_level == 0:
            list_top = etree.Element("ul")
            list_item = etree.Element("li")
            list_item.append(self.make_link("Top", section.get("id")))
            list_top.append(list_item)
            section_stack[0] = list_top
        else:
            list_item = etree.Element("li")
            list_item.append(self.make_link(section[0].text,
                section.get("id")))
            self.append_section(section_stack, new_level, (new_level-1),
                list_item)

    def make_link(self, text, id_link):
        new_link = etree.Element("a")
        new_link.set("href", "{}{}".format("#", id_link))
        new_link.text = text
        return new_link

    def append_section(self, section_stack, new_level, old_level,
        section):
        section_stack[new_level] = section
        section_stack[old_level].append(section_stack[new_level])

class MakeToc(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('tocizer', ContentExtractor(md), '_end')

@register.filter
def mark_toc(text):
    return to_markdown(text, extensions=[EscapeHtml(), TagsPlus(),
        MakeToc()], output_format='html5')

class NavBarMaker(Treeprocessor):
    def run(self, root):
        contents = ContentExtractor().run(root)
        new_tree = self.convert_tree(contents[0],
            "#article-top", "Contents")
        new_root = etree.Element("div")
        new_root.append(new_tree)
        return new_root

    def convert_tree(self, root, link, title):
        new_tree = self.make_nesting(link, title)
        for item in list(root):
            if len(list(item)) > 1:
                nesting = self.convert_tree(item[1],
                    item[0].get("href"), item[0].text)
                new_tree[1][0].append(nesting)

                new_link = etree.Element("a")
                new_link.set("href", item[0].get("href"))
                new_link.text = "Main"
                nesting[1][0].insert(0, self.make_link(new_link))
            else:
                new_tree[1][0].append(self.make_link(item[0]))
        divider = etree.Element("li")
        divider.set("class", "dropdown-divider")
        new_tree[1][0].append(divider)
        return new_tree

    def make_link(self, link):
        list_item = etree.Element("li")
        link.set("class", "nav-link sidenav-item")
        list_item.append(link)
        return list_item

    def make_nesting(self, link, title):
        list_item = etree.Element("li")
        list_item.set("class", "nav-item dropdown")

        raw_link = search("#article-(.*)", link).group(1)
        new_link = "toc-{}".format(raw_link)

        link_item = etree.Element("p")
        link_item.set("class", "nav-link sidenav-item mb-0")
        link_item.set("data-toggle", "collapse")
        link_item.set("data-target", "{}{}".format("#", new_link))
        link_item.set("aria-expanded", "false")
        link_item.set("aria-controls", new_link)
        link_item.text = title
        list_item.append(link_item)

        div_item = etree.Element("div")
        div_item.set("class", "collapse")
        div_item.set("id", new_link)
        list_item.append(div_item)

        ul_item = etree.Element("ul")
        ul_item.set("class", "nav flex-column")
        div_item.append(ul_item)
        return list_item

class MakeTocNav(Extension):
    def extendMarkdown(self, md, md_globals):
        md.treeprocessors.add('tocizer', NavBarMaker(md), '_end')

@register.filter
def mark_nav(text):
    return to_markdown(text, extensions=[EscapeHtml(), TagsPlus(),
        MakeTocNav()], output_format='html5')
