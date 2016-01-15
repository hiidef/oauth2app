def get_from_post_or_get_data(request, key):
    return request.POST.get(key, request.GET.get(key))
