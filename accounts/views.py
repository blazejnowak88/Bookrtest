from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth.models import User, Group
from django.views.generic import CreateView, UpdateView

from accounts.forms import LoginForm, RegisterForm, GroupPermissionAddForm


# Create your views here.
class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get('next', 'home')
                return redirect(next)
        return render(request, 'login.html', {'form': form})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('home')


class RegistrationView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            login(request, user)
            return redirect('home')
        return render(request, 'registration.html', {'form': form})


class HomeView(View):
    def get(self, request):
        return render(request, 'index.html', )


@login_required
def profile(request):
    user = request.user
    permissions = user.get_all_permissions()
    # Get the books read in different months this year
    books_read_by_month = get_books_read_by_month(user.username)

    # Initialize the Axis for graphs, X-Axis is months, Y-axis is books read
    months = [i + 1 for i in range(12)]
    books_read = [0 for _ in range(12)]

    # Set the value for books read per month on Y-Axis
    for num_books_read in books_read_by_month:
        list_index = num_books_read['date_created__month'] - 1
        books_read[list_index] = num_books_read['book_count']

    # Generate a scatter plot HTML
    figure = graphs.Figure()
    scatter = graphs.Scatter(x=months, y=books_read)
    figure.add_trace(scatter)
    figure.update_layout(xaxis_title="Month", yaxis_title="No. of books read")
    plot_html = plot(figure, output_type='div')

    return render(request, 'profile.html',
                  {'user': user, 'permissions': permissions, 'books_read_plot': plot_html})


@login_required
def reading_history(request):
    user = request.user.username
    books_read = get_books_read(user)

    # Create an object to create files in memory
    temp_file = BytesIO()

    # Start a new workbook
    workbook = xlsxwriter.Workbook(temp_file)
    worksheet = workbook.add_worksheet()

    # Prepare the data to be written
    data = []
    for book_read in books_read:
        data.append([book_read['title'], str(book_read['completed_on'])])

    # Write data to worksheet
    for row in range(len(data)):
        for col in range(len(data[row])):
            worksheet.write(row, col, data[row][col])

    # Close the workbook
    workbook.close()

    # Capture data from memory file
    data_to_download = temp_file.getvalue()

    # Prepare response for download
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=reading_history.xlsx'
    response.write(data_to_download)

    return response
