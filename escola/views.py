from rest_framework import viewsets, generics, status
from escola.models import Aluno, Curso, Matricula
from escola.serializers import AlunoSerializer, AlunoSerializerV2, CursoSerializer, MatriculaSerializer, ListaMatriculasAlunoSerializer, ListaAlunosMatriculadosSerializer
from rest_framework.response import Response


class AlunosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os alunos(a)"""
    queryset=Aluno.objects.all()
    def get_serializer_class(self):
        if (self.request.version == 'v2'):
            return AlunoSerializerV2
        else:
            return AlunoSerializer


class CursosViewSet(viewsets.ModelViewSet):
    """Exibindo todos os cursos"""
    queryset=Curso.objects.all()
    serializer_class=CursoSerializer
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if (serializer.is_valid()):
            serializer.save()
            response = Response(serializer.data, status=status.HTTP_201_CREATED)
            id = str(serializer.data['id'])
            response['Location'] = request.build_absolute_uri() + id
            return response

class MatriculasViewSet(viewsets.ModelViewSet):
    """Exibindo todas as matriculas"""
    queryset=Matricula.objects.all()
    serializer_class=MatriculaSerializer
    #Se não especificar os verbos http, ele disponibiliza todos os verbos por padrao
    http_method_names = ['get', 'post', 'put', 'patch']


class ListaMatriculasAluno(generics.ListAPIView):
    """Listando as matriculas de um aluno(a)"""
    def get_queryset(self):
        queryset=Matricula.objects.filter(aluno_id=self.kwargs['pk'])
        return queryset
    serializer_class=ListaMatriculasAlunoSerializer


class ListaAlunosMatriculados(generics.ListAPIView):
    """Listando alunos(as) matriculados em um curso"""
    def get_queryset(self):
        queryset=Matricula.objects.filter(curso_id=self.kwargs['pk'])
        return queryset
    serializer_class=ListaAlunosMatriculadosSerializer