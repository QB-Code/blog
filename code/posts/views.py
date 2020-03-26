from django.shortcuts import render


def uno_post(request, post_id):
    return render(request, template_name='posts/uno-post.html')


def all_posts(request):
    return render(request, template_name='posts/all-posts.html')


def write_post(request, user_id):
    return render(request, template_name='posts/writing-post.html')


def rubrics(request):
    return render(request, template_name='posts/rubrics.html')