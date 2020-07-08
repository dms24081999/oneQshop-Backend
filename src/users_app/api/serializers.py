from rest_framework import serializers

from django.contrib.auth import get_user_model
User=get_user_model()

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    current_user = serializers.SerializerMethodField("curruser")
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "current_user"
        ]    

    def curruser(self, obj):
        try:
            # print(self.context["request"].user.id)
            return self.context["request"].user.id
        except:
            pass

