from rest_framework import serializers

from apps.models import RepositoryAPIKey


class UploadFileTestSerializer(serializers.Serializer):
    file = serializers.FileField()


class UploadArtifactSerializer(serializers.Serializer):
    artifact = serializers.FileField()
    version = serializers.CharField(max_length=50)
    pre_release = serializers.BooleanField(default=False, required=False)
    description = serializers.CharField(max_length=1000, allow_blank=True, required=False)
    key = serializers.CharField(max_length=64)

    def validate(self, attrs):
        if attrs['key'] == '':
            raise serializers.ValidationError('Key cannot be empty')
        key_filter = RepositoryAPIKey.objects.filter(key=attrs['key'])
        if not key_filter.exists():
            raise serializers.ValidationError('Invalid key')
        else:
            attrs['repository'] = key_filter.first().repository
            attrs['user'] = key_filter.first().user
        user_repository_permission = attrs['repository'].permissions.filter(user=attrs['user'])
        if not user_repository_permission.exists():
            raise serializers.ValidationError('You do not have permission to upload artifacts to this repository')
        elif user_repository_permission.first().permission != 'write' and user_repository_permission.first().permission != 'admin':
            raise serializers.ValidationError('You do not have permission to upload artifacts to this repository')
        # File cannot be exceeded 200MB
        if attrs['artifact'].size > 200000000:
            raise serializers.ValidationError('File size cannot exceed 200MB')
        return attrs
