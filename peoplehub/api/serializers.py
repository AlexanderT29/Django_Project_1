from rest_framework import serializers
from .models import Person

class PersonSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    age = serializers.IntegerField()
    city = serializers.CharField(max_length=150)

    def create(self, validated_data):
        return Person.objects.create(**validated_data)
    
    def update(self, instance, validate_date):
        instance.name = validate_date.get("name", instance.name)
        instance.age = validate_date.get("age", instance.age)
        instance.city = validate_date.get("city", instance.city)
        instance.save()
        return instance
    
class PersonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'city', 'age']