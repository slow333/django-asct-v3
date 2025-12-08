from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from aistore.models import Product, Collection
from .forms import SearchForm
from .forms import ProductForm

def home(request):
    # Use select_related to optimize the query by fetching the related collection in the same database hit.
    query_set = Product.objects.select_related('collection').all()
    
    # Get filter, search, and sort parameters from the request
    search_title = request.GET.get('search_title', '')
    collection_id = request.GET.get('collection')
    inventory_filter = request.GET.get('inventory')
    sort = request.GET.get('sort', 'title')
    order = request.GET.get('order', 'asc')
    
    # Search form
    search_form = SearchForm(request.GET or None)
    
    # Apply search and filters
    if search_title:
        query_set = query_set.filter(title__icontains=search_title)
    
    if collection_id:
        query_set = query_set.filter(collection__id=collection_id)
        
    if inventory_filter == 'low':
        query_set = query_set.filter(inventory__lt=10)

    # Apply sorting
    if sort and order:
        if order == 'desc':
            query_set = query_set.order_by('-' + sort)
        else:
            query_set = query_set.order_by(sort)

    paginator = Paginator(query_set, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    collections = Collection.objects.annotate(product_count=Count('product')).all()
    
    context = {
        'page_obj': page_obj,
        'search_form': search_form,
        'search_title': search_title,
        'sort': sort,
        'order': order,
        'collections': collections,
        'selected_collection_id': int(collection_id) if collection_id else None,
        'inventory_filter': inventory_filter,
    }
    return render(request, 'aistore/aistore-home.html', context)


def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the product list page after creation
            return redirect('aistore-home') 
    else:
        form = ProductForm()
    
    return render(request, 'aistore/aistore-product-form.html', {'form': form})

def product_bulk_action(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        selected_ids = request.POST.getlist('selected_ids')

        if not selected_ids:
            messages.warning(request, 'You did not select any products.')
        elif action == 'delete_selected':
            deleted_count, _ = Product.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f'{deleted_count} products were successfully deleted.')
        elif action == 'update_prices':
            products_to_update = []
            for product_id in selected_ids:
                price_key = f'price_{product_id}'
                if price_key in request.POST:
                    try:
                        product = Product.objects.get(pk=product_id)
                        new_price = float(request.POST[price_key])
                        if product.unit_price != new_price:
                            product.unit_price = new_price # type: ignore
                            products_to_update.append(product)
                    except (ValueError, Product.DoesNotExist):
                        continue
            
            if products_to_update:
                Product.objects.bulk_update(products_to_update, ['unit_price'])
                messages.success(request, f'{len(products_to_update)} products were successfully updated.')
        else:
            messages.warning(request, 'No action selected.')

    # Redirect back to the same page, preserving query parameters
    return redirect(request.META.get('HTTP_REFERER', 'aistore-home'))
