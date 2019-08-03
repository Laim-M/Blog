from django.shortcuts import redirect, render
from django.utils import timezone
from .models import Post, UserProfile
from .forms import PostForm
from django.contrib.auth.models import User


def feed(request):
    if not request.user.is_authenticated:
        return redirect('accounts/signup/', )
    else:
        author = request.user
        following = UserProfile.objects.filter(from_follow=author)

        for post in following:
            feed = post.to_follow
            posts = Post.objects.filter(author=feed)
            return render(request, 'feed.html', {'posts': posts})
        return render(request, 'feed.html', {'following': following})

def profile(request):
    if not request.user.is_authenticated:
        return redirect('accounts/signup/', )
    else:
        author = request.user
        posts = Post.objects.filter(author=author)
        following = UserProfile.objects.filter(from_follow=author)
        follower = UserProfile.objects.filter(to_follow=author)
        return render(request, 'profile.html', {'posts': posts, 'following' : following, 'follower' : follower,})

def create_post(request):
    if not request.user.is_authenticated:
        return redirect('accounts/signup/', )
    else:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.published_date = timezone.now()
                order_to_sent = True
                already_sent = False
                post.save()
                if post.order_to_sent:
                    mail_host = "blogsender@gmail.com"
                    user_list = User.objects.all()
                    recipients = []
                    for user in user_list:
                        if user.email == '' or user.email == post.author.email:
                            continue
                        else:
                            recipients.append(user.email)

                     message = 'У пользователя {0} в блоге появилась новая запись!Ссылка:{1}'.format(post.author, 'http://' + request.get_host() + post.get_absolute_url())
                     subject = 'Новый пост'
                     send_mail(subject, message, mail_host, recipients, fail_silently=False)
                     post.order_to_sent = False  # Двойная проверка нужна на случай,если пользователь захочет оповестить несколько раз
                     post.already_sent = True
                     post.save()
                return redirect('/')
        else:
            form = PostForm()
        return render(request, 'create_post.html', {'form': form})

def another_user(request):
    """
    :type request: object
    """
    if not request.user.is_authenticated:
        return redirect('accounts/signup/', )
    else:
        q = request.GET.get("q")  # getting value from form
        try:
            author = User.objects.get(username=q)  # check for user existence
        except:
            return render(request, 'search_error.html', {})  # redirect if there is no match
        else:
            following = UserProfile.objects.filter(from_follow=author)
            follower = UserProfile.objects.filter(to_follow=author)
            posts = Post.objects.filter(author=author)  # Search for users posts

            return render(request, 'another_user.html', {
                'posts': posts,
                'author': author,
            })

def follow(request):
    if not request.user.is_authenticated:
        return redirect('accounts/signup/', )
    else:
        if request.method == "POST":
            follow_id = request.POST.get('follow', False)
            if follow_id:
                try:
                    following = User.objects.get(id=follow_id)
                    follower = request.user
                    follow = UserProfile(from_follow=follower, to_follow=following)
                    follow.save()
                except:
                    return redirect('profile')
                else:
                    return redirect('feed')