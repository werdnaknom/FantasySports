from flask import current_app, request, url_for, jsonify
import datetime
from app import db
import app.api.status as status
from sqlalchemy.exc import SQLAlchemyError

def generate_fake():
    Silicon.insert_silicon()
    Product.generate_fake(100)
    HardwareRevision.generate_fake()
    Test.generate_fake(20)
    TestID.generate_fake(100)
    TestRow.generate_fake(500)


class AddUpdateDelete():
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

#Association Tables
#Product / Silicon
productsilicon = db.Table('product_silicon_association',
                                db.Column('product_id', db.Integer,
                                          db.ForeignKey('product.id')),
                                db.Column('silicon_id', db.Integer,
                                          db.ForeignKey('silicon.id'))
                               )

# Sample / Hardware Revision
samplehardware = db.Table('sample_hardware_association',
                                db.Column('sample_id', db.Integer,
                                          db.ForeignKey('sample.id'),
                                         primary_key = True),
                                db.Column('hardware_revision_id', db.Integer,
                                          db.ForeignKey(
                                              'hardware_revision.id'),
                                         primary_key = True)
                               )
# Hardware Revision / Software Components
hardwaresoftware = db.Table('hardware_software_association',
                                db.Column('software_component_id', db.Integer,
                                          db.ForeignKey(
                                              'software_component.id'),
                                         primary_key = True),
                                db.Column('hardware_revision_id', db.Integer,
                                          db.ForeignKey(
                                              'hardware_revision.id'),
                                         primary_key = True)
                         )




class Product(db.Model, AddUpdateDelete):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    baseSerial = db.Column(db.String(64), index=True, nullable=False)
    customer = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(256))


    #Foreign Relationships
    silicon = db.relationship('Silicon', secondary = productsilicon,
                                     lazy='subquery',
                             backref = db.backref('products',
                                                  lazy='dynamic')
                             )
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

    def to_json(self):
        json_product = {
            'id' : self.id,
            'url' : url_for('api.product', id=self.id),
            'name' : self.name,
            'baseSerial' : self.baseSerial,
            'customer' : self.customer,
            'description' : self.description,
            #TODO 'silicon' : self.silicon.all(),
            #TODO 'samples' : self.samples.all(),
            #TODO 'hardware_revisions' : self.hw_revisions.query.all(),
            #TODO 'tests' : self.test_ids.query.all()
        }
        return json_product
    '''
    @staticmethod
    def from_json(json_post):
        name = json_post.get('name')
        baseSerial = json_post.get('baseSerial')
        customer = json_post.get('customer')
        description = json_post.get('description')
    '''



    def __repr__(self):
        return "{} {}".format(self.customer, self.name)

    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed, randint
        import forgery_py


        seed()
        silicon_count = Silicon.query.count()
        for i in range(count):
            #Creates a product
            name = forgery_py.name.company_name()
            baseSerial = forgery_py.basic.hex_color()
            customer = forgery_py.name.job_title()
            description = forgery_py.lorem_ipsum.sentence()
            p = Product(name, baseSerial, customer, description)
            p.add(p)

            #Adds silicon to product
            for i in range(0,randint(1,3)):

                silicon = Silicon.query.offset(randint(0,silicon_count-1)).first()
                silicon.products.append(p)
                silicon.update()




class Silicon(db.Model, AddUpdateDelete):
    __tablename__ = 'silicon'
    id = db.Column(db.Integer, primary_key=True)
    codename = db.Column(db.String(64), index=True, nullable=False)
    productCode = db.Column(db.String(64), index=True, nullable=False)
    description = db.Column(db.String(256), index=True)

    #Foreign Relationships
    #siliconProducts = db.relationship('ProductSilicon', backref='silicon',
    #                                                        lazy='dynamic')

    def __init__(self, codename, productCode, description=""):
        self.codename = codename
        self.productCode = productCode
        self.description = description

    def to_json(self):
        json_silicon = {
            'id' : self.id,
            'codename' : self.codename,
            'productCode' : self.productCode,
            'description' : self.description
        }
        return json_silicon

    @staticmethod
    def insert_silicon():
        basic_silicon = {
            'Red Rock Canyon' : {'codename' : 'Red Rock Canyon',
                                 'productCode' : 'FM10K',
                                 'description' : '100G Switch Silicon'},
            'Fortville' : {'codename' : 'Fortville',
                                 'productCode' : 'X710',
                                 'description' : '10/25G Network IC'},
            'Sageville' : {'codename' : 'Sageville',
                                 'productCode' : 'X510',
                                 'description' : '10G Base-T Network IC'},
        }

        for s in basic_silicon:
            silicon = Silicon(codename = basic_silicon[s]['codename'],
                                  productCode =
                              basic_silicon[s]['productCode'],
                                  description =
                              basic_silicon[s]['description'])
            db.session.add(silicon)
        db.session.commit()

    def __repr__(self):
        return "{} ({})".format(self.codename, self.productCode)


class Sample(db.Model, AddUpdateDelete):
    __tablename__ = 'sample'
    id = db.Column(db.Integer, primary_key=True)
    serial = db.Column(db.String(64), index=True, nullable=False)

    #Creates the relationship with the PRODUCT table
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                          nullable=False)

    #Foreign Keys
    hardware_revisions = db.relationship('HardwareRevision',
                                         secondary = samplehardware,
                                         lazy = 'subquery',
                                         backref = db.backref('samples',
                                                              lazy = 'subquery'
                                                             )
                                        )

    test_ids = db.relationship('TestID', backref='sample',
                                         lazy='dynamic')

    def __init__(self, serial, product_id):
        self.serial = serial
        self.product_id = product_id

    def to_json(self):
        json_sample = {
            'id' : self.id,
            'serial' : self.serial,
            'product_id' : self.product_id,
            #TODO 'hardware_revisions' : self.hardware_revisions.query.all(),
            #TODO 'test_ids' : self.test_ids.query.all(),
        }
        return json_sample

    @staticmethod
    def from_json(request_dict):
        if not request_dict:
            response = {'message' : 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            serial = request_dict['serial']
            product_id = request_dict['product_id']
            hwrev_id = request_dict['hardware_revision_id']
            sample = Sample(serial = serial,
                           product_id = product_id)
            sample.add(sample)

            hwrev = HardwareRevision.query.get_or_404(hwrev_id)
            hwrev.samples.append(sample)
            hwrev.update()

            query = Sample.query.get(sample.id)
            result = query.to_json()
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error" : str(e)})
            return resp, status.HTTP_400_BAD_REQUEST


    def __repr__(self):
        return "{} ({})".format(self.product_id, self.serial)


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
    software = db.relationship('SoftwareComponent', secondary=hardwaresoftware,
                               lazy = 'dynamic',
                               backref = db.backref('hardware_revision',
                                                    lazy = 'dynamic'))


    test_ids = db.relationship('TestID', backref='hardware_revision', lazy='dynamic')

    def __init__(self, ipn, reworkNumber, description, product_id):
        self.ipn = ipn
        self.reworkNumber = reworkNumber
        self.description = description
        self.product_id = product_id

    def to_json(self):
        json_hwrev = {
            'id' : self.id,
            'ipn' : self.ipn,
            'reworkNumber' : self.reworkNumber,
            'description' : self.description,
            'product_id' : self.product_id,
            #TODO 'samples' : self.samples.query.all(),
            #TODO 'test_ids' : self.test_ids.query.all(),
        }
        return json_hwrev

    def __repr__(self):
        return "{} (Rev: {}) -- {}".format(self.ipn, self.reworkNumber,
                                           self.description)


    @staticmethod
    def generate_fake():
        from random import seed, randint
        import forgery_py

        seed()
        for product in Product.query.all():
            for rev in range(0, randint(0,10)):

                ipn = forgery_py.address.zip_code()
                reworkNumber = rev
                description = forgery_py.lorem_ipsum.sentence()
                hwrev = HardwareRevision(ipn = ipn,
                                     reworkNumber = reworkNumber,
                                     description = description,
                                     product_id = product.id)
                hwrev.add(hwrev)
                for s in range(0, randint(0,10)):
                    sample = Sample(serial=forgery_py.basic.string.hexdigits,
                            product_id=product.id)
                    sample.add(sample)

                    hwrev.samples.append(sample)
                    hwrev.update()



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

    software_revisions = db.relationship('SoftwareRevision',
                                           backref='software_revision',
                                         lazy='dynamic')

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
    component_id = db.Column(db.Integer,
                             db.ForeignKey('software_component.id'),
                             nullable=False)

    def __init__(self, component_id, reworkNumber=0,
                 description="Initial Revision"):
        self.component_id = component_id
        self.reworkNumber = reworkNumber
        self.description = description


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

    def to_json(self):
        json_test = {
            'id' : self.id,
            'name' : self.name,
            'description' : self.description,
            'testids' : self.test_ids.count(),
            #TODO testids.query.all()
        }
        return json_test

    @staticmethod
    def generate_fake(count=20):
        from random import seed, randint
        import forgery_py

        seed()
        for _ in range(0, count):
            name = forgery_py.address.street_name()
            description = forgery_py.lorem_ipsum.sentence()
            test = Test(name=name, description = description)
            test.add(test)




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
    test_rows = db.relationship('TestRow',
                                backref='testid',
                                lazy='subquery')

    def __init__(self, test_id, hwrev_id, product_id, sample_id):
        self.test_id = test_id
        self.hardware_revision_id = hwrev_id
        self.product_id = product_id
        self.sample_id = sample_id

    def to_json(self):
        json_testid = {
            'id' : self.id,
            #TODO 'created' : self.created_date,
            #TODO 'modified' : self.modified_date,
            'hardware_revision' : self.hardware_revision_id,
            'test' : self.test_id,
            'product' : self.product_id,
            'sample_id' : self.sample_id,
            #TODO 'test_rows' : self.test_rows.all(),
        }

        '''
            'hardware_revision' : url_for('api.get_hardware_revision',
                                          id=self.hardware_revision_id),
            'test' : url_for('api.get_test', id=self.test_id),
            'product' : url_for('api.get_product', id=self.product_id),
            'sample_id' : url_for('api.get_sample', id=self.sample_id),
        '''
        return json_testid

    @staticmethod
    def from_json(request_dict):
        if not request_dict:
            response = {'message' : 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            sample_id = request_dict['sample_id']
            sample = Sample.query.get(sample_id)
            testid = TestID(test_id = request_dict['test_id'],
                            hwrev_id = request_dict['hardware_revision_id'],
                            sample = sample
                           )
            testid.add(testid)
            query = TestID.query.get(testid.id)
            result = query.to_json()
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error" : str(e)})
            return resp, status.HTTP_400_BAD_REQUEST


    def __repr__(self):
        return "TESTID {}".format(self.id)

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        hwrev_count = HardwareRevision.query.count()
        test_count = Test.query.count()

        seed()
        for _ in range(0, count):
            test = Test.query.offset(randint(0, test_count-1)).first()
            rand = randint(0, hwrev_count - 1)
            hardware_rev = HardwareRevision.query.get(rand)
            sample_count = len(hardware_rev.samples)
            print(_, sample_count)
            if sample_count != 0:
                sample = hardware_rev.samples[randint(0, sample_count -1 )]
                product = sample.product
                testid = TestID(test_id = test.id, hwrev_id=hardware_rev.id,
                               product_id = product.id, sample_id = sample.id)
                testid.add(testid)
            else:
                pass


class TestRow(db.Model, AddUpdateDelete):
    __tablename__ = 'testrow'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


    #Creates the relationship with the TESTID table
    test_id = db.Column(db.Integer, db.ForeignKey('testid.id'),
                          nullable=False)

    #Foreign Keys
    test_results = db.relationship('TestData',
                                   backref='testrow',
                                   lazy='subquery')

    def __init__(self, test_id):
        self.test_id = test_id

    def to_json(self):
        json_testrow = {
            'id' : self.id,
            #TODO 'created' : self.created_date,
            #TODO 'testid' : url_for('api.get_testid', id=test_id),
            #TODO 'results' : test_results.query.all(),
        }
        return json_testrow

    @staticmethod
    def from_json(request_dict):
        if not request_dict:
            response = {'message' : 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            testrow = TestRow(test_id = request_dict['test_id'])
            testrow.add(testrow)
            query = TestRow.query.get(testrow.id)
            result = query.to_json()
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error" : str(e)})
            return resp, status.HTTP_400_BAD_REQUEST


    def __repr__(self):
        return "TestRow {} TestID:{}".format(self.id, self.test_id)

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        test_id_count = TestID.query.count()

        seed()
        for _ in range(0, count):
            testid = TestID.query.offset( \
                randint(0, test_id_count - 1)).first()

            for row in range(0, randint(0, 100)):
                testrow = TestRow(testid.id)
                testrow.add(testrow)
                attributes = [('BER1',randint(0,100)),
                          ('Voltage', randint(10,14)),
                          ('Current', randint(0,8)),
                          ('BER2', randint(0,100)),
                          ('BER3', randint(0,100)),
                          ('BER4', randint(0,100)),
                          ('Temperature', randint(0,60)),
                          ('User', forgery_py.name.full_name()),
                          ('Chamber', forgery_py.name.last_name())
                         ]
                for a in attributes:
                    attribute = a[0]
                    value = a[1]
                    testData = TestData(
                        test_row = testrow.id,
                        value = value,
                        attribute = attribute,
                        datatype = type(value).__name__)
                    testData.add(testData)



class TestData(db.Model, AddUpdateDelete):
    __tablename__ = 'testdata'
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    value = db.Column(db.String(64))
    attribute = db.Column(db.String(64))
    datatype = db.Column(db.String(64))

    #Creates the relationship with the TESTRUN table
    test_row = db.Column(db.Integer, db.ForeignKey('testrow.id'),
                          nullable=False)

    def __init__(self, test_row, value, attribute,
                 datatype=type(value).__name__):
        self.test_row = test_row
        self.value = value
        self.attribute = attribute
        self.datatype = datatype

    def to_json(self):
        json_data = {
            'id' : self.id,
            #TODO 'created' : self.created_date,
            'value' : self.value,
            'attribute' : self.attribute,
            'datatype' : self.datatype,
            'test_row' : url_for('api.testrow', id=self.test_row)
        }
        return json_data

    @staticmethod
    def from_json(request_dict):
        if not request_dict:
            response = {'message' : 'No input data provided'}
            return response, status.HTTP_400_BAD_REQUEST
        try:
            testdata = TestData(test_row = request_dict['testrow_id'],
                               value = request_dict['value'],
                               attribute = request_dict['attribute'],
                               datatype = request_dict['datatype'])
            testdata.add(testdata)
            query = TestData.query.get(testdata.id)
            result = query.to_json()
            return result, status.HTTP_201_CREATED
        except SQLAlchemyError as e:
            db.session.rollback()
            resp = jsonify({"error" : str(e)})
            return resp, status.HTTP_400_BAD_REQUEST

    def __repr__(self):
        return "Attribute: {}, Data: {}".format(self.attribute, self.value)



