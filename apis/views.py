import mimetypes

from decouple import config
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apis.s3 import get_s3_client
from apis.serializers import UploadFileTestSerializer, UploadArtifactSerializer
from apps.models import RepositoryRelease, RepositoryReleaseArtifact

S3_BUCKET_NAME = config('S3_BUCKET_NAME', default='')
s3_client = get_s3_client()


class UploadFile(APIView):
    def post(self, request):
        payload = UploadFileTestSerializer(data=request.data)
        if payload.is_valid():
            s3_client = get_s3_client()
            print(payload.validated_data['file'].name)
            s3_client.put_object(
                Bucket=S3_BUCKET_NAME,
                Key=payload.validated_data['file'].name,
                Body=payload.validated_data['file'],
                ContentType=mimetypes.guess_type(payload.validated_data['file'].name)[0],
                ACL="private",
                CacheControl="max-age=31536000"
            )
            # print url to file
            print(s3_client.generate_presigned_url(
                ClientMethod='get_object',
                Params={
                    'Bucket': S3_BUCKET_NAME,
                    'Key': payload.validated_data['file'].name
                }
            ))
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UploadArtifact(APIView):
    def post(self, request):
        payload = UploadArtifactSerializer(data=request.data)
        if payload.is_valid():
            release = RepositoryRelease.objects.create(
                repository=payload.validated_data['repository'],
                version=payload.validated_data['version'],
                description=payload.validated_data['description'] if 'description' in payload.validated_data else '',
                pre_release=payload.validated_data['pre_release']
            )
            total_size = 0
            for artifact in request.FILES.getlist('artifact'):
                artifact_key = f'{release.repository.id}/{release.id}/{artifact.name}'
                RepositoryReleaseArtifact.objects.create(
                    release=release,
                    artifact_key=artifact_key,
                    size=artifact.size
                )
                total_size += artifact.size
                s3_client.put_object(
                    Bucket=S3_BUCKET_NAME,
                    Key=artifact_key,
                    Body=artifact,
                    ContentType=mimetypes.guess_type(artifact.name)[0],
                    ACL="private",
                    CacheControl="max-age=31536000"
                )
            return Response({
                'message': 'Artifact uploaded successfully',
                'repository': payload.validated_data['repository'].name,
                'release_id': release.id,
                'pre_release': release.pre_release,
                'version': release.version,
                'artifact_count': len(request.FILES.getlist('artifact')),
                'total_size': total_size
            }, status=status.HTTP_201_CREATED)
        else:
            # return error message
            return Response(payload.errors, status=status.HTTP_400_BAD_REQUEST)
