from rest_framework import serializers
from django.contrib.auth.models import User

from .models import CategoryCost, Cost, DayCost, AddMoney

class CategoryCostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model=CategoryCost
        fields=('name',)
        #depth=1

    def create(self,validated_data):
        category=CategoryCost.objects.update_or_create(
            name=validated_data.get('name',None)
            )
        return category

class CategoryCostSerializer(serializers.ModelSerializer):

    class Meta:
        model=CategoryCost
        fields=('name',)


class CostSerializer(serializers.ModelSerializer):

    category=serializers.SlugRelatedField(slug_field="name", read_only=True)
    user=serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model=Cost
        fields=('user','category','cost_date','cost_name','cost_sum')

class CostDayUpdateSerializer(serializers.ModelSerializer):

    #cost_name=serializers.ChoiceField(choices=[],style={'base_template':'radio.html'})
    class Meta:
        model=Cost
        fields=('cost_name','cost_sum')

class CostCreateSerializer(serializers.ModelSerializer):
  
    class Meta:
        model=Cost
        fields=('user','category','cost_date','cost_name','cost_sum')

    

    def create(self,validated_data):
        cost=Cost.objects.update_or_create(
            #defaults={'user':User.objects.get(username='alex')},#validated_data.get('user'))},
            user=User.objects.get(username=validated_data.get('user')),
            category=CategoryCost.objects.get(name=validated_data.get('category')),
            cost_date=validated_data.get('cost_date',None),
            cost_name=validated_data.get('cost_name',None),
            cost_sum=validated_data.get('cost_sum',None),
            )
        return cost


# class CostManyCreateSerializer(serializers.Serializer):
#
#     user = serializers.CharField()
#     category = serializers.CharField()
#     cost_date = serializers.DateField()
#
#

class DayCostSerializer(serializers.ModelSerializer):

    #costs=serializers.SlugRelatedField(slug_field="cost", read_only=True)

    class Meta:
        model=DayCost
        fields=('user','day_date','costs')

class DayCostCreateSerializer(serializers.ModelSerializer):
  
    class Meta:
        model=DayCost
        fields=('user','day_date','costs')

    

    def create(self,validated_data):
        cost=DayCost.objects.update_or_create(
            user=User.objects.get(username=validated_data.get('user')),
            day_date=validated_data.get('day_date',None),
           
            )
        return cost

class ReportSerializer(serializers.Serializer):

    category=serializers.MultipleChoiceField(choices=[(cat.id,cat.name) for cat in CategoryCost.objects.all()],style={'base_template':'checkbox_multiple.html'})
    date_b=serializers.DateField(style={'width':50})
    date_e=serializers.DateField()
    

class DayCostUpdateSerializer(serializers.ModelSerializer):

    costs=serializers.ChoiceField(choices=[],style={'base_template':'radio.html'})
    #costs - CostSerializer()41-15

    class Meta:
        model=DayCost
        fields=('costs',)
        
class AddMoneySerializer(serializers.ModelSerializer):

    #category=serializers.SlugRelatedField(slug_field="name", read_only=True)
    user=serializers.SlugRelatedField(slug_field="username", read_only=True)
    class Meta:
        model=AddMoney
        fields=('user','category','addmoney_date','addmoney_name','addmoney_sum')

class AddMoneyCreateSerializer(serializers.ModelSerializer):
  
    class Meta:
        model=AddMoney
        fields=('user','category','addmoney_date','addmoney_name','addmoney_sum')

    

    def create(self,validated_data):
        addmoney=AddMoney.objects.update_or_create(
            #defaults={'user':User.objects.get(username='alex')},#validated_data.get('user'))},
            user=User.objects.get(username=validated_data.get('user')),
            category=validated_data.get('category',None),
            addmoney_date=validated_data.get('addmoney_date',None),
            addmoney_name=validated_data.get('addmoney_name',None),
            addmoney_sum=validated_data.get('addmoney_sum',None),
            )
        return addmoney       
