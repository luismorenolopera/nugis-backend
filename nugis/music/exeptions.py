from rest_framework.exceptions import APIException


class VideoUnavailable(APIException):
    status_code = 400
    default_detail = 'This video is unavailable.'
    default_code = 'video_unavailable'
