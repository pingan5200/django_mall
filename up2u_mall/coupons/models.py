from django.db import models
from django.core.validators import MinValueValidator, \
MaxValueValidator


class Coupon(models.Model):
    # 示例：DE8UG50直接减50, SALE30，原价减30%，即打七折
    # 夸张点，WHOSYOURDADDY, 直接到1块
    code = models.CharField(max_length=50, unique=True, verbose_name='优惠码')
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)], default=0)

    active = models.BooleanField()

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = '优惠券'
        verbose_name_plural = verbose_name