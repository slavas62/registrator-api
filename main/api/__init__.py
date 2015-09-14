from userlayers.api.resources.table_proxy.resources import TableProxyResource as TableProxyResourceBase
from django.conf import settings
from sorl.thumbnail import get_thumbnail
from userlayers import get_modeldefinition_model

ModelDef = get_modeldefinition_model()


class TableProxyResource(TableProxyResourceBase):
    def get_inline_class(self, foreign_field, nickname):
        ic_base = super(TableProxyResource, self).get_inline_class(foreign_field, nickname)

        class ThisInline(ic_base):
            def dehydrate(self, bundle):
                bundle = super(ThisInline, self).dehydrate(bundle)
                if self.this_md.resource_type == ModelDef.RESOURCE_TYPE_CHOICES_IMAGE:
                    bundle.data['thumbnails'] = []
                    for thumb in settings.RESOURCE_IMAGE_THUMBNAILS:
                        img_path = ('%s%s' % (settings.MEDIA_ROOT, bundle.obj.file)).replace('//', '/')
                        try:
                            with open(img_path, 'r') as img:
                                bundle.data['thumbnails'].append({
                                    'name': thumb['name'],
                                    'file': get_thumbnail(img, **thumb).url
                                })
                                img.close()
                        except IOError:
                            pass
                bundle.data['resource_uri'] = self.proxy.uri_for_table_object(self.this_md_id, bundle.obj.pk)
                return bundle

        return ThisInline
