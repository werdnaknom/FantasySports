from flask import render_template, redirect, url_for, abort, flash, request, \
current_app, make_response

from app.main import main
from app.main.forms import CreateProductForm, CreateSiliconForm, CreateSampleForm

from app.models import Product, Silicon, ProductSilicon, Sample, \
        HardwareRevision, SoftwareComponent, SoftwareRevision, \
        HardwareSoftware, Test, TestID, TestRow, TestData, \
        SampleHardware



from app import db


@main.route('/', methods=['GET', 'POST'])
def index():
    products = Product.query.all()
    silicon = Silicon.query.all()
    ps = ProductSilicon.query.all()
    return render_template('index.html', products=products)

@main.route('/product/<int:product_id>', methods=['GET', 'POST'])
def product(product_id):
    product = Product.query.filter_by(id=product_id).first_or_404()
    return render_template('product.html', product=product,
                           Silicon=Silicon,
                           HardwareRevision = HardwareRevision)


@main.route('/addSilicon', methods=['GET', 'POST'])
def addSilicon():
    title = "Add Silicon"
    form = CreateSiliconForm()
    if form.validate_on_submit():
        name = form.codename.data
        productCode = form.productCode.data
        description = form.description.data
        silicon = Silicon(codename=name, productCode=productCode,
                          description=description)
        silicon.add(silicon)
        return redirect(url_for('.index'))
    return render_template('basic_form.html', form=form, title=title) 


@main.route('/addProduct', methods=['GET', 'POST'])
def addProduct():
    title = "Add Product"
    form = CreateProductForm()
    if form.validate_on_submit():
        #Gather Product Information from form
        name = form.name.data
        customer = form.customer.data
        baseSerial = form.serial.data
        description = form.description.data
        product = Product(name=name, customer=customer, baseSerial=baseSerial,
                          description=description)

        product.add(product)
        #Gather Silicon Information from Form
        silicon_id = form.silicon.data
        ps = ProductSilicon(product=product.id, silicon=silicon_id)
        ps.add(ps)


        #Update product on database
        product.silicon_id = ps.id
        product.update()

        #Create Default HW Revision
        ipn = form.ipn.data
        hwrev = HardwareRevision(ipn=ipn, reworkNumber=0, description="Initial \
                                 PBA", product_id=product.id)
        hwrev.add(hwrev)

        #Create Default Software Component
        sw = SoftwareComponent(product_id=product.id)
        sw.add(sw)

        #Create Default Software Revision
        swrev = SoftwareRevision(component_id=sw.id,
                                reworkNumber=0,
                                description="Initial Revision")
        swrev.add(swrev)

        #Add the relationship between HW revision and SW revisions
        hwsw =  HardwareSoftware(hw_revision_id = hwrev.id,
                                 software_component_id = sw.id)
        hwsw.add(hwsw)

        return redirect(url_for('.product',product_id=product.id))
    return render_template('basic_form.html', form=form, title=title) 


@main.route('/addSample/<int:product_id>', methods=['GET', 'POST'])
def addSample(product_id):
    title = "Add Sample"
    product = Product.query.filter_by(id=product_id).first_or_404()
    form = CreateSampleForm(product=product)
    if form.validate_on_submit():
        serialNum = form.serialNum.data
        hardware_revision_id = form.hardwareRev.data
        print(dir(form.hardwareRev))
        print(form.hardwareRev.description)
        print(form.hardwareRev.gettext)
        print(form.hardwareRev.id)
        print(form.hardwareRev.label)
        print(form.hardwareRev.choices)

        sample = Sample(serial=serialNum, product=product)
        sample.add(sample)

        #Create Sample/HW Revision link
        samplehw = SampleHardware(sample_id = sample.id,
                                  hardware_revision_id = hardware_revision_id)
        samplehw.add(samplehw)
        return redirect(url_for('.product', product_id=product.id))
    return render_template('basic_form.html', form=form, title=title)


@main.route('/sample/<int:sample_id>', methods=['GET', 'POST'])
def sample(sample_id):
    title = "Sample ID #%d" % sample_id

    sample = Sample.query.filter_by(id=sample_id).first_or_404()
    return render_template('sample.html', title=title, sample=sample,
                          HardwareRevision = HardwareRevision,
                          Test = Test)



@main.route('/hardwarerevision/<int:hardware_revision>',
            methods=['GET', 'POST'])
def hardware_revision(hardware_revision):
    title = "Sample ID #%d" % sample_id

    sample = Sample.query.filter_by(id=sample_id).first_or_404()
    return render_template('hardware_revision.html')



@main.route('/testid/<int:testid_id>', methods=['GET', 'POST'])
def testid(testid_id):
    title = "Test ID #%d" % testid_id

    testid = TestID.query.filter_by(id=testid_id).first_or_404()
    print(testid)
    print(testid.id)
    print(testid.test_rows.all())
    return render_template('testid.html', title=title, testid=testid)

