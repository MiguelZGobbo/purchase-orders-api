import time


def duration_timer(function):
    def  wraper():
        init = time.time()
        function()
        final = time.time()

        print("O tempo total da função: {}, foi de: {}.".format(function.__name__, str(final-init)))

    return wraper

@duration_timer
def main():
    for i in range(1, 10000):
        pass

main()
