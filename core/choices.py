from django.utils.translation import ugettext_lazy as _


class ArquivoIndexadoChoices:
    @staticmethod
    def tipo():
        return (
            ('d', _('digitalização')),
            ('p', _('prontuário')),
        )

    @staticmethod
    def genero():
        return (('m', _('Masculino')), ('M', _('Masculino')),
                ('f', _('Feminino')), ('F', _('Feminino')),
                ('o', _('Outros')),
                ('p', _('Prefiro não responder')),
                ('n', _('Não identificado'))
                )
