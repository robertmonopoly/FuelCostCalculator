import coverage
from test import run_tests
import subprocess, os, sys

def open_url(url):
    try: # should work on Windows
        os.startfile(url)
    except AttributeError:
        try: # should work on MacOS and most linux versions
            subprocess.call(['open', url])
        except:
            print('Could not open URL')

if __name__ == '__main__':
    cov = coverage.Coverage(omit="*test*")

    cov.start()

    run_tests()

    cov.stop()
    cov.save()

    print('Coverage Summary:')
    cov.report()

    # check if command line argument is present
    headless = False
    if len(sys.argv) == 2:
        if sys.argv[1] == 'headless':
            headless = True

    if not headless and input('View detailed coverage report? (y/n): ') == 'y':
        cov.html_report(directory='tmp/coverage')
        open_url('tmp/coverage/index.html')
    cov.erase()