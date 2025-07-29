from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import *
from django.views.generic.edit import DeleteView, UpdateView
from django.urls import reverse_lazy
from .forms import *
from django.http import JsonResponse
from django.contrib import messages

def main_page(request):
    # Получаем все записи из базы данных
    all_records = Record.objects.all().order_by('-created_at')

    # Применяем фильтрацию по GET-параметрам
    filters = {}

    # Фильтрация по статусу
    if request.GET.get('status'):
        filters['status__name'] = request.GET.get('status')

    # Фильтрация по типу
    if request.GET.get('type'):
        filters['type__name'] = request.GET.get('type')

    # Фильтрация по категории
    if request.GET.get('category'):
        filters['category__name'] = request.GET.get('category')

    # Фильтрация по подкатегории
    if request.GET.get('subcategory'):
        filters['subcategory__name'] = request.GET.get('subcategory')

    # Фильтрация по сумме (интервал суммы)
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')
    if min_amount or max_amount:
        if min_amount:
            filters['amount__gte'] = float(min_amount)
        if max_amount:
            filters['amount__lte'] = float(max_amount)

    # Фильтрация по периоду дат
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    if start_date and end_date:
        filters['created_at__range'] = (start_date, end_date)

    # Фильтрация по комментарию
    comment_filter = request.GET.get('comment')
    if comment_filter:
        filters['comment__icontains'] = comment_filter

    # Применяем фильтры
    filtered_records = all_records.filter(**filters)

    # Настройка пагинатора
    paginator = Paginator(filtered_records, per_page=10)  # Показывать по 10 записей на одной странице
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'records': page_obj.object_list,
        'page_obj': page_obj,
        'filter_params': request.GET.dict(),  # Передаём параметры фильтрации в шаблон
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    }

    return render(request, 'dds/main.html', context)

def settings_page(request):
    types = Type.objects.all()
    cats = Category.objects.all()
    subcats = Subcategory.objects.all()

    context = {
        'types': types,
        'cats': cats,
        'subcats': subcats,
    }
    return render(request, 'dds\settings.html', context)


class RecordDeleteView(DeleteView):
    model = Record
    success_url = reverse_lazy('main_page')  # После успешного удаления возвращаемся на главную страницу
    template_name = 'dds/deletor.html'  # Шаблон подтверждения удаления


def create_record(request):
    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.created_at = record.created_at.replace(tzinfo=None)  # Если надо убрать временную зону
            record.save()
            return redirect('main_page')  # Возвращаемся на главную страницу после успешной отправки
    else:
        form = RecordForm()

    return render(request, 'dds/creditor.html', {'form': form})


class EditRecordView(UpdateView):
    model = Record
    form_class = RecordForm
    template_name = 'dds/creditor.html'
    success_url = reverse_lazy('main_page')  # Куда перейдем после успешного редактирования


def ajax_load_categories(request):
    type_id = request.GET.get('type')
    categories = Category.objects.filter(type_id=type_id).values('id', 'name')
    return JsonResponse(list(categories), safe=False)

def admin_panel(request):
    if request.method == 'POST':
        # Определяем, какая форма была отправлена
        form_name = request.POST.get('form_name')

        # Работа с формой для типов
        if form_name == 'type_form':
            type_id = request.POST.get('type_id')
            if type_id:
                # Редактирование существующего типа
                type_instance = get_object_or_404(Type, pk=type_id)
                type_form = TypeForm(request.POST, instance=type_instance)
            else:
                # Создание нового типа
                type_form = TypeForm(request.POST)

            if type_form.is_valid():
                type_form.save()
                messages.success(request, 'Тип успешно сохранён.')
                return redirect('admin_panel')

        # Работа с формой для статусов
        elif form_name == 'status_form':
            status_id = request.POST.get('status_id')
            if status_id:
                # Редактирование существующего статуса
                status_instance = get_object_or_404(Status, pk=status_id)
                status_form = StatusForm(request.POST, instance=status_instance)
            else:
                # Создание нового статуса
                status_form = StatusForm(request.POST)

            if status_form.is_valid():
                status_form.save()
                messages.success(request, 'Статус успешно сохранён.')
                return redirect('admin_panel')

        # Работа с формой для категорий
        elif form_name == 'category_form':
            category_id = request.POST.get('category_id')
            if category_id:
                # Редактирование существующей категории
                category_instance = get_object_or_404(Category, pk=category_id)
                category_form = CategoryForm(request.POST, instance=category_instance)
            else:
                # Создание новой категории
                category_form = CategoryForm(request.POST)

            if category_form.is_valid():
                category_form.save()
                messages.success(request, 'Категория успешно сохранена.')
                return redirect('admin_panel')

        # Работа с формой для подкатегорий
        elif form_name == 'subcategory_form':
            subcategory_id = request.POST.get('subcategory_id')
            if subcategory_id:
                # Редактирование существующей подкатегории
                subcategory_instance = get_object_or_404(Subcategory, pk=subcategory_id)
                subcategory_form = SubcategoryForm(request.POST, instance=subcategory_instance)
            else:
                # Создание новой подкатегории
                subcategory_form = SubcategoryForm(request.POST)

            if subcategory_form.is_valid():
                subcategory_form.save()
                messages.success(request, 'Подкатегория успешно сохранена.')
                return redirect('admin_panel')

        # Формы для создания новых объектов
    type_form = TypeForm(prefix='type')
    status_form = StatusForm(prefix='status')
    category_form = CategoryForm(prefix='category')
    subcategory_form = SubcategoryForm(prefix='subcategory')

    # Загрузка существующих объектов
    types = Type.objects.all()
    statuses = Status.objects.all()
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    context = {
        'type_form': type_form,
        'status_form': status_form,
        'category_form': category_form,
        'subcategory_form': subcategory_form,
        'types': types,
        'statuses': statuses,
        'categories': categories,
        'subcategories': subcategories,
    }

    return render(request, 'dds/settings.html', context)


def edit_object(request, object_type, object_id):
    # Определяем модель и форму в зависимости от типа объекта
    if object_type == 'type':
        model = Type
        form_class = TypeForm
    elif object_type == 'status':
        model = Status
        form_class = StatusForm
    elif object_type == 'category':
        model = Category
        form_class = CategoryForm
    elif object_type == 'subcategory':
        model = Subcategory
        form_class = SubcategoryForm
    else:
        return redirect('admin_panel')

    # Получаем объект по ID
    obj = get_object_or_404(model, id=object_id)

    # Обработка POST-запроса
    if request.method == 'POST':
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Объект "{obj.name}" успешно обновлен!')
            return redirect('admin_panel')
    else:
        form = form_class(instance=obj)

    return render(request, 'dds/objeditor.html', {'form': form, 'object': obj})


def create_object(request, object_type):
    # Определяем модель и форму в зависимости от типа объекта
    if object_type == 'type':
        model = Type
        form_class = TypeForm
    elif object_type == 'status':
        model = Status
        form_class = StatusForm
    elif object_type == 'category':
        model = Category
        form_class = CategoryForm
    elif object_type == 'subcategory':
        model = Subcategory
        form_class = SubcategoryForm
    else:
        return redirect('admin_panel')

    # Обработка POST-запроса
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Объект успешно создан!')
            return redirect('admin_panel')
    else:
        form = form_class()

    return render(request, 'dds/objcreator.html', {'form': form, 'object_type': object_type})


def delete_object(request, object_type, object_id):
    # Определяем модель в зависимости от типа объекта
    if object_type == 'type':
        model = Type
    elif object_type == 'status':
        model = Status
    elif object_type == 'category':
        model = Category
    elif object_type == 'subcategory':
        model = Subcategory
    else:
        return redirect('admin_panel')

    # Получаем объект по ID
    obj = get_object_or_404(model, id=object_id)

    # Обработка DELETE-запроса
    if request.method == 'POST':
        obj.delete()  # Удаляем объект и все зависимые записи
        messages.success(request, f'Объект "{obj.name}" успешно удален!')
        return redirect('admin_panel')

    # Если запрос GET, просто отображаем предупреждение
    return render(request, 'dds/objdel.html', {'object': obj})