from django.shortcuts import redirect


def redirect_base(request):
    return redirect('main_menu_url', permanent=True)
