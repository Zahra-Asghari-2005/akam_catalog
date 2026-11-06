from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

class Category(models.Model):

    name = models.CharField(max_length=250)

    slug = models.SlugField(
        max_length=170,
        unique=True,
        allow_unicode=True,
        blank=True
    )

    description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'دسته‌ بندی'
        verbose_name_plural = 'دسته‌ بندی‌ ها'

    def save(self, *args, **kwargs):

        if not self.slug:
            base_slug = slugify(self.name, allow_unicode=True) or 'category'
            self.slug = base_slug

            counter = 1

            while Category.objects.filter(
                slug=self.slug
            ).exclude(pk=self.pk).exists():

                self.slug = f'{base_slug}-{counter}'
                counter += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Service(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='services'
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=250,
        unique=True,
        allow_unicode=True
    )

    short_description = models.CharField(
        max_length=300,
        blank=True
    )

    description = models.TextField(blank=True)

    image_url = models.URLField(
        max_length=500,
        blank=True
    )

    icon = models.CharField(
        max_length=100,
        blank=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'خدمت'
        verbose_name_plural = 'خدمات'

    def __str__(self):
        return self.title


class ServiceFeature(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='features'
    )

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'ویژگی خدمت'
        verbose_name_plural = 'ویژگی‌های خدمات'

        constraints = [
            models.UniqueConstraint(
                fields=['service', 'name'],
                name='unique_feature_per_service'
            )
        ]

    def __str__(self):
        return f'{self.service.title} - {self.name}'


class ServicePlan(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='plans'
    )

    name = models.CharField(max_length=150)

    description = models.TextField(blank=True)

    badge = models.CharField(
        max_length=100,
        blank=True
    )

    duration = models.CharField(
        max_length=100,
        blank=True
    )

    is_recommended = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    features = models.ManyToManyField(
        ServiceFeature,
        through='PlanFeature',
        related_name='plans',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'پلن خدمت'
        verbose_name_plural = 'پلن‌های خدمات'

        constraints = [
            models.UniqueConstraint(
                fields=['service', 'name'],
                name='unique_plan_per_service'
            )
        ]

    def __str__(self):
        return f'{self.service.title} - {self.name}'


class PlanFeature(models.Model):

    plan = models.ForeignKey(
        ServicePlan,
        on_delete=models.CASCADE,
        related_name='plan_features'
    )

    feature = models.ForeignKey(
        ServiceFeature,
        on_delete=models.CASCADE,
        related_name='plan_features'
    )

    value = models.CharField(
        max_length=200,
        blank=True
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'ویژگی پلن'
        verbose_name_plural = 'ویژگی‌های پلن‌ها'

        constraints = [
            models.UniqueConstraint(
                fields=['plan', 'feature'],
                name='unique_feature_per_plan'
            )
        ]

    def clean(self):

        super().clean()

        if (
            self.plan_id
            and self.feature_id
            and self.plan.service_id != self.feature.service_id
        ):
            raise ValidationError({
                'feature': 'این ویژگی متعلق به خدمت دیگری است.'
            })

    def __str__(self):
        return f'{self.plan.name} - {self.feature.name}'


class ServiceAddon(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='addons'
    )

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'خدمت جانبی'
        verbose_name_plural = 'خدمات جانبی'

    def __str__(self):
        return f'{self.service.title} - {self.name}'


class ServiceOption(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='options'
    )

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'گزینه خدمت'
        verbose_name_plural = 'گزینه‌های خدمات'

        constraints = [
            models.UniqueConstraint(
                fields=['service', 'name'],
                name='unique_option_per_service'
            )
        ]

    def __str__(self):
        return f'{self.service.title} - {self.name}'


class ServiceGuide(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='guides'
    )

    title = models.CharField(max_length=200)

    text = models.TextField()

    class Meta:
        ordering = ['id']
        verbose_name = 'راهنمای خدمت'
        verbose_name_plural = 'راهنماهای خدمات'

    def __str__(self):
        return f'{self.service.title} - {self.title}'


class ServiceNote(models.Model):

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='notes'
    )

    text = models.TextField()

    class Meta:
        ordering = ['id']
        verbose_name = 'نکته خدمت'
        verbose_name_plural = 'نکات خدمات'

    def __str__(self):
        return f'{self.service.title} - {self.id}'



class ConsultationRequest(models.Model):

    class Status(models.TextChoices):

        NEW = 'new', 'جدید'

        DONE = 'done', 'پیگیری شده'

    name = models.CharField(max_length=200)

    phone = models.CharField(max_length=20)

    service = models.ForeignKey(
        Service,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultation_requests'
    )

    plan = models.ForeignKey(
        ServicePlan,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultation_requests'
    )

    message = models.TextField(blank=True)

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.NEW
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'درخواست مشاوره'
        verbose_name_plural = 'درخواست‌های مشاوره'

    def clean(self):

        super().clean()

        if (
            self.service_id
            and self.plan_id
            and self.plan.service_id != self.service_id
        ):
            raise ValidationError({
                'plan': 'این پلن متعلق به خدمت انتخاب‌شده نیست.'
            })

    def __str__(self):
        return f'{self.name} - {self.phone}'