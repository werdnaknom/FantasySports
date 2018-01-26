from flask import current_app, request, url_for
import datetime
from app import db


class AddUpdateDelete():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

class Product(db.Model, AddUpdateDelete):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    baseSerial = db.Column(db.String(64), index=True, nullable=False)
    customer = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(256))


    #Foreign Relationships
    silicon = db.relationship('ProductSilicon', backref='product',
                                     lazy='dynamic')
    samples = db.relationship('Sample', backref='product', lazy='dynamic')
    hw_revisions = db.relationship('HardwareRevision',
                              backref='product', lazy='dynamic')
    test_ids = db.relationship('TestID',
                              backref='product', lazy='dynamic')

    def __init__(self, name, baseSerial, customer, description= ""):
        self.name = name
        self.baseSerial = baseSerial
        self.customer = customer
        self.description = description

    def __repr__(self):
        return "{} {}".format(self.customer, self.name)


class Silicon(db.Model, AddUpdateDelete):
    __tablename__ = 'silicon'
    id = db.Column(db.Integer, primary_key=True)
    codename = db.Column(db.String(64), index=True, nullable=False)
    productCode = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(256), index=True)

    #Foreign Relationships
    siliconProducts = db.relationship('ProductSilicon', backref='silicon',
                                                            lazy='dynamic')

    def __init__(self, codename, productCode, description=""):
        self.codename = codename
        self.productCode = productCode
        self.description = description


    def __repr__(self):
        return "{} ({})".format(self.codename, self.productCode)

class ProductSilicon(db.Model, AddUpdateDelete):
    __tablename__ = 'product_silicon'
    id = db.Column(db.Integer, primary_key=True)

    #Creates the relationship with the PRODUCT table
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                          nullable=False)
    #Creates the relationship with the SILICON table
    silicon_id = db.Column(db.Integer, db.ForeignKey('silicon.id'),
                          nullable=False)

    def __init__(self, product, silicon):
        self.product_id = product
        self.silicon_id = silicon



    def __repr__(self):
        return "{} {}".format(self.product, self.silicon)



class Sample(db.Model, AddUpdateDelete):
    __tablename__ = 'sample'
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(64), index=True, nullable=False)

    #Creates the relationship with the PRODUCT table
    product_ids = db.Column(db.Integer, db.ForeignKey('product.id'),
                          nullable=False)

    #Foreign Keys
    hardware_revisions = db.relationship('SampleHardware', backref='sample',
                                         lazy='dynamic')
    test_ids = db.relationship('TestID', backref='sample',
                                         lazy='dynamic')

    def __init__(serial, product, hardwareRevision):
        self.serial = serial
        self.product_ids = product.id
        self.hardware_revisions = hardwareRevision




    def __repr__(self):
        return "{} ({})".format(self.productID, self.serial)


class HardwareRevision(db.Model, AddUpdateDelete):
    __tablename__ = "hardware_revision"
    id = db.Column(db.Integer, primary_key=True)
    ipn = db.Column(db.String(64), index=True, nullable=False)
    reworkNumber = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256))

    #Creates the relationship with the PRODUCT table
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                          nullable=False)

    #Foreign Relationships
    samples = db.relationship('SampleHardware', backref='hardware_revision', lazy='dynamic')
    test_ids = db.relationship('TestID', backref='hardware_revision', lazy='dynamic')

    def __init__(self, ipn, reworkNumber, description, product_id):
        self.ipn = ipn
        self.reworkNumber = reworkNumber
        self.description = description
        self.product_id = product_id


class SampleHardware(db.Model, AddUpdateDelete):
    __tablename__ = 'sample_hardware'
    id = db.Column(db.Integer, primary_key=True)

    #Creates the relationship with the SAMPLE table
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id'),
                          nullable=False)
    #Creates the relationship with the HARDWARE REVISION table
    hw_revision_id = db.Column(db.Integer, db.ForeignKey('hardware_revision.id'),
                          nullable=False)

class SoftwareComponent(db.Model, AddUpdateDelete):
    __tablename__ = 'software_component'
    id = db.Column(db.Integer, primary_key=True)

    ipn = db.Column(db.String(64), index=True)
    sw_id = db.Column(db.String(64), index=True)
    description = db.Column(db.String(256))

    #Creates the relationship with the PRODUCT table
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                          nullable=False)

    #Foreign Relationships
    hardware_revisions = db.relationship('HardwareSoftware', backref='software_component', lazy='dynamic')
    software_revisions = db.relationship('HardwareSoftware',
                                           backref='software_revision', lazy='dynamic')

    def __init__(self, product_id, ipn="default", sw_id="default",
                 description="default"):
        self.product_id = product_id
        self.ipn=ipn
        self.sw_id=sw_id
        self.description=description



class SoftwareRevision(db.Model, AddUpdateDelete):
    __tablename__ = 'software_revision'
    id = db.Column(db.Integer, primary_key=True)
    reworkNumber = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256))

    #Creates the relationship with the PRODUCT table
    component_id = db.Column(db.Integer, db.ForeignKey('software_component.id'),
                          nullable=False)

    def __init__(self, component_id, reworkNumber=0, description="Initial \
                 Revision"):
        self.component_id = component_id
        self.reworkNumber = reworkNumber
        self.description = description


class HardwareSoftware(db.Model, AddUpdateDelete):
    __tablename__ = 'hardware_software'
    id = db.Column(db.Integer, primary_key=True)

    #Creates the relationship with the HARDWARE REVISION table
    hw_revision_id = db.Column(db.Integer, db.ForeignKey('hardware_revision.id'),
                          nullable=False)
    #Creates the relationship with the SOFTWARE COMPONENT table
    software_id = db.Column(db.Integer, db.ForeignKey('software_component.id'),
                          nullable=False)

    def __init__(self, hw_revision_id, software_component_id):
        self.hw_revision_id = hw_revision_id
        self.software_id = software_component_id

class Test(db.Model, AddUpdateDelete):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(256))


    #Foreign Keys
    test_ids = db.relationship('TestID', backref='test', lazy='dynamic')

    def __init__(self, name, description):
        self.name = name
        self.description = description

class TestID(db.Model, AddUpdateDelete):
    __tablename__ = 'testid'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified_date = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)

    #Creates the relationship with the HARDWARE REVISION table
    hardware_revision_id = db.Column(db.Integer,
                                     db.ForeignKey('hardware_revision.id'),
                          nullable=False)

    #Creates the relationship with the TEST table
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'),
                          nullable=False)

    #Creates the relationship with the PRODUCT table
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                          nullable=False)

    #Creates the relationship with the SAMPLE table
    sample_id = db.Column(db.Integer, db.ForeignKey('sample.id'),
                          nullable=False)


    #Foreign Keys
    test_rows = db.relationship('TestRun', backref='testid', lazy='dynamic')

class TestRun(db.Model, AddUpdateDelete):
    __tablename__ = 'testrun'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    #Creates the relationship with the TESTID table
    test_id = db.Column(db.Integer, db.ForeignKey('testid.id'),
                          nullable=False)

    #Foreign Keys
    test_results = db.relationship('TestData', backref='testrun', lazy='dynamic')


class TestData(db.Model, AddUpdateDelete):
    __tablename__ = 'testdata'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    value = db.Column(db.String(64))
    attribute = db.Column(db.String(64))
    datatype = db.Column(db.String(64))

    #Creates the relationship with the TESTRUN table
    test_run = db.Column(db.Integer, db.ForeignKey('testrun.id'),
                          nullable=False)
