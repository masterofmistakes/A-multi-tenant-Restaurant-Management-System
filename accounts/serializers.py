from rest_framework import serializers 
from .models import User, UserRole

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['fullname', 'phone', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['id', 'fullname', 'phone', 'role','avatar', 'password', 'restaurant']
        read_only_fields = ['id', 'role', 'restaurant']

class CreateRoleSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['id', 'fullname', 'phone', 'role', 'password', 'restaurant']
        read_only_fields = ['id', 'restaurant']

    def create(self, validated_data):
            return User.objects.create_user(**validated_data)

    def validate_role(self, value):
        if value in [UserRole.ADMIN, UserRole.SUPERADMIN]:
            raise serializers.ValidationError("You cannot create this type of account.")
        return value

class UpdateRoleSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only = True)
    class Meta:
        model = User
        fields = ['id', 'fullname', 'phone', 'role', 'password', 'restaurant']
        read_only_fields = ['id', 'restaurant']

    def validate(self, attrs):
        new_role = attrs.get('role')
        if new_role in {UserRole.ADMIN, UserRole.SUPERADMIN}:
           raise serializers.ValidationError("You cant change role to admin and superadmin role")
        
        if self.instance and self.instance.role == UserRole.ADMIN:
            raise serializers.ValidationError("You cant change admin role from herei")
        return attrs


    def update(self, instance, validated_data):
        current_role = instance.role

        if current_role == UserRole.ADMIN:
            raise serializers.ValidationError("You cant update your account")

        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
