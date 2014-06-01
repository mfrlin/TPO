from django.utils.translation import ugettext_lazy as _

from django.conf import settings

GENERIC_GALLERY_IMAGES = {
    'massage_salon': {'title': _('Massage salon'), 'values': ['img-01.jpg', 'img-02.jpg', 'img-03.jpg']}
    , 'cosmetic_salon': {'title': _('Cosmetic salon'), 'values': ['img-01.jpg', 'img-02.jpg', 'img-03.jpg']}
    , 'hairdresser_salon': {'title': _('Hairdresser salon'), 'values': ['img-01.jpg', 'img-02.jpg', 'img-03.jpg']}
}

GENERIC_GALLERY_CHOICES = map(lambda x: (x, GENERIC_GALLERY_IMAGES[x]['title']), GENERIC_GALLERY_IMAGES)

GENERIC_GALLERY_URL = settings.STATIC_URL + "gallery/"

