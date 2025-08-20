from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail.search import index


class SimpleContentBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=100, help_text="Заголовок блока")
    content = blocks.RichTextBlock(features=['bold', 'italic', 'link'])
    image = ImageChooserBlock(required=False)
    alignment = blocks.ChoiceBlock(choices=[
        ('left', 'Слева'),
        ('center', 'По центру'),
        ('right', 'Справа')
    ], default='left')

    class Meta:
        template = 'blocks/simple_content_block.html'


class BlogPage(Page):
    date = models.DateField("Дата публикации")
    intro = models.CharField("Введение", max_length=250)
    body = StreamField([
        ('content', SimpleContentBlock()),
        ('text', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True, blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
    ]