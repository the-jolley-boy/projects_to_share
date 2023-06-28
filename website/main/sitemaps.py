from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from projects.models import Project
from blog.models import Post

class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return ['about', 'contact']

    def location(self, item):
        return reverse(item)

class ProjectsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'


    def items(self):
        return Project.objects.all()

    def location(self,obj):
        return '/projects/%s' % (obj.slug)

class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Post.objects.all()

    def location(self,obj):
        return '/blogs/blogpost/%s' % (obj.slug)
