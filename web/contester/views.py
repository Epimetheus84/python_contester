from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from .models.theme import Theme
from .models.test import Test
from .models.exercise import Exercise
from .models.user import User

import time
import sys

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


def index(request):
    check_login(request)

    context = {
        'themes': Theme.all_exercises(),
    }

    return render(request, 'tasks/main.html', context=context)


def login_page(request):
    return render(request, 'auth/login.html')


def login_post(request):
    try:
        u = User.objects.get(login=request.POST.get('login', False))
    except User.DoesNotExist:
        return redirect('/auth?error=1')

    if not u:
        return redirect('/auth?error=1')

    if u.password != request.POST['password']:
        return redirect('/auth?error=1')

    request.session['user_id'] = u.id
    request.session['user_name'] = u.name
    return redirect('/')


def logout(request):
    del request.session['user_id']
    del request.session['user_name']
    return redirect('/')


def show_exercise(request, exercise_id):
    check_login(request)

    try:
        exercise = Exercise.objects.get(pk=exercise_id)
    except Exercise.DoesNotExist:
        raise Http404("Exercise does not exist")

    try:
        tests = Test.objects.filter(exercise=exercise.id, user=request.session['user_id'])
    except Test.DoesNotExist:
        tests = []

    context = {
        'themes': Theme.all_exercises(),
        'tests': tests,
        'current_exercise': exercise,
    }

    return render(request, 'tasks/main.html', context=context)


def check_login(request):
    if not request.session.get('user_id', False):
        return redirect('/auth')


def submit_exercise(request, exercise_id):
    check_login(request)

    try:
        exercise = Exercise.objects.get(pk=exercise_id)
    except Exercise.DoesNotExist:
        raise Http404("Exercise does not exist")

    result = validate_exercise(exercise, request.POST.get('code', False))
    test = Test(successfully=(result == 'success'), message=result, exercise=exercise,
                user_id=request.session.get('user_id', False))

    test.save()
    return redirect('/exercise/show/' + str(exercise.id))


def validate_exercise(exercise, code):
    needed_inputs = exercise.input.split(';')
    needed_output = exercise.output.split(';')
    print(needed_inputs)
    print(needed_output)

    test_num = 0
    for needed_input, needed_output in zip(needed_inputs, needed_output):
        test_num += 1
        result = execute_users_code(code, needed_input, needed_output, exercise.maximum_time)
        if 'success' not in result:
            return 'test #' + str(test_num) + ' failed:' + result['error']

    return 'success'


class TimeException(Exception):
    pass


def signal_handler(signum, frame):
    raise TimeException("Timed out!")


def execute_users_code(code, needed_input, output, max_execution_time):
    code_out = StringIO()
    code_err = StringIO()

    sys.stdin = StringIO(needed_input)

    sys.stdout = code_out
    sys.stderr = code_err

    start_time = time.time()

    try:
        exec(code)
        execution_time = time.time() - start_time
        if execution_time > max_execution_time:
            raise TimeException
    except TimeException as err:
        # switch back to default console
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        return {'error': 'Timed out'}
    except SyntaxError as err:
        # switch back to default console
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        return {'error': 'Syntax error: ' + str(err.msg) + ' on line ' + str(err.lineno)}
    except ModuleNotFoundError:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        return {'error': 'You cannot import modules'}
    except:
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        return {'error': 'Unexpected error:' + str(sys.exc_info()[0])}

    # switch back to default console
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    s = code_err.getvalue()

    if s:
        return {'error', 'Error during execution ' + str(s)}

    s = code_out.getvalue()

    if s.strip() == output:
        return {'success': 'Executed successfully. Time %.2f' % round(execution_time, 2) + ' sec.'}

    code_out.close()
    code_err.close()
    sys.stdin.close()
    return {'error': 'Incorrect output'}
