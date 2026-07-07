from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views as auth_views
from django.db.models import Case, When, Value, IntegerField
from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo, Category

PRIORITY_ORDER = Case(
    When(priority="high", then=Value(0)),
    When(priority="medium", then=Value(1)),
    When(priority="low", then=Value(2)),
    output_field=IntegerField(),
)


def signup(request):
    if request.user.is_authenticated:
        return redirect("todo_list")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("todo_list")
    else:
        form = UserCreationForm()
    return render(request, "todos/signup.html", {"form": form})


@login_required
def todo_list(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            due_date = request.POST.get("due_date") or None
            priority = request.POST.get("priority", Todo.PRIORITY_MEDIUM)
            category_id = request.POST.get("category") or None
            Todo.objects.create(
                owner=request.user,
                title=title,
                due_date=due_date,
                priority=priority,
                category_id=category_id,
            )
        return redirect_with_params(request)

    status = request.GET.get("filter", "all")
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "")

    todos = Todo.objects.filter(owner=request.user).select_related("category")

    if status == "active":
        todos = todos.filter(completed=False)
    elif status == "completed":
        todos = todos.filter(completed=True)

    if query:
        todos = todos.filter(title__icontains=query)

    if category_id:
        todos = todos.filter(category_id=category_id)

    todos = todos.annotate(priority_rank=PRIORITY_ORDER).order_by(
        "completed", "priority_rank", "due_date", "-created_at"
    )

    owner_todos = Todo.objects.filter(owner=request.user)
    total = owner_todos.count()
    completed_count = owner_todos.filter(completed=True).count()
    percent = round((completed_count / total) * 100) if total else 0

    context = {
        "todos": todos,
        "categories": Category.objects.all(),
        "status": status,
        "query": query,
        "selected_category": category_id,
        "total": total,
        "completed_count": completed_count,
        "percent": percent,
    }
    return render(request, "todos/todo_list.html", context)


@login_required
def toggle_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, owner=request.user)
    todo.completed = not todo.completed
    todo.save()
    return redirect_with_params(request)


@login_required
def delete_todo(request, pk):
    todo = get_object_or_404(Todo, pk=pk, owner=request.user)
    todo.delete()
    return redirect_with_params(request)


def redirect_with_params(request):
    """Redirect back to the list, preserving filter/search state."""
    params = {}
    for key in ("filter", "q", "category"):
        value = request.POST.get(key) or request.GET.get(key)
        if value:
            params[key] = value
    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    url = "/"
    if query_string:
        url = f"{url}?{query_string}"
    return redirect(url)