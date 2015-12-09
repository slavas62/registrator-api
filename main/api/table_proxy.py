import os
from django.conf import settings
from django.core.exceptions import FieldError
from tastypie import fields as tastypie_fields
from sorl.thumbnail import get_thumbnail
from main.contrib.helper import generate_filename
from userlayers import get_modeldefinition_model
from userlayers.api.resources.table_proxy import TableProxyResource as UserlayersTableProxyResource

ModelDef = get_modeldefinition_model()


class TableProxyResource(UserlayersTableProxyResource):
    class Meta(UserlayersTableProxyResource.Meta):
        pass

    def get_resource_class_queryset(self):
        qs = super(TableProxyResource, self).get_resource_class_queryset()
        if not self.user.is_superuser:
            #Objects or media files objects filtering
            try:
                qs = qs.filter(user_id=self.user.id)
            except FieldError as e:
                qs = qs.filter(object__user_id=self.user.id)
        return qs

    def get_inline_class(self, foreign_field, nickname):
        ic_base = super(TableProxyResource, self).get_inline_class(foreign_field, nickname)

        class ThisInline(ic_base):
            class Meta(ic_base.Meta):
                pass

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

    def get_resource_class(self):
        R = super(TableProxyResource, self).get_resource_class()

        class RR(R):
            class Meta(R.Meta):
                pass

            def save(self, bundle, skip_errors=False):
                setattr(bundle.obj, 'user_id', self.request.user.id)
                return super(RR, self).save(bundle, skip_errors)

        retrun = RR

        if R.md.resource_type:
            class RRR(RR):
                upload_to = os.path.join(settings.MEDIA_ROOT, getattr(
                    settings, 'RESOURCE_FOLDER_%sS_IN_MEDIA_ROOT' % dict(
                        R.md.RESOURCE_TYPE_CHOICES)[R.md.resource_type].upper()))
                object_id = tastypie_fields.IntegerField(attribute='object_id', null=True, blank=True)
                file = tastypie_fields.FileField(attribute='file', null=True, blank=True)

                def save(self, bundle, skip_errors=False):
                    bundle.obj.file = self.handle_uploaded_file(bundle.data['file'])
                    return super(RRR, self).save(bundle, skip_errors)

                def handle_uploaded_file(self, f):
                    dst = os.path.join(self.upload_to, generate_filename(str(f)))
                    dst_dir = os.path.dirname(dst)
                    if not os.path.exists(dst_dir):
                        os.makedirs(dst_dir)
                    with open(dst, 'wb+') as dst_file:
                        for chunk in f.chunks():
                            dst_file.write(chunk)
                        dst_file.close()
                    return dst.replace(settings.MEDIA_ROOT, '')

            retrun = RRR

        return retrun
