from rest_framework import serializers
from ..models import User,Hobby
from django.contrib.auth.hashers import make_password


class HobbySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = Hobby
        fields = '__all__'
        

class UserSerilizer(serializers.ModelSerializer):
    
    
    user_hobby = HobbySerializer(many=True)
    class Meta:
        model = User
        fields ='__all__'
        extra_kwargs = {'password': {'write_only': True}}   
        
     
            
        
        
        
    def create(self, validated_data):
        user_hobby = validated_data.pop('user_hobby')
        profile_instance = User.objects.create(**validated_data)
        for hobby in user_hobby:
            Hobby.objects.create(user=profile_instance,**hobby)
        return profile_instance
    
    def update(self, instance, validated_data):
        user_hobby_list = validated_data.pop('user_hobby')
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.address = validated_data.get('address', instance.address)
        instance.gender = validated_data.get('gender', instance.gender)
        
        instance.save()

        hobbies_with_same_profile_instance = Hobby.objects.filter(user=instance.pk).values_list('id', flat=True)
        hobbies_id_pool = []

        for hobby_data in user_hobby_list:
            hobby_id = hobby_data.get('id')
            
            if hobby_id:
                
                try:
                    hobby_instance = Hobby.objects.get(id=hobby_id)
                except Hobby.DoesNotExist:
                    continue
            else:
                
                hobby_instance = Hobby(user=instance)
                
            hobby_instance.name = hobby_data.get('name', hobby_instance.name)
            hobby_instance.save()
            hobbies_id_pool.append(hobby_instance.id)

        
        Hobby.objects.filter(user=instance, id__in=hobbies_with_same_profile_instance).exclude(id__in=hobbies_id_pool).delete()

        return instance
    def validate_email(self, value):
        
        if self.instance is None and User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value