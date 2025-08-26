from rest_framework import serializers
from users.models.user_model import User
from users.models.department_model import Department
from users.models.unit_model import Unit

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]

class UnitSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)

    class Meta:
        model = Unit
        fields = ["id", "name", "department"]

class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    unit = UnitSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "department",
            "unit",
            "is_active",
            "is_staff",
            "date_joined"
        ]
        read_only_fields = ["is_staff", "date_joined", "username"]
