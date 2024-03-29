from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User



# Create your models here.
class Categories(models.Model):
    icon = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    def get_all_category(self):
        return Categories.objects.all().order_by('id')




class Author(models.Model):
    author_profile = models.ImageField(upload_to="Media/author",null=True)
    name = models.CharField(max_length=100, null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name
    
class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Language(models.Model):
    language = models.CharField(max_length=100)

    def __str__(self):
        return self.language


class Course(models.Model):
    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )

    featured_image = models.ImageField(upload_to="Media/featured_img",null=True)
    featured_video = models.FileField(upload_to='Media/featured_video',null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    #video = models.ForeignKey('Video', on_delete=models.CASCADE,related_name='videos')
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    Deadline = models.CharField(max_length=100,null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS,max_length=100,null=True)
    Certificate = models.CharField(null=True, max_length=100)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_details", kwargs={'slug': self.slug})

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)


class What_you_learn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points
    
class Requirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=500)

    def __str__(self):
        return self.points

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " - " + self.course.title
    
class Video (models.Model):
    serial_number = models.IntegerField(null=True)
    #thumbnail = models.ImageField(upload_to="Media/Yt_Thumbnail", null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    #youtube_id = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='Media/video',null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True,null=True)
    time_duration = models.FloatField(null=True)
    preview = models.BooleanField(default=False)
   

    def __str__(self):
        return self.title
    
class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.first_name + " - " + self.course.title
    
class Payment(models.Model):
    order_id = models.CharField(max_length=100, null=True, blank=True)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    user_course = models.ForeignKey(UserCourse, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.user.first_name + " -- " + self.course.title
    
class Blog(models.Model):
    blog_image = models.ImageField(upload_to="Media/Blog_Image", null=True)
    blog_author = models.CharField(max_length=100, null=True)
    blog_date = models.DateTimeField(auto_now_add=True)
    blog_category = models.CharField(max_length=100)
    blog_title = models.CharField(max_length=500)
    website_url = models.URLField(max_length=200, blank=True)

    def __str__(self):
        return self.blog_title
    
class ReviewRating(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review_title = models.CharField(max_length=200, blank=True)
    review_content = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20,blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.review_title


    