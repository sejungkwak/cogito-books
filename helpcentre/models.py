from django.db import models


class UserContact(models.Model):
    """
    A database model for the Contact Us form.
    """

    SUBJECT = (
        ('product', 'Product Enquiries'),
        ('order', 'Order Enquiries'),
        ('loyalty', 'Loyalty Points Enquiries'),
        ('refund', 'Refund Enquiries'),
        ('website', 'Website Enquiries'),
        ('other', 'Other')
    )

    STATUS = (
        ('open', 'Open'),
        ('closed', 'Closed')
    )

    subject = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        choices=SUBJECT,
        default='product')
    name = models.CharField(max_length=254, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    message = models.TextField(null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        null=False,
        blank=False,
        choices=STATUS,
        default='open')

    class Meta:
        ordering = ['status', 'date']

    def __str__(self):
        return f'{self.subject} from {self.name}({self.status})'
