from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
from .models import Post
from .forms import EmailPostForm
from django.core.mail import send_mail
# Create your views here.

# post_list is a view that retrieves all published posts
def post_list(request):
    post_list = Post.published.all()
    # pagination with 3 posts per page
    paginator = Paginator(post_list, 3)
    # Gets 'page' parameter from URL like /?page=2
    # /blog/?page=2   -> page 2
    page_no = request.GET.get('page',1)
    try:
        posts = paginator.page(page_no)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
       # If page_number is out of range get last page of results
       posts = paginator.page(paginator.num_pages) # paginator.num_pages is the total number of pages(the same as the last page number)
    return render(request, 'blog/post/list.html', {'posts': posts})

# post_detail is a view that retrieves a single post by its id
def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, 
        status=Post.Status.PUBLISHED,
        publish__year=year, 
        publish__month=month, 
        publish__day=day, 
        slug=post
    )
    return render(request, 'blog/post/detail.html', {'post': post})

def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id = post_id,
        status = Post.Status.PUBLISHED
    )
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            cd = form.cleaned_data
            # send email
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you reading {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject = subject,
                message = message, 
                from_email = None, 
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form  = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post' : post, 'form' : form, 'sent' : sent})
