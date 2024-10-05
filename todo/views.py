from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm


def create_todo(request):
    message = ""
    user = request.user
    form = None
    if not user.is_authenticated:
        message = "請先登入"
    else:
        form = TodoForm()
        if request.method == "POST":
            try:
                print(request.POST)
                form = TodoForm(request.POST)
                todo = form.save(commit=False)
                todo.user = request.user
                todo.save()
                message = "提交成功!"
                return redirect("todolist")
            except Exception as e:
                print(e)
                message = "提交失敗!"

    return render(request, "todo/create-todo.html", {"form": form, "message": message})


def todo(request, id):
    message = ""
    user = request.user
    todo = None
    try:
        todo = Todo.objects.get(id=id, user=user)
    except Exception as e:
        print(e)
        message = "編號錯誤"

    return render(request, "todo/todo.html", {"todo": todo, "message": message})


# Create your views here.
def todolist(request):
    user = request.user
    todos = None
    if user.is_authenticated:
        todos = Todo.objects.filter(user=user)

    return render(request, "todo/todolist.html", {"todos": todos})
