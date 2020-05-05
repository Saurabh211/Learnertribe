def export_vars(request):
    data = {}
    try:data['login_as'] = request.user.groups.all()[0].name
    except:pass
    return data