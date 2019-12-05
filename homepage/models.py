from enum import Enum

from django.db import models


class Homepage(models.Model):
    title_en = models.CharField(max_length=50)
    title_fa = models.CharField(max_length=50)


class Screen(models.Model):
    width = models.IntegerField()
    height = models.IntegerField()
    homepage = models.ForeignKey(Homepage, on_delete=models.CASCADE)


class Photo(models.Model):
    image = models.ImageField()
    screen = models.ForeignKey(Screen, on_delete=models.CASCADE)


class TimeLineEvent(models.Model):
    text_en = models.CharField(max_length=100)
    text_fa = models.CharField(max_length=100)
    date = models.DateTimeField()
    image = models.ForeignKey(Photo, on_delete=models.CASCADE)


#
# import jdatetime
#  jalili_date = jdatetime.date(1396,2,30).togregorian()
#  gregorian_date =  jdatetime.date.fromgregorian(day=19,month=5,year=2017)

class PrizeText_En(Enum):
    first_prize = 'First'
    second_prize = 'Second'
    third_prize = 'Third'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class PrizeText_Fa(Enum):
    first_prize = 'اول'
    second_prize = 'دوم'
    third_prize = 'سوم'

    def __str__(self):
        return self.value

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Prize(models.Model):
    text_en = models.CharField(max_length=100, choices=PrizeText_En.choices())
    text_fa = models.CharField(max_length=100, choices=PrizeText_Fa.choices())
    prize_value = models.CharField(max_length=1000)


class Link(models.Model):
    phone = models.CharField(max_length=20)
    telegram = models.CharField(max_length=200)
    whastsApp = models.CharField(max_length=200)
    instagram = models.CharField(max_length=200)
    email = models.EmailField()


class Sponsor(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='logo')
    link = models.ForeignKey(Link, on_delete=models.CASCADE, related_name='link')


class Organization(Sponsor):
    homepage = models.ForeignKey(Homepage, on_delete=models.CASCADE)