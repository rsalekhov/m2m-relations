from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Tag, Scope

class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()
        main_scope_count = sum(1 for form in self.forms if form.cleaned_data.get('is_main'))

        if main_scope_count == 0:
            raise ValidationError('Specify exactly one main scope.')
        elif main_scope_count > 1:
            raise ValidationError('Only one main scope allowed.')

class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass
