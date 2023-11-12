from django.shortcuts import render, get_object_or_404
from .models import Course, Lesson, Komment
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse

# Create your views here.
class HomePage(ListView):
    model = Course
    template_name = 'courses/home.html'
    context_object_name = 'courses'
    ordering = ['-id']

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(HomePage, self).get_context_data(**kwargs)
        ctx['title'] = 'Главная страница сайта'
        return ctx

class CoursePage(DetailView):
    model = Course
    template_name = 'courses/course-page.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(CoursePage, self).get_context_data(**kwargs)
        ctx['title'] = Course.objects.filter(slug=self.kwargs['slug']).first()
        ctx['lessons']=Lesson.objects.filter(course=ctx['title']).order_by('number')
#        print(ctx['lessons'].query) # - посмотреть SQL-запрос
 #       print(ctx['lessons'])
        return ctx

class LessonPage(DetailView, CreateView):
    model = Course
    template_name = 'courses/les-page.html'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            self.text = form.cleaned_data.get('comment')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.avtor = self.request.user
        course = Course.objects.filter(slug=self.kwargs['slug']).first()
        les=list(Lesson.objects.filter(course=course).filter(slug=self.kwargs['les_slug']).values())
        ticle = les[0]['id']
        self.object.article=Lesson.objects.get(id=ticle)
        self.object.text = self.text
        self.object.save()
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super(LessonPage, self).get_context_data(**kwargs)
        course = Course.objects.filter(slug=self.kwargs['slug']).first()
        self.les = list(Lesson.objects.filter(course=course).filter(slug=self.kwargs['les_slug']).values())
        #       print(les.query)
        ctx['title'] = self.les[0]['title']
        ctx['desk'] = self.les[0]['description']
        ctx['video'] = self.les[0]['video_url'].split('=')[1]
        ctx['comments'] = Komment.objects.filter(article=self.les[0]['id']).order_by('-date')
        return ctx

    def get_success_url(self):
        return reverse('les-page', kwargs={'slug':self.kwargs['slug'], 'les_slug': self.kwargs['les_slug']})



def tarifPage(request):
    return render(request, 'courses/tarif.html', {'title':'Тарифы на сайте'})