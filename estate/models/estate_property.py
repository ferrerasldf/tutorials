from dateutil.relativedelta import relativedelta
from odoo import fields, models
from datetime import date


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
                   ('sold', 'Sold '),
                   ('cancelled', 'Cancelled')],
        default='new'
    )
    active = fields.Boolean(default=True)