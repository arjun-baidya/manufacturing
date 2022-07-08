from odoo import api, models


class ReportConsumption(models.AbstractModel):
    _name = 'report.merchandising.report_consumption_form'
    _description = 'Consumption Report'

    # report
    @api.model
    def _get_report_values(self, docids, data=None):
        # docs = self.env['pattern.cut.line'].browse(docids[0])
        docs = self.env['pattern.cut.line'].search([])
        # pattern_cut_data = self.env['pattern.cut.line'].search([])
        print('doc', docs)
        # print('pt-data', pattern_cut_data)

        pattern_line = []
        for i in docs:
            vals = {
                'pattern_name': i.pattern_name,
                'material_type': i.material_type,
            }
            pattern_line.append(vals)
        print('pattern line', pattern_line)

        return {
            # 'doc_ids': docids,
            'doc_model': 'pattern.cut.line',
            'data': data,
            'docs': docs,
            # 'pattern_line': pattern_line,
        }
