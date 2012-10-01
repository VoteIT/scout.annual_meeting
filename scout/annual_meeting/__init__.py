from pyramid.i18n import TranslationStringFactory


ScoutMF = TranslationStringFactory('scout.annual_meeting')


def includeme(config):
    config.scan('scout.annual_meeting')
    config.add_translation_dirs('scout.annual_meeting:locale/')
