from rest_framework import serializers

from .models import Employee, EmployeePhoto, EmployeeSkill, Skill


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ["id", "name"]


class EmployeeSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)  # объект навыка, а не id

    class Meta:
        model = EmployeeSkill
        fields = ["skill", "level"]


class EmployeePhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePhoto
        fields = ["id", "image", "order"]


class EmployeeSerializer(serializers.ModelSerializer):
    skills = EmployeeSkillSerializer(
        source="employeeskill_set", many=True, read_only=True
    )
    photos = EmployeePhotoSerializer(many=True, read_only=True)
    workspace_number = serializers.CharField(source="workspace.number", read_only=True)
    tenure_days = serializers.IntegerField(read_only=True)  # property модели

    class Meta:
        model = Employee
        fields = [
            "id",
            "first_name",
            "last_name",
            "gender",
            "role",
            "hired_at",
            "tenure_days",
            "workspace",  # writable: перемещение между столами
            "workspace_number",
            "skills",
            "photos",
        ]
