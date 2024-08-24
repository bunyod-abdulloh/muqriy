from django.db import models


class QuranEDU(models.Model):
    sequence = models.CharField(verbose_name="Tartib raqam", max_length=3)
    sura_name = models.CharField(verbose_name="Sura nomi", max_length=60)
    total_verses = models.IntegerField(verbose_name="Oyatlar soni")
    zip = models.CharField(verbose_name="ZIP ID", max_length=200, null=True, blank=True)
    audiomuqriy = models.CharField(verbose_name="Muqriy Audio ID", max_length=200, null=True, blank=True)
    audiohusary = models.CharField(verbose_name="Husary Audio ID", max_length=200, null=True, blank=True)
    photo = models.CharField(verbose_name="Photo ID", max_length=200, null=True, blank=True)
    photo_link = models.CharField(verbose_name="Photo link", max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Qur'oni Karim (EDU ONE)"
        verbose_name_plural = "Qur'oni Karim (EDU ONE)"
