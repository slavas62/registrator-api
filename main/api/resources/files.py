# coding: utf-8
from django.conf import settings
from sorl.thumbnail import get_thumbnail
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource, fields
from main import models


class ObjectInlineFile(ModelResource):
    class Meta:
        list_allowed_methods = []
        detail_allowed_methods = []
        include_resource_uri = False
        queryset = models.Object.objects.all()


class FileBase(ModelResource):
    object_id = fields.IntegerField(attribute='object_id', null=True, blank=True)

    class Meta:
        allowed_methods = ['get', 'post', 'put', 'delete']
        authorization = Authorization()

    def deserialize(self, request, data, format=None):
        if not format:
            format = request.META.get('CONTENT_TYPE', 'application/json')

        if format == 'application/x-www-form-urlencoded':
            return request.POST

        if format.startswith('multipart'):
            data = request.POST.copy()
            data.update(request.FILES)
            return data

        return super(FileBase, self).deserialize(request, data, format)


class VideoFile(FileBase):
    class Meta(FileBase.Meta):
        queryset = models.ResourceVideo.objects.prefetch_related('object').all()
        resource_name = 'resource_video'


class ImageFile(FileBase):
    class Meta(FileBase.Meta):
        queryset = models.ResourceImage.objects.prefetch_related('object').all()
        resource_name = 'resource_image'

    def dehydrate(self, bundle):
        bundle.data['thumbnails'] = []
        for thumb in settings.RESOURCE_IMAGE_THUMBNAILS:
            bundle.data['thumbnails'].append({
                'name': thumb['name'],
                'file': get_thumbnail(bundle.obj.file, **thumb).url
            })
        return bundle

    def build_schema(self):
        schema = super(ImageFile, self).build_schema()
        schema['fields']['file'].update({'thumbnails': {
            'blank': True,
            'default': 'No default provided.',
            'help_text': '''Array. Ex. {'name': 'qwe', 'file': '/m/asd.jpg'}''',
            'nullable': True,
            'readonly': True,
            'type': 'Array',
            'unique': False
        }})
        return schema


class ObjectResourceBase(ModelResource):
    images = fields.ToManyField(ImageFile, 'images', full=True, null=True, blank=True)
    videos = fields.ToManyField(VideoFile, 'videos', full=True, null=True, blank=True)

    class Meta:
        limit = 100
        max_limit = 100
        allowed_methods = ['get', 'post', 'put', 'delete']
        authorization = Authorization()
