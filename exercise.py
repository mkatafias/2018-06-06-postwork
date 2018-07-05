'''
Poniżej znajduje się implementacja CLI (command line interface) do modułu
turtle, czyli Pythonowego odpowiednika LOGO. Wykorzystano tutaj wzorzec Template
Method (metoda szablonowa).
W pierwszym, obowiązkowym zadaniu, należy dodać wsparcie dla makr, tak aby można
było nagrać ciąg komend, a następnie odtworzyć ten sam ciąg przy pomocy
komendy "playback". W tym celu, należy dodać następujące komendy:
- record -- rozpoczyna nagrywanie makra
- stop -- kończy nagrywanie makra
- playback -- wykonuje makro, tzn. wszystkie komendy po komendzie "record", aż
  do komendy "stop".
Podpowiedź: Użyj wzorca Command (polecenie).
W drugim, nieobowiązkowym zadaniu, zastanów się, jak można zastosować wzorzec
Composite (kompozyt) do tych makr i spróbuj zastosować go.
Rozwiązania wysyłamy tak samo, jak prework, tylko że w jednym Pull Requeście.
'''

import cmd, sys
import turtle

class TurtleShell(cmd.Cmd):
    intro = 'Welcome to the turtle shell.   Type help or ? to list commands.\n'
    prompt = '(turtle) '

    # ----- basic turtle commands -----
    def do_forward(self, arg):
        'Move the turtle forward by the specified distance:  FORWARD 10'
        turtle.forward(int(arg))
    def do_right(self, arg):
        'Turn turtle right by given number of degrees:  RIGHT 20'
        turtle.right(int(arg))
    def do_left(self, arg):
        'Turn turtle left by given number of degrees:  LEFT 90'
        turtle.left(int(arg))
    def do_home(self, arg):
        'Return turtle to the home position:  HOME'
        turtle.home()
    def do_circle(self, arg):
        'Draw circle with given radius an options extent and steps:  CIRCLE 50'
        turtle.circle(int(arg))
    def do_position(self, arg):
        'Print the current turtle position:  POSITION'
        print('Current position is %d %d\n' % turtle.position())
    def do_heading(self, arg):
        'Print the current turtle heading in degrees:  HEADING'
        print('Current heading is %d\n' % (turtle.heading(),))
    def do_reset(self, arg):
        'Clear the screen and return turtle to center:  RESET'
        turtle.reset()
    def do_bye(self, arg):
        'Close the turtle window, and exit:  BYE'
        print('Thank you for using Turtle')
        turtle.bye()
        return True


class TurtleShellBuffered(TurtleShell):
    def __init__(self):
        self.makro = []
        self.recording = False
        super().__init__()

    def __getattribute__(self, item):
        if item.startswith('do_'):
            if self.recording and item not in ('do_record', 'do_stop', 'do_playback'):
                return lambda arg: self.__execute(item, arg)
            else:
                return super().__getattribute__(item)
        else:
            return super().__getattribute__(item)

    def __execute(self, method, args):
        self.makro.append((method, args))

    def do_record(self, arg):
        self.makro = []
        self.recording = True

    def do_playback(self, arg):
        if self.recording:
            print("Recording enabled, can't playback in this state. Type stop to stop recording.")
        else:
            for method, args in self.makro:
                super().__getattribute__(method)(args)

    def do_stop(self, arg):
        self.recording = False


if __name__ == '__main__':
    TurtleShellBuffered().cmdloop()
