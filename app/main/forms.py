from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField, \
SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp
from wtforms import ValidationError
from app.models import Product, Silicon, TestID, TestRow 

class CreateSiliconForm(FlaskForm):
    codename = StringField('Silicon Codename', validators=[DataRequired(),
                                                           Length(1,64)])
    productCode = StringField('Product Code', validators=[DataRequired(),
                                                          Length(1,64)])
    description = TextAreaField('Silicon Description',
                                validators=[Length(0,256)])

    #submit Form
    submit = SubmitField('Submit')

class CreateProductForm(FlaskForm):
    #Product Qualities
    name = StringField('New Product Name:', validators = [DataRequired(),
                                                          Length(1,64)])
    customer = StringField('Product Customer:', validators = [DataRequired(),
                                                              Length(1,64)])
    ipn = StringField('Product IPN (J12345-678', validators=[DataRequired(),
                                                             Length(1,64)])
    serial = StringField('Product Base Serial Numbers (OUI for NIC):',
                         validators = [Length(0,64)])
    description = TextAreaField("Product Description",
                                validators=[Length(0,256)])
    silicon = SelectField('Primary Silicon', coerce=int)

    #Submit Form
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(CreateProductForm, self).__init__(*args, **kwargs)
        self.silicon.choices = [(silicon.id, "{} ({})".format(silicon.codename,
                                                             silicon.productCode)) for
                                silicon in
                                Silicon.query.order_by(Silicon.codename).all()]

class CreateSampleForm(FlaskForm):
    #Sample Fields
    serialNum = StringField('Serial Number (MAC)', validators=[DataRequired(),
                                                               Length(1,64)])
    hardwareRev = SelectField('HW Revision', coerce=int)

    #Submit Form
    submit = SubmitField('Submit')

    def __init__(self, product, *args, **kwargs):
        super(CreateSampleForm, self).__init__(*args, **kwargs)
        print(product.id, product.name, product.hw_revisions.all())
        self.hardwareRev.choices= [(hwrev.id, hwrev.reworkNumber) for hwrev in
                                   product.hw_revisions.all()]

    def set_hardware_choices(self, product):
        self.hardwareRev.choices = [(hwrev.id, hwrev.reworkRev) for hwrev in
                            product.hw_revisions]



class CreateHardwareRevisionForm(FlaskForm):
    #HW Revision Qualities
    ipn = StringField('HW Revision IPN (J12345-678):',
                      validators=[DataRequired(), Length(1,64)])
    reworkRev = StringField('Rework Revision', validators=[DataRequired(),
                                                           Length(1,64), Regexp('^[0-9]+$', 0, 'Only \
                                                      numbers are allowed')])
    revDescription = TextAreaField("HW Revision Description",
                                validators=[Length(0,256)])

    #Submit Form
    submit = SubmitField('Submit')

class CreateSoftwareComponentForm(FlaskForm):

    #Submit Form
    submit = SubmitField('Submit')


class CreateSoftwareRevisionForm(FlaskForm):
    #Submit Form
    submit = SubmitField('Submit')
