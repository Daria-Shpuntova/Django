from django.db import models
from PIL import Image
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

# Create your models here.

class Course(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    img = models.ImageField(default='default.jpg', upload_to='course_img')
    free = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course-page', kwargs={'slug':self.slug})


class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=120)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete= models.SET_NULL, null=True)
    number = models.IntegerField()
    video_url = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('les-page', kwargs={'slug':self.course.slug, 'les_slug':self.slug})


class Komment(models.Model):
    article = models.ForeignKey(Lesson, verbose_name='Слаг', on_delete=models.CASCADE)
#    les_name = models.ForeignKey(Lesson, verbose_name='Название лекции', on_delete=models.CASCADE)
    text = models.TextField('Текст комментария')
    date = models.DateTimeField('Дата', default=timezone.now)
    avtor = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)

    def __str__(self):
 #       print(self.Lesson)
        return f'Комментарий к лекции {self.article} автор {self.avtor}'

    class Meta:
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии'