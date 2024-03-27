from django.test import TestCase
from store.forms import SignupForm, CheckoutForm, ListingForm, BookForm

class SignUpFormTest(TestCase):
    def test_sign_up_form_email_required(self):
        form = SignupForm()
        self.assertTrue(form.fields['email'].required)

    #def test_sign_up_form_types(self):
        #form = signupForm()
        #self.assertTrue(form.fields)

    def test_checkout_input_length(self):
        form = CheckoutForm()
        self.assertTrue(form.fields['cardNum'].max_length==16)
        self.assertTrue(form.fields['CVV'].max_length==3)


    def test_checkout_form_fields(self):
        data = {
            "address":"1000 test",
            "paymentType":"Visa",
            "cardNum":"4444999923410000",
            "CVV":"123",
            "Expiration":"01/20/2025",
            }
        form = CheckoutForm(data)
        self.assertTrue(form.is_valid())

    def test_checkout_form_fields_false(self):
        data = {
            "address":"1000 test",
            "paymentType":"Visa",
            "cardNum":"4444999923410000",
            "CVV":"12345",
            "Expiration":"01/20/2025",
            }
        form = CheckoutForm(data)
        self.assertFalse(form.is_valid())


    def test_listing_form_input_length(self):
        form = ListingForm()
        self.assertTrue(form.fields['isbn'].max_length==13)
        self.assertTrue(form.fields['quantity'].initial==1 and form.fields['quantity'].min_value==1 and form.fields['quantity'].max_value==99)
        self.assertTrue(form.fields['price'].initial==9.99 and form.fields['price'].min_value==1)

    def test_listing_image_req(self):
        form = ListingForm()
        self.assertFalse(form.fields['image'].required)

    def test_listing_form_fields(self):
        data = {
            "isbn":"1936401640382",
            "quantity":"2",
            "price": "19.99",
            }
        form = ListingForm(data)
        self.assertTrue(form.is_valid())

    def test_listing_form_isbn_false(self):
        data = {
            "isbn":"19364016403822",
            "quantity":"2",
            "price": "19.99",
            }
        form = ListingForm(data)
        self.assertFalse(form.is_valid())

    def test_listing_form_quantity_false(self):
        data = {
            "isbn":"19364016403822",
            "quantity":"-1",
            "price": "19.99",
            }
        form = ListingForm(data)
        self.assertFalse(form.is_valid())

    def test_listing_form_price_false(self):
        data = {
            "isbn":"19364016403822",
            "quantity":"2",
            "price": "0.50",
            }
        form = ListingForm(data)
        self.assertFalse(form.is_valid())

    def test_book_form_input_length(self):
        form = BookForm()
        self.assertTrue(form.fields['isbn'].max_length==13)
        self.assertTrue(form.fields['pages'].min_value==1)
        self.assertTrue(form.fields['rating'].min_value == 0 and form.fields['rating'].max_value ==5)

    def test_book_description_req(self):
        form = BookForm()
        self.assertFalse(form.fields['description'].required)

    def test_book_form_fields(self):
        data = {
            "title":"Huckleberry Finn",
            "author":"Mark Twain",
            "isbn":"7364590382738",
            "pages":"362",
            "rating":"4.5"
            }
        form = BookForm(data)
        self.assertTrue(form.is_valid())

    def test_book_form_isbn_false(self):
        data = {
            "title":"Huckleberry Finn",
            "author":"Mark Twain",
            "isbn":"73645903827381",
            "pages":"362",
            "rating":"4.5"
            }
        form = BookForm(data)
        self.assertFalse(form.is_valid())

    def test_book_form_pages_false(self):
        data = {
            "title":"Huckleberry Finn",
            "author":"Mark Twain",
            "isbn":"7364590382738",
            "pages":"0",
            "rating":"4.5"
            }
        form = BookForm(data)
        self.assertFalse(form.is_valid())


    def test_book_form_rating_false(self):
        data = {
            "title":"Huckleberry Finn",
            "author":"Mark Twain",
            "isbn":"7364590382738",
            "pages":"0",
            "rating":"-4.5"
            }
        form = BookForm(data)
        self.assertFalse(form.is_valid())





    '''
    Here are some other example tests I found online that we could potentailly use:

    def test_renew_form_date_field_help_text(self):
        form = RenewBookForm()
        self.assertEqual(form.fields['renewal_date'].help_text, 'Enter a date between now and 4 weeks (default 3).')

    def test_renew_form_date_in_past(self):
        date = datetime.date.today() - datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_too_far_in_future(self):
        date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertFalse(form.is_valid())

    def test_renew_form_date_today(self):
        date = datetime.date.today()
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())

    def test_renew_form_date_max(self):
        date = timezone.localtime() + datetime.timedelta(weeks=4)
        form = RenewBookForm(data={'renewal_date': date})
        self.assertTrue(form.is_valid())
    '''
