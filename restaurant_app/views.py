from django.shortcuts import render, redirect, get_object_or_404
from django.urls import  reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.generic import ListView,  CreateView, UpdateView, DeleteView

from .models import Category, MenuItem, Order, OrderItem, Review
from .forms import ReservationForm, CustomUserCreationForm, ReviewForm, Reservation, CategoryForm, MenuItemForm



def home(request):
    reviews = Review.objects.order_by('-created_at')[:5]
    menu_items = MenuItem.objects.all()
    return render(request, 'restaurant_app/home.html', {
        'reviews': reviews,
        'menu_items': menu_items,
    })


def legacy(request):
    return render(request, 'restaurant_app/legacy.html')


def gallery(request):
    return render(request, 'restaurant_app/gallery.html')


from .forms import ReviewForm  
@login_required
def submit_review(request):
    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('home')
    return render(request, 'restaurant_app/submit_review.html', {'form': form})


def menu_list(request):
    categories = Category.objects.all().prefetch_related('menuitem_set')
    return render(request, 'restaurant_app/menu_list.html', {'categories': categories})

def menu_detail(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    return render(request, 'restaurant_app/menu_detail.html', {'item': item})

@login_required
def reservation(request):
    form = ReservationForm()
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()

            
            subject = 'Your Reservation is Confirmed'
            message = (
                f"Hi {reservation.name},\n\n"
                f"Your reservation on {reservation.date} at {reservation.time} "
                f"for {reservation.guests} guest(s) has been confirmed.\n\nThank you!"
            )
            send_mail(subject, message, settings.EMAIL_HOST_USER, [reservation.email], fail_silently=False)

           
            staff_subject = 'New Reservation Received'
            staff_message = (
                f"New reservation from {reservation.name}.\n\n"
                f"Date: {reservation.date}\nTime: {reservation.time}\n"
                f"Guests: {reservation.guests}\nEmail: {reservation.email}\nPhone: {reservation.phone}"
            )
            send_mail(staff_subject, staff_message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER], fail_silently=True)

            messages.success(request, 'Reservation successful! A confirmation email has been sent.')
            return redirect('reservation_success')

    return render(request, 'restaurant_app/reservation.html', {'form': form})

@login_required
def reservation_success(request):
    return render(request, 'restaurant_app/reservation_success.html')

def contact(request):
    return render(request, 'restaurant_app/contact.html')

@login_required
def place_order(request):
    menu_items = MenuItem.objects.all()
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        order = Order.objects.create(
            customer_name=customer_name,
            phone=phone,
            address=address
        )

        for item in menu_items:
            quantity = int(request.POST.get(f'quantity_{item.id}', 0))
            if quantity > 0:
                OrderItem.objects.create(order=order, menu_item=item, quantity=quantity)

        return render(request, 'restaurant_app/order_success.html', {'order': order})

    return render(request, 'restaurant_app/order.html', {'menu_items': menu_items})

def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'restaurant_app/signup.html', {'form': form})

@login_required
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('home')  

    reservations = Reservation.objects.order_by('-date', '-time')
    orders = Order.objects.order_by('-created_at')
    reviews = Review.objects.order_by('-created_at')
    total_reservations = reservations.count()
    total_orders = orders.count()
    total_reviews = reviews.count()


    return render(request, 'restaurant_app/admin_dashboard.html', {
        'reservations': reservations,
        'orders': orders,
        'reviews': reviews,
          'total_reservations': total_reservations,
    'total_orders': total_orders,
    'total_reviews': total_reviews,
    })

@login_required
def dashboard_redirect(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    else:
        return redirect('home')





@method_decorator(login_required, name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = 'restaurant_app/category_list.html'
    context_object_name = 'categories'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'restaurant_app/category_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Category created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('category_list')


@method_decorator(login_required, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'restaurant_app/category_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Category updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('category_list')


@method_decorator(login_required, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'restaurant_app/category_confirm_delete.html'
    context_object_name = 'category'
    success_url = reverse_lazy('category_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Category deleted successfully.")
        return super().delete(request, *args, **kwargs)



@method_decorator(login_required, name='dispatch')
class MenuItemListView(ListView):
    model = MenuItem
    template_name = 'restaurant_app/menuitem_list.html'
    context_object_name = 'menuitems'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class MenuItemCreateView(CreateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'restaurant_app/menuitem_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Menu item created successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('menuitem_list')


@method_decorator(login_required, name='dispatch')
class MenuItemUpdateView(UpdateView):
    model = MenuItem
    form_class = MenuItemForm
    template_name = 'restaurant_app/menuitem_form.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        messages.success(self.request, "Menu item updated successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('menuitem_list')


@method_decorator(login_required, name='dispatch')
class MenuItemDeleteView(DeleteView):
    model = MenuItem
    template_name = 'restaurant_app/menuitem_confirm_delete.html'
    context_object_name = 'menuitem'
    success_url = reverse_lazy('menuitem_list')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Menu item deleted successfully.")
        return super().delete(request, *args, **kwargs)
