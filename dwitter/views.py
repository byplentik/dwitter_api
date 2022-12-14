from django.shortcuts import render, redirect
from .models import Profile
from .forms import DweetForm

def dashboard(request):
    form = DweetForm(request.POST or None)


    if request.method == 'POST':
        form = DweetForm(request.POST)
        if form.is_valid():
            dweet = form.save(commit=False)
            dweet.user = request.user
            dweet.save()
            return redirect('dwitter:dashboard')

    return render(request, "dwitter/dashboard.html", {'form': form})

def profile_list(request):
    porfiles = Profile.objects.exclude(user=request.user)
    return render(request, 'dwitter/profile_list.html', {'profiles': porfiles})

def profile(request, pk):
    if not hasattr(request.user, 'profile'):
        missing_profile = Profile(user=request.user)
        missing_profile.save()

    profile = Profile.objects.get(pk=pk)

    if request.method == 'POST':
        current_user_profile = request.user.profile
        data = request.POST
        action = data.get('follow')
        if action == 'follow':
            current_user_profile.follows.add(profile)
        elif action == 'unfollow':
            current_user_profile.follows.remove(profile)
        current_user_profile.save()


    return render(request, 'dwitter/profile.html', {'profile': profile})