from rest_framework import authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from constants import ApplicationMessages, Constant
from search_app import utils
from search_app.models import WikiSearchLog
from search_app.serializers import WikiSearchLogSerializer

class WordFrequencyView(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        article_title = request.data.get("title", None)
        num_words = request.data.get("num_words", None)
        formatted_title = utils.validate_payload(article_title, num_words)
        try:
            most_common_words = utils.call_wikipedia_api(formatted_title, num_words)
            if most_common_words:
                # create a log into the database
                utils.log_search_response(article_title, num_words, most_common_words, request.user)
            return Response(
                {"most_common_words": most_common_words}, status=status.HTTP_200_OK
            )
        except:
            return Response({
                    "error": ApplicationMessages.ERROR_FETCHING_DATA
                },
                status=status.HTTP_400_BAD_REQUEST)


class SearchHistoryLog(APIView):

    authentication_classes = [authentication.BasicAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = WikiSearchLogSerializer

    def get_queryset(self, user):
        # if admin show all history if normal user show his own history only
        if user.is_superuser:
            return WikiSearchLog.objects.all()
        return WikiSearchLog.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(self.get_queryset(request.user), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {"error": ApplicationMessages.ERROR_FETCHING_DATA},
                status=status.HTTP_400_BAD_REQUEST,
            )
