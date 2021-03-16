from django.utils.translation import ugettext_lazy as _


class IndexedFileChoices:
    @staticmethod
    def tipo():
        return (
            ('d', _('digitalização')),
            ('p', _('prontuário')),
        )
