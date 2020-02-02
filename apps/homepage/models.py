from django.db import models


class SponsorGradeTypes:
    FIRST = 'first'
    SECOND = 'second'
    THIRD = 'third'
    TYPES = (
        (FIRST, 'First Grade'),
        (SECOND, 'Second Grade'),
        (THIRD, 'Third Grade')
    )


class Intro(models.Model):
    header_en = models.CharField(max_length=100)
    header_fa = models.CharField(max_length=100)
    text_en = models.TextField()
    text_fa = models.TextField()

    term_of_use = models.TextField(null=True)

    def __str__(self):
        return self.header_en


class TimelineEvent(models.Model):
    date = models.DateTimeField()
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100)
    text_en = models.TextField()
    text_fa = models.TextField()

    order = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return self.title_en


class Prize(models.Model):
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100)
    prize_en = models.CharField(max_length=100)
    prize_fa = models.CharField(max_length=100)

    def __str__(self):
        return self.title_en


class Stat(models.Model):
    title_en = models.CharField(max_length=100)
    title_fa = models.CharField(max_length=100)
    stat_en = models.CharField(max_length=100)
    stat_fa = models.CharField(max_length=100)

    def __str__(self):
        return self.title_en


class Sponsor(models.Model):
    name_en = models.CharField(max_length=200)
    name_fa = models.CharField(max_length=200)
    url = models.CharField(max_length=500)
    grade = models.CharField(max_length=20, choices=SponsorGradeTypes.TYPES)

    def upload_path(self, filename):
        return f'sponsor/{self.grade}/{self.name_en}/{filename}'

    image = models.FileField()


class WhyThisEvent(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=300)
    body = models.TextField()


class Quote(models.Model):
    name_en = models.CharField(max_length=200)
    name_fa = models.CharField(max_length=200)
    comment_en = models.TextField()
    comment_fa = models.TextField()
