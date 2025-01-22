from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Post, Perfil
from .forms import PostForm, CadastroForm, PerfilForm

def post_list(request):
    posts = Post.objects.filter(data_publicacao__lte=timezone.now()).order_by('-data_publicacao')
    return render(request, 'appsite/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'appsite/post_detail.html', {'post': post})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.data_publicacao = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'appsite/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.autor != request.user:
        return redirect('post_list')
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.data_publicacao = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'appsite/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.autor != request.user:
        return redirect('post_list')
    
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'appsite/post_delete.html', {'post': post})


def signup(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        profile_form = PerfilForm(request.POST, request.FILES)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.usuario = user
            profile.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = CadastroForm()
        profile_form = PerfilForm()
    return render(request, 'registration/signup.html', {
        'form': form,
        'profile_form': profile_form
    })

@login_required
def profile(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    return render(request, 'appsite/profile.html', {'perfil': perfil})

@login_required
def profile_edit(request):
    perfil, created = Perfil.objects.get_or_create(usuario=request.user)
    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            if 'avatar-clear' in request.POST:
                perfil.avatar = None
            form.save()
            return redirect('profile')
    else:
        form = PerfilForm(instance=perfil)
    return render(request, 'appsite/profile_edit.html', {'form': form})

@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('post_list')
    return redirect('post_list')