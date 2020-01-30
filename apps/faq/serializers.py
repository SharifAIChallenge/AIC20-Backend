from rest_framework.serializers import ModelSerializer


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = ModelSerializer
        fields = ['id', 'title', 'body', 'question']


class QuestionSerializer(ModelSerializer):
    answer = AnswerSerializer(read_only=True)

    class Meta:
        model = ModelSerializer
        fields = ['id', 'title', 'body', 'answer']
