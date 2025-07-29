from django import forms
from .models import Record, Status, Type, Category, Subcategory


class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = ['created_at', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ограничиваем категории в зависимости от выбранного типа
        if not kwargs.get('instance'):
            self.fields['category'].queryset = Category.objects.none()
            self.fields['subcategory'].queryset = Subcategory.objects.none()

        # Привязываем категории к выбранному типу
        try:
            type_id = int(self.data.get('type'))  # Берём ID типа из данных формы
        except (ValueError, TypeError):
            type_id = None

        if type_id:
            self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
        else:
            self.fields['category'].required = False

        # Привязываем подкатегории к выбранной категории
        try:
            category_id = int(self.data.get('category'))  # Берём ID категории из данных формы
        except (ValueError, TypeError):
            category_id = None

        if category_id:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
        else:
            self.fields['subcategory'].required = False





class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название типа'}),
        }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название категории'}),
            'type': forms.Select(attrs={'class': 'form-control'})
        }


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название подкатегории'}),
            'category': forms.Select(attrs={'class': 'form-control'})
        }

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Название статуса'})
        }