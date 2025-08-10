from dateutil.relativedelta import relativedelta
from odoo import fields, models, api
from datetime import date, timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"

    name = fields.Char('Property Name', default="Unknown",required=True)
    description = fields.Text('Property Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Available Date',
                                    copy=False,
                                    default=lambda self: date.today() + relativedelta(months=3))
    expected_price = fields.Float('Expected Price',  required=True)
    selling_price = fields.Float(string='Selling Price', copy=False, readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    last_seen = fields.Datetime("Last Seen", default= fields.Datetime.now)
    state = fields.Selection(
        string='State',
        required=True,
        copy=False,
        selection=[('new', 'New'),
                   ('offer received', 'Offer Received'),
                   ('offer accepted', 'Offer Accepted'),
                   ('sold', 'Sold '),
                   ('cancelled', 'Cancelled')],
        default='new'
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    user_id = fields.Many2one('res.users', string='Salesperson',
                              index=True,
                              tracking=True,
                              default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    total_area = fields.Float("Total Area", compute="_compute_total_area")
    best_price =fields.Float("Best Price", compute="_compute_best_price")

    @api.depends('living_area', 'garden_area' )
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price')) if record.offer_ids else 0

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = ''

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"

    name = fields.Char('Property Type', required=True)

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char('Property Tag', required=True)

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[('accepted', 'Accepted'),
                   ('refused', 'Refused')],
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(string='Validity(days)', default=7)
    date_deadline = fields.Date("Deadline",
                                compute="_compute_date_deadline",
                                inverse="_inverse_date_deadline")

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = date.today() + timedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.date_deadline = record.create_date + relativedelta(days=record.validity)
