from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from classform.models import ClassRoom, ClassRoomStudent
from django.shortcuts import reverse
from form.models import StudentInfo
import calendar
from typing import List

# Create your models here.


class Fine(models.Model):
    fine = models.IntegerField()
    student = models.ForeignKey(ClassRoomStudent, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    submissionDate = models.DateField(null=True)
    description = models.TextField()


class Session(models.Model):
    name = models.CharField(max_length=20, unique=True,
                            null=False, blank=False)
    start = models.DateField(null=False, blank=False)
    end = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.name


class FeeCategory(models.Model):

    class SubmissionMode(models.TextChoices):
        MONTHLY = 'monthly'
        ANUALLY = 'anually'

    submission_mode = models.CharField(
        max_length=30,
        choices=SubmissionMode.choices,
        default=SubmissionMode.ANUALLY,
        null=False,
        blank=False
    )
    name = models.CharField(
        max_length=100,
        unique=True,
        null=False,
        blank=False,
    )
    deduction_order = models.IntegerField(unique=True, null=False)

    def get_absolute_url(self):
        return reverse("editFeeCategory", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Fee category - {self.name}"


class FeeDiscount(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage'
        ABSOLUTE = 'absolute'

    session = models.ForeignKey(Session, null=False, on_delete=models.CASCADE)
    discount_category = models.CharField(
        null=False,
        blank=False,
        max_length=30,
        unique=True
    )
    fee_categories = models.ManyToManyField(
        FeeCategory,
        related_name='discounts'

    )
    discount = models.FloatField(null=False, blank=False)
    discount_type = models.CharField(
        max_length=30,
        null=False,
        blank=False,
        choices=DiscountType.choices,
        default=DiscountType.PERCENTAGE
    )
    description = models.CharField(max_length=1000, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("editFeeDiscount", kwargs={"pk": self.pk})

    def __str__(self):
        return f"Fee Discount: {self.discount_category}"


class ClassSectionFees(models.Model):
    classSection = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    feeCategory = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    fees = models.IntegerField()

    def __str__(self):
        return f"{self.classSection} {self.feeCategory} {self.fees}"


def user_directory_path(instance, filename):
    """file will be uploaded to given path"""
    return 'fee-slip/{0}/{1}'.format(instance.student.student.admissionNumber, filename)


class Fee(models.Model):
    regNo = models.IntegerField()
    classSection = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    student = models.ForeignKey(ClassRoomStudent, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    submissionDate = models.DateField()
    amount = models.IntegerField()
    monthsPaid = models.CharField(max_length=50)
    feeSlip = models.FileField(upload_to=user_directory_path)

    def __str__(self):
        return f"{self.student} {self.amount} {self.monthsPaid}"


class FeeCycle(models.Model):

    class Cycle(models.TextChoices):
        MONTHLY = 'monthly',
        QUATERLY = 'quarterly'
        YEARLY = 'yearly'

    MONTHS = [(i, calendar.month_name[i]) for i in range(1, 13)]

    last_submission_date = models.IntegerField(null=False, blank=False)
    starting_month = models.IntegerField(
        choices=MONTHS, null=False, blank=False
    )
    session = models.OneToOneField(
        Session, null=False, on_delete=models.CASCADE
    )
    cycle = models.CharField(
        choices=Cycle.choices,
        default=Cycle.YEARLY,
        null=False,
        blank=False,
        max_length=50
    )

    def get_absolute_url(self):
        return reverse("editFeeCycle", kwargs={"pk": self.pk})


class FeeConfiguration(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=False)
    amount = models.FloatField(null=False)
    classrooms = models.ManyToManyField(
        ClassRoom,
        related_name='fee_configurstions'
    )
    fee_category = models.ForeignKey(
        FeeCategory,
        on_delete=models.CASCADE, null=False
    )

    def get_absolute_url(self):
        return reverse("editFeeConfiguration", kwargs={"pk": self.pk})

    class Meta:
        unique_together = (('fee_category', 'session'),)


class StudentDiscount(models.Model):
    discount_category = models.ForeignKey(
        FeeDiscount,
        on_delete=models.CASCADE,
        null=False
    )
    student = models.ManyToManyField(
        StudentInfo,
        through='StudentDiscountThrough',
    )

    def get_absolute_url(self):
        return reverse("editStudentDiscount", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.discount_category}"


class StudentDiscountThrough(models.Model):
    student = models.ForeignKey(
        StudentInfo, on_delete=models.CASCADE, related_name='fee_discounts',)
    discount = models.ForeignKey(StudentDiscount, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=10)

    def save(self, *args, **kwargs):
        self.amount = self.discount.discount_category.discount
        return super().save(*args, **kwargs)


class FeeHeadMapping(models.Model):
    amount = models.FloatField(null=False)
    fee_configuration = models.ForeignKey(
        FeeConfiguration,
        on_delete=models.CASCADE,
        null=False
    )
    student = models.ForeignKey(
        StudentInfo,
        on_delete=models.CASCADE,
        null=False,
        related_name='fee_head_mappings'
    )
    fee_category = models.ForeignKey(
        FeeCategory,
        on_delete=models.CASCADE, null=False
    )

    month = models.PositiveIntegerField(null=False, blank=False)


class FeeStatus(models.Model):
    student = models.ForeignKey(StudentInfo, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    month = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField()
    received = models.PositiveIntegerField()
    balance = models.PositiveIntegerField()

    class Meta:
        unique_together = (('student', 'session'),)


@receiver(m2m_changed, sender=StudentDiscount.student.through)
def apply_default_amount(
    sender, instance: StudentDiscount, action: str,
    *args, pk_set, using, **kwargs
):
    if action == 'post_add':
        for pk in pk_set:
            obj: StudentDiscountThrough = StudentDiscountThrough.objects.get(
                student__admissionNumber=pk)
            obj.amount = obj.discount.discount_category.discount
            obj.save()


@receiver(m2m_changed, sender=FeeConfiguration.classrooms.through)
def addFeeHeadMapping(
    sender, instance: FeeConfiguration, action: str,
    *args, pk_set, using, **kwargs
):

    if action == 'pre_remove':
        for pk in pk_set:
            classroom = ClassRoom.objects.get(pk=pk)
            FeeHeadMapping.objects.filter(
                classroom_student__classRoom__pk=pk).delete()

    elif action == 'post_add':
        for pk in pk_set:
            for classroom_student in ClassRoomStudent.objects.filter(classRoom__pk=pk):
                for i in range(1, 13):
                    fee_head_mapping_obj: FeeHeadMapping = FeeHeadMapping()
                    fee_head_mapping_obj.student = classroom_student.student
                    fee_head_mapping_obj.month = i
                    fee_head_mapping_obj.fee_category = instance.fee_category
                    fee_head_mapping_obj.fee_configuration = instance
                    if instance.fee_category.submission_mode == FeeCategory.SubmissionMode.MONTHLY:
                        fee_head_mapping_obj.amount = instance.amount
                        fee_head_mapping_obj.fee_category = instance.fee_category
                        fee_head_mapping_obj.save()
                    elif instance.fee_category.submission_mode == FeeCategory.SubmissionMode.ANUALLY:
                        if i == instance.session.start.month:
                            fee_head_mapping_obj.fee_category = instance.fee_category
                            fee_head_mapping_obj.amount = instance.amount
                            fee_head_mapping_obj.save()
