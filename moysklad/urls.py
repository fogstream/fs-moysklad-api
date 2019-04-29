from .utils import AbstractSingleton


class ApiUrlRegistry(AbstractSingleton):
    @staticmethod
    def get_create_url(entity_name):
        return f'entity/{entity_name}'

    def get_update_url(self, entity_name, entity_id):
        return self.get_by_id_url(entity_name, entity_id)

    def get_delete_url(self, entity_name, entity_id):
        return self.get_by_id_url(entity_name, entity_id)

    @staticmethod
    def get_by_id_url(entity_name, entity_id):
        return f'entity/{entity_name}/{entity_id}'

    @staticmethod
    def get_list_url(entity_name):
        return f'entity/{entity_name}'

    def get_relation_list_url(self, entity_name, entity_id,
                              relation_entity_name):
        return (f'{self.get_list_url(entity_name)}/'
                f'{entity_id}/{relation_entity_name}')

    @staticmethod
    def get_report_url(report_name):
        return f'report/{report_name}'

    @staticmethod
    def get_report_with_param_url(report_name, param):
        return f'report/{report_name}/{param}'

    @staticmethod
    def get_metadata_url(entity_name):
        return f'entity/{entity_name}/metadata'

    @staticmethod
    def get_metadata_attribute_url(entity_name, field_id):
        return f'entity/{entity_name}/metadata/attributes/{field_id}'

    @staticmethod
    def get_new_document_template_url(entity_name):
        return f'entity/{entity_name}/new'

    @staticmethod
    def get_pos_attach_token_url(retail_store_id):
        return f'admin/attach/{retail_store_id}'

    @staticmethod
    def get_pos_retail_store_query_url():
        return 'admin/retailstore/'

    @staticmethod
    def get_document_publications_url(entity_name, id_):
        return f'entity/{entity_name}/{id_}/publication'

    @staticmethod
    def get_document_publication_with_id_url(entity_name, id_, publication_id):
        return f'entity/{entity_name}/{id_}/publication/{publication_id}'

    @staticmethod
    def get_document_export_url(entity_name, id_):
        return f'entity/{entity_name}/{id_}/export/'

    @staticmethod
    def get_metadata_export_embedded_template_url(entity_name):
        return f'entity/{entity_name}/metadata/embeddedtemplate/'

    @staticmethod
    def get_metadata_export_embedded_template_with_id_url(entity_name, id_):
        return f'entity/{entity_name}/metadata/embeddedtemplate/{id_}'

    @staticmethod
    def get_metadata_export_custom_template_url(entity_name):
        return f'entity/{entity_name}/metadata/customtemplate/'

    @staticmethod
    def get_metadata_export_custom_template_with_id_url(entity_name, id_):
        return f'entity/{entity_name}/metadata/customtemplate/{id_}'

    @staticmethod
    def get_audit_url():
        return 'audit/'

    @staticmethod
    def get_audit_events_url(audit_id):
        return f'audit/{audit_id}/events'

    @staticmethod
    def get_audit_events_entity_url(entity_name, id_):
        return f'entity/{entity_name}/{id_}/audit'

    @staticmethod
    def get_audit_filters_url():
        return 'audit/metadata/filters'
