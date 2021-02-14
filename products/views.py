
from django.http.response import Http404
from django.views.generic import DetailView, ListView
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from .models import Product, Variation
from .forms import VariationInventoryFormSet

# Create your views here.



class VariationListView(ListView):
    model = Variation
    queryset = Variation.objects.all()
    template_name = 'products/variation_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(VariationListView, self).get_context_data(*args, **kwargs)
        context["formset"] = VariationInventoryFormSet(queryset=self.get_queryset())
        return context
        
    def get_queryset(self, *args, **kwargs):
        product_pk = self.kwargs.get("pk")
        if product_pk:
            product = get_object_or_404(Product, pk=product_pk)
            queryset = Variation.objects.filter(product = product)
        return queryset
    
    def post(self, request, *args, **kwargs):
        formset = VariationInventoryFormSet(request.POST, request.FILES)
        if formset.is_valid():
            formset.save(commit=False)
            for form in formset:
                new_item = form.save(commit=False)
                product_pk = self.kwargs.get("pk")
                product    = get_object_or_404(Product, pk = product_pk)
                if product is not None:
                    new_item.product = product
                    new_item.save()
                else:
                    new_item.save()

            return redirect("products:product_list")
        raise Http404


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

class ProductListView(ListView):
    model = Product
    queryset = Product.objects.filter(active=True)
    template_name = 'products/product_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        context["query"] = self.request.GET.get("q")
        return context
        
    def get_queryset(self, *args, **kwargs):
        qs = super(ProductListView, self).get_queryset(*args, **kwargs)
        query = self.request.GET.get("q")
        if query:
            qs = self.model.objects.filter(
                Q(title__icontains = query) |
                Q(description__icontains = query)
            )
            try:
                qs2 = self.model.objects.filter(
                    Q(price=query)
                )
                qs(qs | qs2).distinct()
            except:
                pass
        return qs