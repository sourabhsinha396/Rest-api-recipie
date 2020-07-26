from django.urls import path,include

from rest_framework.routers import DefaultRouter

from .views import TagViewset,IngredientViewset

router = DefaultRouter()
router.register('tags',TagViewset)
router.register('ingredients',IngredientViewset)

app_name = 'recipie'

urlpatterns = [
	path('',include(router.urls)),
	]