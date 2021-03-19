
from odoo import models, fields, api, _
from odoo.tools import float_is_zero, float_compare, pycompat

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    pro_forma_number = fields.Char(string="Forma Number", readonly=True, required=False, copy=False)
    # state = fields.Selection(selection_add=[('proforma', "Pro Forma")])
    state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('proforma', 'Pro Forma'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('cancel', 'Cancelled'),
    ], default='draft')

    @api.multi
    def action_invoice_open(self):
        # lots of duplicate calls to action_invoice_open, so we remove those already open
        to_open_invoices = self.filtered(lambda inv: inv.state != 'open')
        if to_open_invoices.filtered(lambda inv: inv.state not in ['draft', 'proforma']):
            raise UserError(_("Invoice must be in draft state in order to validate it."))
        if to_open_invoices.filtered(lambda inv: float_compare(inv.amount_total, 0.0, precision_rounding=inv.currency_id.rounding) == -1):
            raise UserError(_("You cannot validate an invoice with a negative total amount. You should create a credit note instead."))
        to_open_invoices.action_date_assign()
        to_open_invoices.action_move_create()
        return to_open_invoices.invoice_validate()

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

    @api.multi
    def action_proforma_invoice_sent(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        self.ensure_one()
        template = self.env.ref('proforma.email_template_proforma_invoice', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='account.invoice',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment',
            mark_invoice_as_sent=True,
            # custom_layout="account.mail_template_data_notification_email_account_invoice",
            force_email=True
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }