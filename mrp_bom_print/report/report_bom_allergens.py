from odoo import models


class ReportBomAllergens(models.AbstractModel):
    _name = "report.bom.allergens"
    _description = "BoM Allergens report"

    # @api.model
    # def _get_report_values(self, docids, data=None):
    #
    #     # mark the selected products as Up To Date if print succeed
    #     line_obj = self.env["bom.print.wizard.line"]
    #     lines = line_obj.browse([int(x) for x in data["line_data"]])
    #     return {
    #         'doc_ids': docs.ids,
    #         'docs': docs,
    #     }
    #
    # @api.model
    # def _get_report_values(self, docids, data=None):
    #     AccountPaymentOrderObj = self.env['account.payment.order']
    #     docs = AccountPaymentOrderObj.browse(docids)
    #
    #     return {
    #         'doc_ids': docids,
    #         'doc_model': 'account.payment.order',
    #         'docs': docs,
    #         'data': data,
    #         'env': self.env,
    #         'get_bank_account_name': self.get_bank_account_name,
    #         'formatLang': formatLang,
    #     }
    #
    # @api.multi
    # def _get_report_values(self, docids, data=None):
    #     docs = self.env['sale.order'].browse(docids)
    #     return {
    #         'doc_ids': docs.ids,
    #         'doc_model': 'sale.order',
    #         'docs': docs,
    #         'proforma': True
    #     }
