from django.db.models.signals import m2m_changed , post_delete
from django.dispatch import receiver
from .models import Post
from django.core.mail import send_mail

@receiver(m2m_changed , sender=Post.likes.through)
def users_like_changed(sender , instance , **kwargs):
    instance.total_likes = instance.likes.count()
    instance.save()

@receiver(post_delete , sender=Post)
def email_post_delet(sender , instance , **kwargs):
    author = instance.author
    subject = "Your Post Has Been Deleted!"
    message = f"Your Post With ID : {instance.id} Has Been Deleted By The Admin Of Site!"
    send_mail(subject,message,'samazolfkhani12@gmail.com', [author.email] , fail_silently=False)
                