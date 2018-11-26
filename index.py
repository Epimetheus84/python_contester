import time
import sys
import signal

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


class TimeException(Exception):
    pass


def signal_handler(signum, frame):
    raise TimeException("Timed out!")


def execute_users_code(code, needed_input, output, max_execution_time):
    code_out = StringIO()
    code_err = StringIO()

    sys.stdin = StringIO(needed_input)

    # try:
    #     signal.signal(signal.SIGALRM, signal_handler)
    #     signal.alarm(max_execution_time)
    # except AttributeError:
    #     print("This system isn't working on Windows because "
    #           "https://docs.python.org/2/library/signal.html#signal.signal")
    #     return {'error': 'system error'}

    sys.stdout = code_out
    sys.stderr = code_err

    start_time = time.time()

    try:
        exec(code)
    except TimeException:
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

    execution_time = time.time() - start_time
    # switch back to default console
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__

    s = code_err.getvalue()

    if s:
        return {'error', 'Error during execution ' + str(s)}

    s = code_out.getvalue()

    if s.strip() == output:
        return {'success': 'Executed successfully. Time ' + str(execution_time) + ' sec.'}

    code_out.close()
    code_err.close()
    sys.stdin.close()
    return {'error': 'Incorrect output'}


code = """
data = int(input()) ** 2
time.sleep(1)
import selenium
print(data)
"""

needed_inputs = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
needed_output = ['1', '4', '9', '16', '25', '36', '49', '64', '81']

test_num = 0
for needed_input, needed_output in zip(needed_inputs, needed_output):
    test_num += 1
    result = execute_users_code(code, needed_input, needed_output, 1)
    if 'success' not in result:
        print('test #', test_num,' failed:', result['error'])
        break

    print(result['success'])
