from flask import current_app, request, url_for
from app import db


class AddUpdateDelete:
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def add(self, resource):
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

    def __init__(self, codeName, productCode, description=""):
        self.codename = codeName
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
    test_runs = db.relationship('TestRun', backref='hardware_revision', lazy='dynamic')



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


class SoftwareRevision(db.Model, AddUpdateDelete):
    __tablename__ = 'software_revision'
    id = db.Column(db.Integer, primary_key=True)
    ipn = db.Column(db.String(64), index=True, nullable=False)
    reworkNumber = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256))

    #Creates the relationship with the PRODUCT table
    component_id = db.Column(db.Integer, db.ForeignKey('software_component.id'),
                          nullable=False)



class HardwareSoftware(db.Model, AddUpdateDelete):
    __tablename__ = 'hardware_software'
    id = db.Column(db.Integer, primary_key=True)

    #Creates the relationship with the HARDWARE REVISION table
    hw_revision_id = db.Column(db.Integer, db.ForeignKey('hardware_revision.id'),
                          nullable=False)
    #Creates the relationship with the SOFTWARE COMPONENT table
    software_id = db.Column(db.Integer, db.ForeignKey('software_component.id'),
                          nullable=False)


class TestRun(db.Model, AddUpdateDelete):
    __tablename__ = 'testrun'
    id = db.Column(db.Integer, primary_key=True)
    #CreatedDate
    #StoppedDate

    #Creates the relationship with the HARDWARE REVISION table
    hardware_revision_id = db.Column(db.Integer,
                                     db.ForeignKey('hardware_revision.id'),
                          nullable=False)

    #Creates the relationship with the TEST table
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'),
                          nullable=False)

class Test(db.Model, AddUpdateDelete):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(256))


    #Foreign Keys
    test_runs = db.relationship('TestRun', backref='test', lazy='dynamic')

