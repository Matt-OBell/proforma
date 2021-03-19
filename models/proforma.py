
from odoo import models, fields, api, _

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    pro_forma_number = fields.Char(string="Forma Number", readonly=True, required=False, copy=False)
    state = fields.Selection(selection_add=[('proforma', "Pro Forma")])

    @api.multi
    def action_set_to_profoma(self):
        if self.filtered(lambda inv: inv.state != 'draft'):
            raise UserError(_('Invoice must be paid in order to set it to register payment.'))
        return self.write({'state': 'proforma'})

    def action_profoma_invoice_cancel(self):
        return self.write({'state': 'cancel'})

    @api.model
    def create(self, vals):
       vals['pro_forma_number'] = self.env['ir.sequence'].next_by_code("proforma.invoice")
       result = super(AccountInvoice, self).create(vals)
       return result

    @api.multi
    def _get_printed_report_name(self):
        self.ensure_one()

        return  self.type == 'out_invoice' and self.state == 'draft' and _('Proforma Invoice') or \
                self.type == 'out_invoice' and self.state in ('open','in_payment','paid') and _('Invoice - %s') % (self.number) or \
                self.type == 'out_refund' and self.state == 'draft' and _('Credit Note') or \
                self.type == 'out_refund' and _('Credit Note - %s') % (self.number) or \
                self.type == 'in_invoice' and self.state == 'draft' and _('Vendor Bill') or \
                self.type == 'in_invoice' and self.state in ('open','in_payment','paid') and _('Vendor Bill - %s') % (self.number) or \
                self.type == 'in_refund' and self.state == 'draft' and _('Vendor Credit Note') or \
                self.type == 'in_refund' and _('Vendor Credit Note - %s') % (self.number) or \
                self.type == 'out_invoice' and _('Proforma - %s') % (self.pro_forma_number)