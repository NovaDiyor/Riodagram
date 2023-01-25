from datetime import date
from rest_framework import status
from django.contrib.auth import authenticate, logout
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializer import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


@api_view(['POST'])
def login_view(request):
    try:
        username = request.data['username']
        password = request.data['password']
        try:
            usr = User.objects.get(username=username)
            user = authenticate(username=username, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    'username': username,
                    'user_id': usr.id,
                    'token': token.key,
                }
                return Response(data, status.HTTP_200_OK)
            else:
                message = 'Username or Password is wrong!'
                data = {
                    'message': message,
                }
                return Response(data, status.HTTP_403_FORBIDDEN)
        except User.DoesNotExist:
            message = {
                'message': 'This User Doesnt Exist'
            }
            return Response(message, status.HTTP_404_NOT_FOUND)
    except Exception as err:
        return Response({"error": f'{err}'})


@api_view(['POST'])
def register(request):
    try:
        if request.method == 'POST':
            username = request.POST['username']
            name = request.POST['name']
            surname = request.POST['surname']
            email = request.POST['email']
            password = request.POST['password']
            if email[-10:] == '@gmail.com':
                if len(email) >= 11:
                    if len(password) >= 6:
                        usr = User.objects.create_user(
                            username=username,
                            first_name=name,
                            last_name=surname,
                            email=email,
                            password=password,
                            status=2)
                        token = Token.objects.create(user=usr)
                        LikedPost.objects.create(user=usr)
                        Alp.objects.create(user=usr)
                        data = {
                            'username': username,
                            'name': name,
                            'surname': surname,
                            'email': email,
                            'user_id': usr.id,
                            'token': token.key
                        }
                        return Response(data, status.HTTP_200_OK)
                    else:
                        return Response('Password have to consist of 6 letter', status.HTTP_403_FORBIDDEN)
                else:
                    return Response('Email have to consist something except @gmail.com', status.HTTP_401_UNAUTHORIZED)
            else:
                return Response('Wrong email, email have to end with @gmail.com', status.HTTP_401_UNAUTHORIZED)
        else:
            return Response('wrong method', status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as err:
        return Response({"error": f'{err}'}, status.HTTP_417_EXPECTATION_FAILED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def logout_view(request):
    try:
        if request.method == 'DELETE':
            user = request.user
            user.delete()
            logout(request)
            return Response('You logout')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def give_follow(request):
    try:
        if request.method == 'POST':
            blogger = User.objects.get(username=request.POST.get('username'))
            giver = request.user
            if giver != blogger:
                e = 0
                for i in Follow.objects.all():
                    if i.user == blogger:
                        e += 1
                    else:
                        e += 0
                if e == 0:
                    obj = Follow.objects.create(user=blogger)
                    obj.follower.add(giver)
                    blogger.followers += 1
                    giver.following += 1
                    blogger.save()
                    giver.save()
                    return Response('Successful')
                elif e > 0:
                    followers = Follow.objects.get(user=blogger)
                    f = 0
                    for i in followers.follower.all():
                        if i.id == giver.id:
                            return Response('You already follower')
                        else:
                            f += 1
                    if f > 1:
                        followers.follower.add(giver)
                        blogger.followers += 1
                        giver.following += 1
                        blogger.save()
                        giver.save()
                        return Response('Successful')
            else:
                return Response('Wrong')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def give_like(request):
    try:
        if request.method == 'POST':
            taker = User.objects.get(id=request.POST.get('blogger'))
            liker = User.objects.get(id=request.POST.get('liker'))
            post = Posts.objects.get(id=request.POST.get('post'))
            liked = LikedPost.objects.get(user=liker)
            if taker == liker:
                return Response('wrong user')
            else:
                if post.author_id == taker.id:
                    if post.likes.count() > 0:
                        e = 0
                        for i in post.likes.all():
                            if liker.id == i.id:
                                e += 1
                            else:
                                e += 0
                        if e > 0:
                            liker.liked -= 1
                            liker.save()
                            liked.post.remove(post)
                            post.likes.remove(liker)
                            return Response('successful you deleted your like')
                        elif e == 0:
                            liker.liked += 1
                            liker.save()
                            liked.post.add(post)
                            post.likes.add(liker)
                            return Response('successful you liked this post')
                    else:
                        liker.liked += 1
                        liker.save()
                        liked.post.add(post)
                        post.likes.add(liker)
                        return Response('successful')
                else:
                    return Response('wrong author')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def unfollow(request):
    try:
        if request.method == 'POST':
            blogger = User.objects.get(id=request.POST.get('blogger'))
            customer = User.objects.get(id=request.POST.get('follower'))
            follower = Follow.objects.get(user=blogger)
            f = 0
            for i in follower.follower.all():
                if customer.id == i.id:
                    blogger.followers -= 1
                    customer.following -= 1
                    follower.follower.remove(customer)
                    blogger.save()
                    customer.save()
                    follower.save()
                    return Response('You Successfully deleted your follow')
                else:
                    f += 1
            if f > 0:
                return Response("You Don't Follow to this user")
        else:
            return Response('Wrong')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def leave_comment(request):
    try:
        if request.method == 'POST':
            user = request.user
            post = Posts.objects.get(id=request.POST.get('post'))
            message = request.POST.get('comment')
            if message != '':
                f = 0
                for i in range(100):
                    if message == ' ' * i:
                        f += 1
                    else:
                        f += 0
                if f > 0:
                    return Response('you have to write something')
                else:
                    c = Comment.objects.create(message=message, user=user)
                    post.comments.add(c)
                    return Response('you published comment')
            else:
                return Response('you have to write')
        else:
            return Response('wrong method')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_post(request):
    try:
        if request.method == 'POST':
            user = request.user
            content = request.FILES.getlist('content')
            bio = request.POST['bio']
            post = Posts.objects.create(author=user, bio=bio)
            for i in content:
                image = Image.objects.create(content=i)
                post.content.add(image)
            return Response('You successfully published post')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def create_stories(request):
    try:
        if request.method == 'POST':
            user = request.user
            content = request.FILES.get('content')
            Stories.objects.create(author=user, content=content)
            return Response('You Created The Stories')
        else:
            return Response('wrong method')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_user_username(request, pk):
    try:
        if request.method == 'GET':
            user = User.objects.get(username=pk)
            following = Follow.objects.get(user=user)
            post = Alp.objects.get(user=user)
            if user.img:
                img = user.img.url
            else:
                img = None
            if post.post.count() > 0:
                post = PostOne(post, many=True).data
            else:
                post = None
            data = {
                'username': user.username,
                'name': user.first_name,
                'surname': user.last_name,
                'bio': user.bio,
                'img': img,
                'following': user.following,
                'followers': UserVisible(following.follower, many=True).data,
                'publications': user.publications,
                'site': user.site,
                'post': post
            }
            return Response(data)
        else:
            return Response('wrong method')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_stories(request, pk):
    try:
        if request.method == 'DELETE':
            user = request.user
            story = Stories.objects.get(id=pk)
            if story is not None:
                if story.author == user:
                    story.delete()
                    return Response('You Successfully deleted stories')
                else:
                    return Response('You are not author')
            else:
                return Response('Stories Doesnt exist')
        else:
            return Response('wrong method')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_post(request, pk):
    try:
        if request.method == 'DELETE':
            user = request.user
            post = Posts.objects.get(id=pk)
            if post is None:
                return Response('This Post Doesnt Exist!')
            else:
                if post.author == user:
                    post.delete()
                    return Response('You successfully deleted your post')
                else:
                    return Response('You are not author')
        else:
            return Response('wrong method')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_comment(request, pk):
    try:
        if request.method == 'DELETE':
            user = request.user
            comment = Comment.objects.get(id=pk)
            if comment.user == user:
                comment.delete()
                return Response('you deleted your comment')
            else:
                return Response('wrong User')
        else:
            return Response('wrong method')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def get_liked(request):
    try:
        user = request.user
        post = LikedPost.objects.get(user=user)
        opinion = []
        content = []
        for i in post.post.all():
            comment = i.comments.all()
            for x in comment:
                cl = {
                    'id': x.id,
                    'message': x.message,
                    'user': UserVisible(x.user).data
                }
                opinion.append(cl)
            data = {
                'id': i.id,
                'content': i.content.url,
                'bio': i.bio,
                'day': i.day,
                'author': UserVisible(i.author).data,
                'likes': UserVisible(i.likes, many=True).data,
                'comment': opinion
            }
            content.append(data)
            return Response(content)
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['GET'])
def get_post(request, pk):
    try:
        if request.method == 'GET':
            post = Posts.objects.get(id=pk)
            comment = []
            for i in post.comments.all():
                cl = {
                    'id': i.id,
                    'message': i.message,
                    'user': UserVisible(i.user).data
                }
                comment.append(cl)
            data = {
                'id': post.id,
                'content': ContentOne(post.content.all(), many=True).data,
                'bio': post.bio,
                'day': post.day,
                'author': UserVisible(post.author).data,
                'likes': UserVisible(post.likes, many=True).data,
                'comment': comment
            }
            return Response(data)
        else:
            return Response('wrong method')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['GET'])
def get_post_follow(request):
    try:
        if request.method == 'GET':
            user = request.user
            follow = []
            post = []
            day = date.today()
            for i in Follow.objects.all():
                for x in i.follower.all():
                    if x == user:
                        follow.append(i.user)
            for i in follow:
                new = Posts.objects.get(author=i, day__day=day.day)
                post.append(new)
            return Response(PostOne(post, many=True).data)
        else:
            return Response('wrong method')
    except Exception as err:
        return Response(f'error: {err}')


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def change_profile(request):
    try:
        if request.method == 'PATCH':
            user = request.user
            username = request.POST.get('username')
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            img = request.POST.get('image')
            bio = request.POST.get('bio')
            site = request.POST.get('site')
            email = request.POST.get('email')
            number = request.POST.get('number')
            if username:
                user.username = username
            if name:
                user.first_name = name
            if surname:
                user.last_name = surname
            if img:
                user.img = img
            if bio:
                user.bio = bio
            if site:
                user.site = site
            if email:
                user.email = email
            if number:
                user.number = number
            user.save()
            return Response('Successful', status.HTTP_200_OK)
        return Response('wrong method', status.HTTP_405_METHOD_NOT_ALLOWED)
    except Exception as err:
        return Response(f'error: {err}', status.HTTP_204_NO_CONTENT)

