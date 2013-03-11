from django.forms import widgets
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse
from django.utils import simplejson as json
from django.conf import settings


GLOBAL_OPTIONS = getattr(settings, 'AJAX_UPLOAD', {})


INIT_JS = """
<script>
  $(function(){
    initUpload('%s', %s)
  })
</script>
"""


class AjaxEditor(widgets.TextInput):

    class Media:
        js = (
            'fileupload/js/jquery.ui.widget.js',
            'fileupload/js/jquery.iframe-transport.js',
            'fileupload/js/jquery.fileupload.js',
            'fileupload/js/ajaxupload.js',
        )
        css = {
            'all': (
                'fileupload/css/styles.css',
            )
        }

    def __init__(self, *args, **kwargs):
        self.upload_to = kwargs.pop('upload_to', '')
        self.custom_options = kwargs.pop('ajax_options', {})
        super(AjaxEditor, self).__init__(*args, **kwargs)

    def get_options(self):
        options = GLOBAL_OPTIONS.copy()
        options.update(self.custom_options)
        options.update({
            'url': reverse('ajax_upload_image', kwargs={'upload_to': self.upload_to}),
        })
        return json.dumps(options)

    def render(self, name, value, attrs=None):
        html = super(AjaxEditor, self).render(name, value, attrs)
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id')
        html += INIT_JS % (id_, self.get_options())
        return mark_safe(html)