from django.apps.registry import apps
from django.shortcuts import render

parser_plugins = apps.get_app_config('core').parser_plugins
visualizer_plugins = apps.get_app_config('core').visualizer_plugins
core_visualizer = apps.get_app_config('core').core_visualizer
active_visualizer = 'view_simple'
active_file = ''

def get_main_view(parsed_data):
    return visualizer_plugins[active_visualizer].main_view(parsed_data)

def get_bird_view(parsed_data):
    return visualizer_plugins[active_visualizer].bird_view(parsed_data)

def get_tree_view(parsed_data):
    return core_visualizer.tree_view(parsed_data)

def books(request, arg=None):
    global active_file
    active_file = 'books'
    return display(request, arg)

def items(request, arg=None):
    global active_file
    active_file = 'items'
    return display(request, arg)

def simple(request, arg=None):
    global active_visualizer
    active_visualizer = 'view_simple'
    return display(request,arg)

def complex(request, arg=None):
    global active_visualizer
    active_visualizer = 'view_complex'
    return display(request,arg)

def display(request, arg=None):

    parsed_data = apps.get_app_config('core').parsed_xml_files[active_file]

    if request.method == 'POST':
        if arg == 'search':
            query = request.POST['search']
            result = parsed_data.search(query)
            main_view = get_main_view(result)
            bird_view = get_bird_view(result)
            tree_view = get_tree_view(result)
            return render(request, 'index.html',
                          {
                           "main_view":main_view,
                           "bird_view":bird_view,
                           "tree_view":tree_view,
                           "origin":active_file 
                           })
        else:
            query = request.POST['filter']
            try:
                result = parsed_data.filter(query)
                main_view = get_main_view(result)
                bird_view = get_bird_view(result)
                tree_view = get_tree_view(result)
            except:
                return render(request, 'index.html',
                          {
                            "error": "Invalid filter query!",
                            "origin":active_file
                          })

            return render(request, 'index.html',
                          { 
                           "main_view":main_view,
                           "tree_view":tree_view,
                           "bird_view":bird_view,
                           "origin":active_file
                           })

    main_view = get_main_view(parsed_data)
    bird_view = get_bird_view(parsed_data)
    tree_view = get_tree_view(parsed_data)

    return render(request, "index.html", {
        "main_view":main_view,
        "bird_view":bird_view,
        "tree_view":tree_view,
        "origin":active_file
    })