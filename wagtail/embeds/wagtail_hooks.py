from django.conf.urls import include, url
from django.urls import reverse
from django.utils.html import format_html

from wagtail.admin.rich_text import HalloPlugin
from wagtail.admin.rich_text.converters.editor_html import EmbedTypeRule
from wagtail.core import hooks
from wagtail.embeds import urls
from wagtail.embeds.rich_text import MediaEmbedHandler, media_embedtype_handler


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        url(r'^embeds/', include(urls, namespace='wagtailembeds')),
    ]


@hooks.register('insert_editor_js')
def editor_js():
    return format_html(
        """
            <script>
                window.chooserUrls.embedsChooser = '{0}';
            </script>
        """,
        reverse('wagtailembeds:chooser')
    )


@hooks.register('register_rich_text_features')
def register_embed_feature(features):
    # define a handler for converting <embed embedtype="media"> tags into frontend HTML
    features.register_embed_type('media', media_embedtype_handler)

    # define a hallo.js plugin to use when the 'embed' feature is active
    features.register_editor_plugin(
        'hallo', 'embed',
        HalloPlugin(
            name='hallowagtailembeds',
            js=['wagtailembeds/js/hallo-plugins/hallo-wagtailembeds.js'],
        )
    )

    # define how to convert between editorhtml's representation of embeds and
    # the database representation
    features.register_converter_rule('editorhtml', 'embed', [
        EmbedTypeRule('media', MediaEmbedHandler)
    ])

    # add 'embed' to the set of on-by-default rich text features
    features.default_features.append('embed')
